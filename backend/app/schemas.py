"""Pydantic schemas used across the API."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class SolarSample(BaseModel):
    """Single solar position reading."""

    timestamp: datetime = Field(..., description="UTC timestamp of the reading")
    sun_azimuth: float = Field(..., description="Solar azimuth in degrees")
    sun_altitude: float = Field(..., description="Solar altitude in degrees")


class TrafficSample(BaseModel):
    """Traffic volume observation."""

    timestamp: datetime
    volume: float = Field(..., ge=0, description="Vehicles per hour")


class WeatherSample(BaseModel):
    """Weather observation affecting glare weighting."""

    timestamp: datetime
    cloud_cover: Optional[float] = Field(
        None,
        ge=0,
        le=1,
        description="Fractional cloud cover (0-1)",
    )
    solar_irradiance: Optional[float] = Field(
        None,
        ge=0,
        description="Solar irradiance in W/m^2",
    )


class RiskParameters(BaseModel):
    """Tunable thresholds for the risk calculation."""

    alignment_tolerance: float = Field(10.0, ge=0, description="Degrees")
    altitude_min: float = Field(0.0, description="Minimum solar altitude")
    altitude_max: float = Field(45.0, description="Maximum solar altitude")
    sg_weight: float = Field(0.5, ge=0, le=1)
    st_weight: float = Field(0.5, ge=0, le=1)


class RiskRequest(BaseModel):
    """Request payload for risk estimation."""

    road_azimuth: float = Field(..., description="Road heading in degrees")
    solar: List[SolarSample]
    traffic: List[TrafficSample]
    weather: List[WeatherSample] = Field(default_factory=list)
    params: RiskParameters = Field(default_factory=RiskParameters)


class RiskResponse(BaseModel):
    """Standard risk response structure."""

    sg: float
    st: float
    risk_percent: float
    grade: str
