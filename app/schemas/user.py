from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    nombre: str
    apellido: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserProfileUpdate(BaseModel):
    """Schema para actualizar el perfil del usuario"""
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    identificacion: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None

    @field_validator('identificacion')
    def validar_identificacion(cls, v):
        if v is not None and v.strip():
            v_clean = v.strip()
            if not v_clean.isdigit():
                raise ValueError('La identificación debe contener solo dígitos')
            if len(v_clean) < 6 or len(v_clean) > 15:
                raise ValueError('La identificación debe tener entre 6 y 15 dígitos')
        return v

    @field_validator('telefono')
    def validar_telefono(cls, v):
        if v is not None and v.strip():
            v_clean = v.strip()
            if not v_clean.isdigit():
                raise ValueError('El teléfono debe contener solo dígitos')
            if len(v_clean) < 7 or len(v_clean) > 15:
                raise ValueError('El teléfono debe tener entre 7 y 15 dígitos')
        return v


class UserResponse(UserBase):
    id: int
    identificacion: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    perfil_completo: bool
    is_active: bool
    is_admin: bool
    email_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


class PerfilEstado(BaseModel):
    """Indica qué campos del perfil están completos y cuáles faltan"""
    completo: bool
    campos_faltantes: list[str]
    campos_completados: list[str]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class ResendVerificationRequest(BaseModel):
    email: EmailStr


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

    @field_validator('new_password')
    def validar_password(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        return v
