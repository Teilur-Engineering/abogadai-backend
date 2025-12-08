"""
Datos de referencia para el sistema legal colombiano
"""

# Derechos Fundamentales según la Constitución Política de Colombia 1991
DERECHOS_FUNDAMENTALES = [
    {
        "articulo": "11",
        "derecho": "Derecho a la Vida",
        "descripcion": "El derecho a la vida es inviolable. No habrá pena de muerte."
    },
    {
        "articulo": "12",
        "derecho": "Integridad Personal",
        "descripcion": "Nadie será sometido a desaparición forzada, a torturas ni a tratos o penas crueles, inhumanos o degradantes."
    },
    {
        "articulo": "13",
        "derecho": "Igualdad",
        "descripcion": "Todas las personas nacen libres e iguales ante la ley, recibirán la misma protección y trato de las autoridades."
    },
    {
        "articulo": "14",
        "derecho": "Personalidad Jurídica",
        "descripcion": "Toda persona tiene derecho al reconocimiento de su personalidad jurídica."
    },
    {
        "articulo": "15",
        "derecho": "Intimidad",
        "descripcion": "Todas las personas tienen derecho a su intimidad personal y familiar y a su buen nombre."
    },
    {
        "articulo": "16",
        "derecho": "Libre Desarrollo de la Personalidad",
        "descripcion": "Todas las personas tienen derecho al libre desarrollo de su personalidad sin más limitaciones que las que imponen los derechos de los demás y el orden jurídico."
    },
    {
        "articulo": "17",
        "derecho": "Prohibición de Esclavitud",
        "descripcion": "Se prohíben la esclavitud, la servidumbre y la trata de seres humanos en todas sus formas."
    },
    {
        "articulo": "18",
        "derecho": "Libertad de Conciencia",
        "descripcion": "Se garantiza la libertad de conciencia. Nadie será molestado por razón de sus convicciones o creencias."
    },
    {
        "articulo": "19",
        "derecho": "Libertad de Cultos",
        "descripcion": "Se garantiza la libertad de cultos. Toda persona tiene derecho a profesar libremente su religión."
    },
    {
        "articulo": "20",
        "derecho": "Libertad de Expresión",
        "descripcion": "Se garantiza a toda persona la libertad de expresar y difundir su pensamiento y opiniones."
    },
    {
        "articulo": "21",
        "derecho": "Honra",
        "descripcion": "Se garantiza el derecho a la honra. La ley señalará la forma de su protección."
    },
    {
        "articulo": "23",
        "derecho": "Derecho de Petición",
        "descripcion": "Toda persona tiene derecho a presentar peticiones respetuosas a las autoridades."
    },
    {
        "articulo": "24",
        "derecho": "Libertad de Circulación",
        "descripcion": "Todo colombiano, con las limitaciones que establezca la ley, tiene derecho a circular libremente por el territorio nacional."
    },
    {
        "articulo": "25",
        "derecho": "Derecho al Trabajo",
        "descripcion": "El trabajo es un derecho y una obligación social y goza, en todas sus modalidades, de la especial protección del Estado."
    },
    {
        "articulo": "26",
        "derecho": "Libertad de Escoger Profesión u Oficio",
        "descripcion": "Toda persona es libre de escoger profesión u oficio."
    },
    {
        "articulo": "27",
        "derecho": "Libertad de Enseñanza",
        "descripcion": "El Estado garantiza las libertades de enseñanza, aprendizaje, investigación y cátedra."
    },
    {
        "articulo": "28",
        "derecho": "Libertad Personal",
        "descripcion": "Toda persona es libre. Nadie puede ser molestado en su persona o familia."
    },
    {
        "articulo": "29",
        "derecho": "Debido Proceso",
        "descripcion": "El debido proceso se aplicará a toda clase de actuaciones judiciales y administrativas."
    },
    {
        "articulo": "30",
        "derecho": "Habeas Corpus",
        "descripcion": "Quien estuviere privado de su libertad, y creyere estarlo ilegalmente, tiene derecho a invocar ante cualquier autoridad judicial el Habeas Corpus."
    },
    {
        "articulo": "31",
        "derecho": "Apelación o Consulta",
        "descripcion": "Toda sentencia judicial podrá ser apelada o consultada, salvo las excepciones que consagre la ley."
    },
    {
        "articulo": "33",
        "derecho": "No Autoincriminación",
        "descripcion": "Nadie podrá ser obligado a declarar contra sí mismo o contra su cónyuge, compañero permanente o parientes."
    },
    {
        "articulo": "34",
        "derecho": "Prohibición de Penas",
        "descripcion": "Se prohíben las penas de destierro, prisión perpetua y confiscación."
    },
    {
        "articulo": "37",
        "derecho": "Reunión y Manifestación",
        "descripcion": "Toda parte del pueblo puede reunirse y manifestarse pública y pacíficamente."
    },
    {
        "articulo": "38",
        "derecho": "Libertad de Asociación",
        "descripcion": "Se garantiza el derecho de libre asociación para el desarrollo de las distintas actividades que las personas realizan en sociedad."
    },
    {
        "articulo": "40",
        "derecho": "Participación Política",
        "descripcion": "Todo ciudadano tiene derecho a participar en la conformación, ejercicio y control del poder político."
    },
    {
        "articulo": "41",
        "derecho": "Acceso a Documentos Públicos",
        "descripcion": "En todas las instituciones de educación, oficiales o privadas, serán obligatorios el estudio de la Constitución."
    },
    # Derechos Fundamentales por Conexidad (importantes para tutelas)
    {
        "articulo": "44",
        "derecho": "Derechos de los Niños",
        "descripcion": "Son derechos fundamentales de los niños: la vida, la integridad física, la salud, la seguridad social, la educación y la cultura, entre otros.",
        "nota": "Fundamental - Menores"
    },
    {
        "articulo": "48",
        "derecho": "Seguridad Social",
        "descripcion": "Se garantiza a todos los habitantes el derecho irrenunciable a la Seguridad Social.",
        "nota": "Por conexidad"
    },
    {
        "articulo": "49",
        "derecho": "Salud",
        "descripcion": "La atención de la salud y el saneamiento ambiental son servicios públicos a cargo del Estado.",
        "nota": "Por conexidad"
    },
    {
        "articulo": "51",
        "derecho": "Vivienda Digna",
        "descripcion": "Todos los colombianos tienen derecho a vivienda digna.",
        "nota": "Por conexidad"
    },
    {
        "articulo": "53",
        "derecho": "Principios Mínimos del Trabajo",
        "descripcion": "El Congreso expedirá el estatuto del trabajo conforme a los principios mínimos fundamentales.",
        "nota": "Por conexidad"
    },
    {
        "articulo": "67",
        "derecho": "Educación",
        "descripcion": "La educación es un derecho de la persona y un servicio público que tiene una función social.",
        "nota": "Fundamental - Menores / Por conexidad - Adultos"
    },
]


