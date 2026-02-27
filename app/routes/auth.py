import secrets
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token
)
from app.core.config import settings
from app.models.user import User
from app.schemas.user import (
    UserCreate, UserLogin, UserResponse, Token,
    ForgotPasswordRequest, ResetPasswordRequest
)
from app.services.email_service import enviar_email_reset_contrasena

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )

    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
        )

    return user


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    # Crear nuevo usuario
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        nombre=user_data.nombre,
        apellido=user_data.apellido,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # Buscar usuario
    user = db.query(User).filter(User.email == user_data.email).first()

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )

    # Crear token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(
    request_data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Solicita recuperación de contraseña.

    Genera un token de reset (válido 1 hora) y envía el email.
    Siempre retorna 200 para no revelar si el email existe o no.
    """
    user = db.query(User).filter(User.email == request_data.email).first()

    if user and user.is_active:
        token = secrets.token_urlsafe(32)
        user.reset_password_token = token
        user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        db.commit()

        try:
            await enviar_email_reset_contrasena(
                email_destino=user.email,
                nombre=user.nombre,
                token=token
            )
        except Exception:
            # No exponer el error al cliente; el log ya registró el detalle
            pass

    return {
        "message": "Si el email está registrado, recibirás un enlace para restablecer tu contraseña"
    }


@router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password(
    request_data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Restablece la contraseña usando el token recibido por email.

    El token es de un solo uso y expira en 1 hora.
    """
    user = db.query(User).filter(
        User.reset_password_token == request_data.token
    ).first()

    token_invalido = (
        user is None
        or user.reset_token_expires is None
        or datetime.utcnow() > user.reset_token_expires
    )

    if token_invalido:
        # Limpiar token si el usuario existe pero expiró
        if user:
            user.reset_password_token = None
            user.reset_token_expires = None
            db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido o expirado"
        )

    user.hashed_password = get_password_hash(request_data.new_password)
    user.reset_password_token = None
    user.reset_token_expires = None
    db.commit()

    return {"message": "Contraseña restablecida exitosamente"}
