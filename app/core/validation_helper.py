"""
Helper de validación para casos legales

Este módulo proporciona validaciones amigables con dos niveles:
- ADVERTENCIAS: El campo tiene formato sospechoso pero se permite guardar
- ERRORES CRÍTICOS: El campo es obligatorio para generar el documento legal
"""

from typing import Dict, List, Optional
from .validators import (
    validar_cedula_colombiana,
    validar_nit_colombiano,
    validar_telefono_colombiano,
    validar_email
)


class ValidationLevel:
    """Niveles de severidad de validación"""
    WARNING = "warning"  # 🟡 Advertencia - permite continuar
    ERROR = "error"      # 🔴 Error crítico - bloquea generar documento


class ValidationMessage:
    """Representa un mensaje de validación"""
    def __init__(self, field: str, level: str, message: str):
        self.field = field
        self.level = level
        self.message = message

    def to_dict(self) -> dict:
        return {
            "field": self.field,
            "level": self.level,
            "message": self.message
        }


def validar_identificacion(identificacion: Optional[str]) -> Optional[ValidationMessage]:
    """
    Valida el formato de una identificación (cédula o NIT)

    Returns:
        ValidationMessage si hay problema, None si es válido
    """
    if not identificacion or identificacion.strip() == "":
        return None  # Campo vacío no genera advertencia aquí

    # Intentar validar como cédula o NIT
    if validar_cedula_colombiana(identificacion) or validar_nit_colombiano(identificacion):
        return None

    # Si no es válida, generar advertencia
    return ValidationMessage(
        field="identificacion_solicitante",
        level=ValidationLevel.WARNING,
        message="Esta identificación no parece tener un formato válido. Verifica que sea correcta. Formato esperado: cédula de 6-10 dígitos o NIT con formato XXXXXXXXX-X"
    )


def validar_telefono(telefono: Optional[str]) -> Optional[ValidationMessage]:
    """
    Valida el formato de un teléfono colombiano

    Returns:
        ValidationMessage si hay problema, None si es válido
    """
    if not telefono or telefono.strip() == "":
        return None

    if validar_telefono_colombiano(telefono):
        return None

    return ValidationMessage(
        field="telefono_solicitante",
        level=ValidationLevel.WARNING,
        message="Este teléfono no parece tener un formato válido. Los celulares colombianos tienen 10 dígitos (ejemplo: 3001234567) y los fijos 7 dígitos."
    )


def validar_email_format(email: Optional[str]) -> Optional[ValidationMessage]:
    """
    Valida el formato de un email

    Returns:
        ValidationMessage si hay problema, None si es válido
    """
    if not email or email.strip() == "":
        return None

    if validar_email(email):
        return None

    return ValidationMessage(
        field="email_solicitante",
        level=ValidationLevel.WARNING,
        message="Este email no parece tener un formato válido. Verifica que tenga @ y un dominio (ejemplo: usuario@dominio.com)"
    )


