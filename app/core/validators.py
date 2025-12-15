"""
Validadores para datos colombianos
"""
import re
from typing import Optional


def validar_cedula_colombiana(cedula: str) -> bool:
    """
    Valida el formato de una cédula de ciudadanía colombiana.

    Formato aceptado:
    - Solo números
    - Entre 6 y 10 dígitos
    - Puede tener puntos como separadores (ej: 1.234.567.890)

    Args:
        cedula: Número de cédula a validar

    Returns:
        bool: True si es válida, False en caso contrario
    """
    if not cedula:
        return False

    # Remover puntos y espacios
    cedula_limpia = cedula.replace('.', '').replace(' ', '').replace(',', '')

    # Validar que solo contenga números
    if not cedula_limpia.isdigit():
        return False

    # Validar longitud (6 a 10 dígitos)
    if len(cedula_limpia) < 6 or len(cedula_limpia) > 10:
        return False

    return True


def formatear_cedula(cedula: str) -> str:
    """
    Formatea una cédula con separadores de miles.

    Args:
        cedula: Cédula sin formato

    Returns:
        str: Cédula formateada (ej: 1.234.567.890)
    """
    if not cedula:
        return ""

    # Limpiar la cédula
    cedula_limpia = cedula.replace('.', '').replace(' ', '').replace(',', '')

    # Formatear con puntos
    cedula_formateada = "{:,}".format(int(cedula_limpia)).replace(',', '.')

    return cedula_formateada


def validar_nit_colombiano(nit: str) -> bool:
    """
    Valida el formato de un NIT colombiano.

    Formato: XXXXXXXXX-X (9 dígitos, guión, 1 dígito verificador)

    Args:
        nit: NIT a validar

    Returns:
        bool: True si es válido, False en caso contrario
    """
    if not nit:
        return False

    # Remover espacios y puntos
    nit_limpio = nit.replace(' ', '').replace('.', '')

    # Verificar formato: debe tener un guión
    if '-' not in nit_limpio:
        # Intentar validar sin guión (solo números)
        if nit_limpio.isdigit() and 8 <= len(nit_limpio) <= 10:
            return True
        return False

    partes = nit_limpio.split('-')

    # Debe tener exactamente 2 partes
    if len(partes) != 2:
        return False

    numero, digito_verificacion = partes

    # Validar que ambas partes sean numéricas
    if not (numero.isdigit() and digito_verificacion.isdigit()):
        return False

    # El número debe tener entre 8 y 10 dígitos
    if len(numero) < 8 or len(numero) > 10:
        return False

    # El dígito de verificación debe ser de 1 dígito
    if len(digito_verificacion) != 1:
        return False

    return True


def calcular_digito_verificacion_nit(nit: str) -> Optional[int]:
    """
    Calcula el dígito de verificación de un NIT colombiano.

    Args:
        nit: Número de NIT sin dígito de verificación

    Returns:
        int: Dígito de verificación (0-9)
    """
    if not nit or not nit.isdigit():
        return None

    # Secuencia de números primos para el cálculo
    primos = [3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71]

    # Invertir el NIT
    nit_invertido = nit[::-1]

    suma = 0
    for i, digito in enumerate(nit_invertido):
        if i < len(primos):
            suma += int(digito) * primos[i]

    residuo = suma % 11

    if residuo == 0 or residuo == 1:
        return residuo
    else:
        return 11 - residuo


def formatear_nit(nit: str) -> str:
    """
    Formatea un NIT con separadores y dígito de verificación.

    Args:
        nit: NIT sin formato

    Returns:
        str: NIT formateado (ej: 900.123.456-7)
    """
    if not nit:
        return ""

    # Limpiar el NIT
    nit_limpio = nit.replace('.', '').replace(' ', '').replace('-', '')

    if not nit_limpio.isdigit():
        return nit

    # Separar número y dígito de verificación si existe
    if len(nit_limpio) >= 9:
        numero = nit_limpio[:-1]
        dv = nit_limpio[-1]
    else:
        numero = nit_limpio
        dv = str(calcular_digito_verificacion_nit(numero) or 0)

    # Formatear con puntos
    numero_formateado = "{:,}".format(int(numero)).replace(',', '.')

    return f"{numero_formateado}-{dv}"


def validar_telefono_colombiano(telefono: str) -> bool:
    """
    Valida el formato de un teléfono colombiano.

    Formatos aceptados:
    - Celular: 10 dígitos (ej: 3001234567)
    - Fijo: 7 dígitos con indicativo (ej: 6012345678)
    - Con prefijo +57

    Args:
        telefono: Número de teléfono

    Returns:
        bool: True si es válido
    """
    if not telefono:
        return False

    # Limpiar el teléfono
    tel_limpio = telefono.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')

    # Remover +57 si existe
    if tel_limpio.startswith('+57'):
        tel_limpio = tel_limpio[3:]
    elif tel_limpio.startswith('57'):
        tel_limpio = tel_limpio[2:]

    # Validar que solo contenga números
    if not tel_limpio.isdigit():
        return False

    # Validar longitud (7 o 10 dígitos)
    if len(tel_limpio) not in [7, 10]:
        return False

    # Si es celular, debe empezar con 3
    if len(tel_limpio) == 10 and not tel_limpio.startswith('3'):
        return False

    return True


def formatear_telefono(telefono: str) -> str:
    """
    Formatea un teléfono colombiano para display.

    Args:
        telefono: Número de teléfono

    Returns:
        str: Teléfono formateado (ej: "300 123 4567" o "601 234 5678")
    """
    if not telefono:
        return telefono

    # Limpiar el teléfono
    tel_limpio = telefono.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')

    # Remover +57 si existe
    if tel_limpio.startswith('+57'):
        tel_limpio = tel_limpio[3:]
    elif tel_limpio.startswith('57'):
        tel_limpio = tel_limpio[2:]

    # Formatear según longitud
    if len(tel_limpio) == 10:
        # Celular: 300 123 4567
        return f"{tel_limpio[:3]} {tel_limpio[3:6]} {tel_limpio[6:]}"
    elif len(tel_limpio) == 7:
        # Fijo: 234 5678
        return f"{tel_limpio[:3]} {tel_limpio[3:]}"
    else:
        return telefono


def validar_email(email: str) -> bool:
    """
    Valida el formato de un email.

    Args:
        email: Email a validar

    Returns:
        bool: True si es válido
    """
    if not email:
        return False

    # Expresión regular para validar email
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    return re.match(patron, email) is not None
