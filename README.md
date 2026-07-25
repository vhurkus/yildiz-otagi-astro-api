# Yıldız Otağı Astro API

This repository is the public corresponding source for the astrology
calculation service used by the Yıldız Otağı mobile application.

The service converts a supplied birth time and location into deterministic
planet, house, and natal-wheel data. It does not persist requests or user
profiles.

## Source offer

Every HTTP response advertises this repository through a `Link` header with
`rel="source"`. The unauthenticated `/source` and `/health` endpoints also
return:

- the source repository URL;
- the exact deployed Git commit;
- the service license.

Production deployments must set `SOURCE_COMMIT` to the full commit SHA used to
build the running revision. See [SOURCE_OFFER.md](SOURCE_OFFER.md) for the
complete retrieval process.

## API

Public metadata endpoints:

- `GET /`
- `GET /source`
- `GET /health`

Authenticated calculation endpoints:

- `POST /western/planets`
- `POST /western/houses`
- `POST /western/natal-wheel-chart`

Calculation endpoints require the `x-api-key` header. API credentials are
deployment secrets and are intentionally excluded from this repository.

## Configuration

| Variable | Required | Purpose |
| --- | --- | --- |
| `ASTRO_API_KEY` | Yes | Server-to-server authentication for calculation endpoints |
| `SOURCE_CODE_URL` | No | Public corresponding-source URL; defaults to this repository |
| `SOURCE_COMMIT` | Production | Exact full Git commit SHA deployed to the running revision |

## Local development

Prerequisites:

- Python 3.11
- [uv](https://docs.astral.sh/uv/)

Install the locked environment and run the checks:

```bash
uv sync --locked --group dev
uv run ruff check .
uv run ruff format --check .
uv run python -m unittest discover -s tests -p 'test_*.py' -v
```

Start the API:

```bash
ASTRO_API_KEY=local-development-key \
SOURCE_COMMIT="$(git rev-parse HEAD)" \
uv run uvicorn main:app --host 127.0.0.1 --port 8080
```

## Container

Build and run the same locked dependency graph used by production:

```bash
docker build -t yildiz-otagi-astro-api .
docker run --rm -p 8080:8080 \
  -e ASTRO_API_KEY=local-development-key \
  -e SOURCE_COMMIT="$(git rev-parse HEAD)" \
  yildiz-otagi-astro-api
```

Deploy only from a clean checkout of the commit placed in `SOURCE_COMMIT`.
Never bake `ASTRO_API_KEY` into an image or source file.

## Third-party source

Exact direct dependency versions are recorded in `uv.lock` and
`requirements.txt`. Licensing and upstream-source details are in
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

To download and verify the source distributions of the copyleft calculation
dependencies:

```bash
./scripts/fetch_dependency_sources.sh
```

## Security and privacy

The service is stateless and does not intentionally store request bodies.
Do not use real personal birth data in issues, tests, logs, or pull requests.
See [SECURITY.md](SECURITY.md) for private vulnerability reporting.

## License

Copyright © 2026 Yıldız Otağı contributors.

This repository is licensed under
[GNU Affero General Public License v3.0 only](LICENSE). Network users must be
offered the corresponding source of the version they interact with.
