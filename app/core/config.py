# app/core/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SaaS API"
    environment: str = "local"
    debug: bool = True

    # use psycopg (not psycopg2) to match your stack
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/saas_db"

    jwt_secret_key: str = "change-me"  # or keep required if you prefer
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
