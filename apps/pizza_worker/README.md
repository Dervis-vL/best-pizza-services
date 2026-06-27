# pizza-worker

Background batch worker for the pizza platform. Runs the long-running scrape + parse
pipelines that don't fit inside a synchronous HTTP request, deployed as a
[Scaleway Serverless Job](https://www.scaleway.com/en/serverless-jobs/).

The `pizza_api` endpoints no longer execute these pipelines themselves — they validate
input, persist it, **trigger a worker run**, and return `202 Accepted`. The worker then
does the work where there is no request timeout.

## Why this exists

`POST /categories/` and `POST /maintenance/all` each run a full pipeline
(scrape editions → parse editions → scrape pizzeria webpages → parse webpages → enrich
geolocation). Across hundreds of pizzerias these take many minutes — longer than the
Scaleway Functions request limit, which caused `504 activator request timeout`. Moving
the pipelines into a run-to-completion Job removes the timeout entirely.

## Modes

The worker is a [Typer](https://typer.tiangolo.com/) CLI with one subcommand per job mode:

| Command | Use case | Triggered by |
|---|---|---|
| `pizza-worker run-pending` | `ProcessPendingUseCase` — scrape + parse everything still pending | `POST /maintenance/all` |
| `pizza-worker add-category --payload-id <id>` | `AddCategoryUseCase` — seed new categories/editions, then run the full pipeline | `POST /categories/` |

`--payload-id` / `--limit` can also be supplied via env vars (`WORKER_PAYLOAD_ID`,
`WORKER_LIMIT`) so Scaleway can pass them as per-run overrides.

## How `add-category` receives its payload

The category/edition JSON cannot be "passed as a dict" — the API and the worker are
separate processes started at different times, with no shared memory. Instead the payload
is handed off through a **staging table** (claim-check pattern):

```
API:    validate CategoryCreateRequest  →  insert row into category_payload_staging (JSONB)
        →  trigger worker run with the row's integer id  →  202 { job_run_id, payload_id }

Worker: read payload by id  →  AddCategoryUseCase.execute(...)  →  mark row status=consumed
```

Only a single integer (`payload_id`) crosses the process boundary. The row is retained as
history — `status` flips `pending → consumed | failed`, with `created_at` / `consumed_at`
timestamps — so submitted ingestions stay queryable in Postgres. The staging model,
migration, and repository live in `services/pizza_data_storage`.

## Architecture

In hexagonal terms the worker is a second **driving (primary) adapter** for the same core
use cases the API used to call directly — it adds no new ports and does not change the
collector. It owns its composition root and a dedicated database engine.

```
src/pizza_worker/
├── __main__.py         # python -m pizza_worker → cli.app()
├── cli.py              # Driving adapter: Typer subcommands (run-pending, add-category)
├── engine.py          # create_worker_engine() — NullPool + pool_pre_ping (hardcoded)
├── runner.py          # Composition root: build_process_pending_uc / build_add_category_uc
├── settings.py        # WorkerSettings (pydantic-settings)
└── application/
    ├── results.py      # Dataclasses returned by use cases
    └── use_cases/      # ProcessPending, AddCategory, scrape_*, parse_*
```

### Database engine — `NullPool`

Unlike the API (a long-lived server with a `QueuePool`), the worker is a single-shot
process: it opens a connection, does the work, and exits. It therefore uses a **fixed,
non-pooled** topology — `poolclass=NullPool, pool_pre_ping=True` — hardcoded in
`engine.py`, not exposed as an env var. `NullPool` avoids holding/leaking connections
across a short-lived run; `pool_pre_ping` guards against a stale connection if the run sat
queued or the database bounced.

## Configuration

Settings are loaded from environment variables with the `WORKER_` prefix (and optionally a
`.env` file). Database and object-storage connections come from `pizza_platform_shared`
settings (same env vars as the API).

| Variable | Default | Description |
|----------|---------|-------------|
| `WORKER_LIMIT` | _(none)_ | Optional cap on items processed per `run-pending` invocation |
| `WORKER_PAYLOAD_ID` | _(none)_ | Staging-table row id consumed by `add-category` |
| `SCRAPER_MAX_ATTEMPTS` | `4` | Retry attempts for transient upstream 5xx / timeouts |
| `SCRAPER_TIMEOUT` | `10` | Per-request scrape timeout (seconds) |

## Development

Run a mode locally against the compose stack (Postgres + MinIO must be up):

```bash
uv sync
uv run pizza-worker run-pending
uv run pizza-worker add-category --payload-id 1
```

Or through compose — the worker is an on-demand service under the `worker` profile, so it
does not start with `just compose`:

```bash
podman compose run --rm pizza_worker                              # run-pending (default)
podman compose run --rm pizza_worker add-category --payload-id 1
```

## Docker

```bash
# Build (context is the repo root — this is a uv workspace member)
podman build -f apps/pizza_worker/Dockerfile -t pizza-worker .

# Run a mode
podman run --rm --env-file .env pizza-worker run-pending
```

The image uses `ENTRYPOINT ["pizza-worker"]` with a default `CMD ["run-pending"]`, so the
subcommand can be overridden per run — which is how the API selects the mode via the
Scaleway Jobs API. It runs as a non-root user.

## Production

Deployed as a **Scaleway Serverless Job**. The image is published to the container
registry, a Job Definition points at it, and `pizza_api` starts runs on demand via the
Scaleway Jobs API — overriding the command (`run-pending` vs `add-category`) and env
(`WORKER_PAYLOAD_ID`) per run. No HTTP request waits for the pipeline, so there is no
request timeout in the path.
