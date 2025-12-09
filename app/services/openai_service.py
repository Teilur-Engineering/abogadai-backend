from openai import OpenAI
from ..core.config import settings
import json

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generar_tutela(datos_caso: dict) -> str:
    """
    Genera un documento de tutela completo usando GPT-4
    """

    prompt = f"""Eres un abogado experto en derecho constitucional colombiano especializado en acciones de tutela.

Genera un documento de ACCIÓN DE TUTELA completo, formal y profesional siguiendo la estructura legal colombiana.

DATOS DEL CASO:

SOLICITANTE:
- Nombre: {datos_caso.get('nombre_solicitante', '')}
- Identificación: {datos_caso.get('identificacion_solicitante', '')}
- Dirección: {datos_caso.get('direccion_solicitante', '')}
- Teléfono: {datos_caso.get('telefono_solicitante', '')}
- Email: {datos_caso.get('email_solicitante', '')}

ENTIDAD ACCIONADA:
- Nombre: {datos_caso.get('entidad_accionada', '')}
- Dirección: {datos_caso.get('direccion_entidad', '')}
- Representante Legal: {datos_caso.get('representante_legal', '')}

HECHOS:
{datos_caso.get('hechos', '')}

DERECHOS VULNERADOS:
{datos_caso.get('derechos_vulnerados', '')}

PRETENSIONES:
{datos_caso.get('pretensiones', '')}

FUNDAMENTOS DE DERECHO:
{datos_caso.get('fundamentos_derecho', '')}

INSTRUCCIONES:
1. Genera un documento formal de tutela con encabezado dirigido al Juez competente
2. ESTRUCTURA REQUERIDA (en este orden):
   - I. HECHOS: Narrativa clara y cronológica de los hechos que fundamentan la acción
   - II. DERECHOS VULNERADOS: Identificación explícita de los derechos fundamentales vulnerados con sus artículos constitucionales
   - III. PRETENSIONES: Lo que se solicita que ordene el juez de manera clara y específica
   - IV. FUNDAMENTOS DE DERECHO: Base jurídica constitucional (Art. 86 C.P. y Decreto 2591 de 1991)
   - V. PRUEBAS: Enumeración de las pruebas que se anexan o se solicitarán
   - VI. JURAMENTO: Manifestación bajo juramento de no haber presentado otra tutela por los mismos hechos
   - VII. NOTIFICACIONES: Dirección física y correo electrónico para notificaciones
3. Usa lenguaje jurídico apropiado pero comprensible
4. Cita artículos constitucionales relevantes (ej: Art. 11, 13, 15, 16, 20, 48, 49, etc. según corresponda)
5. Las PRETENSIONES deben solicitar órdenes específicas al juez (no son "peticiones" como en un derecho de petición)
6. El documento debe demostrar: procedencia, derechos fundamentales vulnerados, y subsidiariedad
7. Asegúrate de que el documento sea completo y listo para radicar

IMPORTANTE SOBRE JURISPRUDENCIA:
- SOLO cita jurisprudencia si estás COMPLETAMENTE SEGURO de que existe
- Si no estás seguro de una sentencia específica, NO LA CITES
- Es mejor NO citar jurisprudencia que citar sentencias inventadas
- Si citas, usa SOLO sentencias muy conocidas y emblemáticas de la Corte Constitucional
- Puedes mencionar "según jurisprudencia reiterada de la Corte Constitucional" sin número específico
- NUNCA inventes números de sentencias

El documento debe estar listo para ser presentado ante un juez de la República de Colombia."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un abogado constitucionalista experto en Colombia. Generas documentos legales formales, completos y profesionales."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=4000
        )

        documento_generado = response.choices[0].message.content
        return documento_generado

    except Exception as e:
        raise Exception(f"Error generando tutela con OpenAI: {str(e)}")


def generar_derecho_peticion(datos_caso: dict) -> str:
    """
    Genera un documento de derecho de petición usando GPT-4
    """

    prompt = f"""Eres un abogado experto en derecho administrativo colombiano especializado en derechos de petición.

