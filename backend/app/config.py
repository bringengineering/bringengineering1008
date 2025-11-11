"""Application configuration management."""
from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Environment-driven configuration."""

    road_corp_api_key: str = Field(..., env="ROAD_CORP_API_KEY")
    road_corp_endpoint: str = Field(
        "https://openapi.ex.co.kr/trafficapi/naturalEvent/trafficVolume.do",
        env="ROAD_CORP_ENDPOINT",
    )

    kma_api_key: str = Field(..., env="KMA_API_KEY")
    kma_weather_endpoint: str = Field(
        "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst",
        env="KMA_WEATHER_ENDPOINT",
    )

    kasi_api_key: str = Field(..., env="KASI_API_KEY")
    kasi_solar_endpoint: str = Field(
        "https://apis.data.go.kr/B090041/openapi/service/SrAltDpService/getSunAltWorldTime",
        env="KASI_SOLAR_ENDPOINT",
    )

    http_timeout: float = Field(10.0, env="HTTP_TIMEOUT")

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """Return a cached instance of :class:`Settings`."""

    return Settings()
