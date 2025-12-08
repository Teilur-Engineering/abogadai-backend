# Abogadai Backend

Backend de la plataforma Abogadai para generación de tutelas y derechos de petición con IA.

## Tecnologías

- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Python 3.12+

## Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
cp .env.example .env
```

Edita `.env` y configura:
- `DATABASE_URL`: URL de conexión a PostgreSQL
- `SECRET_KEY`: Clave secreta para JWT (genera una segura)
- `FRONTEND_URL`: URL del frontend

4. Crear base de datos PostgreSQL:
```sql
CREATE DATABASE abogadai_db;
```

## Ejecución

### Desarrollo
```bash
uvicorn app.main:app --reload --port 8000
```

### Producción
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Documentación API

Una vez corriendo el servidor, accede a:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints principales

### Autenticación

- `POST /auth/signup` - Registro de usuario
- `POST /auth/login` - Login (retorna JWT token)
- `GET /auth/me` - Obtener usuario actual (requiere autenticación)

## Estructura del proyecto

```
abogadai-backend/
├── app/
│   ├── core/           # Configuración, database, security
│   ├── models/         # Modelos SQLAlchemy
│   ├── schemas/        # Schemas Pydantic
│   ├── routes/         # Endpoints API
│   ├── services/       # Lógica de negocio
│   └── main.py         # Aplicación principal
├── .env                # Variables de entorno
├── requirements.txt    # Dependencias
└── README.md           # Este archivo
```

## Generar SECRET_KEY

Para generar una SECRET_KEY segura:

```python
import secrets
print(secrets.token_urlsafe(32))
```