def validar_campos_criticos_tutela(datos_caso: dict) -> List[ValidationMessage]:
    """
    Valida los campos CRÍTICOS necesarios para generar una tutela

    Args:
        datos_caso: Diccionario con los datos del caso

    Returns:
        Lista de ValidationMessage con errores críticos (vacía si todo está bien)
    """
    errores = []

    # Campos obligatorios para tutela
    if not datos_caso.get('nombre_solicitante') or datos_caso['nombre_solicitante'].strip() == "":
        errores.append(ValidationMessage(
            field="nombre_solicitante",
            level=ValidationLevel.ERROR,
            message="El nombre del solicitante es obligatorio para generar el documento legal."
        ))

    if not datos_caso.get('identificacion_solicitante') or datos_caso['identificacion_solicitante'].strip() == "":
        errores.append(ValidationMessage(
            field="identificacion_solicitante",
            level=ValidationLevel.ERROR,
            message="La identificación del solicitante es obligatoria para generar el documento legal."
        ))
    else:
        # Si tiene identificación, validar que sea válida (error crítico, no advertencia)
        if not (validar_cedula_colombiana(datos_caso['identificacion_solicitante']) or
                validar_nit_colombiano(datos_caso['identificacion_solicitante'])):
            errores.append(ValidationMessage(
                field="identificacion_solicitante",
                level=ValidationLevel.ERROR,
                message="La identificación debe tener un formato válido de cédula colombiana (6-10 dígitos) o NIT (XXXXXXXXX-X)."
            ))

    if not datos_caso.get('entidad_accionada') or datos_caso['entidad_accionada'].strip() == "":
        errores.append(ValidationMessage(
            field="entidad_accionada",
            level=ValidationLevel.ERROR,
            message="La entidad accionada es obligatoria. Debes especificar contra quién se presenta la tutela."
        ))

    if not datos_caso.get('hechos') or datos_caso['hechos'].strip() == "":
        errores.append(ValidationMessage(
            field="hechos",
            level=ValidationLevel.ERROR,
            message="Los hechos del caso son obligatorios. Debes narrar qué sucedió para fundamentar la tutela."
        ))

    # NOTA: derechos_vulnerados ya NO es obligatorio (ahora es recomendado pero opcional)
    # La IA intentará extraerlo, pero si no lo hace o el usuario no lo completa, no bloqueará

    if not datos_caso.get('pretensiones') or datos_caso['pretensiones'].strip() == "":
        errores.append(ValidationMessage(
            field="pretensiones",
            level=ValidationLevel.ERROR,
            message="Las pretensiones son obligatorias. Debes indicar qué solicitas que ordene el juez."
        ))

    return errores


def validar_campos_criticos_derecho_peticion(datos_caso: dict) -> List[ValidationMessage]:
    """
    Valida los campos CRÍTICOS necesarios para generar un derecho de petición

    Args:
        datos_caso: Diccionario con los datos del caso

    Returns:
        Lista de ValidationMessage con errores críticos (vacía si todo está bien)
    """
    errores = []

    # Campos obligatorios para derecho de petición
    if not datos_caso.get('nombre_solicitante') or datos_caso['nombre_solicitante'].strip() == "":
        errores.append(ValidationMessage(
            field="nombre_solicitante",
            level=ValidationLevel.ERROR,
            message="El nombre del solicitante es obligatorio para generar el documento legal."
        ))

    if not datos_caso.get('identificacion_solicitante') or datos_caso['identificacion_solicitante'].strip() == "":
        errores.append(ValidationMessage(
            field="identificacion_solicitante",
            level=ValidationLevel.ERROR,
            message="La identificación del solicitante es obligatoria para generar el documento legal."
        ))
    else:
        # Validar formato
        if not (validar_cedula_colombiana(datos_caso['identificacion_solicitante']) or
                validar_nit_colombiano(datos_caso['identificacion_solicitante'])):
            errores.append(ValidationMessage(
                field="identificacion_solicitante",
                level=ValidationLevel.ERROR,
                message="La identificación debe tener un formato válido de cédula colombiana (6-10 dígitos) o NIT (XXXXXXXXX-X)."
            ))

    if not datos_caso.get('entidad_accionada') or datos_caso['entidad_accionada'].strip() == "":
        errores.append(ValidationMessage(
            field="entidad_accionada",
            level=ValidationLevel.ERROR,
            message="La entidad destinataria es obligatoria. Debes especificar a quién se dirige el derecho de petición."
        ))

    if not datos_caso.get('hechos') or datos_caso['hechos'].strip() == "":
        errores.append(ValidationMessage(
            field="hechos",
            level=ValidationLevel.ERROR,
            message="Los hechos del caso son obligatorios. Debes narrar la situación que motiva la petición."
        ))

    if not datos_caso.get('pretensiones') or datos_caso['pretensiones'].strip() == "":
        errores.append(ValidationMessage(
            field="pretensiones",
            level=ValidationLevel.ERROR,
            message="Las peticiones son obligatorias. Debes indicar qué información o actuación solicitas a la entidad."
        ))

    return errores


