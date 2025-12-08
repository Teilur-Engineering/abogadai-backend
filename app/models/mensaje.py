from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from ..core.database import Base


class Mensaje(Base):
    """
    Modelo para almacenar mensajes de conversaciones con el avatar durante las sesiones
    """
    __tablename__ = "mensajes"

    id = Column(Integer, primary_key=True, index=True)
    caso_id = Column(Integer, ForeignKey("casos.id"), nullable=False, index=True)

    # Contenido del mensaje
    remitente = Column(String(50), nullable=False)  # 'usuario' o 'asistente'
    texto = Column(Text, nullable=False)

    # Metadata
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    duracion_audio = Column(Integer, nullable=True)  # En milisegundos
    confianza = Column(Integer, nullable=True)  # Confianza del STT (0-100)

    # Relación con caso
    caso = relationship("Caso", back_populates="mensajes")
