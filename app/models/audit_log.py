from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from ..core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    admin_email = Column(String(200), nullable=False)

    # Qué acción se realizó
    accion = Column(String(100), nullable=False)   # APROBAR_REEMBOLSO, RECHAZAR_REEMBOLSO, etc.

    # Sobre qué entidad
    entidad = Column(String(50), nullable=False)   # caso, usuario, etc.
    entidad_id = Column(Integer, nullable=True)

    # Detalle libre (JSON) para contexto adicional
    detalle = Column(JSON, nullable=True)

    # Red
    ip = Column(String(50), nullable=True)

    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    admin = relationship("User", foreign_keys=[admin_id])
