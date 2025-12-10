# 📋 EJEMPLOS DE DATOS DE PRUEBA - ABOGADAI

## CÓMO USAR ESTOS EJEMPLOS

### Opción 1: Crear caso mediante API (Postman/Thunder Client)

```http
POST http://localhost:8000/casos/
Authorization: Bearer {tu_token_jwt}
Content-Type: application/json

{
  "tipo_documento": "tutela",
  "nombre_solicitante": "María González Pérez",
  ...
}
```

### Opción 2: Crear caso mediante Frontend (Manual)

1. Navegar a: `http://localhost:5173/app/tutela/nueva`
2. Llenar el formulario con los datos del ejemplo
3. **IMPORTANTE:** Modificar temporalmente el código del frontend para cambiar `tipo_documento`
4. Click en "Crear Tutela"
5. Click en "Generar Documento con IA"

---

## 🔵 EJEMPLO 1: TUTELA (DERECHO A LA SALUD)

### Datos para el formulario:

#### TIPO DE DOCUMENTO
```
tipo_documento: "tutela"
```

#### DATOS DEL SOLICITANTE
```
nombre_solicitante: María González Pérez
identificacion_solicitante: 52841239
direccion_solicitante: Calle 45 #23-67, Barrio La Esperanza, Bogotá
telefono_solicitante: 3154729801
email_solicitante: maria.gonzalez@gmail.com
```

#### ENTIDAD ACCIONADA
```
entidad_accionada: Sanitas EPS S.A.
direccion_entidad: Carrera 7 #99-53, Bogotá
representante_legal: Dr. Carlos Alberto Ramírez
```

#### CONTENIDO DE LA TUTELA
```
hechos:
La señora María González Pérez, de 58 años de edad, diagnosticada con diabetes tipo 2 e hipertensión arterial desde hace 10 años, requiere con urgencia un procedimiento quirúrgico de revascularización coronaria (bypass) debido a una cardiopatía isquémica severa detectada el pasado 15 de noviembre de 2024.

El médico cardiólogo tratante, Dr. Andrés Moreno (Registro Médico 12345), ordenó mediante prescripción médica No. 2024-11-15-001 la realización urgente de la cirugía, indicando que la paciente presenta riesgo vital inminente y que el procedimiento debe realizarse en un término máximo de 30 días.

El día 20 de noviembre de 2024, la paciente radicó ante Sanitas EPS la solicitud de autorización del procedimiento quirúrgico junto con toda la documentación médica requerida (historia clínica, exámenes de laboratorio, electrocardiograma, cateterismo cardíaco).

El 25 de noviembre de 2024, la EPS emitió una respuesta negando la autorización del procedimiento argumentando que "el procedimiento no está contemplado en el Plan de Beneficios en Salud (PBS) para el nivel de afiliación de la paciente" y sugiriendo "tratamientos alternativos menos invasivos".

El día 28 de noviembre de 2024, la paciente interpuso derecho de petición solicitando reconsideración de la negativa, adjuntando concepto médico adicional que confirma la urgencia vital del procedimiento. A la fecha (9 de diciembre de 2024) no ha recibido respuesta alguna.

La paciente ha presentado deterioro progresivo de su estado de salud, con episodios recurrentes de dolor torácico (angina de pecho), dificultad respiratoria y limitación severa para realizar actividades cotidianas. Su médico tratante ha reiterado la urgencia del procedimiento quirúrgico ante el riesgo de muerte súbita o infarto agudo de miocardio.

La negativa de la EPS a autorizar el procedimiento quirúrgico prescrito está vulnerando los derechos fundamentales a la salud, la vida y la integridad personal de la accionante, quien no cuenta con recursos económicos para asumir los costos del procedimiento (aproximadamente $45.000.000).

derechos_vulnerados:
Derecho a la Vida (Art. 11 C.P.)
Derecho a la Integridad Personal (Art. 12 C.P.)
Derecho a la Salud (Art. 49 C.P.)
Derecho a la Seguridad Social (Art. 48 C.P.)

pretensiones:
PRIMERO: Que se ordene a SANITAS EPS S.A. autorizar de manera inmediata el procedimiento quirúrgico de revascularización coronaria (bypass) prescrito por el médico tratante a la señora María González Pérez.

SEGUNDO: Que se ordene a SANITAS EPS S.A. garantizar la programación y realización del procedimiento quirúrgico en un término máximo de ocho (8) días hábiles contados a partir de la notificación del fallo de tutela.

TERCERO: Que se ordene a SANITAS EPS S.A. asumir la totalidad de los costos del procedimiento quirúrgico, incluyendo honorarios médicos, hospitalización, medicamentos, exámenes prequirúrgicos, posquirúrgicos y todos los tratamientos y cuidados necesarios para la recuperación de la paciente.

CUARTO: Que se ordene a SANITAS EPS S.A. garantizar la continuidad en la atención integral de salud de la accionante, incluyendo controles médicos periódicos, medicamentos y terapias de rehabilitación requeridas posterior al procedimiento quirúrgico.

fundamentos_derecho:
Constitución Política de Colombia: Artículos 11 (Derecho a la Vida), 12 (Derecho a la Integridad Personal), 48 (Derecho a la Seguridad Social), 49 (Derecho a la Salud), 86 (Acción de Tutela).

Ley 1751 de 2015 (Ley Estatutaria de Salud): Artículo 2 (Derecho fundamental a la salud), Artículo 8 (Orden de no desconocer el derecho fundamental a la salud), Artículo 10 (Derechos y deberes de las personas en relación con el Sistema de Salud).

Decreto 780 de 2016 (Decreto Único Reglamentario del Sector Salud): Artículos relativos a las obligaciones de las EPS en la prestación de servicios de salud.

Sentencia T-760 de 2008 de la Corte Constitucional: Protección del derecho fundamental a la salud y obligaciones de las EPS.

Circular 049 de 2008 de la Superintendencia Nacional de Salud: Sobre la garantía de continuidad en la prestación de servicios de salud.
```

