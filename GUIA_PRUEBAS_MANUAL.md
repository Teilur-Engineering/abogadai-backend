# 🧪 GUÍA DE PRUEBAS MANUALES - FASE 3

## 📌 OBJETIVO

Probar la generación de documentos (tutelas y derechos de petición) de forma **MANUAL** usando el formulario del frontend o API directa, **SIN pasar por la sesión con IA**.

---

## 🚀 OPCIÓN 1: PRUEBAS CON POSTMAN/THUNDER CLIENT (RECOMENDADO)

### Paso 1: Obtener Token de Autenticación

#### Login:
```http
POST http://localhost:8000/auth/login
Content-Type: application/json

{
  "email": "tu_email@ejemplo.com",
  "password": "tu_password"
}
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "tu_email@ejemplo.com",
    "nombre": "Tu Nombre"
  }
}
```

**⚠️ IMPORTANTE:** Copia el `access_token` para usarlo en los siguientes requests.

---

### Paso 2A: Crear una TUTELA

```http
POST http://localhost:8000/casos/
Authorization: Bearer {tu_access_token}
Content-Type: application/json

{
  "tipo_documento": "tutela",
  "nombre_solicitante": "María González Pérez",
  "identificacion_solicitante": "52841239",
  "direccion_solicitante": "Calle 45 #23-67, Barrio La Esperanza, Bogotá",
  "telefono_solicitante": "3154729801",
  "email_solicitante": "maria.gonzalez@gmail.com",
  "entidad_accionada": "Sanitas EPS S.A.",
  "direccion_entidad": "Carrera 7 #99-53, Bogotá",
  "representante_legal": "Dr. Carlos Alberto Ramírez",
  "hechos": "La señora María González Pérez, de 58 años de edad, diagnosticada con diabetes tipo 2 e hipertensión arterial desde hace 10 años, requiere con urgencia un procedimiento quirúrgico de revascularización coronaria (bypass) debido a una cardiopatía isquémica severa detectada el pasado 15 de noviembre de 2024.\n\nEl médico cardiólogo tratante, Dr. Andrés Moreno (Registro Médico 12345), ordenó mediante prescripción médica No. 2024-11-15-001 la realización urgente de la cirugía, indicando que la paciente presenta riesgo vital inminente y que el procedimiento debe realizarse en un término máximo de 30 días.\n\nEl día 20 de noviembre de 2024, la paciente radicó ante Sanitas EPS la solicitud de autorización del procedimiento quirúrgico junto con toda la documentación médica requerida (historia clínica, exámenes de laboratorio, electrocardiograma, cateterismo cardíaco).\n\nEl 25 de noviembre de 2024, la EPS emitió una respuesta negando la autorización del procedimiento argumentando que el procedimiento no está contemplado en el Plan de Beneficios en Salud (PBS) para el nivel de afiliación de la paciente y sugiriendo tratamientos alternativos menos invasivos.\n\nLa negativa de la EPS a autorizar el procedimiento quirúrgico prescrito está vulnerando los derechos fundamentales a la salud, la vida y la integridad personal de la accionante.",
  "derechos_vulnerados": "Derecho a la Vida (Art. 11 C.P.)\nDerecho a la Integridad Personal (Art. 12 C.P.)\nDerecho a la Salud (Art. 49 C.P.)\nDerecho a la Seguridad Social (Art. 48 C.P.)",
  "pretensiones": "PRIMERO: Que se ordene a SANITAS EPS S.A. autorizar de manera inmediata el procedimiento quirúrgico de revascularización coronaria (bypass) prescrito por el médico tratante a la señora María González Pérez.\n\nSEGUNDO: Que se ordene a SANITAS EPS S.A. garantizar la programación y realización del procedimiento quirúrgico en un término máximo de ocho (8) días hábiles contados a partir de la notificación del fallo de tutela.\n\nTERCERO: Que se ordene a SANITAS EPS S.A. asumir la totalidad de los costos del procedimiento quirúrgico, incluyendo honorarios médicos, hospitalización, medicamentos, exámenes prequirúrgicos, posquirúrgicos y todos los tratamientos y cuidados necesarios para la recuperación de la paciente.",
  "fundamentos_derecho": "Constitución Política de Colombia: Artículos 11 (Derecho a la Vida), 12 (Derecho a la Integridad Personal), 48 (Derecho a la Seguridad Social), 49 (Derecho a la Salud), 86 (Acción de Tutela).\n\nLey 1751 de 2015 (Ley Estatutaria de Salud): Artículo 2 (Derecho fundamental a la salud), Artículo 8 (Orden de no desconocer el derecho fundamental a la salud).\n\nSentencia T-760 de 2008 de la Corte Constitucional: Protección del derecho fundamental a la salud y obligaciones de las EPS."
}
```

