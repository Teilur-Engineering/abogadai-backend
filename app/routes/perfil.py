from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.user import User
from ..schemas.user import UserProfileUpdate, UserResponse, PerfilEstado
from .auth import get_current_user

router = APIRouter(prefix="/perfil", tags=["Perfil"])


@router.get("/", response_model=UserResponse)
def obtener_perfil(current_user: User = Depends(get_current_user)):
    """
    Obtiene el perfil completo del usuario autenticado
    """
    return current_user


@router.get("/estado", response_model=PerfilEstado)
def verificar_estado_perfil(current_user: User = Depends(get_current_user)):
    """
    Verifica qué campos del perfil están completos y cuáles faltan
    """
    campos_requeridos = {
        'nombre': current_user.nombre,
        'apellido': current_user.apellido,
        'email': current_user.email,
        'identificacion': current_user.identificacion,
        'direccion': current_user.direccion,
        'telefono': current_user.telefono
    }

    campos_completados = [k for k, v in campos_requeridos.items() if v and str(v).strip()]
    campos_faltantes = [k for k, v in campos_requeridos.items() if not v or not str(v).strip()]

    return {
        "completo": len(campos_faltantes) == 0,
        "campos_faltantes": campos_faltantes,
        "campos_completados": campos_completados
    }


@router.put("/", response_model=UserResponse)
def actualizar_perfil(
    perfil_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualiza el perfil del usuario
    Solo actualiza los campos enviados
    """
    update_data = perfil_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(current_user, field, value)

    # Verificar si el perfil está completo
    current_user.perfil_completo = current_user.tiene_perfil_completo()

    db.commit()
    db.refresh(current_user)

    return current_user


@router.post("/completar", response_model=UserResponse)
def completar_perfil(
    perfil_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Endpoint para completar el perfil por primera vez
    Valida que todos los campos requeridos estén presentes
    """
    if not all([
        perfil_data.identificacion,
        perfil_data.direccion,
        perfil_data.telefono
    ]):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Faltan campos requeridos: identificacion, direccion, telefono"
        )

    current_user.identificacion = perfil_data.identificacion
    current_user.direccion = perfil_data.direccion
    current_user.telefono = perfil_data.telefono

    if perfil_data.nombre:
        current_user.nombre = perfil_data.nombre
    if perfil_data.apellido:
        current_user.apellido = perfil_data.apellido

    current_user.perfil_completo = True

    db.commit()
    db.refresh(current_user)

    return current_user