---

## 🟢 EJEMPLO 2: DERECHO DE PETICIÓN (SOLICITUD DE INFORMACIÓN)

### Datos para el formulario:

#### TIPO DE DOCUMENTO
```
tipo_documento: "derecho_peticion"
```

#### DATOS DEL SOLICITANTE
```
nombre_solicitante: Carlos Eduardo Martínez Silva
identificacion_solicitante: 80123456
direccion_solicitante: Carrera 15 #34-89, Apartamento 502, Medellín
telefono_solicitante: 3012345678
email_solicitante: carlos.martinez@outlook.com
```

#### ENTIDAD DESTINATARIA
```
entidad_accionada: Secretaría de Hacienda Municipal de Medellín
direccion_entidad: Calle 44 #52-165, Centro Administrativo La Alpujarra, Medellín
representante_legal: Secretario de Hacienda Municipal
```

#### CONTENIDO DEL DERECHO DE PETICIÓN
```
hechos:
El señor Carlos Eduardo Martínez Silva, propietario del inmueble ubicado en la Carrera 15 #34-89, Apartamento 502 de Medellín, identificado con matrícula inmobiliaria No. 001-123456, ha recibido durante los últimos tres años facturas del impuesto predial con valores que considera excesivos y sin justificación aparente.

Para el año gravable 2022, el avalúo catastral de su inmueble fue establecido en $180.000.000 y el impuesto predial a pagar fue de $3.240.000.

Para el año gravable 2023, el avalúo catastral aumentó a $245.000.000 (incremento del 36%) y el impuesto predial a pagar fue de $4.410.000 (incremento del 36%).

Para el año gravable 2024, el avalúo catastral aumentó nuevamente a $320.000.000 (incremento del 31%) y el impuesto predial a pagar es de $5.760.000 (incremento del 31%).

El peticionario considera que estos incrementos anuales son desproporcionados y no se ajustan a la realidad del mercado inmobiliario ni a las características de su inmueble. Además, otros propietarios de apartamentos similares en el mismo edificio reportan avalúos catastrales significativamente menores.

El día 15 de noviembre de 2024, el peticionario se acercó personalmente a las oficinas de la Secretaría de Hacienda Municipal ubicadas en el Centro Administrativo La Alpujarra para solicitar información sobre los criterios utilizados para establecer el avalúo catastral de su inmueble, sin obtener una respuesta clara o documentación que sustente dichos valores.

El peticionario requiere conocer de manera detallada y documentada los criterios técnicos, metodologías y elementos utilizados para determinar el avalúo catastral de su inmueble durante los años 2022, 2023 y 2024, con el fin de ejercer su derecho de defensa y, si es del caso, interponer los recursos administrativos correspondientes.

pretensiones:
PRIMERO: Que la Secretaría de Hacienda Municipal de Medellín suministre copia de la ficha catastral actualizada del inmueble identificado con matrícula inmobiliaria No. 001-123456, correspondiente a los años gravables 2022, 2023 y 2024.

SEGUNDO: Que se informe de manera detallada y técnica la metodología, criterios y elementos utilizados para determinar el avalúo catastral del inmueble en los años 2022, 2023 y 2024, incluyendo:
   a) Área construida considerada
   b) Uso del suelo aplicado
   c) Estrato socioeconómico
   d) Año de construcción
   e) Estado de conservación
   f) Zonas homogéneas físicas y geoeconómicas aplicadas
   g) Valores unitarios de construcción y terreno utilizados

TERCERO: Que se proporcione copia de los actos administrativos (resoluciones, decretos o cualquier otro documento oficial) que establezcan o modifiquen el avalúo catastral del inmueble para los años 2022, 2023 y 2024.

CUARTO: Que se informe sobre los mecanismos, procedimientos y términos disponibles para que el peticionario pueda solicitar revisión del avalúo catastral o interponer recursos administrativos si considera que el avalúo no corresponde a la realidad del inmueble.

QUINTO: Que se certifique si el inmueble se encuentra al día con el pago del impuesto predial o si existen obligaciones pendientes.

fundamentos_derecho:
Constitución Política de Colombia: Artículo 23 (Derecho de Petición), Artículo 74 (Derecho de Acceso a Documentos Públicos).

Código de Procedimiento Administrativo y de lo Contencioso Administrativo (Ley 1437 de 2011):
- Artículo 13: Derecho de petición de información
- Artículo 14: Modalidades del derecho de petición
- Artículo 15: Término para resolver las peticiones
- Artículo 16: Peticiones entre autoridades
- Artículo 17: Solicitudes de documentos

Ley 1755 de 2015 (Estatuto del Derecho Fundamental de Petición):
- Artículo 1: Objeto
- Artículo 5: Derecho de petición de información
- Artículo 14: Términos para resolver
- Artículo 29: Silencio administrativo

Ley 962 de 2005 (Ley Anti-trámites): Artículo 1 (Objeto), Artículo 6 (Derecho de petición).

Decreto 1077 de 2015: Normas sobre avalúos catastrales.

Resolución 070 de 2011 del IGAC: Formación catastral y avalúos.
```