**Respuesta esperada:**
```json
{
  "id": 1,
  "user_id": 1,
  "tipo_documento": "tutela",
  "estado": "borrador",
  "nombre_solicitante": "María González Pérez",
  ...
  "created_at": "2024-12-09T...",
  "updated_at": "2024-12-09T..."
}
```

**✅ GUARDA EL `id` DEL CASO CREADO** (ejemplo: 1)

---

### Paso 2B: Crear un DERECHO DE PETICIÓN

```http
POST http://localhost:8000/casos/
Authorization: Bearer {tu_access_token}
Content-Type: application/json

{
  "tipo_documento": "derecho_peticion",
  "nombre_solicitante": "Carlos Eduardo Martínez Silva",
  "identificacion_solicitante": "80123456",
  "direccion_solicitante": "Carrera 15 #34-89, Apartamento 502, Medellín",
  "telefono_solicitante": "3012345678",
  "email_solicitante": "carlos.martinez@outlook.com",
  "entidad_accionada": "Secretaría de Hacienda Municipal de Medellín",
  "direccion_entidad": "Calle 44 #52-165, Centro Administrativo La Alpujarra, Medellín",
  "representante_legal": "Secretario de Hacienda Municipal",
  "hechos": "El señor Carlos Eduardo Martínez Silva, propietario del inmueble ubicado en la Carrera 15 #34-89, Apartamento 502 de Medellín, identificado con matrícula inmobiliaria No. 001-123456, ha recibido durante los últimos tres años facturas del impuesto predial con valores que considera excesivos y sin justificación aparente.\n\nPara el año gravable 2022, el avalúo catastral de su inmueble fue establecido en $180.000.000 y el impuesto predial a pagar fue de $3.240.000.\n\nPara el año gravable 2023, el avalúo catastral aumentó a $245.000.000 (incremento del 36%) y el impuesto predial a pagar fue de $4.410.000.\n\nPara el año gravable 2024, el avalúo catastral aumentó nuevamente a $320.000.000 (incremento del 31%) y el impuesto predial a pagar es de $5.760.000.\n\nEl peticionario considera que estos incrementos anuales son desproporcionados y no se ajustan a la realidad del mercado inmobiliario.",
  "pretensiones": "PRIMERO: Que la Secretaría de Hacienda Municipal de Medellín suministre copia de la ficha catastral actualizada del inmueble identificado con matrícula inmobiliaria No. 001-123456, correspondiente a los años gravables 2022, 2023 y 2024.\n\nSEGUNDO: Que se informe de manera detallada y técnica la metodología, criterios y elementos utilizados para determinar el avalúo catastral del inmueble en los años 2022, 2023 y 2024.\n\nTERCERO: Que se proporcione copia de los actos administrativos (resoluciones, decretos o cualquier otro documento oficial) que establezcan o modifiquen el avalúo catastral del inmueble para los años 2022, 2023 y 2024.",
  "fundamentos_derecho": "Constitución Política de Colombia: Artículo 23 (Derecho de Petición), Artículo 74 (Derecho de Acceso a Documentos Públicos).\n\nLey 1437 de 2011: Artículo 13 (Derecho de petición de información), Artículo 15 (Término para resolver las peticiones).\n\nLey 1755 de 2015: Artículo 5 (Derecho de petición de información), Artículo 14 (Términos para resolver - 15 días hábiles)."
}
```

**✅ GUARDA EL `id` DEL CASO CREADO**

---

### Paso 3: Generar el Documento con IA

```http
POST http://localhost:8000/casos/{caso_id}/generar
Authorization: Bearer {tu_access_token}
```

