from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..core.database import get_db
from ..models.mensaje import Mensaje
from ..models.caso import Caso
from ..schemas.mensaje import MensajeCreate, MensajeResponse

router = APIRouter(prefix="/mensajes", tags=["Mensajes"])


@router.post("/", response_model=MensajeResponse)
async def crear_mensaje(
    mensaje: MensajeCreate,
    db: Session = Depends(get_db)
):
    """
    🎯 ENDPOINT CRÍTICO - Webhook para guardar mensajes

    El agente llama este endpoint cada vez que hay:
    - Un mensaje del usuario (STT)
    - Una respuesta del asistente
    """
    # Verificar que el caso existe
    caso = db.query(Caso).filter(Caso.id == mensaje.caso_id).first()
    if not caso:
        raise HTTPException(status_code=404, detail="Caso no encontrado")

    nuevo_mensaje = Mensaje(**mensaje.model_dump())
    db.add(nuevo_mensaje)
    db.commit()
    db.refresh(nuevo_mensaje)

    return nuevo_mensaje


@router.get("/caso/{caso_id}", response_model=List[MensajeResponse])
async def obtener_mensajes_caso(
    caso_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene todos los mensajes de un caso ordenados por timestamp
    """
    # Verificar que el caso existe
    caso = db.query(Caso).filter(Caso.id == caso_id).first()
    if not caso:
        raise HTTPException(status_code=404, detail="Caso no encontrado")

    mensajes = db.query(Mensaje).filter(
        Mensaje.caso_id == caso_id
    ).order_by(Mensaje.timestamp).all()

    return mensajes
