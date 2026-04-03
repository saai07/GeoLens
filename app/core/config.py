"""Centralized app configuration via pydantic-settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    gemini_api_key: str
    gemini_model: str = "gemini-2.5-flash"
    app_name: str = "GeoLens Audit API"
    app_version: str = "1.0.0"
    debug: bool = False
    scraper_timeout_seconds: float = 10.0


@lru_cache
def get_settings() -> Settings:
    return Settings()
