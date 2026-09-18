from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "GACHINGLAB API"
    database_url: str = "sqlite:///./gachinglab.db"
    jwt_secret_key: str = "change-this-secret"
    jwt_refresh_secret_key: str = "change-this-refresh-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 14
    encryption_key: str = "2Y4ahB8be4itAupMb7j13bXvjj-45NuoTuNlY5fX1_k="
    rate_limit_per_minute: int = 120

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
