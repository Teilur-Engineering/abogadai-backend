# 📚 DOCUMENTACIÓN COMPLETA - SISTEMA ABOGADAI

## 🌟 Visión General del Sistema

**AbogadAI** es una plataforma completa de asistencia legal para Colombia que permite a usuarios crear **Tutelas** y **Derechos de Petición** mediante:

1. **Conversación con Avatar AI** (voz en tiempo real)
2. **Procesamiento inteligente con IA** (extracción automática de datos)
3. **Generación de documentos legales** (listos para radicar)
4. **Análisis de calidad y viabilidad** (validación con IA)

---

## 🏗️ ARQUITECTURA DEL SISTEMA

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + Vite)                       │
│  - Autenticación de usuarios                                     │
│  - Interfaz de conversación con avatar                           │
│  - Editor de casos (tutelas/derechos de petición)               │
│  - Descarga de documentos (PDF/DOCX)                            │
│  - Panel de análisis de calidad                                 │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ HTTP/WebSocket
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│               BACKEND (FastAPI + PostgreSQL)                     │
│  - API REST completa                                            │
│  - Autenticación JWT                                            │
│  - Gestión de casos y usuarios                                  │
│  - Integración con OpenAI (GPT-4o)                              │
│  - Generación de documentos                                     │
│  - Análisis de calidad y fortaleza                              │
│  - Integración con LiveKit                                      │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ WebSocket + Webhooks
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│          AGENTS (LiveKit + Simli + OpenAI Realtime)             │
│  - Avatar conversacional en tiempo real                          │
│  - Transcripción automática (STT)                               │
│  - Síntesis de voz (TTS)                                        │
│  - Guardado automático de conversaciones                        │
│  - Especialización legal colombiana                             │
└─────────────────────────────────────────────────────────────────┘
```

---

# 🖥️ BACKEND (FastAPI + PostgreSQL)

## 📁 Estructura del Proyecto

```
abogadai-backend/
├── app/
│   ├── core/                    # Configuración central
│   │   ├── config.py           # Variables de entorno
│   │   ├── database.py         # Conexión PostgreSQL
│   │   ├── security.py         # JWT, hashing
│   │   ├── validators.py       # Validadores colombianos
│   │   └── datos_colombia.py   # Ciudades/departamentos
│   │
│   ├── models/                  # Modelos SQLAlchemy
│   │   ├── user.py             # Usuario
│   │   ├── caso.py             # Caso legal
│   │   └── mensaje.py          # Mensajes de conversación
│   │
│   ├── schemas/                 # Schemas Pydantic
│   │   ├── user.py             # Validación de usuarios
│   │   ├── caso.py             # Validación de casos
│   │   └── mensaje.py          # Validación de mensajes
│   │
│   ├── routes/                  # Endpoints API
│   │   ├── auth.py             # Autenticación
│   │   ├── casos.py            # CRUD de casos
│   │   ├── livekit.py          # Integración LiveKit
│   │   ├── sesiones.py         # Sesiones de avatar
│   │   ├── mensajes.py         # Mensajes
│   │   └── referencias.py      # Datos de referencia
│   │
│   ├── services/                # Lógica de negocio
│   │   ├── openai_service.py   # Generación con GPT-4o
│   │   ├── ai_analysis_service.py  # Análisis de calidad
│   │   └── document_service.py # Generación PDF/DOCX
│   │
│   └── main.py                  # Aplicación principal
│
├── .env                         # Variables de entorno
├── requirements.txt             # Dependencias
└── README.md
```

---

## 🔐 MODELOS DE BASE DE DATOS

### 1️⃣ **User** (Usuario)

```python
- id: int (PK)
- email: str (único, índice)
- hashed_password: str
- nombre_completo: str
- is_active: bool (default: True)
- created_at: datetime
- updated_at: datetime

# Relaciones
- casos: List[Caso]
```

**Propósito:** Gestión de usuarios con autenticación JWT.

---

### 2️⃣ **Caso** (Caso Legal)

```python
- id: int (PK)
- user_id: int (FK → User)

# Tipo y estado
- tipo_documento: Enum("tutela", "derecho_peticion")
- estado: Enum("borrador", "generado", "finalizado")

# Datos del solicitante
- nombre_solicitante: str
- identificacion_solicitante: str
- direccion_solicitante: str
- telefono_solicitante: str
- email_solicitante: str

# Datos de la entidad
- entidad_accionada: str
- direccion_entidad: str
- representante_legal: str

# Contenido del caso
- hechos: text
- derechos_vulnerados: text (solo tutelas)
- pretensiones: text
- fundamentos_derecho: text

# Documento generado
- documento_generado: text

