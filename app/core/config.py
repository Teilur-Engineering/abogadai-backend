from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 días por defecto

    # CORS
    FRONTEND_URL: str = "http://localhost:5173"

    # Server
    PORT: int = 8000

    # LiveKit
    LIVEKIT_API_KEY: str
    LIVEKIT_API_SECRET: str
    LIVEKIT_URL: str

    # OpenAI
    OPENAI_API_KEY: str

    # Vita Wallet
    VITA_API_URL: str = "https://api.vitawallet.io"
    VITA_API_KEY: Optional[str] = None  # X-Trans-Key para autenticación
    VITA_API_SECRET: Optional[str] = None
    VITA_BUSINESS_SECRET: Optional[str] = None  # Secret para validar webhooks (HMAC-SHA256)
    VITA_X_LOGIN: Optional[str] = None  # Hash hexadecimal del business (para firmas)
    VITA_WALLET_MASTER_UUID: Optional[str] = None  # UUID de la wallet maestra
    VITA_ENVIRONMENT: str = "sandbox"  # sandbox | production

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
