from openai import OpenAI
from ..core.config import settings

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
1. Genera un documento formal de tutela con encabezado apropiado
2. Incluye todas las secciones requeridas: I. HECHOS, II. DERECHOS VULNERADOS, III. PRETENSIONES, IV. FUNDAMENTOS DE DERECHO, V. PRUEBAS, VI. JURAMENTO, VII. NOTIFICACIONES
3. Usa lenguaje jurídico apropiado pero claro
4. Cita artículos relevantes de la Constitución Política de Colombia
5. Estructura el documento de manera profesional
6. Incluye fundamentos jurídicos sólidos
7. Asegúrate de que el documento sea completo y listo para radicar

IMPORTANTE SOBRE JURISPRUDENCIA:
- SOLO cita jurisprudencia si estás COMPLETAMENTE SEGURO de que existe
- Si no estás seguro de una sentencia específica, NO LA CITES
- Es mejor NO citar jurisprudencia que citar sentencias inventadas
- Si citas, usa SOLO sentencias muy conocidas y emblemáticas
- Indica "según jurisprudencia de la Corte Constitucional" sin número específico si no estás seguro
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
1. Genera un documento formal de derecho de petición con encabezado apropiado
2. Incluye: I. OBJETO, II. HECHOS, III. FUNDAMENTOS DE DERECHO, IV. PETICIONES, V. NOTIFICACIONES
3. Menciona el Artículo 23 de la Constitución y el Código de Procedimiento Administrativo (Ley 1437 de 2011)
4. Recuerda el término de 15 días hábiles para respuesta
5. Usa lenguaje formal y respetuoso
6. El documento debe estar listo para ser radicado

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
