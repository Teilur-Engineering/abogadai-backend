"""
Endpoints para recibir webhooks de pasarelas de pago

Este módulo maneja las notificaciones (IPN) de:
- Vita Wallet: Confirmaciones de pago
"""

from fastapi import APIRouter, Request, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import logging
import json

from ..core.database import get_db
from ..models.pago import Pago, EstadoPago, MetodoPago
from ..models.caso import Caso, EstadoCaso
from ..services.vitawallet_service import vitawallet_service
from ..services.pago_service import procesar_pago_exitoso

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])
logger = logging.getLogger(__name__)


@router.get("/vita")
async def vita_webhook_verificacion():
    """Endpoint GET para verificación de URL por Vita Wallet"""
    return {"status": "ok", "message": "Webhook endpoint activo"}


@router.post("/vita")
async def webhook_vita(
    request: Request,
    authorization: Optional[str] = Header(None),
    x_date: Optional[str] = Header(None, alias="X-Date")
):
    """
    Recibe notificaciones de pago de Vita Wallet (IPN)

    Headers esperados:
    - Authorization: V2-HMAC-SHA256, Signature: {signature}
    - X-Date: {timestamp_ISO8601}

    Body: Evento con datos de la transacción

    Flujo:
    1. Extraer y validar firma HMAC-SHA256
    2. Parsear evento
    3. Buscar pago por public_code o transaction_id
    4. Procesar según estado (completed, denied, failed, etc.)
    5. Retornar 200 OK
    """
    # Obtener sesión de BD
    from ..core.database import SessionLocal
    db = SessionLocal()

    try:
        # Leer body raw para validación de firma
        body_bytes = await request.body()
        body_str = body_bytes.decode('utf-8')

        try:
            body = json.loads(body_str)
        except json.JSONDecodeError:
            logger.error(f"Webhook Vita: Body no es JSON válido")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Body debe ser JSON válido"
            )

        logger.info(f"Webhook Vita recibido: event_type={body.get('event_type')}")

        # Extraer firma del header Authorization
        signature = vitawallet_service.extraer_signature_de_header(authorization)

        if not signature:
            logger.warning("Webhook Vita: No se encontró firma en Authorization header")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Firma no encontrada en header Authorization"
            )

        if not x_date:
            logger.warning("Webhook Vita: No se encontró header X-Date")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Header X-Date requerido"
            )

        # Validar firma HMAC-SHA256 (siempre, en todos los entornos)
        is_valid = vitawallet_service.verificar_firma_webhook(
            x_date=x_date,
            body=body,
            signature_recibida=signature
        )

        if not is_valid:
            logger.error(
                f"Webhook Vita: Firma inválida "
                f"(entorno={vitawallet_service.environment})"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Firma de webhook inválida"
            )

        # Parsear evento
        evento = vitawallet_service.parsear_evento_webhook(body)

        # Extraer public_code del body (viene en diferentes lugares según el evento)
        public_code = None
        if "data" in body:
            data = body["data"]
            if isinstance(data, dict):
                # 1. Directo en data.public_code (payment_order.paid)
                public_code = data.get("public_code")
                # 2. En data.order (transaction.completed)
                if not public_code:
                    public_code = data.get("order")
                # 3. En data.payment_order.public_code (payment_order_attempt.paid)
                if not public_code and "payment_order" in data:
                    public_code = data.get("payment_order", {}).get("public_code")
                # 4. En data.attributes.public_code (formato alternativo)
                if not public_code:
                    public_code = data.get("attributes", {}).get("public_code")

        logger.info(
            f"Evento parseado: type={evento['event_type']}, "
            f"status={evento['status']}, "
            f"transaction_id={evento['transaction_id']}, "
            f"public_code={public_code}"
        )

        # Log del body completo para debug
        logger.debug(f"Webhook body completo: {body}")

        # Buscar el pago asociado
        pago = None

        # 1. Buscar por public_code (payment orders de Vita)
        if public_code:
            pago = db.query(Pago).filter(
                Pago.vita_public_code == public_code
            ).first()
            if pago:
                logger.info(f"Pago encontrado por public_code: {pago.id}")

        # 2. Si no, buscar por transaction_id (referencia_pago)
        if not pago and evento.get("transaction_id"):
            pago = db.query(Pago).filter(
                Pago.referencia_pago == str(evento["transaction_id"])
            ).first()
            if pago:
                logger.info(f"Pago encontrado por transaction_id: {pago.id}")

        # 3. Si no, buscar por descripción (que contiene el caso_id)
        if not pago and evento.get("description"):
            # La descripción tiene formato "Pago Tutela - Caso #123"
            desc = evento["description"]
            if "Caso #" in desc:
                try:
                    caso_id = int(desc.split("Caso #")[1].split()[0])
                    # Buscar pago pendiente para ese caso
                    pago = db.query(Pago).filter(
                        Pago.caso_id == caso_id,
                        Pago.estado == EstadoPago.PENDIENTE,
                        Pago.metodo_pago == MetodoPago.VITA_WALLET
                    ).order_by(Pago.created_at.desc()).first()

                    if pago:
                        logger.info(f"Pago encontrado por caso_id: {pago.id}")
                except (ValueError, IndexError):
                    pass

        if not pago:
            logger.warning(
                f"Webhook Vita: No se encontró pago para transaction_id={evento.get('transaction_id')}"
            )
            # Retornamos 200 para que Vita no reintente
            # pero registramos el evento huérfano
            return {
                "status": "warning",
                "message": "Pago no encontrado, evento ignorado",
                "event_id": evento.get("event_id")
            }

        # Verificar idempotencia - si ya procesamos este pago, ignorar
        if pago.estado == EstadoPago.EXITOSO:
            logger.info(f"Pago {pago.id} ya está en estado EXITOSO, ignorando webhook")
            return {
                "status": "ok",
                "message": "Pago ya procesado anteriormente",
                "pago_id": pago.id
            }

        if pago.estado == EstadoPago.REEMBOLSADO:
            logger.info(f"Pago {pago.id} está REEMBOLSADO, ignorando webhook")
            return {
                "status": "ok",
                "message": "Pago ya reembolsado",
                "pago_id": pago.id
            }

        # Procesar según el estado del evento
        if vitawallet_service.es_pago_exitoso(evento):
            # PAGO EXITOSO
            logger.info(f"Procesando pago exitoso: pago_id={pago.id}")

            pago.estado = EstadoPago.EXITOSO
            pago.fecha_pago = datetime.utcnow()

            # Si tenemos el transaction_id de Vita, guardarlo
            if evento.get("transaction_id"):
                pago.referencia_pago = str(evento["transaction_id"])

            db.commit()

            # Procesar beneficios (desbloquear documento, actualizar nivel, etc.)
            try:
                beneficios = procesar_pago_exitoso(pago.id, db)
                logger.info(f"Beneficios procesados: {beneficios}")
            except Exception as e:
                logger.error(f"Error procesando beneficios: {str(e)}")
                # El pago ya está marcado como exitoso, los beneficios se pueden
                # procesar manualmente si fallan

            return {
                "status": "ok",
                "message": "Pago procesado exitosamente",
                "pago_id": pago.id,
                "caso_id": pago.caso_id
            }

        elif vitawallet_service.es_pago_fallido(evento):
            # PAGO FALLIDO
            logger.info(f"Procesando pago fallido: pago_id={pago.id}, status={evento['status']}")

            pago.estado = EstadoPago.FALLIDO
            pago.notas_admin = f"Fallido via webhook: {evento['status']} - {evento.get('event_type')}"

            db.commit()

            return {
                "status": "ok",
                "message": "Pago marcado como fallido",
                "pago_id": pago.id
            }

        else:
            # Estado no reconocido o pendiente
            logger.info(
                f"Evento con estado no procesable: {evento['status']}, "
                f"event_type={evento['event_type']}"
            )

            return {
                "status": "ok",
                "message": "Evento recibido pero no requiere acción",
                "event_type": evento["event_type"],
                "status": evento["status"]
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error procesando webhook Vita: {str(e)}", exc_info=True)
        # Retornamos 200 para evitar reintentos infinitos de Vita
        # pero registramos el error
        return {
            "status": "error",
            "message": f"Error interno: {str(e)}"
        }
    finally:
        db.close()


@router.get("/vita/health")
async def vita_webhook_health():
    """
    Endpoint de health check para verificar que el webhook está activo

    Vita puede usar esto para verificar conectividad
    """
    return {
        "status": "ok",
        "service": "vita_webhook",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/vita/config")
async def obtener_configuracion_vita():
    """
    Obtiene la configuración actual del webhook desde Vita API.

    Útil para verificar:
    - Si el webhook_url está correctamente configurado
    - Si las categorías incluyen "payment"

    NOTA: Si 'payment' no está en configured_categories,
    los webhooks de pago NO llegarán.
    """
    config = await vitawallet_service.obtener_configuracion_webhook()

    # Verificar si payment está configurado
    tiene_payment = "payment" in config.get("configured_categories", [])

    return {
        **config,
        "tiene_categoria_payment": tiene_payment,
        "recomendacion": None if tiene_payment else
            "IMPORTANTE: La categoría 'payment' no está configurada. "
            "Los webhooks de pago no llegarán hasta que se agregue."
    }


@router.post("/vita/config")
async def actualizar_configuracion_vita(
    webhook_url: str = None,
    categories: list = None
):
    """
    Actualiza la configuración del webhook en Vita.

    Args:
        webhook_url: URL del webhook (requerido la primera vez, ej: https://abogadai-backend.onrender.com/webhooks/vita)
        categories: Lista de categorías (opcional, usa ["payment"] si no se especifica)

    Ejemplo de uso:
        POST /webhooks/vita/config?webhook_url=https://abogadai-backend.onrender.com/webhooks/vita&categories=payment
    """
    # Valores por defecto
    if not webhook_url:
        # Intentar obtener la config actual y usar esa URL
        config_actual = await vitawallet_service.obtener_configuracion_webhook()
        webhook_url = config_actual.get("webhook_url")

        if not webhook_url:
            return {
                "success": False,
                "error": "webhook_url es requerido. Ej: https://abogadai-backend.onrender.com/webhooks/vita"
            }

    if not categories:
        categories = ["payment"]

    result = await vitawallet_service.actualizar_configuracion_webhook(
        webhook_url=webhook_url,
        categories=categories
    )

    return result


@router.get("/vita/eventos")
async def obtener_ultimos_eventos_vita():
    """
    Obtiene los últimos 10 eventos del negocio desde Vita.

    Útil para:
    - Debugging de webhooks
    - Verificar si los eventos de pago están siendo generados
    - Ver el estado de entrega de webhooks
    """
    return await vitawallet_service.obtener_ultimos_eventos()
