from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/videomind"
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "secret"

    # Telegram
    TELEGRAM_BOT_TOKEN: str = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"

    # Rate limiting
    RATE_LIMIT_MAX_REQUESTS: int = 10
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    # AI Services
    GROQ_API_KEY: str = "gsk_xxx"
    WHISPER_MODEL_SIZE: str = "base"  # tiny, base, small, medium
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Storage (opcional)
    S3_ENABLED: bool = False
    S3_BUCKET_NAME: str = "video-search-media"
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"

    # Processing
    TEMP_DIR: str = "/tmp/video_processor"

    # API
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    ALLOWED_HOSTS: List[str] = ["localhost"]
    ENVIRONMENT: str = "development"  # development, production
    DEBUG: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
