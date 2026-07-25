# Third-Party Notices

This service depends on the following pinned packages. Their licenses remain
the property of their respective copyright holders.

## Copyleft calculation dependencies

### Kerykeion 5.12.9

- Upstream: <https://github.com/g-battaglia/kerykeion>
- Declared license: AGPL-3.0
- Source distribution:
  <https://files.pythonhosted.org/packages/d8/8f/d91e01365843509e55c81febb4fe20e4480dc2485da4311f1efc80789b6d/kerykeion-5.12.9.tar.gz>
- SHA-256:
  `a7ef7bd6a46973913953fe0aa78cb714bd54fda4b20f01355b913fcf348f0216`

### PySwissEph 2.10.3.2

- Upstream: <https://github.com/astrorigin/pyswisseph>
- Public-distribution license: GNU Affero General Public License v3
- Swiss Ephemeris licensing information:
  <https://www.astro.com/swisseph/swephinfo_e.htm>
- Source distribution:
  <https://files.pythonhosted.org/packages/66/a6/db70d67a00dda42ebd033538c086879328f4c17f670eafe8aca2f11abfef/pyswisseph-2.10.3.2.tar.gz>
- SHA-256:
  `c54c305e83dbd5d2b71e58d8a69d8ee41de24c4d3328ce09e2af860a3537624d`

PySwissEph and the underlying Swiss Ephemeris are also available under
separate professional-license terms from their respective licensors. This
repository follows the public AGPL path and does not grant a professional
license.

## Permissive direct dependencies

| Package | Version | Upstream license |
| --- | --- | --- |
| FastAPI | 0.140.0 | MIT |
| Uvicorn | 0.51.0 | BSD-3-Clause |
| timezonefinder | 8.2.5 | MIT |
| pytz | 2026.2 | MIT |
| Pydantic | 2.13.4 | MIT |

Transitive package versions are fixed in `uv.lock`. License texts distributed
inside installed packages continue to apply. Run the dependency-source script
and inspect the source archives for authoritative copyright and license text.
