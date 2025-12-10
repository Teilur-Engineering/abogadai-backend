from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum
from ..core.validators import (
    validar_cedula_colombiana,
    validar_nit_colombiano,
    validar_telefono_colombiano,
    validar_email
)


class TipoDocumentoEnum(str, Enum):
    TUTELA = "tutela"
    DERECHO_PETICION = "derecho_peticion"


class EstadoCasoEnum(str, Enum):
    BORRADOR = "borrador"
    GENERADO = "generado"
    FINALIZADO = "finalizado"


class CasoBase(BaseModel):
    tipo_documento: TipoDocumentoEnum = TipoDocumentoEnum.TUTELA
    nombre_solicitante: Optional[str] = None
    identificacion_solicitante: Optional[str] = None
    direccion_solicitante: Optional[str] = None
    telefono_solicitante: Optional[str] = None
    email_solicitante: Optional[str] = None
    actua_en_representacion: bool = False
    nombre_representado: Optional[str] = None
    identificacion_representado: Optional[str] = None
    relacion_representado: Optional[str] = None
    tipo_representado: Optional[str] = None
    entidad_accionada: Optional[str] = None
    direccion_entidad: Optional[str] = None
    representante_legal: Optional[str] = None
    hechos: Optional[str] = None
    derechos_vulnerados: Optional[str] = None
    pretensiones: Optional[str] = None
    fundamentos_derecho: Optional[str] = None
    pruebas: Optional[str] = None

    @field_validator('identificacion_solicitante')
    @classmethod
    def validar_identificacion(cls, v: Optional[str]) -> Optional[str]:
        """Valida que la identificación sea una cédula o NIT válido"""
        if v is None or v.strip() == "":
            return v

        # Intentar validar como cédula primero
        if validar_cedula_colombiana(v):
            return v

        # Si no es cédula, intentar como NIT
        if validar_nit_colombiano(v):
            return v

        # Si no es ninguno, lanzar error
        raise ValueError(
            'La identificación debe ser una cédula colombiana válida (6-10 dígitos) '
            'o un NIT válido (formato: XXXXXXXXX-X)'
        )

    @field_validator('telefono_solicitante')
    @classmethod
    def validar_telefono(cls, v: Optional[str]) -> Optional[str]:
        """Valida que el teléfono tenga formato colombiano"""
        if v is None or v.strip() == "":
            return v

        if not validar_telefono_colombiano(v):
            raise ValueError(
                'El teléfono debe ser un número colombiano válido '
                '(7 dígitos para fijo o 10 para celular)'
            )

        return v

    @field_validator('email_solicitante')
    @classmethod
    def validar_email_solicitante(cls, v: Optional[str]) -> Optional[str]:
        """Valida que el email tenga formato válido"""
        if v is None or v.strip() == "":
            return v

        if not validar_email(v):
            raise ValueError('El email no tiene un formato válido')

        return v


class CasoCreate(CasoBase):
    pass


class CasoUpdate(BaseModel):
    tipo_documento: Optional[TipoDocumentoEnum] = None
    nombre_solicitante: Optional[str] = None
    identificacion_solicitante: Optional[str] = None
    direccion_solicitante: Optional[str] = None
    telefono_solicitante: Optional[str] = None
    email_solicitante: Optional[str] = None
    actua_en_representacion: Optional[bool] = None
    nombre_representado: Optional[str] = None
    identificacion_representado: Optional[str] = None
    relacion_representado: Optional[str] = None
    tipo_representado: Optional[str] = None
    entidad_accionada: Optional[str] = None
    direccion_entidad: Optional[str] = None
    representante_legal: Optional[str] = None
    hechos: Optional[str] = None
    derechos_vulnerados: Optional[str] = None
    pretensiones: Optional[str] = None
    fundamentos_derecho: Optional[str] = None
    pruebas: Optional[str] = None
    estado: Optional[EstadoCasoEnum] = None
    documento_generado: Optional[str] = None


class CasoResponse(CasoBase):
    id: int
    user_id: int
    estado: EstadoCasoEnum
    documento_generado: Optional[str] = None
    analisis_fortaleza: Optional[Dict[str, Any]] = None
    analisis_calidad: Optional[Dict[str, Any]] = None
    analisis_jurisprudencia: Optional[Dict[str, Any]] = None
    sugerencias_mejora: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CasoListResponse(BaseModel):
    id: int
    tipo_documento: TipoDocumentoEnum
    estado: EstadoCasoEnum
    nombre_solicitante: Optional[str] = None
    entidad_accionada: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
