from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Campos de perfil
    identificacion = Column(String(50), nullable=True, index=True)
    direccion = Column(Text, nullable=True)
    telefono = Column(String(50), nullable=True)
    perfil_completo = Column(Boolean, default=False, nullable=False)

    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    casos = relationship("Caso", back_populates="user")

    def tiene_perfil_completo(self):
        """Verifica si todos los campos del perfil están completos"""
        return all([
            self.nombre,
            self.apellido,
            self.email,
            self.identificacion,
            self.direccion,
            self.telefono
        ])
