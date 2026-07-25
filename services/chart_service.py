import os
import tempfile
from datetime import datetime

from kerykeion import KerykeionChartSVG

from .planet_service import _create_subject


def get_natal_chart_svg(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    lat: float,
    lng: float,
    tz_offset: float,
    language: str = "en",
    house_system: str = "Placidus",
    utc_datetime: datetime | None = None,
) -> str:
    """Generate natal wheel chart SVG using kerykeion. Returns SVG string."""
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

    # kerykeion generates SVG to a temp file
    with tempfile.TemporaryDirectory() as tmpdir:
        chart = KerykeionChartSVG(
            subject,
            chart_type="Natal",
            new_output_directory=tmpdir,
        )
        chart.makeSVG()

        # Read the generated SVG file
        svg_files = [f for f in os.listdir(tmpdir) if f.endswith(".svg")]
        if not svg_files:
            return ""

        svg_path = os.path.join(tmpdir, svg_files[0])
        with open(svg_path, "r", encoding="utf-8") as f:
            return f.read()
