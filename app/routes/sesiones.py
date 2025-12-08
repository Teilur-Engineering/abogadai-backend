from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from livekit import api
from datetime import datetime, timedelta
import uuid

from ..core.config import settings
from ..core.database import get_db
from ..models.user import User
from ..models.caso import Caso, TipoDocumento, EstadoCaso
from .auth import get_current_user

router = APIRouter(prefix="/sesiones", tags=["Sesiones"])


@router.post("/iniciar")
async def iniciar_sesion(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    🎯 ENDPOINT CRÍTICO - Inicia una sesión con el avatar

    1. Crea un nuevo Caso con estado 'borrador'
    2. Genera un room_name único
    3. Genera un token de acceso para LiveKit
    4. Retorna toda la info para conectar al frontend
    """

    try:
        # 1. Crear nuevo caso
        room_name = f"caso-{uuid.uuid4().hex[:12]}"
        session_id = str(uuid.uuid4())

        nuevo_caso = Caso(
            user_id=current_user.id,
            tipo_documento=TipoDocumento.TUTELA,
            estado=EstadoCaso.BORRADOR,
            session_id=session_id,
            room_name=room_name,
            fecha_inicio_sesion=datetime.utcnow(),
            nombre_solicitante=f"{current_user.nombre} {current_user.apellido}",
            email_solicitante=current_user.email
        )

        db.add(nuevo_caso)
        db.commit()
        db.refresh(nuevo_caso)

        # 2. Generar token de LiveKit
        if not settings.LIVEKIT_API_KEY or not settings.LIVEKIT_API_SECRET:
            raise HTTPException(
                status_code=500,
                detail="LiveKit credentials not configured"
            )

        token = api.AccessToken(settings.LIVEKIT_API_KEY, settings.LIVEKIT_API_SECRET)
        token.with_identity(f"user-{nuevo_caso.id}")
        token.with_name(f"{current_user.nombre} {current_user.apellido}")
        token.with_grants(api.VideoGrants(
            room_join=True,
            room=room_name,
        ))
        token.with_metadata(f"caso_id:{nuevo_caso.id}")  # Metadata importante para el agente
        token.with_ttl(timedelta(hours=2))

        access_token = token.to_jwt()

        return {
            "caso_id": nuevo_caso.id,
            "session_id": session_id,
            "room_name": room_name,
            "livekit_url": settings.LIVEKIT_URL,
            "access_token": access_token
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error iniciando sesión: {str(e)}"
        )


@router.put("/{caso_id}/finalizar")
async def finalizar_sesion(
    caso_id: int,
    db: Session = Depends(get_db)
):
    """
    🎯 ENDPOINT CRÍTICO - Finaliza una sesión con el avatar

    Marca la fecha de finalización de la sesión
    NO cambia el estado porque el caso sigue en 'borrador' hasta que el usuario genere el documento
    """
    caso = db.query(Caso).filter(Caso.id == caso_id).first()
    if not caso:
        raise HTTPException(status_code=404, detail="Caso no encontrado")

    caso.fecha_fin_sesion = datetime.utcnow()
    db.commit()

    return {
        "message": "Sesión finalizada",
        "caso_id": caso_id,
        "duracion_minutos": (caso.fecha_fin_sesion - caso.fecha_inicio_sesion).total_seconds() / 60 if caso.fecha_inicio_sesion else None
    }
