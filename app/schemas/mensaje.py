from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MensajeBase(BaseModel):
    remitente: str  # 'usuario' o 'asistente'
    texto: str


class MensajeCreate(MensajeBase):
    caso_id: int
    duracion_audio: Optional[int] = None
    confianza: Optional[int] = None


class MensajeResponse(MensajeBase):
    id: int
    caso_id: int
    timestamp: datetime
    duracion_audio: Optional[int]
    confianza: Optional[int]

    class Config:
        from_attributes = True
