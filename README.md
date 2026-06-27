[![CI](https://github.com/Dervis-vL/best-pizza-services/actions/workflows/ci.yml/badge.svg)](https://github.com/Dervis-vL/best-pizza-services/actions/workflows/ci.yml)  ![Python](https://img.shields.io/badge/python-3.14-blue)  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)  [![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

## Table of Content

- [1. Best Pizza Services](#1-best-pizza-services)
  - [1.1. Quick start](#11-quick-start)
    - [1.1.1. Prerequisites](#111-prerequisites)
    - [1.1.2. Setup](#112-setup)
    - [1.1.3. Run the full stack](#113-run-the-full-stack)
  - [1.2. Workspace layout](#12-workspace-layout)
  - [1.3. Projects](#13-projects)
    - [1.3.1. `apps/pizza_api`](#131-appspizza_api)
    - [1.3.2. `apps/pizza_app`](#132-appspizza_app)
    - [1.3.3. `apps/pizza_worker`](#133-appspizza_worker)
    - [1.3.4. `services/pizza_data_collector`](#134-servicespizza_data_collector)
    - [1.3.5. `services/pizza_data_storage`](#135-servicespizza_data_storage)
    - [1.3.6. `services/geolocation`](#136-servicesgeolocation)
    - [1.3.7. `packages/pizza_platform_shared`](#137-packagespizza_platform_shared)
  - [1.4. Data model](#14-data-model)
  - [1.5. Architecture](#15-architecture)
    - [1.5.1. Hexagonal architecture (ports \& adapters)](#151-hexagonal-architecture-ports--adapters)
    - [1.5.2. Repository pattern](#152-repository-pattern)
    - [1.5.3. Factory pattern (`pizza_api`)](#153-factory-pattern-pizza_api)
    - [1.5.4. Dependency injection (`pizza_api`)](#154-dependency-injection-pizza_api)
  - [1.6. Tech stack](#16-tech-stack)
  - [1.7. Dev toolchain](#17-dev-toolchain)
    - [1.7.1. Dev dependencies (workspace root)](#171-dev-dependencies-workspace-root)
    - [1.7.2. Common `just` recipes](#172-common-just-recipes)
    - [1.7.3. Apply database migrations (dev)](#173-apply-database-migrations-dev)
  - [1.8. uv workspace](#18-uv-workspace)
  - [1.9. CI](#19-ci)
  - [1.10. Production](#110-production)
    - [1.10.1. Apply database migrations (production)](#1101-apply-database-migrations-production)

# 1. Best Pizza Services

A monorepo that collects, stores, and visualises pizzeria data from the [50 Top Pizza](https://www.50toppizza.it/) world rankings.

This README is for **developers, testers, contributors, and people studying the code or wanting to fork it**. For user-facing documentation, see the READMEs inside `apps/`.

---

## 1.1. Quick start

### 1.1.1. Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) — `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [Podman](https://podman.io/) with Podman Compose (or Docker Compose)
- [just](https://just.systems/)
- [Trivy](https://trivy.dev/) — only needed for security checks (`just security`)

### 1.1.2. Setup

```bash
just setup
```

Installs all workspace dependencies, installs pre-commit hooks, and creates a `.env` from `.env.example` if one does not already exist. Edit `.env` with your credentials before starting the stack.

### 1.1.3. Run the full stack

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

`pizza_worker` is a run-to-completion batch job, not a long-running service, so it is
**not** started by `just compose`. It lives under the `worker` compose profile and is
invoked on demand once the stack is up:

```bash
podman compose run --rm pizza_worker                              # scrape + parse pending
podman compose run --rm pizza_worker add-category --payload-id 1  # ingest a staged payload
```

Apply database migrations after the stack is up — see
[1.7.3](#173-apply-database-migrations-dev) for dev and
[1.10.1](#1101-apply-database-migrations-production) for production.

---

## 1.2. Workspace layout

```
best-pizza-services/
├── apps/
│   ├── pizza_api/              # FastAPI REST API (deployable)
│   ├── pizza_app/              # Streamlit viewer (deployable)
│   └── pizza_worker/           # Batch worker — runs the scrape + parse pipelines (deployable)
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

**Services are libraries, not deployables.** `pizza_data_collector`, `pizza_data_storage`, and `geolocation` contain all business logic and are imported by `pizza_api` and `pizza_worker` as workspace dependencies — no inter-service HTTP calls.

`pizza_api`, `pizza_app`, and `pizza_worker` are the three deployment targets and each has its own `Dockerfile` and `README.md`. The API and worker share the same service libraries: the API serves HTTP and triggers work, while the worker runs the long pipelines off the request path.

---

## 1.3. Projects

### 1.3.1. `apps/pizza_api`

FastAPI application. Wires the three service libraries together and exposes REST endpoints for scraping, storage, and querying. Uses a **factory pattern** to build the shared database engine on startup, which is then provided to request handlers via FastAPI's dependency injection layer.

### 1.3.2. `apps/pizza_app`

Streamlit interactive viewer. Reads from the API and displays pizzerias on a Folium map and in a card list, with sidebar filters for year, category, and awards. Data is cached per session.

### 1.3.3. `apps/pizza_worker`

Background batch worker that runs the long scrape + parse pipelines off the HTTP request path, deployed as a [Scaleway Serverless Job](https://www.scaleway.com/en/serverless-jobs/). A [Typer](https://typer.tiangolo.com/) CLI with two modes: `run-pending` (scrape + parse everything still pending, behind `POST /maintenance/all`) and `add-category` (seed staged categories/editions, then run the full pipeline, behind `POST /categories/`). The API triggers a worker run and returns `202` instead of executing the pipeline synchronously, which removes the request timeout that long runs used to hit. See its [README](apps/pizza_worker/README.md) for the staging-table payload hand-off and the dedicated `NullPool` engine.

### 1.3.4. `services/pizza_data_collector`

Web scraper and HTML parser for [50toppizza.it](https://www.50toppizza.it/). Two scraping passes: edition pages (ranked lists + special awards) and individual pizzeria pages (address, phone, GPS coordinates). The HTTP client retries transient upstream failures (5xx / timeouts) with exponential backoff, configurable via `SCRAPER_*` env vars.

### 1.3.5. `services/pizza_data_storage`

Persistence layer. Manages writes and reads to PostgreSQL via SQLAlchemy and archives raw HTML to S3-compatible storage (MinIO locally, Scaleway in production). Also owns the `category_payload_staging` table that hands `add-category` payloads from the API to the worker. Alembic is configured here and migrations live in `alembic/`.

### 1.3.6. `services/geolocation`

Reverse geocodes GPS coordinates to city and country via the [Nominatim](https://nominatim.openstreetmap.org/) API (OpenStreetMap). Enforces a 1 req/s rate limit to comply with Nominatim's usage policy. If you display map data, attribution to OpenStreetMap contributors is required.

### 1.3.7. `packages/pizza_platform_shared`

Shared library used across all services and apps:

- **Pydantic schemas** — `PizzeriaSchema`, `LocationSchema`, `RankingSchema`, `AwardSchema`, `EditionSchema`, `CategorySchema` (plus `Read` variants with `id`, `created_at`, `updated_at`)
- **SQLAlchemy ORM models** — mirror the database schema with full `back_populates` relationships
- **`DatabaseSettings`** — reads connection config from `.env` via `pydantic-settings`, exposes `.connection_string`

---

## 1.4. Data model

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

## 1.5. Architecture

### 1.5.1. Hexagonal architecture (ports & adapters)

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

### 1.5.2. Repository pattern

`pizza_data_storage` defines repository ports in `application/ports/` (`PizzeriaRepository`, `HtmlRepository`, `RankingRepository`) and ships concrete implementations in `repositories/` (SQLAlchemy for the database, S3 client for HTML archives). The API injects the correct implementation via its `dependencies/` module.

### 1.5.3. Factory pattern (`pizza_api`)

The API's `main.py` uses a `create_engine()` factory to build the shared database engine once at startup and attaches it to `app.state`. The engine is never constructed at import time — only when the application starts.

### 1.5.4. Dependency injection (`pizza_api`)

The `dependencies/` module forms a typed DI chain built on FastAPI's `Depends`. Each layer is exposed as an `Annotated` type alias so router handlers declare what they need and FastAPI resolves the graph:

```
app.state.engine  →  EngineDep
EngineDep         →  PizzeriaRepoDep / RankingRepoDep / HtmlRepoDep
PizzeriaRepoDep   →  ReadPizzeriasUCDep
```

Routers import only the leaf alias (e.g. `ReadPizzeriasUCDep`) and never touch engine construction or repository wiring directly. This means the infrastructure can be swapped without touching any router.

---

## 1.6. Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3.14 |
| Package / workspace manager | [uv](https://docs.astral.sh/uv/) |
| Task runner | [just](https://just.systems/) |
| API framework | FastAPI + uvicorn |
| Frontend | Streamlit + Folium |
| Worker CLI | [Typer](https://typer.tiangolo.com/) |
| Background jobs | Scaleway Serverless Jobs |
| ORM | SQLAlchemy 2.x |
| Migrations | Alembic |
| Validation | Pydantic v2 |
| Database | PostgreSQL 16 |
| Object storage | MinIO (local) / Scaleway S3 (production) |
| Containers | Podman + Podman Compose |
| Container registry | GHCR (`ghcr.io/dervis-vl`) |

---

## 1.7. Dev toolchain

### 1.7.1. Dev dependencies (workspace root)

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

### 1.7.2. Common `just` recipes

```bash
just setup                       # Install deps, hooks, create .env
just compose                     # Start full stack (postgres, minio, api, app)
just compose down                # Stop full stack
just test                        # Run the full test suite (parallel)
just check                       # Run everything: fmt, typecheck, lint, deps-check, spell, test, version
just fmt                         # Auto-format and fix safe lint issues
just typecheck                   # mypy strict on all packages
just lint                        # ruff check
just alembic-upgrade             # Apply pending migrations (loads .env by default)
just alembic-upgrade .env.local  # Apply migrations against the env in .env.local (see Production)
just alembic-revision "message"  # Generate a new migration revision
just build                       # Build all container images (api, app, worker)
```

Run `just` with no arguments to list all available recipes.

### 1.7.3. Apply database migrations (dev)

With the local stack running (`just compose`), apply pending migrations against the
compose database, which is loaded from `.env`:

```bash
just alembic-upgrade
```

`just alembic-upgrade` runs Alembic from your host against the Postgres container (the `db`
service publishes port 5432 for exactly this). For migrating a real environment, see
[Production](#1101-apply-database-migrations-production).

---

## 1.8. uv workspace

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

## 1.9. CI

GitHub Actions runs on every push. The pipeline runs the full `just check` suite: formatting, type checking, linting, dependency hygiene, spell checking, tests, and version consistency. See `.github/workflows/ci.yml`.

---

## 1.10. Production

| Component | Provider |
|---|---|
| REST API (`pizza_api`) | Scaleway Serverless Functions (Paris, `fr-par`) |
| Viewer (`pizza_app`) | Streamlit Community Cloud |
| Batch worker (`pizza_worker`) | Scaleway Serverless Jobs (Paris, `fr-par`) |
| PostgreSQL | Clever Cloud |
| Object storage | Scaleway Cloud Storage (Paris, `fr-par`) |
| Container images | GHCR (`ghcr.io/dervis-vl`) |

The API runs as a Serverless Function and handles HTTP only. Long pipelines
(`POST /categories/`, `POST /maintenance/all`) are not executed in the request — the API
validates input, stages it, and triggers a `pizza_worker` run via the Scaleway Jobs API,
returning `202`. The worker runs to completion as a Job with no request timeout. See the
[worker README](apps/pizza_worker/README.md) for the trigger flow and staging-table
hand-off.

### 1.10.1. Apply database migrations (production)

Production migrations are run from your host against the live database, using a separate
dotenv that holds the real production connection variables. Keep these in `.env.local`
(git-ignored) — **never** commit production credentials — and pass that file to the recipe:

```bash
just alembic-upgrade .env.local
```

The `alembic-upgrade` recipe sources the dotenv you pass (defaulting to `.env` for dev) and
runs `alembic upgrade head` against whatever database those variables point at. Run this
after publishing a new image and before/with the corresponding worker or API release so
the schema matches the deployed code.
