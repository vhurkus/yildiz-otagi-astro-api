from datetime import datetime

import pytz
from kerykeion import AstrologicalSubjectFactory
from timezonefinder import TimezoneFinder

tf = TimezoneFinder()

HOUSE_SYSTEM_IDENTIFIERS = {
    "Placidus": "P",
    "WholeSign": "W",
    "Equal": "A",
}

SIGN_NAMES = [
    "",
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

# kerykeion returns abbreviated sign names — map to full names
SIGN_ABBREV_TO_FULL = {
    "Ari": "Aries",
    "Tau": "Taurus",
    "Gem": "Gemini",
    "Can": "Cancer",
    "Leo": "Leo",
    "Vir": "Virgo",
    "Lib": "Libra",
    "Sco": "Scorpio",
    "Sag": "Sagittarius",
    "Cap": "Capricorn",
    "Aqu": "Aquarius",
    "Pis": "Pisces",
}


def _normalize_sign(sign: str) -> str:
    """Convert kerykeion abbreviated sign name to full name."""
    return SIGN_ABBREV_TO_FULL.get(sign, sign)


def _house_system_identifier(house_system: str) -> str:
    """Translate the public API house-system name to Swiss Ephemeris code."""
    try:
        return HOUSE_SYSTEM_IDENTIFIERS[house_system]
    except KeyError as error:
        raise ValueError(f"Unsupported house system: {house_system}") from error


def _create_subject(
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
):
    """Create a kerykeion AstrologicalSubject from input parameters."""
    tz_name = tf.timezone_at(lat=lat, lng=lng) or "UTC"
    if utc_datetime is not None:
        if utc_datetime.tzinfo is None:
            raise ValueError("utc_datetime must include timezone information")
        local_datetime = utc_datetime.astimezone(pytz.timezone(tz_name))
        year = local_datetime.year
        month = local_datetime.month
        day = local_datetime.day
        hour = local_datetime.hour
        minute = local_datetime.minute

    return AstrologicalSubjectFactory.from_birth_data(
        name="Subject",
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        lat=lat,
        lng=lng,
        tz_str=tz_name,
        online=False,
        houses_system_identifier=_house_system_identifier(house_system),
        suppress_geonames_warning=True,
    )


def _sign_number(sign_name: str) -> int:
    """Convert sign name to number (Aries=1 ... Pisces=12)."""
    try:
        return SIGN_NAMES.index(sign_name)
    except ValueError:
        return 0


def _format_planet(
    name: str, full_degree: float, norm_degree: float, is_retro: bool, sign: str
) -> dict:
    """Format a planet entry to match the external API response."""
    full_sign = _normalize_sign(sign)
    return {
        "planet": {"en": name},
        "zodiac_sign": {
            "name": {"en": full_sign},
            "number": _sign_number(full_sign),
        },
        "fullDegree": round(full_degree, 6),
        "normDegree": round(norm_degree, 6),
        "isRetro": is_retro,
    }


def get_planets(
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
    """Calculate planet positions using kerykeion. Returns list matching external API format."""
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

    planets = []

    # Main celestial bodies from kerykeion
    planet_attrs = [
        ("sun", "Sun"),
        ("moon", "Moon"),
        ("mercury", "Mercury"),
        ("venus", "Venus"),
        ("mars", "Mars"),
        ("jupiter", "Jupiter"),
        ("saturn", "Saturn"),
        ("uranus", "Uranus"),
        ("neptune", "Neptune"),
        ("pluto", "Pluto"),
        ("chiron", "Chiron"),
        ("mean_north_lunar_node", "Mean Node"),
        ("true_north_lunar_node", "True Node"),
    ]

    for attr, display_name in planet_attrs:
        obj = getattr(subject, attr, None)
        if obj is None:
            continue
        planets.append(
            _format_planet(
                name=display_name,
                full_degree=obj.abs_pos,
                norm_degree=obj.position,
                is_retro=obj.retrograde if hasattr(obj, "retrograde") else False,
                sign=obj.sign,
            )
        )

    # Ascendant and MC (computed points, not planets)
    # First house cusp = Ascendant
    if subject.first_house:
        asc = subject.first_house
        planets.append(
            _format_planet(
                name="Ascendant",
                full_degree=asc.abs_pos,
                norm_degree=asc.position,
                is_retro=False,
                sign=asc.sign,
            )
        )

    # Tenth house cusp = MC (Midheaven)
    if subject.tenth_house:
        mc = subject.tenth_house
        planets.append(
            _format_planet(
                name="MC",
                full_degree=mc.abs_pos,
                norm_degree=mc.position,
                is_retro=False,
                sign=mc.sign,
            )
        )

    return planets
