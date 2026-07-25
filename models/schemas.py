from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ChartConfig(BaseModel):
    observation_point: Literal["geocentric"] = "geocentric"
    ayanamsha: Literal["tropical"] = "tropical"
    house_system: Literal["Placidus", "WholeSign", "Equal"] = "Placidus"
    language: str | None = None


class ChartRequest(BaseModel):
    year: int = Field(ge=1900, le=2100)
    month: int = Field(ge=1, le=12)
    date: int = Field(alias="date")
    hours: int = Field(ge=0, le=23)
    minutes: int = Field(ge=0, le=59)
    seconds: int = Field(default=0, ge=0, le=59)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    timezone: float = Field(ge=-14, le=14)
    utc_datetime: datetime | None = None
    config: ChartConfig | None = None


class PlanetOutput(BaseModel):
    planet: dict  # {"en": "Sun"}
    zodiac_sign: dict  # {"name": {"en": "Aries"}, "number": 1}
    fullDegree: float
    normDegree: float
    isRetro: bool


class HouseOutput(BaseModel):
    House: int
    degree: float
    normDegree: float
    zodiac_sign: dict  # {"name": {"en": "Aries"}, "number": 1}


class PlanetsResponse(BaseModel):
    output: list[PlanetOutput]


class HousesResponse(BaseModel):
    output: dict  # {"Houses": [...]}


class ChartResponse(BaseModel):
    output: str  # SVG string
