"""
Servicio para integración con Vita Wallet API

Documentación: https://docs.vitawallet.io/

Este servicio maneja:
- Creación de órdenes de pago (payment_orders)
- Validación de webhooks (firma HMAC-SHA256)
- Verificación de estado de pagos

AUTENTICACIÓN:
- Cada request debe firmarse con HMAC-SHA256
- El request_body para firma es: concatenar clave+valor ordenados alfabéticamente SIN separadores
- El secret se usa como string UTF-8 (no como bytes hex)
- Formato: signature = hmac(secret, x_login + x_date + request_body_hash)
"""

import hmac
import hashlib
import json
import logging
import httpx
from typing import Optional
from datetime import datetime, timezone

from ..core.config import settings

logger = logging.getLogger(__name__)


class VitaWalletError(Exception):
    """Excepción personalizada para errores de Vita Wallet"""
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


class VitaWalletService:
    """
    Cliente para la API de Vita Wallet

    Uso:
        vita = VitaWalletService()
        result = vita.crear_payment_order(monto=39000, caso_id=123, ...)
    """

    def __init__(self):
        self.base_url = settings.VITA_API_URL.rstrip('/')
        self.x_trans_key = settings.VITA_API_KEY  # X-Trans-Key header
        self.api_secret = settings.VITA_API_SECRET
        self.business_secret = settings.VITA_BUSINESS_SECRET  # Para firmar requests Y validar webhooks
        self.x_login = settings.VITA_X_LOGIN
        self.wallet_master_uuid = getattr(settings, 'VITA_WALLET_MASTER_UUID', None)
        self.environment = settings.VITA_ENVIRONMENT

    def _calculate_request_body_hash(self, body: dict) -> str:
        """
        Calcula el hash del body para la firma HMAC.

        Vita NO firma el JSON, sino una concatenación de clave+valor
        ordenados alfabéticamente SIN separadores.

        Ejemplo:
            {"amount": 400, "currency": "USD"}
            -> "amount400currencyUSD"
        """
        if not body:
            return ""
        return "".join(f"{k}{body[k]}" for k in sorted(body.keys()))

    def _generate_signature(self, x_date: str, body: dict) -> str:
        """
        Genera la firma HMAC-SHA256 para autenticación.

        Formula: hmac(secret, x_login + x_date + request_body_hash)

        El secret se usa como string UTF-8 (no como bytes hex).
        """
        request_body_hash = self._calculate_request_body_hash(body)
        message = f"{self.x_login}{x_date}{request_body_hash}"

        signature = hmac.new(
            self.business_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        return signature

    def _get_headers(self, body: dict = None) -> dict:
        """
        Genera los headers de autenticación para requests a Vita.

        Incluye:
        - X-Login: identificador del business
        - X-Trans-Key: clave de transacción
        - X-Date: timestamp ISO8601 con milisegundos
        - Authorization: V2-HMAC-SHA256, Signature: {firma}
        """
        # X-Date en ISO8601 con milisegundos y Z
        x_date = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')

        # Calcular firma
        signature = self._generate_signature(x_date, body or {})

        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Login": self.x_login,
            "X-Trans-Key": self.x_trans_key,
            "X-Date": x_date,
            "Authorization": f"V2-HMAC-SHA256, Signature: {signature}",
        }

    def _build_redirect_urls(self, caso_id: int) -> dict:
        """
        Construye las URLs de redirección para después del pago

        Vita redirige al usuario según el resultado:
        - success: Pago completado (redirige a thank you page en Webflow)
        - cancel: Usuario canceló
        - error: Error en el proceso
        - pending: Pago pendiente de confirmación

        El thank you page de Webflow tiene el evento de conversión de Google Ads
        y un botón que redirige al usuario a la app para ver su documento.
        """
        caso_url = f"{settings.FRONTEND_URL}/app/tutela/{caso_id}"
        casos_url = f"{settings.FRONTEND_URL}/app/casos"

        return {
            # Exitoso va al thank you page de Webflow para tracking de conversión
            "success_redirect_url": f"https://www.abogadai.com/gracias?caso_id={caso_id}",
            "pending_redirect_url": f"{caso_url}?pago=pendiente",
            # Cancelado y error van a la lista de casos
            "cancel_redirect_url": f"{casos_url}?pago=cancelado&caso_id={caso_id}",
            "error_redirect_url": f"{casos_url}?pago=error&caso_id={caso_id}",
        }

    async def crear_payment_order(
        self,
        monto: int,
        caso_id: int,
        tipo_documento: str,
        descripcion: Optional[str] = None
    ) -> dict:
        """
        Crea una orden de pago en Vita Wallet

        Args:
            monto: Monto en COP (sin decimales, ej: 39000)
            caso_id: ID del caso en Abogadai
            tipo_documento: "TUTELA" o "DERECHO_PETICION"
            descripcion: Descripción opcional del pago

        Returns:
            {
                "payment_url": "https://vitawallet.io/checkout?...",
                "public_code": "uuid-...",
                "vita_order_id": "123",
                "expires_at": "2024-03-12T03:27:34Z"
            }

        Raises:
            VitaWalletError: Si hay error en la API
        """
        # Validar que tenemos credenciales
        if not self.x_trans_key or not self.business_secret:
            raise VitaWalletError(
                "Credenciales de Vita Wallet no configuradas. "
                "Configure VITA_API_KEY y VITA_BUSINESS_SECRET en .env"
            )

        # Construir issue/descripción
        tipo_doc_legible = "Tutela" if tipo_documento == "TUTELA" else "Derecho de Petición"
        issue = descripcion or f"Pago {tipo_doc_legible} - Caso #{caso_id}"

        # Construir URLs de redirección
        redirect_urls = self._build_redirect_urls(caso_id)

        # Payload según documentación de Vita
        # IMPORTANTE: country_iso_code debe ser MAYÚSCULA
        payload = {
            "amount": monto,
            "country_iso_code": "CO",  # Colombia - MAYÚSCULA
            "issue": issue,
            **redirect_urls
        }

        logger.info(f"Creando payment order en Vita: caso={caso_id}, monto={monto}")

        try:
            # Generar headers con firma HMAC
            headers = self._get_headers(payload)

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/businesses/payment_orders",
                    headers=headers,
                    json=payload
                )

                response_data = response.json()

                if response.status_code not in [200, 201]:
                    logger.error(f"Error Vita API: {response.status_code} - {response_data}")
                    raise VitaWalletError(
                        message=f"Error creando orden de pago: {response_data}",
                        status_code=response.status_code,
                        response_data=response_data
                    )

                # Extraer datos de la respuesta
                # Estructura: { "data": { "id": "37", "type": "payment_order", "attributes": {...} } }
                data = response_data.get("data", {})
                attributes = data.get("attributes", {})

                result = {
                    "payment_url": attributes.get("url"),
                    "public_code": attributes.get("public_code"),
                    "vita_order_id": data.get("id"),
                    "expires_at": attributes.get("expires_at"),
                    "status": attributes.get("status", "pending")
                }

                logger.info(f"Payment order creada: public_code={result['public_code']}")

                return result

        except httpx.TimeoutException:
            logger.error("Timeout conectando con Vita Wallet API")
            raise VitaWalletError("Timeout conectando con Vita Wallet")
        except httpx.RequestError as e:
            logger.error(f"Error de conexión con Vita: {str(e)}")
            raise VitaWalletError(f"Error de conexión: {str(e)}")

    def verificar_firma_webhook(
        self,
        x_date: str,
        body: dict,
        signature_recibida: str
    ) -> bool:
        """
        Valida la firma HMAC-SHA256 del webhook de Vita

        Según documentación:
        - string_to_sign = x_login + x_date + JSON.stringify(data_hash)
        - signature = HMAC-SHA256(business_secret, string_to_sign)

        Args:
            x_date: Timestamp ISO8601 del header X-Date
            body: Body del webhook (dict)
            signature_recibida: Firma del header Authorization (después de "Signature: ")

        Returns:
            bool: True si la firma es válida
        """
        if not self.business_secret or not self.x_login:
            logger.warning("business_secret o x_login no configurados, no se puede validar firma")
            return False

        try:
            # Convertir body a JSON compacto (sin espacios, sin saltos de línea)
            body_json = json.dumps(body, separators=(',', ':'), ensure_ascii=False)

            # Construir string a firmar: x_login + x_date + body_json
            string_to_sign = self.x_login + x_date + body_json

            # Calcular firma esperada
            expected_signature = hmac.new(
                self.business_secret.encode('utf-8'),
                string_to_sign.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()

            # Comparar de forma segura (timing-safe)
            is_valid = hmac.compare_digest(expected_signature.lower(), signature_recibida.lower())

            if not is_valid:
                logger.warning(f"Firma de webhook inválida. Esperada: {expected_signature[:16]}...")

            return is_valid

        except Exception as e:
            logger.error(f"Error validando firma de webhook: {str(e)}")
            return False

    def extraer_signature_de_header(self, authorization_header: str) -> Optional[str]:
        """
        Extrae la firma del header Authorization

        Formato esperado: "V2-HMAC-SHA256, Signature: {signature}"

        Args:
            authorization_header: Valor del header Authorization

        Returns:
            str: La firma hexadecimal (64 caracteres) o None si no se encuentra
        """
        if not authorization_header:
            return None

        try:
            # Buscar "Signature: " en el header
            if "Signature:" in authorization_header:
                parts = authorization_header.split("Signature:")
                if len(parts) > 1:
                    signature = parts[1].strip()
                    # Validar que parece una firma hexadecimal (64 chars)
                    if len(signature) == 64 and all(c in '0123456789abcdefABCDEF' for c in signature):
                        return signature

            return None

        except Exception as e:
            logger.error(f"Error extrayendo firma: {str(e)}")
            return None

    def parsear_evento_webhook(self, body: dict) -> dict:
        """
        Parsea el evento de webhook y extrae información relevante

        Args:
            body: Body del webhook

        Returns:
            {
                "event_type": "transaction.completed",
                "event_id": "uuid",
                "status": "completed",
                "amount": "39000.0",
                "total": "39000.0",
                "category": "payment",
                "public_code": "uuid" (si aplica),
                "created_at": "2024-01-15T12:40:50Z"
            }
        """
        data = body.get("data", {})

        return {
            "event_type": body.get("event_type"),
            "event_id": body.get("event_id"),
            "created_at": body.get("created_at"),
            "transaction_id": data.get("id"),
            "status": data.get("status"),
            "amount": data.get("amount"),
            "total": data.get("total"),
            "category": data.get("category"),
            "currency": data.get("currency"),
            "description": data.get("description"),
            "statuses": data.get("statuses", []),
            # Campos específicos de payment
            "funding_source_user_name": data.get("funding_source_user_name"),
            "funding_source_user_document_number": data.get("funding_source_user_document_number"),
        }

    def es_pago_exitoso(self, evento: dict) -> bool:
        """
        Determina si el evento representa un pago exitoso

        Args:
            evento: Evento parseado de parsear_evento_webhook()

        Returns:
            bool: True si el pago fue exitoso
        """
        event_type = evento.get("event_type", "")
        status = evento.get("status", "")

        # Eventos que indican pago exitoso
        eventos_exitosos = [
            "transaction.completed",
            "payment_order.paid",
            "payment_order_attempt.paid",
        ]

        if event_type in eventos_exitosos:
            return True

        if "completed" in event_type or status == "completed":
            return True

        if "paid" in event_type or status == "paid":
            return True

        return False

    def es_pago_fallido(self, evento: dict) -> bool:
        """
        Determina si el evento representa un pago fallido

        Args:
            evento: Evento parseado de parsear_evento_webhook()

        Returns:
            bool: True si el pago falló
        """
        event_type = evento.get("event_type", "")
        status = evento.get("status", "")

        # Pago fallido
        estados_fallidos = ["denied", "failed", "time_out", "cancelled", "rejected"]

        if any(estado in event_type for estado in estados_fallidos):
            return True

        if status in estados_fallidos:
            return True

        return False


    async def consultar_estado_payment_order(self, public_code: str) -> dict:
        """
        Consulta el estado actual de una payment order buscando en los eventos de Vita.

        Busca en los últimos eventos si hay alguno relacionado con este public_code
        que indique que el pago fue completado.

        Args:
            public_code: UUID público de la payment order

        Returns:
            {
                "status": "pending|paid|expired|cancelled",
                "amount": 39000,
                "paid_at": "2024-03-12T...",  # si fue pagado
                "error": None  # o mensaje de error
            }
        """
        if not public_code:
            return {"status": "unknown", "error": "No public_code provided"}

        try:
            # Usar el endpoint de eventos que sí está documentado
            eventos = await self.obtener_ultimos_eventos()

            if eventos.get("error"):
                return {"status": "unknown", "error": eventos["error"]}

            # Buscar eventos relacionados con este public_code
            for evento in eventos.get("events", []):
                payload = evento.get("payload", {})
                event_type = evento.get("event_type", "")

                # Buscar el public_code en diferentes ubicaciones del payload
                evento_public_code = None

                # Puede estar en payload.public_code
                if payload.get("public_code") == public_code:
                    evento_public_code = public_code
                # O en payload.order (para transaction.completed)
                elif payload.get("order") == public_code:
                    evento_public_code = public_code
                # O en la descripción
                elif public_code in str(payload.get("description", "")):
                    evento_public_code = public_code

                if evento_public_code:
                    status = payload.get("status", "")
                    logger.info(f"Evento encontrado para {public_code}: type={event_type}, status={status}")

                    # Determinar estado basado en el evento
                    if event_type in ["payment_order.paid", "payment_order_attempt.paid"] or status == "paid":
                        return {
                            "status": "paid",
                            "amount": payload.get("amount"),
                            "paid_at": evento.get("created_at"),
                            "event_type": event_type,
                            "error": None
                        }
                    elif event_type == "transaction.completed" or status == "completed":
                        return {
                            "status": "completed",
                            "amount": payload.get("amount"),
                            "paid_at": evento.get("created_at"),
                            "event_type": event_type,
                            "error": None
                        }
                    elif status in ["expired", "cancelled", "failed", "denied", "time_out"]:
                        return {
                            "status": status,
                            "amount": payload.get("amount"),
                            "event_type": event_type,
                            "error": None
                        }

            # Si no encontramos eventos relacionados, el pago sigue pendiente
            logger.info(f"No se encontraron eventos para public_code {public_code}, asumiendo pendiente")
            return {"status": "pending", "error": None}

        except Exception as e:
            logger.error(f"Error consultando estado de payment order: {str(e)}")
            return {"status": "unknown", "error": str(e)}

    async def obtener_configuracion_webhook(self) -> dict:
        """
        Obtiene la configuración actual del webhook desde Vita.

        Útil para verificar si las categorías correctas están configuradas.

        Returns:
            {
                "webhook_url": "https://...",
                "configured_categories": ["payment", "deposit"],
                "available_categories": ["payment", "deposit", ...],
                "error": None
            }
        """
        try:
            headers = self._get_headers({})

            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{self.base_url}/api/businesses/webhooks",
                    headers=headers
                )

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "webhook_url": data.get("webhook_url"),
                        "configured_categories": data.get("configured_categories", []),
                        "available_categories": data.get("available_categories", []),
                        "error": None
                    }
                else:
                    return {
                        "webhook_url": None,
                        "configured_categories": [],
                        "available_categories": [],
                        "error": f"HTTP {response.status_code}: {response.text}"
                    }

        except Exception as e:
            logger.error(f"Error obteniendo configuración webhook: {str(e)}")
            return {
                "webhook_url": None,
                "configured_categories": [],
                "available_categories": [],
                "error": str(e)
            }

    async def actualizar_configuracion_webhook(
        self,
        webhook_url: str,
        categories: list
    ) -> dict:
        """
        Actualiza la configuración del webhook en Vita.

        Args:
            webhook_url: URL HTTPS donde Vita enviará los webhooks
            categories: Lista de categorías (ej: ["payment", "deposit"])

        Returns:
            {
                "success": True/False,
                "message": "...",
                "error": None
            }
        """
        try:
            payload = {
                "webhook_url": webhook_url,
                "categories": categories
            }

            headers = self._get_headers(payload)

            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.put(
                    f"{self.base_url}/api/businesses/webhooks",
                    headers=headers,
                    json=payload
                )

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "success": True,
                        "message": data.get("message", "Configuración actualizada"),
                        "webhook_url": data.get("webhook_url"),
                        "categories": data.get("categories"),
                        "error": None
                    }
                else:
                    return {
                        "success": False,
                        "message": "Error actualizando configuración",
                        "error": f"HTTP {response.status_code}: {response.text}"
                    }

        except Exception as e:
            logger.error(f"Error actualizando webhook: {str(e)}")
            return {
                "success": False,
                "message": "Error de conexión",
                "error": str(e)
            }

    async def obtener_ultimos_eventos(self) -> dict:
        """
        Obtiene los últimos 10 eventos del negocio desde Vita.

        Útil para debugging y verificar si los webhooks están llegando.

        Returns:
            {
                "events": [...],
                "total": 10,
                "error": None
            }
        """
        try:
            headers = self._get_headers({})

            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{self.base_url}/api/businesses/events",
                    headers=headers
                )

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "events": data.get("events", []),
                        "total": data.get("total", 0),
                        "error": None
                    }
                else:
                    return {
                        "events": [],
                        "total": 0,
                        "error": f"HTTP {response.status_code}: {response.text}"
                    }

        except Exception as e:
            logger.error(f"Error obteniendo eventos: {str(e)}")
            return {
                "events": [],
                "total": 0,
                "error": str(e)
            }


# Instancia global del servicio
vitawallet_service = VitaWalletService()
