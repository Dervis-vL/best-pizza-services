# pizza-api

FastAPI service for managing pizza shop rankings. Seeds categories, scrapes ranking pages and pizzeria websites, parses structured data, and enriches results with geolocation.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/categories/` | Add new categories and run a full scrape + parse cycle |
| `POST` | `/maintenance/all` | Re-run scrape + parse for all pending items |

### `POST /categories/`

Seeds new categories and editions, then runs the full pipeline: scrape editions → parse editions → scrape pizzeria webpages → parse webpages → enrich with geolocation.

**Request body:**
```json
{
  "categories": [
    { "...": "CategorySchema fields" }
  ]
}
```

**Response:**
```json
{
  "editions_scraped":  { "scraped": 0, "failed": 0 },
  "editions_parsed":   { "parsed": 0, "skipped": 0, "failed": 0 },
  "webpages_scraped":  { "scraped": 0, "failed": 0 },
  "webpages_parsed":   { "parsed": 0, "skipped": 0, "failed": 0 },
  "warnings": []
}
```

### `POST /maintenance/all`

Processes items already in the database that haven't been scraped or parsed yet. Same response shape as above.

## Configuration

Settings are loaded from environment variables with the `PIZZA_API_` prefix (and optionally a `.env` file).

| Variable | Default | Description |
|----------|---------|-------------|
| `PIZZA_API_TITLE` | `Best Pizza API` | OpenAPI title |
| `PIZZA_API_DEBUG` | `false` | Enable debug mode |

Database connection is configured via `pizza_platform_shared` settings (see the shared package for its env vars).

## Development

From the repo root:

```bash
uv sync
uvicorn pizza_api.main:app --reload --host 0.0.0.0 --port 8000
```

Interactive docs are available at `http://localhost:8000/docs`.

## Docker

```bash
# Build
docker build -t pizza-api apps/pizza_api/

# Run
docker run -p 8000:8000 --env-file .env pizza-api
```

The image runs as a non-root user on port 8000.

## Architecture

The app uses a layered architecture:

```
routers/          HTTP layer — request parsing, response construction
dependencies/     Wires repositories and use cases via FastAPI DI
application/
  use_cases/      Business logic — one class per operation
  results.py      Dataclasses returned by use cases
schemas/          Pydantic request/response models
settings/         Pydantic-settings configuration
```

The SQLAlchemy engine is created on startup, stored in `app.state`, and request-scoped repositories are built per-request via dependency injection.

Warnings emitted during a pipeline run are captured and surfaced in the response body rather than silently dropped.