def validar_campos_importantes(datos_caso: dict) -> List[ValidationMessage]:
    """
    Valida los campos IMPORTANTES pero no críticos
    Genera advertencias que no bloquean la generación del documento

    Args:
        datos_caso: Diccionario con los datos del caso

    Returns:
        Lista de ValidationMessage con advertencias
    """
    advertencias = []

    # Validar formato de identificación (si existe)
    if datos_caso.get('identificacion_solicitante'):
        msg = validar_identificacion(datos_caso['identificacion_solicitante'])
        if msg:
            advertencias.append(msg)

    # Validar formato de teléfono (si existe)
    if datos_caso.get('telefono_solicitante'):
        msg = validar_telefono(datos_caso['telefono_solicitante'])
        if msg:
            advertencias.append(msg)

    # Validar formato de email (si existe)
    if datos_caso.get('email_solicitante'):
        msg = validar_email_format(datos_caso['email_solicitante'])
        if msg:
            advertencias.append(msg)

    # Advertencia si falta dirección (importante para notificaciones)
    if not datos_caso.get('direccion_solicitante') or datos_caso['direccion_solicitante'].strip() == "":
        advertencias.append(ValidationMessage(
            field="direccion_solicitante",
            level=ValidationLevel.WARNING,
            message="Se recomienda especificar una dirección completa para recibir notificaciones judiciales."
        ))

    return advertencias


def validar_caso_preliminar(caso, tipo_documento: str) -> Dict[str, any]:
    """
    🎯 VALIDACIÓN PRELIMINAR (NO BLOQUEANTE)

    Valida el caso después del auto-llenado con IA.
    Genera SOLO ADVERTENCIAS, nunca bloquea.
    Permite que el usuario vea todos los datos extraídos (incluso si están mal)
    y los corrija antes de generar el documento.

    Args:
        caso: Objeto Caso de SQLAlchemy
        tipo_documento: "tutela" o "derecho_peticion"

    Returns:
        Dict con estructura:
        {
            "valido": false (siempre, porque es preliminar),
            "errores": [],  # Siempre vacío en validación preliminar
            "advertencias": [...]  # Todas las validaciones como advertencias
        }
    """
    # Convertir caso a dict
    datos_caso = {
        'nombre_solicitante': caso.nombre_solicitante,
        'identificacion_solicitante': caso.identificacion_solicitante,
        'direccion_solicitante': caso.direccion_solicitante,
        'telefono_solicitante': caso.telefono_solicitante,
        'email_solicitante': caso.email_solicitante,
        'entidad_accionada': caso.entidad_accionada,
        'hechos': caso.hechos,
        'derechos_vulnerados': caso.derechos_vulnerados,
        'pretensiones': caso.pretensiones,
    }

    advertencias = []

    # Campos obligatorios - generar advertencias si están vacíos
    if not datos_caso.get('nombre_solicitante') or datos_caso['nombre_solicitante'].strip() == "":
        advertencias.append(ValidationMessage(
            field="nombre_solicitante",
            level=ValidationLevel.WARNING,
            message="El nombre del solicitante está vacío. Debes completarlo antes de generar el documento."
        ))

    if not datos_caso.get('identificacion_solicitante') or datos_caso['identificacion_solicitante'].strip() == "":
        advertencias.append(ValidationMessage(
            field="identificacion_solicitante",
            level=ValidationLevel.WARNING,
            message="La identificación del solicitante está vacía. Debes completarla antes de generar el documento."
        ))
    else:
        # Validar formato (como advertencia, no como error)
        if not (validar_cedula_colombiana(datos_caso['identificacion_solicitante']) or
                validar_nit_colombiano(datos_caso['identificacion_solicitante'])):
            advertencias.append(ValidationMessage(
                field="identificacion_solicitante",
                level=ValidationLevel.WARNING,
                message="Esta identificación no parece válida. Verifica que sea correcta (cédula de 6-10 dígitos o NIT)."
            ))

    if not datos_caso.get('entidad_accionada') or datos_caso['entidad_accionada'].strip() == "":
        tipo_entidad = "destinataria" if tipo_documento == "DERECHO_PETICION" else "accionada"
        advertencias.append(ValidationMessage(
            field="entidad_accionada",
            level=ValidationLevel.WARNING,
            message=f"La entidad {tipo_entidad} está vacía. Debes completarla antes de generar el documento."
        ))

    if not datos_caso.get('hechos') or datos_caso['hechos'].strip() == "":
        advertencias.append(ValidationMessage(
            field="hechos",
            level=ValidationLevel.WARNING,
            message="Los hechos del caso están vacíos. Debes narrar qué sucedió antes de generar el documento."
        ))

    if tipo_documento == "TUTELA":
        if not datos_caso.get('derechos_vulnerados') or datos_caso['derechos_vulnerados'].strip() == "":
            advertencias.append(ValidationMessage(
                field="derechos_vulnerados",
                level=ValidationLevel.WARNING,
                message="Los derechos vulnerados están vacíos. Debes indicar qué derechos fundamentales están siendo afectados antes de generar el documento."
            ))

    if not datos_caso.get('pretensiones') or datos_caso['pretensiones'].strip() == "":
        campo_nombre = "peticiones" if tipo_documento == "DERECHO_PETICION" else "pretensiones"
        advertencias.append(ValidationMessage(
            field="pretensiones",
            level=ValidationLevel.WARNING,
            message=f"Las {campo_nombre} están vacías. Debes indicar qué solicitas antes de generar el documento."
        ))

    # Validar campos importantes (formato de teléfono, email, etc.)
    advertencias_formato = validar_campos_importantes(datos_caso)
    advertencias.extend(advertencias_formato)

    return {
        "valido": len(advertencias) == 0,
        "errores": [],  # Nunca errores en validación preliminar
        "advertencias": [a.to_dict() for a in advertencias]
    }


