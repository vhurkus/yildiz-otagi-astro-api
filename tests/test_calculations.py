import unittest
from datetime import UTC, datetime

from services.house_service import get_houses
from services.planet_service import _house_system_identifier, get_planets


class HouseSystemTests(unittest.TestCase):
    def test_public_house_systems_map_to_kerykeion_identifiers(self):
        self.assertEqual(_house_system_identifier("Placidus"), "P")
        self.assertEqual(_house_system_identifier("WholeSign"), "W")
        self.assertEqual(_house_system_identifier("Equal"), "A")
        with self.assertRaises(ValueError):
            _house_system_identifier("Unknown")

    def test_supported_house_systems_produce_distinct_cusps(self):
        kwargs = {
            "year": 1990,
            "month": 5,
            "day": 17,
            "hour": 8,
            "minute": 30,
            "lat": 41.0082,
            "lng": 28.9784,
            "tz_offset": 3,
        }
        systems = {
            name: get_houses(**kwargs, house_system=name)
            for name in ("Placidus", "WholeSign", "Equal")
        }

        for houses in systems.values():
            self.assertEqual(len(houses), 12)

        cusp_sets = {
            name: tuple(house["degree"] for house in houses) for name, houses in systems.items()
        }
        self.assertNotEqual(cusp_sets["Placidus"], cusp_sets["WholeSign"])
        self.assertNotEqual(cusp_sets["Placidus"], cusp_sets["Equal"])
        self.assertNotEqual(cusp_sets["WholeSign"], cusp_sets["Equal"])


class UtcInstantTests(unittest.TestCase):
    def test_same_utc_instant_keeps_geocentric_sun_position(self):
        instant = datetime(2026, 7, 25, 10, 15, tzinfo=UTC)
        common = {
            "year": 2000,
            "month": 1,
            "day": 1,
            "hour": 0,
            "minute": 0,
            "tz_offset": 0,
            "utc_datetime": instant,
        }
        istanbul = get_planets(
            **common,
            lat=41.0082,
            lng=28.9784,
        )
        new_york = get_planets(
            **common,
            lat=40.7128,
            lng=-74.0060,
        )

        istanbul_sun = next(item for item in istanbul if item["planet"]["en"] == "Sun")
        new_york_sun = next(item for item in new_york if item["planet"]["en"] == "Sun")
        self.assertAlmostEqual(
            istanbul_sun["fullDegree"],
            new_york_sun["fullDegree"],
            places=5,
        )


if __name__ == "__main__":
    unittest.main()