# Análisis de IA (JSON)
- analisis_fortaleza: JSON
- analisis_calidad: JSON
- analisis_jurisprudencia: JSON
- sugerencias_mejora: JSON

# Sesión LiveKit
- session_id: str (UUID)
- room_name: str
- fecha_inicio_sesion: datetime
- fecha_fin_sesion: datetime

# Metadata
- created_at: datetime
- updated_at: datetime

# Relaciones
- user: User
- mensajes: List[Mensaje]
```

**Propósito:** Representa un caso legal completo (tutela o derecho de petición).

---

### 3️⃣ **Mensaje** (Conversación)

```python
- id: int (PK)
- caso_id: int (FK → Caso)
- remitente: Enum("usuario", "asistente")
- texto: text
- timestamp: datetime

# Relaciones
- caso: Caso
```

**Propósito:** Guarda la transcripción completa de la conversación con el avatar.

---

## 🛣️ ENDPOINTS DEL API

### 🔐 **Autenticación** (`/auth`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/auth/signup` | Registro de usuario | ❌ |
| POST | `/auth/login` | Login (retorna JWT) | ❌ |
| GET | `/auth/me` | Usuario actual | ✅ |

**Ejemplo de registro:**
```bash
POST /auth/signup
{
  "email": "usuario@example.com",
  "password": "Password123!",
  "nombre_completo": "Juan Pérez"
}
```

---

### 📋 **Casos** (`/casos`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/casos/` | Crear caso | ✅ |
| GET | `/casos/` | Listar casos del usuario | ✅ |
| GET | `/casos/{id}` | Obtener caso específico | ✅ |
| PUT | `/casos/{id}` | Actualizar caso | ✅ |
| DELETE | `/casos/{id}` | Eliminar caso | ✅ |
| POST | `/casos/{id}/procesar-transcripcion` | **Procesar IA** | ✅ |
| POST | `/casos/{id}/analizar-fortaleza` | **Analizar viabilidad** | ✅ |
| POST | `/casos/{id}/generar` | **Generar documento** | ✅ |
| GET | `/casos/{id}/descargar/pdf` | Descargar PDF | ✅ |
| GET | `/casos/{id}/descargar/docx` | Descargar DOCX | ✅ |

---

### 🎯 **Sesiones de Avatar** (`/sesiones`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/sesiones/iniciar` | Inicia sesión + crea caso | ✅ |
| PUT | `/sesiones/{id}/finalizar` | Finaliza sesión | ✅ |

**Flujo:**
1. Frontend llama `/sesiones/iniciar` → Backend crea caso + genera token LiveKit
2. Frontend conecta a LiveKit con el token
3. Usuario conversa con avatar
4. Al terminar, frontend llama `/sesiones/{id}/finalizar`

---

### 💬 **Mensajes** (`/mensajes`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/mensajes/` | Guardar mensaje | ❌ |
| GET | `/mensajes/caso/{id}` | Obtener mensajes | ✅ |

**Nota:** El endpoint POST es llamado por el agente (webhook), no requiere auth de usuario.

---

### 🗺️ **Referencias** (`/referencias`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/referencias/departamentos` | Lista departamentos | ❌ |
| GET | `/referencias/ciudades/{depto}` | Ciudades por departamento | ❌ |

---

## 🤖 SERVICIOS DE IA

### 1️⃣ **OpenAI Service** (`openai_service.py`)

#### **Funciones principales:**

**a) `extraer_datos_conversacion(mensajes: list) -> dict`**

Extrae información estructurada de la conversación con el avatar.

**Input:**
```python
[
  {"remitente": "usuario", "texto": "Mi EPS negó una cirugía", "timestamp": "..."},
  {"remitente": "asistente", "texto": "Entiendo, ¿qué EPS es?", "timestamp": "..."},
  {"remitente": "usuario", "texto": "Sanitas", "timestamp": "..."}
]
```

**Output:**
```python
{
  "tipo_documento": "tutela",  # o "derecho_peticion"
  "hechos": "El señor Juan Pérez...",
  "derechos_vulnerados": "Derecho a la Salud (Art. 49 C.P.)",
  "entidad_accionada": "EPS Sanitas S.A.",
  "pretensiones": "Ordenar a Sanitas autorizar...",
  "fundamentos_derecho": "Artículo 86 C.P., Decreto 2591..."
}
```

**Tecnología:** GPT-4o con JSON mode, temperatura 0.3 (alta precisión)

---

**b) `generar_tutela(datos_caso: dict) -> str`**

Genera documento completo de acción de tutela.