def validar_caso_completo(caso, tipo_documento: str) -> Dict[str, any]:
    """
    🔒 VALIDACIÓN COMPLETA (BLOQUEANTE)

    Valida un caso completo antes de generar el documento.
    Genera ERRORES CRÍTICOS que bloquean la generación si faltan campos obligatorios
    o tienen formato inválido.

    Args:
        caso: Objeto Caso de SQLAlchemy
        tipo_documento: "tutela" o "derecho_peticion"

    Returns:
        Dict con estructura:
        {
            "valido": bool,
            "errores": [...],  # Errores críticos que bloquean generación
            "advertencias": [...]  # Advertencias que no bloquean
        }
    """
    # Convertir caso a dict
    datos_caso = {
        'nombre_solicitante': caso.nombre_solicitante,
        'identificacion_solicitante': caso.identificacion_solicitante,
        'direccion_solicitante': caso.direccion_solicitante,
        'telefono_solicitante': caso.telefono_solicitante,
        'email_solicitante': caso.email_solicitante,
        'entidad_accionada': caso.entidad_accionada,
        'hechos': caso.hechos,
        'derechos_vulnerados': caso.derechos_vulnerados,
        'pretensiones': caso.pretensiones,
    }

    # Validar campos críticos según el tipo de documento
    if tipo_documento == "TUTELA":
        errores = validar_campos_criticos_tutela(datos_caso)
    else:
        errores = validar_campos_criticos_derecho_peticion(datos_caso)

    # Validar campos importantes (advertencias)
    advertencias = validar_campos_importantes(datos_caso)

    return {
        "valido": len(errores) == 0,
        "errores": [e.to_dict() for e in errores],
        "advertencias": [a.to_dict() for a in advertencias]
    }


# =============================================================================
# DETECCIÓN INTELIGENTE DE DERECHOS FUNDAMENTALES
# Basado en feedback jurídico sobre subsidiariedad flexible
# =============================================================================

