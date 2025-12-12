from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.routes import auth, livekit, casos, referencias, sesiones, mensajes

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Abogadai API",
    description="API para la plataforma Abogadai - Generación de tutelas y derechos de petición con IA",
    version="2.0.0"
)

# Configurar CORS
# Permitir frontend de producción y desarrollo
allowed_origins = [
    settings.FRONTEND_URL,  # De .env (localhost en dev)
    "https://abogadai-frontend.onrender.com",  # Producción
    "http://localhost:5173",  # Desarrollo local
    "http://localhost:3000",  # Desarrollo alternativo
]

# Remover duplicados
allowed_origins = list(set(allowed_origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)
app.include_router(livekit.router)
app.include_router(casos.router)
app.include_router(referencias.router)
app.include_router(sesiones.router)  # NUEVO
app.include_router(mensajes.router)  # NUEVO


@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a Abogadai API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}
