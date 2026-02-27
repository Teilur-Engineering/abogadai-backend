import secrets
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
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
    UserCreate, UserLogin, UserResponse,
    ForgotPasswordRequest, ResetPasswordRequest, ResendVerificationRequest
)
from app.services.email_service import enviar_email_reset_contrasena, enviar_email_verificacion

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    # Read token from cookie first, then Bearer header as fallback (for agent)
    token = request.cookies.get('access_token')
    if not token:
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header[7:]

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
        )

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


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    hashed_password = get_password_hash(user_data.password)
    verification_token = secrets.token_urlsafe(32)
    new_user = User(
        email=user_data.email,
        nombre=user_data.nombre,
        apellido=user_data.apellido,
        hashed_password=hashed_password,
        email_verified=False,
        email_verification_token=verification_token,
        email_verification_expires=datetime.utcnow() + timedelta(hours=settings.EMAIL_VERIFICATION_EXPIRE_HOURS)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    try:
        await enviar_email_verificacion(
            email_destino=new_user.email,
            nombre=new_user.nombre,
            token=verification_token
        )
    except Exception:
        pass

    return {"message": "Cuenta creada. Revisa tu email para verificar."}


@router.post("/login")
def login(user_data: UserLogin, response: Response, db: Session = Depends(get_db)):
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

    if not user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="EMAIL_NOT_VERIFIED"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite=settings.COOKIE_SAMESITE,
        secure=settings.COOKIE_SECURE,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/"
    )

    # También devolver el token en el cuerpo para clientes cross-site
    # donde las cookies SameSite=lax no se envían en peticiones AJAX
    return {"message": "Login exitoso", "access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token", path="/")
    return {"message": "Sesión cerrada"}


@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.email_verification_token == token
    ).first()

    token_invalido = (
        user is None
        or user.email_verification_expires is None
        or datetime.utcnow() > user.email_verification_expires
    )

    if token_invalido:
        if user:
            user.email_verification_token = None
            user.email_verification_expires = None
            db.commit()
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/login?verificado=error")

    user.email_verified = True
    user.email_verification_token = None
    user.email_verification_expires = None
    db.commit()

    return RedirectResponse(url=f"{settings.FRONTEND_URL}/login?verificado=true")


@router.post("/resend-verification", status_code=status.HTTP_200_OK)
async def resend_verification(
    request_data: ResendVerificationRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == request_data.email).first()

    if user and user.is_active and not user.email_verified:
        token = secrets.token_urlsafe(32)
        user.email_verification_token = token
        user.email_verification_expires = datetime.utcnow() + timedelta(hours=settings.EMAIL_VERIFICATION_EXPIRE_HOURS)
        db.commit()

        try:
            await enviar_email_verificacion(
                email_destino=user.email,
                nombre=user.nombre,
                token=token
            )
        except Exception:
            pass

    return {"message": "Si el email está registrado y sin verificar, recibirás un nuevo enlace de verificación"}


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
