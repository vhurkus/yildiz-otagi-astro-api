from datetime import datetime

from .planet_service import _create_subject, _normalize_sign, _sign_number


def get_houses(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    lat: float,
    lng: float,
    tz_offset: float,
    house_system: str = "Placidus",
    utc_datetime: datetime | None = None,
) -> list[dict]:
    """Calculate house cusps using kerykeion. Returns list matching external API format."""
    subject = _create_subject(
        year,
        month,
        day,
        hour,
        minute,
        lat,
        lng,
        tz_offset,
        house_system=house_system,
        utc_datetime=utc_datetime,
    )

    house_attrs = [
        "first_house",
        "second_house",
        "third_house",
        "fourth_house",
        "fifth_house",
        "sixth_house",
        "seventh_house",
        "eighth_house",
        "ninth_house",
        "tenth_house",
        "eleventh_house",
        "twelfth_house",
    ]

    houses = []
    for i, attr in enumerate(house_attrs, start=1):
        house_obj = getattr(subject, attr, None)
        if house_obj is None:
            continue
        full_sign = _normalize_sign(house_obj.sign)
        houses.append(
            {
                "House": i,
                "degree": round(house_obj.abs_pos, 6),
                "normDegree": round(house_obj.position, 6),
                "zodiac_sign": {
                    "name": {"en": full_sign},
                    "number": _sign_number(full_sign),
                },
            }
        )

    return houses