# Palabras clave para detección automática de derechos críticos urgentes
DERECHOS_CRITICOS_URGENTES = {
    "vida": [
        "muerte", "morir", "fallecer", "agonía", "peligro de muerte",
        "riesgo de muerte", "mortal", "terminal", "fallecimiento"
    ],
    "salud_urgente": [
        # Procedimientos médicos urgentes
        "cirugía", "operación", "intervención quirúrgica", "procedimiento médico",
        "urgente", "emergencia", "urgencias", "emergencias médicas",
        # Medicamentos y tratamientos
        "medicamento", "tratamiento", "terapia", "quimioterapia", "radioterapia",
        "diálisis", "hemodiálisis", "transfusión",
        # Síntomas graves
        "dolor insoportable", "dolor severo", "dolor agudo", "hemorragia",
        "sangrado", "crisis", "convulsiones", "desmayo",
        # Enfermedades graves
        "cáncer", "tumor", "infarto", "derrame", "accidente cerebrovascular",
        "insuficiencia", "falla", "paro", "shock",
        # Contexto hospitalario
        "hospital", "clínica", "uci", "unidad de cuidados intensivos",
        "hospitalización", "internado", "ingreso hospitalario",
        # Negación de servicios críticos
        "negaron", "negó", "niegan", "rechazaron", "no autorizan",
        "no aprueban", "sin autorización", "sin cita"
    ],
    "educacion_critica": [
        "no puede estudiar", "expulsión", "expulsado", "expulsaron",
        "matrícula cancelada", "sin cupo", "impedido de asistir",
        "no lo dejan entrar", "bloqueado", "suspendido del colegio",
        "no puede graduarse", "perdió el semestre", "cancelaron matrícula"
    ],
    "minimo_vital": [
        "sin dinero", "hambre", "no tengo para comer", "indigencia",
        "sin vivienda", "desalojo", "desalojar", "en la calle",
        "pensión", "subsidio vital", "mesada pensional",
        "sin ingresos", "sin sustento", "sin recursos"
    ],
    "dignidad_humana": [
        "maltrato", "tortura", "tratos crueles", "degradante",
        "humillación", "discriminación", "exclusión",
        "violencia", "abuso", "acoso"
    ]
}

# Palabras clave para casos administrativos (requieren derecho de petición previo)
DERECHOS_ADMINISTRATIVOS = {
    "peticion": [
        "solicitud", "certificado", "copia", "información",
        "respuesta", "contestación", "oficio", "radicado",
        "constancia", "certificación"
    ],
    "habeas_data": [
        "datos personales", "historial crediticio", "reportes",
        "centrales de riesgo", "información personal",
        "actualización de datos", "corrección de información"
    ],
    "administrativo": [
        "trámite", "procedimiento administrativo", "actuación administrativa",
        "consulta", "requerimiento", "notificación administrativa"
    ]
}


def detectar_palabras_clave(categoria: str, texto: str) -> bool:
    """
    Detecta si un texto contiene palabras clave de una categoría específica

    Args:
        categoria: Categoría a buscar (ej: "vida", "salud_urgente", "peticion")
        texto: Texto donde buscar (hechos, pretensiones, conversación)

    Returns:
        True si se encontró al menos una palabra clave de la categoría
    """
    if not texto:
        return False

    texto_lower = texto.lower()

    # Buscar en derechos críticos urgentes
    if categoria in DERECHOS_CRITICOS_URGENTES:
        palabras = DERECHOS_CRITICOS_URGENTES[categoria]
        return any(palabra in texto_lower for palabra in palabras)

    # Buscar en derechos administrativos
    if categoria in DERECHOS_ADMINISTRATIVOS:
        palabras = DERECHOS_ADMINISTRATIVOS[categoria]
        return any(palabra in texto_lower for palabra in palabras)

    return False


