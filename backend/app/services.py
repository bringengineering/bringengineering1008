"""Business logic helpers for risk calculations."""
from __future__ import annotations

from math import cos
from typing import Iterable, Sequence

from .schemas import RiskParameters, SolarSample, TrafficSample, WeatherSample


def _angular_difference(a: float, b: float) -> float:
    """Return the smallest difference between two headings in degrees."""

    diff = abs((a - b) % 360)
    return min(diff, 360 - diff)


def compute_sg(
    road_azimuth: float,
    solar_samples: Sequence[SolarSample],
    params: RiskParameters,
) -> float:
    """Compute the geometric alignment score (0-1)."""

    if not solar_samples:
        return 0.0

    valid = [
        sample
        for sample in solar_samples
        if params.altitude_min <= sample.sun_altitude <= params.altitude_max
        and _angular_difference(sample.sun_azimuth, road_azimuth)
        <= params.alignment_tolerance
    ]
    return len(valid) / len(solar_samples)


def compute_st(
    road_azimuth: float,
    solar_samples: Sequence[SolarSample],
    traffic_samples: Sequence[TrafficSample],
    weather_samples: Sequence[WeatherSample],
    params: RiskParameters,
) -> float:
    """Compute the exposure score based on traffic and weighting (0-1)."""

    if not solar_samples or not traffic_samples:
        return 0.0

    traffic_by_time = {sample.timestamp: sample.volume for sample in traffic_samples}
    weather_by_time = {
        sample.timestamp: sample.cloud_cover if sample.cloud_cover is not None else 1.0
        for sample in weather_samples
    }

    total_volume = 0.0
    weighted_volume = 0.0
    for sample in solar_samples:
        volume = traffic_by_time.get(sample.timestamp)
        if volume is None:
            continue
        total_volume += volume

        if (
            params.altitude_min <= sample.sun_altitude <= params.altitude_max
            and _angular_difference(sample.sun_azimuth, road_azimuth)
            <= params.alignment_tolerance
        ):
            weight = weather_by_time.get(sample.timestamp, 1.0)
            weighted_volume += volume * weight

    if total_volume == 0:
        return 0.0

    return weighted_volume / total_volume


def grade_from_risk(risk_percent: float) -> str:
    """Convert a risk percentage into a qualitative grade."""

    thresholds = {
        "A": 20,
        "B": 40,
        "C": 60,
        "D": 80,
    }
    for grade, limit in thresholds.items():
        if risk_percent < limit:
            return grade
    return "E"


def combine_scores(sg: float, st: float, params: RiskParameters) -> float:
    """Blend Sg and St into a percentage risk value."""

    total_weight = params.sg_weight + params.st_weight
    if total_weight == 0:
        return 0.0

    sg_norm = max(0.0, min(1.0, sg))
    st_norm = max(0.0, min(1.0, st))
    risk_fraction = (
        params.sg_weight * sg_norm + params.st_weight * st_norm
    ) / total_weight
    return risk_fraction * 100
