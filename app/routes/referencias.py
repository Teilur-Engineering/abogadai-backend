"""
Rutas para acceder a datos de referencia colombianos
"""
from fastapi import APIRouter, Query
from typing import List, Dict, Optional
from ..core.datos_colombia import (
    DERECHOS_FUNDAMENTALES,
    ENTIDADES_PUBLICAS,
    DEPARTAMENTOS,
    CIUDADES_PRINCIPALES,
    obtener_derechos_por_categoria,
    obtener_entidades_por_tipo,
    buscar_entidad
)

router = APIRouter(prefix="/api/referencias", tags=["referencias"])


@router.get("/derechos-fundamentales")
def obtener_derechos(
    categoria: Optional[str] = Query(None, description="Filtrar por: fundamentales, conexidad")
):
    """
    Obtiene la lista de derechos fundamentales de la Constitución Política de Colombia.

    - **categoria**: Opcional - 'fundamentales' para derechos fundamentales puros,
                    'conexidad' para derechos por conexidad
    """
    return {
        "derechos": obtener_derechos_por_categoria(categoria),
        "total": len(obtener_derechos_por_categoria(categoria))
    }


@router.get("/entidades-publicas")
def obtener_entidades(
    tipo: Optional[str] = Query(
        None,
        description="Tipo de entidad: EPS, MINISTERIOS, SUPERINTENDENCIAS, etc."
    )
):
    """
    Obtiene la lista de entidades públicas comunes en Colombia.

    - **tipo**: Opcional - EPS, MINISTERIOS, SUPERINTENDENCIAS, ENTIDADES_AUTONOMAS,
               FUERZAS_PUBLICAS, EDUCACION, GOBIERNOS_TERRITORIALES, PENSIONES
    """
    if tipo:
        entidades = obtener_entidades_por_tipo(tipo)
        return {
            "tipo": tipo,
            "entidades": entidades,
            "total": len(entidades)
        }
    else:
        return {
            "categorias": ENTIDADES_PUBLICAS,
            "total_categorias": len(ENTIDADES_PUBLICAS)
        }


@router.get("/entidades-publicas/buscar")
def buscar_entidades(
    q: str = Query(..., description="Término de búsqueda", min_length=2)
):
    """
    Busca entidades públicas por término.

    - **q**: Término de búsqueda (mínimo 2 caracteres)
    """
    resultados = buscar_entidad(q)
    return {
        "query": q,
        "resultados": resultados,
        "total": len(resultados)
    }


@router.get("/departamentos")
def obtener_departamentos():
    """
    Obtiene la lista de departamentos de Colombia.
    """
    return {
        "departamentos": DEPARTAMENTOS,
        "total": len(DEPARTAMENTOS)
    }


@router.get("/ciudades")
def obtener_ciudades():
    """
    Obtiene la lista de ciudades principales de Colombia.
    """
    return {
        "ciudades": CIUDADES_PRINCIPALES,
        "total": len(CIUDADES_PRINCIPALES)
    }


@router.get("/validar/cedula/{cedula}")
def validar_cedula_endpoint(cedula: str):
    """
    Valida si una cédula colombiana tiene formato válido.

    - **cedula**: Número de cédula a validar
    """
    from ..core.validators import validar_cedula_colombiana, formatear_cedula

    es_valida = validar_cedula_colombiana(cedula)

    return {
        "cedula": cedula,
        "es_valida": es_valida,
        "cedula_formateada": formatear_cedula(cedula) if es_valida else None
    }


@router.get("/validar/nit/{nit}")
def validar_nit_endpoint(nit: str):
    """
    Valida si un NIT colombiano tiene formato válido.

    - **nit**: NIT a validar
    """
    from ..core.validators import validar_nit_colombiano, formatear_nit

    es_valido = validar_nit_colombiano(nit)

    return {
        "nit": nit,
        "es_valido": es_valido,
        "nit_formateado": formatear_nit(nit) if es_valido else None
    }
