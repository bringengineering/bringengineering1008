"""Clients for interacting with external OpenAPI providers."""
from __future__ import annotations

from typing import Any, Dict

import httpx

from .config import Settings


class ExternalServiceError(RuntimeError):
    """Raised when an external API call fails."""


async def _request_json(url: str, params: Dict[str, Any], timeout: float) -> Dict[str, Any]:
    """Perform an HTTP GET request and return the decoded payload.

    The helpers prefer JSON responses but will fall back to returning a raw text
    body if the provider does not support JSON serialization.
    """

    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
        except httpx.TimeoutException as exc:  # pragma: no cover - network failure
            raise ExternalServiceError(f"Request to {url} timed out") from exc
        except httpx.HTTPStatusError as exc:  # pragma: no cover - network failure
            raise ExternalServiceError(
                f"Request to {url} failed with status {exc.response.status_code}"
            ) from exc
        except httpx.RequestError as exc:  # pragma: no cover - network failure
            raise ExternalServiceError(f"Failed to call {url}: {exc}") from exc

    try:
        return response.json()
    except ValueError:
        return {"raw": response.text}


async def fetch_solar_data(settings: Settings, lat: float, lon: float, date: str) -> Dict[str, Any]:
    """Call the configured KASI solar altitude OpenAPI endpoint."""

    params = {
        "serviceKey": settings.kasi_api_key,
        "locdate": date.replace("-", ""),
        "latitude": lat,
        "longitude": lon,
        "_type": "json",
    }
    return await _request_json(settings.kasi_solar_endpoint, params, settings.http_timeout)


async def fetch_traffic_data(settings: Settings, station_id: str, date: str) -> Dict[str, Any]:
    """Call the configured Korea Expressway OpenAPI endpoint."""

    params = {
        "serviceKey": settings.road_corp_api_key,
        "stationId": station_id,
        "searchDate": date.replace("-", ""),
        "type": "json",
    }
    return await _request_json(settings.road_corp_endpoint, params, settings.http_timeout)


async def fetch_weather_data(settings: Settings, station_id: str, date: str) -> Dict[str, Any]:
    """Call the configured KMA OpenAPI endpoint."""

    params = {
        "serviceKey": settings.kma_api_key,
        "stationId": station_id,
        "base_date": date.replace("-", ""),
        "dataType": "JSON",
    }
    return await _request_json(settings.kma_weather_endpoint, params, settings.http_timeout)