# Entidades Públicas Comunes en Colombia
ENTIDADES_PUBLICAS = {
    "EPS": [
        "Sanitas EPS",
        "Compensar EPS",
        "Sura EPS",
        "Nueva EPS",
        "Famisanar EPS",
        "Salud Total EPS",
        "Coomeva EPS",
        "Aliansalud EPS",
        "Medimás EPS",
        "Capital Salud EPS",
        "SOS EPS",
        "Coosalud EPS",
        "Mutual Ser EPS",
        "Asmet Salud",
    ],
    "MINISTERIOS": [
        "Ministerio de Salud y Protección Social",
        "Ministerio de Educación Nacional",
        "Ministerio del Trabajo",
        "Ministerio de Justicia y del Derecho",
        "Ministerio de Hacienda y Crédito Público",
        "Ministerio del Interior",
        "Ministerio de Defensa Nacional",
        "Ministerio de Relaciones Exteriores",
        "Ministerio de Agricultura y Desarrollo Rural",
        "Ministerio de Transporte",
        "Ministerio de Vivienda, Ciudad y Territorio",
        "Ministerio de Ambiente y Desarrollo Sostenible",
        "Ministerio de Tecnologías de la Información y las Comunicaciones",
        "Ministerio de Comercio, Industria y Turismo",
        "Ministerio de Minas y Energía",
        "Ministerio de Cultura",
        "Ministerio del Deporte",
        "Ministerio de Ciencia, Tecnología e Innovación",
    ],
    "SUPERINTENDENCIAS": [
        "Superintendencia Nacional de Salud",
        "Superintendencia de Industria y Comercio",
        "Superintendencia Financiera de Colombia",
        "Superintendencia de Sociedades",
        "Superintendencia de Servicios Públicos Domiciliarios",
        "Superintendencia de Notariado y Registro",
        "Superintendencia de Vigilancia y Seguridad Privada",
        "Superintendencia de Puertos y Transporte",
        "Superintendencia de Economía Solidaria",
    ],
    "ENTIDADES_AUTONOMAS": [
        "ICBF - Instituto Colombiano de Bienestar Familiar",
        "SENA - Servicio Nacional de Aprendizaje",
        "DIAN - Dirección de Impuestos y Aduanas Nacionales",
        "Registraduría Nacional del Estado Civil",
        "Contraloría General de la República",
        "Procuraduría General de la Nación",
        "Defensoría del Pueblo",
        "Fiscalía General de la Nación",
        "Consejo Superior de la Judicatura",
    ],
    "FUERZAS_PUBLICAS": [
        "Policía Nacional de Colombia",
        "Ejército Nacional de Colombia",
        "Armada Nacional de Colombia",
        "Fuerza Aérea Colombiana",
        "Ministerio de Defensa Nacional",
    ],
    "EDUCACION": [
        "ICETEX - Instituto Colombiano de Crédito Educativo",
        "Universidad Nacional de Colombia",
        "Secretaría de Educación Distrital",
        "Secretaría de Educación Departamental",
        "Ministerio de Educación Nacional",
    ],
    "GOBIERNOS_TERRITORIALES": [
        "Alcaldía de Bogotá D.C.",
        "Alcaldía de Medellín",
        "Alcaldía de Cali",
        "Alcaldía de Barranquilla",
        "Alcaldía de Cartagena",
        "Gobernación de Cundinamarca",
        "Gobernación de Antioquia",
        "Gobernación del Valle del Cauca",
        "Gobernación del Atlántico",
        "Gobernación de Bolívar",
    ],
    "PENSIONES": [
        "Colpensiones",
        "Porvenir",
        "Protección",
        "Colfondos",
        "Old Mutual",
    ],
}


