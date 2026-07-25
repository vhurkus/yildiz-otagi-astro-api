import logging
import os
import secrets

from fastapi import Depends, FastAPI, Header, HTTPException

from models.schemas import ChartRequest
from services.chart_service import get_natal_chart_svg
from services.house_service import get_houses
from services.planet_service import get_planets

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Yildiz Otagi Astro API",
    description="Self-hosted astrology calculation API using Swiss Ephemeris",
    version="1.0.0",
)

API_KEY = os.environ.get("ASTRO_API_KEY", "")
_IS_DEV_PLACEHOLDER = API_KEY in ("", "dev-key-change-me")
SOURCE_CODE_URL = os.environ.get(
    "SOURCE_CODE_URL",
    "https://github.com/vhurkus/yildiz-otagi-astro-api",
).strip()
SOURCE_COMMIT = os.environ.get("SOURCE_COMMIT", "development").strip()


@app.middleware("http")
async def add_source_offer_header(request, call_next):
    response = await call_next(request)
    response.headers["Link"] = f'<{SOURCE_CODE_URL}>; rel="source"'
    response.headers["X-Source-Code"] = SOURCE_CODE_URL
    response.headers["X-Source-Commit"] = SOURCE_COMMIT
    return response


def _house_system(req: ChartRequest) -> str:
    return req.config.house_system if req.config else "Placidus"


async def verify_api_key(x_api_key: str = Header(default="")):
    # Reject every calculation when production authentication is missing or
    # still uses the documented development placeholder.
    if _IS_DEV_PLACEHOLDER:
        raise HTTPException(
            status_code=503,
            detail="Server misconfigured: ASTRO_API_KEY env not set",
        )
    if not secrets.compare_digest(x_api_key, API_KEY):
        raise HTTPException(status_code=401, detail="Invalid API key")


@app.get("/")
@app.get("/source")
async def source_offer():
    return {
        "service": "Yildiz Otagi Astro API",
        "license": "AGPL-3.0-only",
        "source_code": SOURCE_CODE_URL,
        "source_commit": SOURCE_COMMIT,
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "source_code": SOURCE_CODE_URL,
        "source_commit": SOURCE_COMMIT,
    }


@app.post("/western/planets", dependencies=[Depends(verify_api_key)])
async def western_planets(req: ChartRequest):
    try:
        planets = get_planets(
            year=req.year,
            month=req.month,
            day=req.date,
            hour=req.hours,
            minute=req.minutes,
            lat=req.latitude,
            lng=req.longitude,
            tz_offset=req.timezone,
            house_system=_house_system(req),
            utc_datetime=req.utc_datetime,
        )
        return {"output": planets}
    except Exception as error:
        logger.exception("Planet calculation failed")
        raise HTTPException(status_code=500, detail="Calculation failed") from error


@app.post("/western/houses", dependencies=[Depends(verify_api_key)])
async def western_houses(req: ChartRequest):
    try:
        houses = get_houses(
            year=req.year,
            month=req.month,
            day=req.date,
            hour=req.hours,
            minute=req.minutes,
            lat=req.latitude,
            lng=req.longitude,
            tz_offset=req.timezone,
            house_system=_house_system(req),
            utc_datetime=req.utc_datetime,
        )
        return {"output": {"Houses": houses}}
    except Exception as error:
        logger.exception("House calculation failed")
        raise HTTPException(status_code=500, detail="Calculation failed") from error


@app.post("/western/natal-wheel-chart", dependencies=[Depends(verify_api_key)])
async def western_natal_wheel_chart(req: ChartRequest):
    try:
        language = "en"
        if req.config and req.config.language:
            language = req.config.language

        svg = get_natal_chart_svg(
            year=req.year,
            month=req.month,
            day=req.date,
            hour=req.hours,
            minute=req.minutes,
            lat=req.latitude,
            lng=req.longitude,
            tz_offset=req.timezone,
            language=language,
            house_system=_house_system(req),
            utc_datetime=req.utc_datetime,
        )
        return {"output": svg}
    except Exception as error:
        logger.exception("Natal chart rendering failed")
        raise HTTPException(status_code=500, detail="Calculation failed") from error


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
