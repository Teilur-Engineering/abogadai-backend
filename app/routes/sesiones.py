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
    🎯 ENDPOINT MODIFICADO - Crea un caso pero NO genera token LiveKit

    Cambio según plan.md:
    - Solo crea el caso en estado BORRADOR
    - Pre-llena datos del perfil del usuario
    - Genera room_name único para uso futuro
    - NO genera token de LiveKit (eso se hace en /sesiones/{caso_id}/conectar)
    - NO marca fecha_inicio_sesion (eso se hace al conectar)

    El frontend mostrará la UI en estado "Pre-llamada" con botón "Iniciar sesión"
    """

    try:
        # 1. Crear nuevo caso (sin iniciar sesión de LiveKit aún)
        session_id = str(uuid.uuid4())

        # Crear el caso primero para obtener el ID
        nuevo_caso = Caso(
            user_id=current_user.id,
            tipo_documento=TipoDocumento.TUTELA,
            estado=EstadoCaso.BORRADOR,
            session_id=session_id,
            room_name=None,  # Se asignará después de obtener el ID
            # ❌ NO marcar fecha_inicio_sesion aquí (se marca al conectar)
            # fecha_inicio_sesion=datetime.utcnow(),
            # ✅ Auto-llenar TODOS los datos del perfil del usuario
            nombre_solicitante=f"{current_user.nombre} {current_user.apellido}",
            email_solicitante=current_user.email,
            identificacion_solicitante=current_user.identificacion if current_user.identificacion else None,
            direccion_solicitante=current_user.direccion if current_user.direccion else None,
            telefono_solicitante=current_user.telefono if current_user.telefono else None
        )

        db.add(nuevo_caso)
        db.commit()  # Commit para obtener el ID
        db.refresh(nuevo_caso)

        # Ahora que tenemos el ID, actualizar el room_name en formato esperado por el agente
        nuevo_caso.room_name = f"caso-{nuevo_caso.id}"  # ✅ Formato: caso-123
        db.commit()
        db.refresh(nuevo_caso)

        # 2. ✅ NO generar token de LiveKit aquí
        # El token se generará cuando el usuario presione "Iniciar sesión"
        # mediante el endpoint /sesiones/{caso_id}/conectar

        return {
            "caso_id": nuevo_caso.id,
            "session_id": session_id,
            "room_name": nuevo_caso.room_name,
            "tipo_documento": nuevo_caso.tipo_documento.value,
            "nombre_solicitante": nuevo_caso.nombre_solicitante
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error creando caso: {str(e)}"
        )


@router.post("/{caso_id}/conectar")
async def conectar_sesion(
    caso_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    🎯 ENDPOINT NUEVO - Genera token de LiveKit para conectar a la sesión

    Cambio según plan.md:
    - Se llama cuando el usuario presiona "Iniciar sesión" en el estado Pre-llamada
    - Genera el token de acceso para LiveKit
    - Marca fecha_inicio_sesion
    - Retorna token y URL para que el frontend se conecte

    Este endpoint separa la creación del caso (POST /iniciar) de la conexión a LiveKit
    """
    caso = db.query(Caso).filter(
        Caso.id == caso_id,
        Caso.user_id == current_user.id
    ).first()

    if not caso:
        raise HTTPException(status_code=404, detail="Caso no encontrado")

    try:
        # 1. Marcar inicio de sesión
        if not caso.fecha_inicio_sesion:
            caso.fecha_inicio_sesion = datetime.utcnow()
            db.commit()

        # 2. Generar token de LiveKit
        if not settings.LIVEKIT_API_KEY or not settings.LIVEKIT_API_SECRET:
            raise HTTPException(
                status_code=500,
                detail="LiveKit credentials not configured"
            )

        token = api.AccessToken(settings.LIVEKIT_API_KEY, settings.LIVEKIT_API_SECRET)
        token.with_identity(f"user-{caso.id}")
        token.with_name(f"{current_user.nombre} {current_user.apellido}")
        token.with_grants(api.VideoGrants(
            room_join=True,
            room=caso.room_name,
        ))
        token.with_metadata(f"caso_id:{caso.id}")  # Metadata importante para el agente
        token.with_ttl(timedelta(hours=2))

        access_token = token.to_jwt()

        return {
            "caso_id": caso.id,
            "room_name": caso.room_name,
            "livekit_url": settings.LIVEKIT_URL,
            "access_token": access_token,
            "user_identity": f"user-{caso.id}",
            "user_name": f"{current_user.nombre} {current_user.apellido}"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generando token de LiveKit: {str(e)}"
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