Genera un documento de DERECHO DE PETICIÓN completo, formal y profesional siguiendo la estructura legal colombiana.

DATOS DEL CASO:

SOLICITANTE:
- Nombre: {datos_caso.get('nombre_solicitante', '')}
- Identificación: {datos_caso.get('identificacion_solicitante', '')}
- Dirección: {datos_caso.get('direccion_solicitante', '')}
- Teléfono: {datos_caso.get('telefono_solicitante', '')}
- Email: {datos_caso.get('email_solicitante', '')}

ENTIDAD DESTINATARIA:
- Nombre: {datos_caso.get('entidad_accionada', '')}
- Dirección: {datos_caso.get('direccion_entidad', '')}
- Representante Legal: {datos_caso.get('representante_legal', '')}

HECHOS:
{datos_caso.get('hechos', '')}

PETICIONES:
{datos_caso.get('pretensiones', '')}

FUNDAMENTOS DE DERECHO:
{datos_caso.get('fundamentos_derecho', '')}

INSTRUCCIONES:
1. Genera un documento formal de derecho de petición con encabezado apropiado dirigido a la entidad destinataria
2. ESTRUCTURA REQUERIDA (en este orden):
   - I. OBJETO: Presentar la naturaleza de la petición de manera clara y directa
   - II. HECHOS: Relatar los hechos cronológicamente y de forma clara
   - III. FUNDAMENTOS DE DERECHO: Mencionar el Art. 23 C.P. y la Ley 1437 de 2011 (Código de Procedimiento Administrativo y de lo Contencioso Administrativo)
   - IV. PETICIONES: Enumerar de forma clara, específica y accionable lo que se solicita a la entidad
   - V. NOTIFICACIONES: Indicar dirección física y correo electrónico para notificaciones
3. Menciona el término de 15 días hábiles que tiene la entidad para responder según el Art. 14 de la Ley 1437
4. Usa lenguaje formal, respetuoso y técnico apropiado
5. Las PETICIONES deben ser específicas y accionables (no son "pretensiones" como en una tutela)
6. NO cites jurisprudencia a menos que esté explícitamente en los fundamentos proporcionados
7. El documento debe estar completo y listo para radicar

El documento debe estar listo para ser presentado ante la entidad correspondiente en Colombia."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un abogado experto en derecho administrativo en Colombia. Generas documentos legales formales, completos y profesionales."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=3000
        )

        documento_generado = response.choices[0].message.content
        return documento_generado

    except Exception as e:
        raise Exception(f"Error generando derecho de petición con OpenAI: {str(e)}")


