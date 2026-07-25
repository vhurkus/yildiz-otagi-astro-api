# Corresponding Source Offer

Yıldız Otağı Astro API is operated under the GNU Affero General Public License
version 3 only.

## Identify the running version

Request either public metadata endpoint:

```bash
curl -i https://astro-api-49745214653.europe-west1.run.app/source
curl -i https://astro-api-49745214653.europe-west1.run.app/health
```

The response body contains `source_code` and `source_commit`. Every response
also contains:

```text
Link: <https://github.com/vhurkus/yildiz-otagi-astro-api>; rel="source"
X-Source-Code: https://github.com/vhurkus/yildiz-otagi-astro-api
X-Source-Commit: <full-git-commit>
```

## Retrieve the corresponding source

```bash
git clone https://github.com/vhurkus/yildiz-otagi-astro-api.git
cd yildiz-otagi-astro-api
git checkout <source_commit>
uv sync --locked --group dev
```

The checked-out commit, its `uv.lock`, build instructions, tests, and container
definition are the corresponding source and installation information for that
deployed revision.

The source distributions for the copyleft calculation dependencies can be
retrieved and verified with:

```bash
./scripts/fetch_dependency_sources.sh
```

Release archives may provide the same files as a convenience. The Git commit
reported by the running service is the authoritative version identifier.