---

## 🟡 EJEMPLO 3: DERECHO DE PETICIÓN (QUEJA Y SOLICITUD DE ACTUACIÓN)

### Datos para el formulario:

#### TIPO DE DOCUMENTO
```
tipo_documento: "derecho_peticion"
```

#### DATOS DEL SOLICITANTE
```
nombre_solicitante: Andrea Paola Rojas Mendoza
identificacion_solicitante: 1015428976
direccion_solicitante: Transversal 23 #45-12, Barrio El Poblado, Cali
telefono_solicitante: 3187654321
email_solicitante: andrea.rojas@hotmail.com
```

#### ENTIDAD DESTINATARIA
```
entidad_accionada: EMCALI EICE ESP (Empresas Municipales de Cali)
direccion_entidad: Calle 8 #3-14, Cali
representante_legal: Gerente General EMCALI
```

#### CONTENIDO DEL DERECHO DE PETICIÓN
```
hechos:
La señora Andrea Paola Rojas Mendoza, usuaria del servicio de acueducto prestado por EMCALI EICE ESP en el inmueble ubicado en la Transversal 23 #45-12 de Cali, identificado con número de cuenta 123-456789, presenta formal derecho de petición ante los siguientes hechos:

Desde hace tres meses (septiembre, octubre y noviembre de 2024), la peticionaria ha venido recibiendo facturas del servicio de acueducto con valores anormalmente elevados que no corresponden al consumo real del inmueble:

- Septiembre 2024: Consumo facturado 85 m³ - Valor $420.000
- Octubre 2024: Consumo facturado 92 m³ - Valor $465.000
- Noviembre 2024: Consumo facturado 88 m³ - Valor $445.000

El inmueble es habitado únicamente por la peticionaria y su hijo menor de edad, y el consumo promedio histórico durante los últimos dos años ha sido de 15 a 18 m³ mensuales, con facturas promedio de $85.000 a $95.000.

El día 5 de octubre de 2024, la peticionaria radicó PQR No. 2024-10-05-789 ante EMCALI solicitando revisión del medidor y reclamando por el cobro excesivo. La empresa respondió el 20 de octubre mediante oficio No. 2024-10-20-456 indicando que "el medidor se encuentra funcionando correctamente" y que "el consumo facturado corresponde al registrado en el equipo de medición".

El 10 de noviembre de 2024, la peticionaria solicitó nuevamente mediante radicado No. 2024-11-10-321 la visita de un técnico de EMCALI para verificación presencial del medidor y del sistema de tuberías del inmueble. A la fecha (9 de diciembre de 2024) no ha recibido respuesta ni se ha realizado visita técnica alguna.

El 25 de noviembre de 2024, la peticionaria contrató los servicios de un plomero certificado quien realizó revisión completa del sistema de tuberías del inmueble y del medidor, certificando mediante documento escrito que "no se detectan fugas de agua ni irregularidades en las instalaciones internas" y que "el medidor presenta anomalías en su funcionamiento, registrando consumos superiores al flujo real de agua".

La situación ha generado un perjuicio económico grave a la peticionaria, quien es madre cabeza de familia y cuyos ingresos mensuales son limitados. Actualmente acumula facturas impagas por valor de $1.330.000 que exceden ampliamente su capacidad de pago y que no corresponden a su consumo real.

pretensiones:
PRIMERO: Que EMCALI EICE ESP responda de manera clara, precisa y de fondo las solicitudes radicadas mediante PQR No. 2024-10-05-789 y No. 2024-11-10-321, en especial la solicitud de revisión técnica presencial del medidor.

SEGUNDO: Que se ordene a EMCALI realizar de manera inmediata (dentro de los 3 días hábiles siguientes) una visita técnica especializada al inmueble ubicado en la Transversal 23 #45-12 para:
   a) Verificar el estado y funcionamiento del medidor de agua
   b) Revisar las instalaciones internas de acueducto
   c) Determinar la causa de los consumos anormalmente elevados registrados

TERCERO: Que si la visita técnica determina que el medidor se encuentra defectuoso o registra incorrectamente los consumos, se proceda a su reemplazo inmediato sin costo para el usuario.

CUARTO: Que se realice el reliquidación de las facturas de los meses de septiembre, octubre y noviembre de 2024 tomando como base el consumo promedio histórico del inmueble (15-18 m³) y se emita nueva facturación con los valores correctos.

QUINTO: Que se suspendan las acciones de cobro jurídico o corte del servicio relacionadas con las facturas en reclamación hasta tanto se resuelva de fondo la presente petición.

SEXTO: Que se informe a la peticionaria sobre los mecanismos de reclamación adicionales disponibles ante la Superintendencia de Servicios Públicos Domiciliarios en caso de no obtener respuesta satisfactoria.

fundamentos_derecho:
Constitución Política de Colombia: Artículo 23 (Derecho de Petición), Artículo 365 (Servicios Públicos Domiciliarios).

Ley 1755 de 2015 (Derecho Fundamental de Petición): Artículo 5 (Petición de información), Artículo 14 (Términos para resolver - 15 días hábiles), Artículo 17 (Petición de quejas).

Ley 142 de 1994 (Régimen de Servicios Públicos Domiciliarios):
- Artículo 135: Obligación de revisar el medidor
- Artículo 150: Reclamaciones de los usuarios
- Artículo 154: Suspensión del servicio

Ley 1480 de 2011 (Estatuto del Consumidor): Artículos 5, 23 y 58 sobre derechos de los consumidores.

Resolución CRA 457 de 2008: Régimen de facturación y reclamaciones en servicios de acueducto.
```

