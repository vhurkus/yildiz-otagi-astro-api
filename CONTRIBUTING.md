# Contributing

Contributions must preserve the service's narrow, stateless calculation
boundary and its public corresponding-source offer.

## Before opening a pull request

```bash
uv sync --locked --group dev
uv run ruff check .
uv run ruff format --check .
uv run python -m unittest discover -s tests -p 'test_*.py' -v
docker build -t yildiz-otagi-astro-api .
```

Requirements:

- use synthetic test dates and locations only;
- never commit secrets, tokens, request logs, or personal birth data;
- pin intentional dependency changes and refresh `uv.lock`;
- document license changes in `THIRD_PARTY_NOTICES.md`;
- keep `/source`, source headers, and the deployed commit identifier intact;
- add or update tests for behavior changes.

By contributing, you agree that your contribution is distributed under this
repository's AGPL-3.0-only license.
