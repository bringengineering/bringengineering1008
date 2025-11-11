"""Application configuration management."""
from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Environment-driven configuration."""

    road_corp_api_key: str = Field(..., env="ROAD_CORP_API_KEY")
    kma_api_key: str = Field(..., env="KMA_API_KEY")
    kasi_api_key: str = Field(..., env="KASI_API_KEY")

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """Return a cached instance of :class:`Settings`."""

    return Settings()
