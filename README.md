[![CI](https://github.com/Dervis-vL/best-pizza-services/actions/workflows/ci.yml/badge.svg)](https://github.com/Dervis-vL/best-pizza-services/actions/workflows/ci.yml)  ![Python](https://img.shields.io/badge/python-3.14-blue)  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)  [![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

# Best Pizza Services

A monorepo that collects, stores, and visualises pizzeria data from the [50 Top Pizza](https://www.50toppizza.it/) world rankings.

This README is for **developers, testers, contributors, and people studying the code or wanting to fork it**. For user-facing documentation, see the READMEs inside `apps/`.

---

## Quick start

### Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) — `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [Podman](https://podman.io/) with Podman Compose (or Docker Compose)
- [just](https://just.systems/)

### Setup

```bash
just setup
```

Installs all workspace dependencies, installs pre-commit hooks, and creates a `.env` from `.env.example` if one does not already exist. Edit `.env` with your credentials before starting the stack.

### Run the full stack

```bash
just compose        # builds and starts PostgreSQL, MinIO, pizza_api, pizza_app
just compose down   # stops and removes the containers
```

After startup:

| Service | URL |
|---|---|
| REST API | http://localhost:8000 |
| Streamlit app | http://localhost:8501 |
| MinIO console | http://localhost:9001 |

### Apply database migrations

```bash
just alembic-upgrade
```

---

## Workspace layout

```
best-pizza-services/
├── apps/
│   ├── pizza_api/              # FastAPI REST API (deployable)
│   └── pizza_app/              # Streamlit viewer (deployable)
├── services/
│   ├── pizza_data_collector/   # Web scraper + HTML parser (library)
│   ├── pizza_data_storage/     # PostgreSQL + S3 storage layer (library)
│   └── geolocation/            # Nominatim reverse geocoding (library)
├── packages/
│   └── pizza_platform_shared/  # Shared Pydantic schemas, SQLAlchemy models, DB config
├── just/                       # Modular justfile recipes
├── dev/                        # ERDs and scratch files
└── compose.yaml                # Full-stack local environment
```

**Services are libraries, not deployables.** `pizza_data_collector`, `pizza_data_storage`, and `geolocation` contain all business logic and are imported by `pizza_api` as workspace dependencies — no inter-service HTTP calls.

`pizza_api` and `pizza_app` are the two deployment targets and each has its own `Dockerfile` and `README.md`.

---

## Projects

### `apps/pizza_api`

FastAPI application. Wires the three service libraries together and exposes REST endpoints for scraping, storage, and querying. Uses a **factory pattern** to build the shared database engine on startup, which is then provided to request handlers via FastAPI's dependency injection layer.

### `apps/pizza_app`

Streamlit interactive viewer. Reads from the API and displays pizzerias on a Folium map and in a card list, with sidebar filters for year, category, and awards. Data is cached per session.

### `services/pizza_data_collector`

Web scraper and HTML parser for [50toppizza.it](https://www.50toppizza.it/). Two scraping passes: edition pages (ranked lists + special awards) and individual pizzeria pages (address, phone, GPS coordinates).

### `services/pizza_data_storage`

Persistence layer. Manages writes and reads to PostgreSQL via SQLAlchemy and archives raw HTML to S3-compatible storage (MinIO locally, Scaleway in production). Alembic is configured here and migrations live in `alembic/`.

### `services/geolocation`

Reverse geocodes GPS coordinates to city and country via the [Nominatim](https://nominatim.openstreetmap.org/) API (OpenStreetMap). Enforces a 1 req/s rate limit to comply with Nominatim's usage policy. If you display map data, attribution to OpenStreetMap contributors is required.

### `packages/pizza_platform_shared`

Shared library used across all services and apps:

- **Pydantic schemas** — `PizzeriaSchema`, `LocationSchema`, `RankingSchema`, `AwardSchema`, `EditionSchema`, `CategorySchema` (plus `Read` variants with `id`, `created_at`, `updated_at`)
- **SQLAlchemy ORM models** — mirror the database schema with full `back_populates` relationships
- **`DatabaseSettings`** — reads connection config from `.env` via `pydantic-settings`, exposes `.connection_string`

---

## Data model

<!-- ERD goes here -->

| Table | Purpose |
|---|---|
| `categories` | Pizza categories (World, Italy, Europe, USA, Latin America, Asia-Pacific) |
| `pizzerias` | Pizzeria identity records |
| `editions` | Ranking list per category + year |
| `webpages` | Individual pizzeria pages on 50toppizza.it |
| `rankings` | Ranked position of a pizzeria within an edition |
| `awards` | Special awards per edition |
| `locations` | GPS coordinates, address, city, country, phone |

All tables live in the `api_v1` schema. The schema name is configurable via `PIZZA_DB_SCHEMA_NAME`.

---

## Architecture

### Hexagonal architecture (ports & adapters)

All three service libraries follow hexagonal architecture. The `application/` layer defines abstract **ports** (interfaces). Concrete **adapters** live outside it and implement those interfaces:

```
service/
├── application/
│   ├── ports/          # Abstract interfaces (e.g. HttpClient, PizzeriaRepository)
│   └── use_cases/      # Orchestration logic — depends only on ports, never on adapters
├── scrapers/           # Adapter: HTTP client implementation
├── parsers/            # Adapter: HTML parsing implementation
└── repositories/       # Adapter: SQLAlchemy / S3 implementations
```

This keeps business logic free of framework and infrastructure concerns. Swapping an adapter (e.g. replacing the HTTP client or storage backend) requires no changes to use cases.

### Repository pattern

`pizza_data_storage` defines repository ports in `application/ports/` (`PizzeriaRepository`, `HtmlRepository`, `RankingRepository`) and ships concrete implementations in `repositories/` (SQLAlchemy for the database, S3 client for HTML archives). The API injects the correct implementation via its `dependencies/` module.

### Factory pattern (`pizza_api`)

The API's `main.py` uses a `create_engine()` factory to build the shared database engine once at startup and attaches it to `app.state`. The engine is never constructed at import time — only when the application starts.

### Dependency injection (`pizza_api`)

The `dependencies/` module forms a typed DI chain built on FastAPI's `Depends`. Each layer is exposed as an `Annotated` type alias so router handlers declare what they need and FastAPI resolves the graph:

```
app.state.engine  →  EngineDep
EngineDep         →  PizzeriaRepoDep / RankingRepoDep / HtmlRepoDep
PizzeriaRepoDep   →  ReadPizzeriasUCDep
```

Routers import only the leaf alias (e.g. `ReadPizzeriasUCDep`) and never touch engine construction or repository wiring directly. This means the infrastructure can be swapped without touching any router.

---

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3.14 |
| Package / workspace manager | [uv](https://docs.astral.sh/uv/) |
| Task runner | [just](https://just.systems/) |
| API framework | FastAPI + uvicorn |
| Frontend | Streamlit + Folium |
| ORM | SQLAlchemy 2.x |
| Migrations | Alembic |
| Validation | Pydantic v2 |
| Database | PostgreSQL 16 |
| Object storage | MinIO (local) / Scaleway S3 (production) |
| Containers | Podman + Podman Compose |
| Container registry | GHCR (`ghcr.io/dervis-vl`) |

---

## Dev toolchain

### Dev dependencies (workspace root)

| Tool | Purpose |
|---|---|
| `pytest` + `pytest-asyncio` | Testing with async support |
| `pytest-cov` | Coverage reporting |
| `pytest-xdist` | Parallel test execution |
| `mypy` | Static type checking (strict mode) |
| `ruff` | Linting and formatting |
| `deptry` | Unused / missing dependency detection |
| `pre-commit` | Git hook runner |
| `codespell` | Spell checking |
| `hypothesis` | Property-based testing |
| `bump-my-version` | Version management |

### Common `just` recipes

```bash
just setup            # Install deps, hooks, create .env
just compose          # Start full stack (postgres, minio, api, app)
just compose down     # Stop full stack
just test             # Run the full test suite (parallel)
just check            # Run everything: fmt, typecheck, lint, deps-check, spell, test, version
just fmt              # Auto-format and fix safe lint issues
just typecheck        # mypy strict on all packages
just lint             # ruff check
just alembic-upgrade  # Apply pending migrations
just build            # Build both container images
```

Run `just` with no arguments to list all available recipes.

---

## uv workspace

The repo is a [uv workspace](https://docs.astral.sh/uv/concepts/workspaces/). A single `uv.lock` covers all members. Workspace members reference each other via `[tool.uv.sources]` in their own `pyproject.toml`:

```toml
[tool.uv.sources]
pizza-platform-shared = { workspace = true }
pizza-data-collector  = { workspace = true }
```

Useful commands:

```bash
uv add httpx --package pizza_api   # Add a dep to a specific package
uv add --dev pytest-xdist          # Add a dev dep at the workspace root
uv lock --upgrade                  # Upgrade all deps
uv sync                            # Sync after pulling changes
```

---

## CI

GitHub Actions runs on every push. The pipeline runs the full `just check` suite: formatting, type checking, linting, dependency hygiene, spell checking, tests, and version consistency. See `.github/workflows/ci.yml`.

---

## Production

| Component | Provider |
|---|---|
| PostgreSQL | Clever Cloud |
| Object storage | Scaleway Cloud Storage (Paris, `fr-par`) |
| Container images | GHCR (`ghcr.io/dervis-vl`) |