def extraer_datos_conversacion(mensajes: list) -> dict:
    """
    Extrae información estructurada de una conversación entre usuario y asistente legal

    Args:
        mensajes: Lista de diccionarios con formato:
                  [{"remitente": "usuario|asistente", "texto": "...", "timestamp": "..."}]

    Returns:
        dict con los campos extraídos: hechos, derechos_vulnerados, entidad_accionada,
        pretensiones, fundamentos_derecho
    """

    # Construir la conversación en formato legible
    conversacion_texto = ""
    for msg in mensajes:
        remitente = "ASISTENTE" if msg["remitente"] == "asistente" else "USUARIO"
        conversacion_texto += f"{remitente}: {msg['texto']}\n\n"

    prompt = f"""Eres un asistente legal experto en derecho constitucional y administrativo colombiano.

Analiza la siguiente conversación entre un usuario y un asistente legal que está recopilando información para crear un documento legal.

CONVERSACIÓN:
{conversacion_texto}

TAREA:
Extrae y estructura la siguiente información en formato JSON:

1. **tipo_documento**: Determina el tipo de documento legal apropiado según la conversación.
   - "tutela": Si se trata de vulneración de derechos fundamentales que requiere protección judicial inmediata
   - "derecho_peticion": Si se trata de solicitar información, documentos, o actuaciones administrativas a una entidad pública

   CRITERIOS:
   - TUTELA: Urgencia, derechos fundamentales vulnerados (salud, vida, educación, etc.), requiere orden judicial
   - DERECHO DE PETICIÓN: Solicitud de información, trámites administrativos, quejas, reclamos, petición de servicios

2. **hechos**: Narrativa cronológica y detallada de los hechos.
   Redacta en tercera persona, estilo legal, usando el nombre del solicitante si está disponible.
   Si no hay información suficiente, deja este campo vacío.

3. **derechos_vulnerados**: (Solo para tutelas) Lista de derechos fundamentales vulnerados con sus artículos constitucionales.
   Formato: "Derecho a la Salud (Art. 49 C.P.), Derecho a la Vida (Art. 11 C.P.)"
   Si es derecho de petición o no hay información suficiente, deja este campo vacío.

4. **entidad_accionada**: Nombre completo de la entidad, empresa o institución.
   Debe ser el nombre oficial completo (ejemplo: "EPS Sanitas S.A.", "Ministerio de Salud").
   Si no hay información suficiente, deja este campo vacío.

5. **pretensiones**: Lo que solicita el usuario.
   - Para tutelas: Qué solicita que ordene el juez
   - Para derechos de petición: Qué información o actuación solicita
   Si no hay información suficiente, deja este campo vacío.

6. **fundamentos_derecho**: Leyes, decretos o jurisprudencia aplicable mencionada en la conversación.
   Solo incluye lo que fue EXPLÍCITAMENTE mencionado. Si nada fue mencionado, deja este campo vacío.

INSTRUCCIONES IMPORTANTES:
- Si algún campo no tiene información suficiente en la conversación, devuélvelo como cadena vacía ""
- Mantén lenguaje legal apropiado para Colombia
- Redacta los hechos de forma coherente y cronológica
- Sé preciso con los artículos constitucionales (usa "Art. XX C.P.")
- NO inventes información que no esté en la conversación
- NO cites jurisprudencia a menos que haya sido mencionada explícitamente
- IMPORTANTE: Determina correctamente el tipo_documento basándote en el contexto de la conversación

FORMATO DE SALIDA:
Devuelve ÚNICAMENTE un objeto JSON válido con esta estructura exacta, sin markdown ni texto adicional:
{{
    "tipo_documento": "tutela" o "derecho_peticion",
    "hechos": "texto aquí o cadena vacía",
    "derechos_vulnerados": "texto aquí o cadena vacía",
    "entidad_accionada": "texto aquí o cadena vacía",
    "pretensiones": "texto aquí o cadena vacía",
    "fundamentos_derecho": "texto aquí o cadena vacía"
}}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente legal experto en derecho constitucional colombiano. Extraes información de conversaciones y la estructuras en formato JSON válido."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,  # Baja temperatura para mayor precisión
            max_tokens=2000,
            response_format={"type": "json_object"}  # Forzar respuesta JSON
        )

        resultado_texto = response.choices[0].message.content

        # Parsear el JSON
        datos_extraidos = json.loads(resultado_texto)

        # Validar que tenga las claves esperadas
        campos_esperados = ["tipo_documento", "hechos", "derechos_vulnerados", "entidad_accionada", "pretensiones", "fundamentos_derecho"]
        for campo in campos_esperados:
            if campo not in datos_extraidos:
                if campo == "tipo_documento":
                    datos_extraidos[campo] = "tutela"  # Valor por defecto
                else:
                    datos_extraidos[campo] = ""

        # Validar que tipo_documento tenga un valor válido
        if datos_extraidos["tipo_documento"] not in ["tutela", "derecho_peticion"]:
            datos_extraidos["tipo_documento"] = "tutela"  # Fallback a tutela si el valor no es válido

        return datos_extraidos

    except json.JSONDecodeError as e:
        raise Exception(f"Error al parsear respuesta JSON de OpenAI: {str(e)}")
    except Exception as e:
        raise Exception(f"Error extrayendo datos de conversación con OpenAI: {str(e)}")
