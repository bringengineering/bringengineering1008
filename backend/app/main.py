"""FastAPI application wiring."""
from fastapi import Depends, FastAPI, Query

from .config import Settings, get_settings
from .schemas import RiskRequest, RiskResponse
from .services import combine_scores, compute_sg, compute_st, grade_from_risk

app = FastAPI(title="Tunnel Glare Risk API", version="0.1.0")


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Simple health endpoint."""

    return {"status": "ok"}


@app.get("/api/solar", tags=["data"])
def solar_proxy(
    lat: float = Query(..., description="Latitude in WGS84"),
    lon: float = Query(..., description="Longitude in WGS84"),
    date: str = Query(..., description="ISO date"),
    settings: Settings = Depends(get_settings),
) -> dict[str, object]:
    """Placeholder solar endpoint showing required parameters."""

    return {
        "message": "Invoke external solar API here",
        "lat": lat,
        "lon": lon,
        "date": date,
        "api_key_present": bool(settings.kasi_api_key),
    }


@app.get("/api/traffic", tags=["data"])
def traffic_proxy(
    station_id: str = Query(..., description="Road traffic station identifier"),
    date: str = Query(..., description="ISO date"),
    settings: Settings = Depends(get_settings),
) -> dict[str, object]:
    """Placeholder traffic endpoint showing required parameters."""

    return {
        "message": "Invoke Korea Expressway traffic API here",
        "station_id": station_id,
        "date": date,
        "api_key_present": bool(settings.road_corp_api_key),
    }


@app.get("/api/weather", tags=["data"])
def weather_proxy(
    station_id: str = Query(..., description="KMA weather station identifier"),
    date: str = Query(..., description="ISO date"),
    settings: Settings = Depends(get_settings),
) -> dict[str, object]:
    """Placeholder weather endpoint showing required parameters."""

    return {
        "message": "Invoke KMA weather API here",
        "station_id": station_id,
        "date": date,
        "api_key_present": bool(settings.kma_api_key),
    }


@app.post("/api/risk", response_model=RiskResponse, tags=["risk"])
def estimate_risk(payload: RiskRequest) -> RiskResponse:
    """Calculate glare risk from client-provided time-series data."""

    sg = compute_sg(payload.road_azimuth, payload.solar, payload.params)
    st = compute_st(
        payload.road_azimuth,
        payload.solar,
        payload.traffic,
        payload.weather,
        payload.params,
    )
    risk = combine_scores(sg, st, payload.params)
    grade = grade_from_risk(risk)

    return RiskResponse(sg=sg, st=st, risk_percent=risk, grade=grade)


@app.get("/api/tunnels", tags=["data"])
def tunnel_lookup(query: str = Query(..., min_length=1)) -> dict[str, object]:
    """Return mock tunnel lookup results."""

    sample = {
        "id": "sample-tunnel",
        "name": "Sample Tunnel",
        "lat": 37.5665,
        "lon": 126.978,
        "road_azimuth": 90.0,
    }
    matches = [sample] if query.lower() in sample["name"].lower() else []
    return {"items": matches}
