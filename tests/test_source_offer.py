import asyncio
import unittest

import main


class SourceOfferTests(unittest.TestCase):
    def test_public_source_offer_identifies_license_and_repository(self):
        result = asyncio.run(main.source_offer())

        self.assertEqual(result["license"], "AGPL-3.0-only")
        self.assertEqual(
            result["source_code"],
            "https://github.com/vhurkus/yildiz-otagi-astro-api",
        )
        self.assertTrue(result["source_commit"])

    def test_health_response_includes_corresponding_source(self):
        result = asyncio.run(main.health())

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["source_code"], main.SOURCE_CODE_URL)
        self.assertEqual(result["source_commit"], main.SOURCE_COMMIT)


if __name__ == "__main__":
    unittest.main()
