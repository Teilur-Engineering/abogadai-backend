"""
Servicio de auditoría para acciones administrativas.
Registra cada acción sensible con admin, entidad, detalle e IP.
"""
import logging
from datetime import datetime
from typing import Optional, Any
from sqlalchemy.orm import Session

from ..models.audit_log import AuditLog

logger = logging.getLogger(__name__)

# Constantes de acciones (evitar strings mágicos en el resto del código)
ACCION_APROBAR_REEMBOLSO = "APROBAR_REEMBOLSO"
ACCION_RECHAZAR_REEMBOLSO = "RECHAZAR_REEMBOLSO"
ACCION_PROCESAR_REEMBOLSO = "PROCESAR_REEMBOLSO"
ACCION_DESBLOQUEAR_DOCUMENTO = "DESBLOQUEAR_DOCUMENTO"


def registrar_auditoria(
    db: Session,
    admin_id: int,
    admin_email: str,
    accion: str,
    entidad: str,
    entidad_id: Optional[int] = None,
    detalle: Optional[dict] = None,
    ip: Optional[str] = None,
) -> AuditLog:
    """
    Registra una acción administrativa en el log de auditoría.

    Args:
        db: Sesión de base de datos
        admin_id: ID del admin que realiza la acción
        admin_email: Email del admin (desnormalizado para lectura rápida)
        accion: Identificador de la acción (usar constantes ACCION_*)
        entidad: Nombre de la entidad afectada ("caso", "usuario", etc.)
        entidad_id: ID de la entidad afectada
        detalle: Dict con información adicional (motivo, resultado, etc.)
        ip: IP del cliente

    Returns:
        Registro AuditLog creado
    """
    try:
        log = AuditLog(
            admin_id=admin_id,
            admin_email=admin_email,
            accion=accion,
            entidad=entidad,
            entidad_id=entidad_id,
            detalle=detalle or {},
            ip=ip,
            timestamp=datetime.utcnow(),
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        logger.info(
            f"[AUDIT] {accion} | admin={admin_email} | "
            f"{entidad}={entidad_id} | ip={ip}"
        )
        return log
    except Exception as e:
        # La auditoría nunca debe romper el flujo principal
        logger.error(f"[AUDIT] Error registrando auditoría: {e}")
        try:
            db.rollback()
        except Exception:
            pass
        return None