def clasificar_derecho_vulnerado(hechos: str, pretensiones: str, derechos_vulnerados: str = "") -> Dict[str, any]:
    """
    Clasifica el tipo de derecho fundamental presuntamente vulnerado
    según las reglas de subsidiariedad flexible de la Corte Constitucional

    Args:
        hechos: Narrativa de los hechos del caso
        pretensiones: Lo que solicita el usuario
        derechos_vulnerados: Derechos identificados (opcional)

    Returns:
        Dict con estructura:
        {
            "clasificacion": "CRITICO_URGENTE" | "ADMINISTRATIVO" | "MIXTO",
            "derechos_detectados": [...],
            "requiere_proteccion_inmediata": bool,
            "debe_preguntar_derecho_peticion_previo": bool,
            "justificacion": str
        }
    """
    texto_completo = f"{hechos} {pretensiones} {derechos_vulnerados}".lower()

    derechos_detectados = []
    es_critico = False

    # Detectar derechos críticos urgentes
    if detectar_palabras_clave("vida", texto_completo):
        derechos_detectados.append("Derecho a la vida (Art. 11 C.P.)")
        es_critico = True

    if detectar_palabras_clave("salud_urgente", texto_completo):
        derechos_detectados.append("Derecho a la salud (Art. 49 C.P.)")
        es_critico = True

    if detectar_palabras_clave("educacion_critica", texto_completo):
        derechos_detectados.append("Derecho a la educación (Art. 67 C.P.)")
        es_critico = True

    if detectar_palabras_clave("minimo_vital", texto_completo):
        derechos_detectados.append("Derecho al mínimo vital (conexo con Art. 1 C.P.)")
        es_critico = True

    if detectar_palabras_clave("dignidad_humana", texto_completo):
        derechos_detectados.append("Derecho a la dignidad humana (Art. 1 C.P.)")
        es_critico = True

    # Detectar derechos administrativos
    es_administrativo = False
    if detectar_palabras_clave("peticion", texto_completo):
        derechos_detectados.append("Derecho de petición (Art. 23 C.P.)")
        es_administrativo = True

    if detectar_palabras_clave("habeas_data", texto_completo):
        derechos_detectados.append("Derecho de habeas data (Art. 15 C.P.)")
        es_administrativo = True

    if detectar_palabras_clave("administrativo", texto_completo):
        es_administrativo = True

    # Clasificación final
    if es_critico and not es_administrativo:
        return {
            "clasificacion": "CRITICO_URGENTE",
            "derechos_detectados": derechos_detectados,
            "requiere_proteccion_inmediata": True,
            "debe_preguntar_derecho_peticion_previo": False,
            "justificacion": "Caso involucra derechos fundamentales que requieren protección inmediata. La espera del término legal del derecho de petición (15 días) podría hacer ineficaz la protección o agravar el daño. Procede tutela directamente."
        }

    elif es_administrativo and not es_critico:
        return {
            "clasificacion": "ADMINISTRATIVO",
            "derechos_detectados": derechos_detectados,
            "requiere_proteccion_inmediata": False,
            "debe_preguntar_derecho_peticion_previo": True,
            "justificacion": "Caso relacionado principalmente con solicitudes administrativas que pueden ser protegidas eficazmente mediante derecho de petición. Debe verificarse agotamiento de vía administrativa."
        }

    elif es_critico and es_administrativo:
        return {
            "clasificacion": "MIXTO",
            "derechos_detectados": derechos_detectados,
            "requiere_proteccion_inmediata": True,
            "debe_preguntar_derecho_peticion_previo": False,
            "justificacion": "Aunque involucra aspecto administrativo, la urgencia del derecho fundamental crítico prevalece. Aplica subsidiariedad flexible por conexidad con vida, salud o dignidad humana."
        }

    else:
        # No se detectaron palabras clave claras
        return {
            "clasificacion": "INDETERMINADO",
            "derechos_detectados": [],
            "requiere_proteccion_inmediata": False,
            "debe_preguntar_derecho_peticion_previo": True,
            "justificacion": "No se detectaron palabras clave claras. Se recomienda verificar si hubo derecho de petición previo y evaluar subsidiariedad caso por caso."
        }
