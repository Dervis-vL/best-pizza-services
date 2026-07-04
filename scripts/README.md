# scripts

Standalone **developer / operational utilities**. These are run directly
(`uv run python scripts/<name>.py`) or mounted into a container — they are *not* importable
modules and are **never deployed** as part of `apps/`, `services/`, or `packages/`.

Because they live outside the packaged workspace, they have no `__init__.py`; `scripts/*.py`
is exempt from ruff's `INP001` (implicit-namespace-package) rule via `per-file-ignores`.

## Scripts

| Script | Purpose |
|---|---|
| [`serve_local.py`](serve_local.py) | DEV-only local stand-in for the Scaleway Serverless Jobs API. |
| [`drop_all.py`](drop_all.py) | Destructive reset of the pizza database schema. |

### `serve_local.py` — local Scaleway Jobs mock

Lets the `pizza_worker` job pipeline run end-to-end in `podman compose` **without** a real
Scaleway control plane, while the API keeps using the real Scaleway SDK unchanged.

It's a tiny stdlib HTTP server that:
1. answers the Jobs "start" endpoint (`POST /serverless-jobs/v1alpha2/regions/*/job-definitions/{id}/start`),
2. maps the job-definition id to a worker subcommand (`run-pending` / `add-category`) and
   launches it as a fire-and-forget subprocess, forwarding any `environment_variables`
   (e.g. `WORKER_PAYLOAD_ID`) from the request,
3. returns a minimal `StartJobDefinitionResponse` the SDK can unmarshal.

How it's wired (no dev-only code in the app — pure config seam, mirroring MinIO↔S3):
- the compose `scaleway-jobs-mock` service (built from the worker image) mounts this file
  and runs it as its entrypoint;
- `pizza_api` points `SCW_API_URL` at `http://scaleway-jobs-mock:8080`, so the SDK's real
  request is intercepted here instead of hitting `api.scaleway.com`.

You don't normally run it by hand — `podman compose up` starts it. To point compose at a
copy elsewhere, set `SCW_MOCK_SCRIPT` to its path. Add new job mappings in the `JOBS` dict
(the keys must match the `SCW_*_JOB_ID` values in `.env`).

### `drop_all.py` — reset the database schema

⚠️ **Destructive.** Drops the configured `PIZZA_DB_SCHEMA_NAME` schema `CASCADE` and
recreates it empty — wiping every table and row in it. Interactive: you must retype the
schema name to confirm.

```bash
uv run python scripts/drop_all.py
```

Use it to start from a clean slate locally (after which you re-run `just alembic-upgrade`).
Never run it against a database whose data you care about.

## `.env`

`scripts/.env` holds environment for running these utilities locally (DB connection, etc.).
It is git-ignored and dev-only — do not put production credentials here.
