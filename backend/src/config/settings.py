from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/videomind"
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "secret"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