---

## 📝 NOTAS IMPORTANTES

### Validaciones del Backend:

**Campos OBLIGATORIOS para generar documento:**
- `nombre_solicitante`
- `entidad_accionada`
- `hechos`

**Campos OPCIONALES pero RECOMENDADOS:**
- Para **tutelas**: `derechos_vulnerados` (casi obligatorio para que tenga sentido)
- Para **derechos de petición**: `pretensiones` (importante para especificar qué se solicita)

### Diferencias Clave:

| Aspecto | Tutela | Derecho de Petición |
|---------|--------|---------------------|
| **Propósito** | Proteger derechos fundamentales | Solicitar información/actuación |
| **Dirigida a** | Juez (pero se acciona contra entidad) | Entidad pública o privada directamente |
| **Urgencia** | Sí (perjuicio irremediable) | No necesariamente |
| **Derechos vulnerados** | Requerido (Art. 11-41 C.P.) | No aplica |
| **Término respuesta** | 10 días (juez decide) | 15 días hábiles (entidad responde) |
| **Fundamento legal** | Art. 86 C.P., Decreto 2591/91 | Art. 23 C.P., Ley 1755/2015 |

### Cómo Probar:

1. **Backend directo con Postman:**
   ```
   POST http://localhost:8000/casos/
   Authorization: Bearer {token}
   Body: Copia el JSON del ejemplo
   ```

2. **Frontend (requiere modificación temporal):**
   - Editar `NuevaTutela.jsx` línea 27
   - Cambiar de `tipo_documento: 'tutela'` a `tipo_documento: 'derecho_peticion'`
   - Llenar formulario con datos del ejemplo
   - Guardar y generar documento

3. **Verificar generación:**
   ```
   POST http://localhost:8000/casos/{caso_id}/generar
   ```
   - Debe usar plantilla de tutela o derecho de petición según `tipo_documento`
   - Debe generar documento formateado correctamente
