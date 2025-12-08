from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from livekit import api
from datetime import datetime, timedelta
import uuid

from ..core.config import settings
from ..core.database import get_db
from ..models.user import User
from ..models.caso import Caso, TipoDocumento, EstadoCaso
from .auth import get_current_user

router = APIRouter(prefix="/livekit", tags=["livekit"])


@router.post("/token")
async def get_livekit_token(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    🔄 ENDPOINT LEGACY - Redirige a la nueva lógica de sesiones

    Genera un token de LiveKit Y crea un caso automáticamente
    Este endpoint mantiene compatibilidad con el frontend antiguo
    """
    try:
        # 1. Crear nuevo caso (igual que /sesiones/iniciar)
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
        token = api.AccessToken(
            settings.LIVEKIT_API_KEY,
            settings.LIVEKIT_API_SECRET
        )

        user_identity = f"user-{nuevo_caso.id}"
        user_name = f"{current_user.nombre} {current_user.apellido}"

        # Agregar permisos al token
        token.with_identity(user_identity).with_name(user_name).with_grants(
            api.VideoGrants(
                room_join=True,
                room=room_name,
                can_publish=True,
                can_subscribe=True,
            )
        )

        # Agregar metadata con el caso_id (CRÍTICO para el agente)
        token.with_metadata(f"caso_id:{nuevo_caso.id}")

        # Tiempo de expiración del token (2 horas)
        token.with_ttl(timedelta(hours=2))

        # Generar el JWT
        jwt_token = token.to_jwt()

        return {
            "token": jwt_token,
            "url": settings.LIVEKIT_URL,
            "room_name": room_name,
            "user_identity": user_identity,
            "user_name": user_name,
            "caso_id": nuevo_caso.id,  # NUEVO: retornar el caso_id
            "session_id": session_id
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error generando token de LiveKit: {str(e)}"
        )
