from functools import lru_cache
import json

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def normalize_database_url(url: str) -> str:
    """Normalize postgres URLs for SQLAlchemy + psycopg3."""
    if url.startswith("postgres://"):
        url = "postgresql://" + url.removeprefix("postgres://")
    if url.startswith("postgresql://") and "+psycopg" not in url.split("://", 1)[0]:
        url = "postgresql+psycopg://" + url.removeprefix("postgresql://")
    return url


def normalize_cors_origin(origin: str) -> str:
    return origin.strip().rstrip("/")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "WQuiz API"
    api_prefix: str = "/api"
    database_url: str = "postgresql+psycopg://wquiz:wquiz@localhost:5432/wquiz"
    secret_key: str = "wquiz-dev-secret-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ]
    admin_email: str = "admin@example.com"
    admin_password: str = "admin123"
    session_time_limit_minutes: int = 120

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _normalize_cors_origins(cls, value: object) -> object:
        if isinstance(value, str):
            raw = value.strip()
            if raw.startswith("["):
                value = json.loads(raw)
            else:
                value = [part.strip() for part in raw.split(",") if part.strip()]
        if isinstance(value, list):
            return [normalize_cors_origin(str(item)) for item in value if str(item).strip()]
        return value

    @property
    def sqlalchemy_database_url(self) -> str:
        return normalize_database_url(self.database_url)


@lru_cache
def get_settings() -> Settings:
    return Settings()