# Departamentos de Colombia
DEPARTAMENTOS = [
    "Amazonas", "Antioquia", "Arauca", "Atlántico", "Bogotá D.C.", "Bolívar",
    "Boyacá", "Caldas", "Caquetá", "Casanare", "Cauca", "Cesar", "Chocó",
    "Córdoba", "Cundinamarca", "Guainía", "Guaviare", "Huila", "La Guajira",
    "Magdalena", "Meta", "Nariño", "Norte de Santander", "Putumayo", "Quindío",
    "Risaralda", "San Andrés y Providencia", "Santander", "Sucre", "Tolima",
    "Valle del Cauca", "Vaupés", "Vichada"
]


# Ciudades principales de Colombia
CIUDADES_PRINCIPALES = [
    "Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena", "Cúcuta",
    "Bucaramanga", "Pereira", "Santa Marta", "Ibagué", "Pasto", "Manizales",
    "Neiva", "Villavicencio", "Armenia", "Valledupar", "Montería", "Sincelejo",
    "Popayán", "Tunja", "Florencia", "Riohacha", "Quibdó", "Yopal",
    "Mocoa", "San Andrés"
]


def obtener_derechos_por_categoria(categoria: str = None):
    """
    Obtiene los derechos fundamentales, opcionalmente filtrados por categoría.

    Args:
        categoria: 'fundamentales' o 'conexidad'

    Returns:
        Lista de derechos
    """
    if categoria == "fundamentales":
        return [d for d in DERECHOS_FUNDAMENTALES if "nota" not in d]
    elif categoria == "conexidad":
        return [d for d in DERECHOS_FUNDAMENTALES if "nota" in d]
    else:
        return DERECHOS_FUNDAMENTALES


def obtener_entidades_por_tipo(tipo: str = None):
    """
    Obtiene entidades públicas por tipo.

    Args:
        tipo: Tipo de entidad (EPS, MINISTERIOS, etc.)

    Returns:
        Lista de entidades
    """
    if tipo and tipo.upper() in ENTIDADES_PUBLICAS:
        return ENTIDADES_PUBLICAS[tipo.upper()]

    # Retornar todas las entidades como lista plana
    todas = []
    for categoria, entidades in ENTIDADES_PUBLICAS.items():
        todas.extend(entidades)
    return todas


def buscar_entidad(termino: str):
    """
    Busca una entidad por término de búsqueda.

    Args:
        termino: Término a buscar

    Returns:
        Lista de entidades que coinciden
    """
    termino_lower = termino.lower()
    resultados = []

    for categoria, entidades in ENTIDADES_PUBLICAS.items():
        for entidad in entidades:
            if termino_lower in entidad.lower():
                resultados.append({
                    "entidad": entidad,
                    "categoria": categoria
                })

    return resultados