**Estructura generada:**
- Encabezado (dirigido al juez)
- I. HECHOS
- II. DERECHOS VULNERADOS
- III. PRETENSIONES
- IV. FUNDAMENTOS DE DERECHO
- V. PRUEBAS
- VI. JURAMENTO
- VII. NOTIFICACIONES

**Tecnología:** GPT-4o, temperatura 0.7, max 4000 tokens

---

**c) `generar_derecho_peticion(datos_caso: dict) -> str`**

Genera documento completo de derecho de petición.

**Estructura generada:**
- Encabezado (dirigido a la entidad)
- I. OBJETO
- II. HECHOS
- III. FUNDAMENTOS DE DERECHO (Art. 23 C.P., Ley 1437)
- IV. PETICIONES
- V. NOTIFICACIONES

**Tecnología:** GPT-4o, temperatura 0.7, max 3000 tokens

---

### 2️⃣ **AI Analysis Service** (`ai_analysis_service.py`)

#### **Funciones principales:**

**a) `analizar_fortaleza_caso(datos_caso: dict, tipo_documento: str) -> dict`**

Evalúa la viabilidad del caso ANTES de generar el documento.

**Para Tutelas evalúa:**
- Procedencia de la tutela (0-20 pts)
- Derechos fundamentales (0-20 pts)
- Subsidiaridad (0-20 pts)
- Legitimación (0-15 pts)
- Claridad de hechos (0-15 pts)
- Inmediatez (0-10 pts)

**Para Derechos de Petición evalúa:**
- Claridad de la solicitud (0-20 pts)
- Legitimación del peticionario (0-20 pts)
- Competencia de la entidad (0-20 pts)
- Claridad de hechos (0-15 pts)
- Especificidad (0-15 pts)
- Fundamentos (0-10 pts)

**Output:**
```python
{
  "fortaleza_total": 85,
  "probabilidad_exito": "alta",
  "procedencia_tutela": {"puntos": 18, "comentario": "..."},
  "puntos_fuertes": ["Lista de fortalezas"],
  "puntos_debiles": ["Lista de debilidades"],
  "recomendaciones": ["Sugerencias"],
  "debe_proceder": true
}
```

---

**b) `analizar_calidad_documento(documento: str, datos_caso: dict, tipo_documento: str) -> dict`**

Evalúa la calidad del documento generado.

**Para Tutelas evalúa:**
- Estructura completa (0-20 pts)
- Coherencia (0-20 pts)
- Datos completos (0-20 pts)
- Lenguaje jurídico (0-20 pts)
- Fundamentos (0-10 pts)
- Completitud (0-10 pts)

**Para Derechos de Petición evalúa:**
- Estructura completa (0-20 pts)
- Coherencia (0-20 pts)
- Datos completos (0-15 pts)
- Lenguaje formal (0-15 pts)
- Fundamentos legales (0-10 pts)
- Peticiones claras (0-10 pts)
- Completitud (0-10 pts)

---

**c) `validar_jurisprudencia(documento: str) -> dict`**

Valida que las sentencias citadas no sean alucinaciones.

**Proceso:**
1. Busca patrones: `Sentencia T-XXX/XXXX`, `C-XXX/XXXX`, `SU-XXX/XXXX`
2. Envía a GPT-4o para validar si existen
3. Retorna análisis de cada sentencia

**Output:**
```python
{
  "sentencias_citadas": [
    {
      "referencia": "Sentencia T-760/2008",
      "posiblemente_real": true,
      "tema_conocido": "Derecho a la salud",
      "riesgo_alucinacion": "bajo"
    }
  ],
  "total_sentencias": 1,
  "advertencia": "Verifica manualmente..."
}
```

---

**d) `analisis_completo_documento(documento: str, datos_caso: dict, tipo_documento: str) -> dict`**

Realiza análisis completo: calidad + jurisprudencia + sugerencias.

**Output:**
```python
{
  "jurisprudencia": {...},
  "calidad": {...},
  "sugerencias": {...},
  "listo_para_radicar": true/false,
  "resumen": {
    "puntuacion_calidad": 85,
    "sentencias_citadas": 2,
    "sugerencias_criticas": 0,
    "recomendacion": "Listo para radicar"
  }
}
```

---

### 3️⃣ **Document Service** (`document_service.py`)

**Funciones:**

**a) `generar_pdf(contenido: str, nombre: str) -> BytesIO`**

Convierte el documento generado a PDF profesional.

**b) `generar_docx(contenido: str, nombre: str) -> BytesIO`**

Convierte el documento a formato Word editable.

---

## ⚙️ VALIDADORES COLOMBIANOS

### **Validators** (`validators.py`)

```python
validar_cedula_colombiana(cedula: str) -> bool
validar_nit_colombiano(nit: str) -> bool
validar_telefono_colombiano(telefono: str) -> bool
validar_email(email: str) -> bool
```

