from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "WQuiz API"
    api_prefix: str = "/api"
    database_url: str = "sqlite:///./wquiz.db"
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


@lru_cache
def get_settings() -> Settings:
    return Settings()
