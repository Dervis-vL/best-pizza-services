# 🍕 Best Pizza Services

A monorepo for collecting, storing, and visualising data from the [50 Top Pizza](https://www.50toppizza.it/) world rankings. It scrapes pizzeria data across six global categories, enriches it with geolocation data, persists everything in PostgreSQL, and surfaces it through an interactive Streamlit map and a REST API.

---

## 📐 Architecture

```
best-pizza-services/
├── apps/
│   ├── pizza_app/              # Streamlit interactive map & list viewer
│   └── pizza_api/              # REST API (aggregates all services)
├── services/
│   ├── pizza_data_collector/   # Web scraper + HTML parser
│   ├── pizza_data_storage/     # PostgreSQL + S3 storage layer
│   └── geolocation/            # Nominatim reverse geocoding
├── packages/
│   └── pizza_platform_shared/  # Shared Pydantic schemas, SQLAlchemy models, DB config
└── dev/
    ├── env/                    # Docker Compose (local PostgreSQL)
    ├── ERD/                    # Entity relationship diagrams
    └── scratch/                # Experimental code
```

### Design decisions

- **Services are libraries, not deployables.** `pizza_data_collector`, `pizza_data_storage`, and `geolocation` are installable Python packages. They contain all business logic and are imported by `pizza_api` as workspace dependencies — no inter-service HTTP calls needed at this scale.
- **`pizza_api` is the single deployment target** for the backend. It wires the three service packages together and exposes REST endpoints.
- **`pizza_app`** is a standalone Streamlit frontend deployed separately. It reads directly from the database.
- **`pizza_platform_shared`** holds the shared SQLAlchemy models, Pydantic schemas, and database configuration used across services and apps.

---

## 🗂️ Components

### 🕷️ `pizza_data_collector`

Scrapes [50toppizza.it](https://www.50toppizza.it/) across six categories:

| Category slug | Region |
|---|---|
| `world` | Global top 50/100 |
| `pizza-italia` | Italy |
| `europe` | Europe |
| `usa` | United States |
| `pizza-latin-america` | Latin America |
| `pizza-asia-pacific` | Asia-Pacific |

**Two scraping passes:**
1. **Edition pages** (`/world/2024`) → ranked list of pizzerias + special awards per year
2. **Pizzeria pages** (`/referenza/pepe-in-grani`) → address, phone, GPS coordinates

Coordinates are extracted from embedded JavaScript using regex fallback chains (JS map init → JSON object → Google Maps link → generic lat/lon attributes).

---

### 🗄️ `pizza_data_storage`

Manages all persistence:

- **PostgreSQL** (via SQLAlchemy + Alembic) — stores pizzerias, editions, rankings, awards, locations, webpages
- **S3-compatible object storage** (Scaleway Cloud Storage) — archives raw HTML pages in `STANDARD` class for cost efficiency

**Database schema (`api_v1`):**

| Table | Purpose |
|---|---|
| `categories` | Pizza categories (World, Italy, USA, …) |
| `pizzerias` | Pizzeria identity records |
| `editions` | Ranking list per category + year |
| `webpages` | Individual pizzeria pages on 50toppizza.it |
| `rankings` | Ranked position per edition |
| `awards` | Special/sponsored awards per edition |
| `locations` | GPS coords, address, city, country, phone |

---

### 🌍 `geolocation`

Reverse geocodes GPS coordinates to city + country using the [Nominatim](https://nominatim.openstreetmap.org/) API (OpenStreetMap). Enforces a 1 req/s rate limit to comply with Nominatim's usage policy.

> **Attribution required:** If you display map data, include "© OpenStreetMap contributors".

---

### 📦 `pizza_platform_shared`

Shared library used across services and apps:

- **Pydantic schemas** — `PizzeriaSchema`, `LocationSchema`, `RankingSchema`, `AwardSchema`, `EditionSchema`, `CategorySchema` (plus `Read` variants with `id`, `created_at`, `updated_at`)
- **SQLAlchemy ORM models** — mirror the database schema with full `back_populates` relationships
- **`DatabaseSettings`** — reads connection config from `.env` via `pydantic-settings`, exposes `.connection_string`

---

### 🗺️ `pizza_app` (Streamlit)

Interactive viewer for the collected data:

- **Map view** — Folium map with marker clusters; clicking a marker shows a popup with rankings table
- **List view** — card-based layout
- **Sidebar filters** — year, category, special awards
- Data is cached for 5 hours per Streamlit session

Run at: `http://localhost:8501`

---

### 🔌 `pizza_api`

FastAPI application that exposes `pizza_data_collector`, `pizza_data_storage`, and `geolocation` as REST endpoints. Currently in active development.

---

## 🚀 Getting started

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) — install via:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

- A running PostgreSQL instance (see [Local database](#local-database))

### Install dependencies

```bash
# Install all workspace packages + dev dependencies
uv sync
```

### Local database

Start a PostgreSQL 16 container:

```bash
docker compose -f dev/env/compose.yaml up -d
```

Run migrations:

```bash
uv run alembic -c services/pizza_data_storage/alembic.ini upgrade head
```

### Environment variables

Copy the example and fill in your values:

```bash
cp .env.example .env
```

```env
# PostgreSQL — application
PIZZA_DB_HOST=localhost
PIZZA_DB_PORT=5432
PIZZA_DB_USER_NAME=best_pizza_user
PIZZA_DB_PASSWORD=your_password
PIZZA_DB_NAME=pizza_platform
PIZZA_DB_SCHEMA_NAME=api_v1
PIZZA_DB_SSL_ENABLED=False

# PostgreSQL — migrations (can be the same DB with a superuser)
MAINTENANCE_DB_HOST=localhost
MAINTENANCE_DB_PORT=5432
MAINTENANCE_DB_USER_NAME=best_pizza_user
MAINTENANCE_DB_PASSWORD=your_password
MAINTENANCE_DB_NAME=pizza_platform
MAINTENANCE_DB_SCHEMA_NAME=api_v1
MAINTENANCE_DB_SSL_ENABLED=False

# S3-compatible object storage (Scaleway example)
STORAGE_ENDPOINT=https://s3.fr-par.scw.cloud
STORAGE_KEY_ID=your_key_id
STORAGE_SECRET=your_secret
STORAGE_BUCKET=pizza-html
STORAGE_REGION=fr-par
```

---

## 🏃 Running the apps

### Streamlit app

```bash
uv run streamlit run apps/pizza_app/src/pizza_app/app.py
# → http://localhost:8501
```

Or via the installed script:

```bash
uv run pizza-app
```

### REST API

```bash
# (FastAPI + uvicorn — in development)
uv run uvicorn pizza_api.main:app --reload
# → http://localhost:8000
```

---

## 🧪 Testing

Run the full test suite from the workspace root:

```bash
uv run pytest
```

Run a specific service in isolation:

```bash
uv run pytest services/pizza_data_collector/
uv run pytest services/geolocation/
```

Coverage reports are written to `reports/coverage/`.

---

## 🔍 Code quality

```bash
# Lint
uv run ruff check .

# Format
uv run ruff format .

# Type checking
uv run mypy apps/ services/ packages/

# Dependency hygiene
uv run deptry .
```

---

## 🗃️ Dependency management

This repo is a [uv workspace](https://docs.astral.sh/uv/concepts/workspaces/). All members share a single lock file (`uv.lock`).

```bash
# Add a dependency to a specific package
uv add httpx --package pizza_api

# Add a dev dependency at the workspace root
uv add --dev pytest-xdist

# Upgrade all dependencies
uv lock --upgrade

# Sync after pulling changes
uv sync
```

Workspace members reference each other via `[tool.uv.sources]`:

```toml
[tool.uv.sources]
pizza-platform-shared = { workspace = true }
pizza-data-collector  = { workspace = true }
```

---

## 🗺️ Data flow

```
50toppizza.it
     │
     ▼
pizza_data_collector  ──────────────────────────────────────────┐
  • scrape edition pages (rankings + awards)                     │
  • scrape pizzeria pages (address, phone, GPS)                  │
     │                                                           │
     ▼                                                           ▼
geolocation                                           pizza_data_storage
  • GPS → city/country                                  • PostgreSQL (structured data)
  (Nominatim/OSM)                                       • S3 (raw HTML archive)
     │                                                           │
     └────────────────────────┬──────────────────────────────────┘
                              │
                   ┌──────────┴──────────┐
                   │                     │
              pizza_api            pizza_app
          (REST endpoints)    (Streamlit viewer)
```

---

## ☁️ Production

| Component | Provider |
|---|---|
| PostgreSQL | [Clever Cloud](https://www.clever-cloud.com/) |
| Object storage | [Scaleway Cloud Storage](https://www.scaleway.com/en/object-storage/) (Paris, `fr-par`) |
| FastAPI | Standalone deployment |
| Streamlit app | Standalone deployment |