**Uso:** Se aplican automáticamente en los schemas de Pydantic.

---

## 🔒 SEGURIDAD

### **JWT Authentication** (`security.py`)

```python
create_access_token(data: dict) -> str
verify_password(plain: str, hashed: str) -> bool
get_password_hash(password: str) -> str
get_current_user(token: str) -> User
```

**Configuración:**
- Algoritmo: HS256
- Expiración: 30 días
- Secret key: Variable de entorno

---

## 📊 FLUJO COMPLETO DE UN CASO

### **Fase 1: Conversación con Avatar**

```
1. Usuario hace click en "Iniciar Sesión"
2. Frontend → POST /sesiones/iniciar
3. Backend crea Caso (estado: "borrador")
4. Backend genera token LiveKit
5. Frontend conecta a LiveKit
6. Usuario conversa con avatar
7. Agente guarda cada mensaje → POST /mensajes/
8. Usuario termina → PUT /sesiones/{id}/finalizar
```

**Resultado:** Caso con transcripción completa guardada.

---

### **Fase 2: Procesamiento con IA**

```
1. Usuario hace click en "Procesar con IA"
2. Frontend → POST /casos/{id}/procesar-transcripcion
3. Backend llama a extraer_datos_conversacion()
4. GPT-4o extrae: hechos, derechos, entidad, pretensiones
5. Backend actualiza el caso con datos extraídos
6. Frontend muestra formulario pre-llenado
```

**Resultado:** Formulario con datos estructurados.

---

### **Fase 3: Generación de Documento**

```
1. Usuario revisa/edita datos
2. Usuario hace click en "Generar Documento"
3. Frontend → POST /casos/{id}/generar
4. Backend llama a generar_tutela() o generar_derecho_peticion()
5. GPT-4o genera documento completo
6. Backend realiza análisis_completo_documento()
7. Backend guarda documento + análisis
8. Frontend muestra documento y análisis
```

**Resultado:** Documento legal listo para radicar.

---

### **Fase 4: Descarga**

```
1. Usuario hace click en "Descargar PDF" o "Descargar DOCX"
2. Frontend → GET /casos/{id}/descargar/pdf
3. Backend genera archivo
4. Usuario descarga
```

**Resultado:** Archivo listo para imprimir/radicar.

---

## 🔧 VARIABLES DE ENTORNO

```bash
# Base de datos
DATABASE_URL=postgresql://user:pass@localhost:5432/abogadai_db

# Seguridad
SECRET_KEY=tu-clave-secreta-jwt

# OpenAI
OPENAI_API_KEY=sk-...

# LiveKit
LIVEKIT_URL=wss://...
LIVEKIT_API_KEY=...
LIVEKIT_API_SECRET=...

# Frontend
FRONTEND_URL=http://localhost:5173

# Entorno
ENVIRONMENT=development
```

---

## 📦 DEPENDENCIAS PRINCIPALES

```
fastapi==0.115.6
uvicorn==0.34.0
sqlalchemy==2.0.36
psycopg2-binary==2.9.10
pydantic==2.10.3
pydantic-settings==2.6.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.20
openai==1.58.1
livekit==0.18.2
livekit-api==0.8.3
reportlab==4.2.5
python-docx==1.1.2
```

---

## 🚀 COMANDOS DE EJECUCIÓN

### **Desarrollo:**
```bash
uvicorn app.main:app --reload --port 8000
```

### **Producción:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### **Migraciones:**
```bash
# Crear migración
alembic revision --autogenerate -m "mensaje"

# Aplicar migración
alembic upgrade head
```

---

## 📈 CARACTERÍSTICAS DESTACADAS

✅ **Soporte de 2 tipos de documentos** (tutela y derecho de petición)
✅ **Análisis diferenciado** por tipo de documento
✅ **Detección automática** de tipo según conversación
✅ **Validación de jurisprudencia** con IA
✅ **Análisis de fortaleza** pre-generación
✅ **Análisis de calidad** post-generación
✅ **Generación PDF/DOCX** profesional
✅ **Validadores colombianos** (cédula, NIT, teléfono)
✅ **Autenticación JWT** robusta
✅ **Integración LiveKit** para avatar
✅ **Persistencia de conversaciones**

---

## 🎯 PRÓXIMOS PASOS

- [ ] Sistema de notificaciones por email
- [ ] Dashboard de administración
- [ ] Métricas y analytics
- [ ] Sistema de pagos
- [ ] Plantillas personalizables
- [ ] Firma digital
- [ ] Radicación electrónica

---

**Última actualización:** Diciembre 2024
**Versión:** 2.0.0