**Ejemplo:**
```http
POST http://localhost:8000/casos/1/generar
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Respuesta esperada:**
```json
{
  "id": 1,
  "tipo_documento": "tutela",
  "estado": "generado",
  "documento_generado": "SEÑOR JUEZ CIVIL MUNICIPAL DE BOGOTÁ\n\nACCIÓN DE TUTELA\n\nMaría González Pérez...",
  "analisis_calidad": {
    "puntuacion_total": 85,
    "listo_para_radicar": true,
    ...
  },
  "analisis_jurisprudencia": {...},
  "sugerencias_mejora": {...},
  ...
}
```

**✅ VERIFICA:**
- ✅ `documento_generado` contiene el texto del documento
- ✅ Para tutela: debe tener secciones I. HECHOS, II. DERECHOS VULNERADOS, III. PRETENSIONES, etc.
- ✅ Para derecho de petición: debe tener I. OBJETO, II. HECHOS, III. FUNDAMENTOS, IV. PETICIONES, etc.
- ✅ `estado` cambió a `"generado"`
- ✅ `analisis_calidad`, `analisis_jurisprudencia` y `sugerencias_mejora` están presentes

---

### Paso 4: Descargar el Documento

#### Descargar PDF:
```http
GET http://localhost:8000/casos/{caso_id}/descargar/pdf
Authorization: Bearer {tu_access_token}
```

**✅ VERIFICA el nombre del archivo:**
- Para tutela: `tutela_Maria_Gonzalez_Perez_1.pdf`
- Para derecho de petición: `derecho_peticion_Carlos_Martinez_2.pdf`

#### Descargar DOCX:
```http
GET http://localhost:8000/casos/{caso_id}/descargar/docx
Authorization: Bearer {tu_access_token}
```

---

## 🌐 OPCIÓN 2: PRUEBAS CON FRONTEND (Requiere modificación temporal)

### Paso 1: Modificar el Frontend

**Archivo:** `C:\Users\jeiso\Desktop\abogadai-frontend\src\pages\NuevaTutela.jsx`

**Línea 27 - ANTES:**
```javascript
const [formData, setFormData] = useState({
  tipo_documento: 'tutela',  // ❌ Hardcoded
  nombre_solicitante: '',
  ...
```

**Línea 27 - DESPUÉS (para probar derecho de petición):**
```javascript
const [formData, setFormData] = useState({
  tipo_documento: 'derecho_peticion',  // ✅ Cambiado temporalmente
  nombre_solicitante: '',
  ...
```

**O MEJOR AÚN - Agregar selector:**
```javascript
const [formData, setFormData] = useState({
  tipo_documento: 'tutela',  // Valor por defecto
  nombre_solicitante: '',
  ...
```

Y en el JSX, agregar antes de la sección "Datos del Solicitante":
```jsx
{/* Selector de tipo de documento */}
<div className="mb-6">
  <label className="block text-sm font-medium text-gray-700 mb-2">
    Tipo de Documento
  </label>
  <select
    name="tipo_documento"
    value={formData.tipo_documento}
    onChange={handleChange}
    className="w-full px-4 py-2 border border-gray-300 rounded-lg"
  >
    <option value="tutela">Tutela</option>
    <option value="derecho_peticion">Derecho de Petición</option>
  </select>
</div>
```

### Paso 2: Iniciar el Frontend

```bash
cd C:\Users\jeiso\Desktop\abogadai-frontend
npm run dev
```

### Paso 3: Navegar y Crear Caso

1. Ir a `http://localhost:5173/login`
2. Iniciar sesión
3. Click en "Nueva Tutela" (o navegar a `/app/tutela/nueva`)
4. **Seleccionar tipo de documento** (si agregaste el selector)
5. Llenar formulario con datos del ejemplo
6. Click en "Crear Tutela"
7. Esperar redirección automática a `/app/tutela/{casoId}`

### Paso 4: Generar Documento

1. En la página de edición del caso
2. Click en "Generar Documento con IA"
3. Esperar (puede tardar 10-30 segundos)
4. Ver documento generado en pantalla

### Paso 5: Descargar

1. Click en "Descargar PDF"
2. Click en "Descargar DOCX"
3. Verificar nombres de archivo

---

## ✅ CHECKLIST DE PRUEBAS

### Para TUTELA:

- [ ] Crear caso con `tipo_documento: "tutela"`
- [ ] Verificar que se guarda con estado `"borrador"`
- [ ] Generar documento con `POST /casos/{id}/generar`
- [ ] Verificar que estado cambia a `"generado"`
- [ ] Verificar estructura del documento:
  - [ ] Encabezado: "SEÑOR JUEZ CIVIL MUNICIPAL DE..."
  - [ ] Sección I. HECHOS
  - [ ] Sección II. DERECHOS FUNDAMENTALES VULNERADOS
  - [ ] Sección III. PRETENSIONES
  - [ ] Sección IV. FUNDAMENTOS DE DERECHO
  - [ ] Sección V. PRUEBAS
  - [ ] Sección VI. JURAMENTO
  - [ ] Sección VII. NOTIFICACIONES
- [ ] Verificar análisis de calidad (puntuación 0-100)
- [ ] Verificar análisis de jurisprudencia
- [ ] Verificar sugerencias de mejora
- [ ] Descargar PDF con nombre: `tutela_Maria_Gonzalez_Perez_{id}.pdf`
- [ ] Descargar DOCX con nombre: `tutela_Maria_Gonzalez_Perez_{id}.docx`

### Para DERECHO DE PETICIÓN:

- [ ] Crear caso con `tipo_documento: "derecho_peticion"`
- [ ] Verificar que se guarda con estado `"borrador"`
- [ ] Generar documento con `POST /casos/{id}/generar`
- [ ] Verificar que estado cambia a `"generado"`
- [ ] Verificar estructura del documento:
  - [ ] Encabezado con destinatario (entidad)
  - [ ] Sección I. OBJETO
  - [ ] Sección II. HECHOS
  - [ ] Sección III. FUNDAMENTOS DE DERECHO (Art. 23 C.P., Ley 1437/2011)
  - [ ] Sección IV. PETICIONES
  - [ ] Sección V. NOTIFICACIONES
  - [ ] Mención del plazo de 15 días hábiles
- [ ] Verificar análisis de calidad (puntuación 0-100)
- [ ] Verificar análisis de jurisprudencia
- [ ] Verificar sugerencias de mejora
- [ ] Descargar PDF con nombre: `derecho_peticion_Carlos_Martinez_{id}.pdf`
- [ ] Descargar DOCX con nombre: `derecho_peticion_Carlos_Martinez_{id}.docx`

### Para ANÁLISIS DE FORTALEZA (Opcional):

- [ ] Tutela: `POST /casos/{id}/analizar-fortaleza` → Verifica criterios de tutela
- [ ] Derecho Petición: `POST /casos/{id}/analizar-fortaleza` → Verifica criterios administrativos
- [ ] Verificar puntuación 0-100
- [ ] Verificar probabilidad de éxito (baja/media/alta)
- [ ] Verificar puntos fuertes y débiles
- [ ] Verificar recomendaciones

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Error: "El caso debe tener al menos: nombre del solicitante, entidad accionada y hechos"
- **Causa:** Campos requeridos vacíos
- **Solución:** Asegúrate de llenar `nombre_solicitante`, `entidad_accionada` y `hechos`

### Error: "Para analizar fortaleza de una tutela se requiere: hechos y derechos vulnerados"
- **Causa:** Intentas analizar fortaleza de tutela sin derechos vulnerados
- **Solución:** Llena el campo `derechos_vulnerados` para tutelas

### Documento generado está vacío o tiene errores
- **Causa:** Error en OpenAI API o falta de API key
- **Solución:** Verifica que `OPENAI_API_KEY` esté configurada en `.env`

### Nombres de archivo incorrectos
- **Causa:** No se actualizó el código de descarga
- **Solución:** Verifica cambios en `app/routes/casos.py` líneas 431 y 481

---

## 📊 LOGS ÚTILES

Revisa los logs del backend para debugging:

```bash
# Al procesar generación
🧠 Llamando a GPT-4o para generar tutela...
✅ Tutela generada exitosamente

# O
🧠 Llamando a GPT-4o para generar derecho de petición...
✅ Derecho de petición generado exitosamente
```

---

## 🎯 PRÓXIMOS PASOS

Una vez que las pruebas manuales funcionen correctamente:

1. ✅ Verificar que la generación manual funciona para ambos tipos
2. ⏭️ Probar el flujo con IA (sesión de avatar)
3. ⏭️ Verificar que la IA detecta correctamente el tipo de documento
4. ⏭️ Ajustar frontend para soportar ambos tipos visualmente

