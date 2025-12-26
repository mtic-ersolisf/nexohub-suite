from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Lee variables desde .env en la raíz: services/api/.env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "NexoHub API"
    ENV: str = "local"

    # CORS
    CORS_ORIGINS: str = Field(default="http://localhost:3000")
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: str = "*"   # "*" o "GET,POST,PUT,DELETE"
    CORS_ALLOW_HEADERS: str = "*"   # "*" o "Authorization,Content-Type"

    def cors_origins_list(self) -> List[str]:
        v = (self.CORS_ORIGINS or "").strip()
        if not v:
            return []
        if v == "*":
            return ["*"]
        return [o.strip() for o in v.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

