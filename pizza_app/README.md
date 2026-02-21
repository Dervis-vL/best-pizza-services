# pizza_app

A Streamlit app that displays the world's best pizzerias on an interactive map, sourced from [50 Top Pizza](https://www.50toppizza.it/) rankings.

## Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) package manager
- A running PostgreSQL instance populated by the other services in this monorepo

## Setup

Install dependencies:

```bash
uv sync
```

Create a `.env` file in this directory with your database connection details:

```env
PIZZA_DB_HOST=localhost
PIZZA_DB_PORT=5432
PIZZA_DB_USERNAME=your_user
PIZZA_DB_PASSWORD=your_password
PIZZA_DB_DATABASE_NAME=pizza_platform
PIZZA_DB_SCHEMA_NAME=api_v1
PIZZA_DB_SSL_ENABLED=False
```

## Running

```bash
uv run streamlit run src/pizza_app/app.py
```

The app will be available at `http://localhost:8501`.

## Stack

| Library | Purpose |
|---|---|
| [Streamlit](https://streamlit.io/) | Web app framework |
| [Folium](https://python-visualization.github.io/folium/) | Interactive map rendering |
| [streamlit-folium](https://folium.streamlit.app/) | Folium integration for Streamlit |
| [SQLAlchemy](https://www.sqlalchemy.org/) | Database access |
| [Pydantic](https://docs.pydantic.dev/) | Settings and data validation |

## Development

Run the linter and type checker:

```bash
uv run ruff check src/
uv run mypy src/
```

Run tests:

```bash
uv run pytest
```
