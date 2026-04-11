"""Utility functions for the scraper."""

import pathlib

import bs4 as bs
import sqlalchemy as sa
from pizza_platform_shared import schemas, settings
from sqlalchemy import event, orm

from pizza_data_collector import (
    models,
)


def create_location_schema(
    soup: bs.BeautifulSoup, pizzeria_id: int
) -> schemas.LocationSchema:
    """Create a LocationSchema from the scraped HTML soup."""
    # Get lat/lon
    coordinates = models.coordinate_patterns.extract(
        html=str(soup),
    )
    # Get phone
    phone_number = models.phone_patterns.extract(
        html=str(soup),
    )
    # Get adress
    adress = models.adress_patterns.extract(
        html=str(soup),
    )

    return schemas.LocationSchema(
        pizzaria_id=pizzeria_id,
        adress=adress,
        city=None,
        country=None,
        latitude=coordinates[0] if coordinates else None,
        longitude=coordinates[1] if coordinates else None,
        phone=phone_number,
    )


def soup_to_file(soup: bs.BeautifulSoup, file_path: pathlib.Path) -> None:
    """Save BeautifulSoup object to an HTML file.

    :param soup: The BeautifulSoup object to save.
    :type soup: bs
    :param file_path: The path to the output HTML file.
    :type file_path: str
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(str(soup))


def get_sqlite_engine(
    db_path: pathlib.Path | None, model: orm.DeclarativeBase
) -> sa.engine.Engine:
    """Create engine with SQLite schema handling."""
    if db_path:
        url = f"sqlite:///{db_path}"
        poolclass = sa.pool.StaticPool
    else:
        url = "sqlite:///:memory:"
        poolclass = sa.pool.NullPool

    # Create engine with appropriate pool class for SQLite
    sqlite_engine = sa.create_engine(
        url,
        connect_args={"check_same_thread": False},
        poolclass=poolclass,
    )

    # Enable foreign key enforcement for SQLite
    @event.listens_for(sqlite_engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    # Remove schema for SQLite
    for table in model.metadata.tables.values():
        table.schema = None

    # Create tables
    model.metadata.create_all(bind=sqlite_engine)

    return sqlite_engine


def get_postgres_engine(db_url: str, model: orm.DeclarativeBase) -> sa.engine.Engine:
    """Create engine with PostgreSQL schema handling."""
    postgres_engine = sa.create_engine(db_url)
    schema_name = settings.pizza_db.schema_name

    # raise an error if schema does not exist
    with postgres_engine.connect() as connection:
        result = connection.execute(
            sa.text(
                f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{schema_name}'"
            )
        )
        if result.first() is None:
            raise ValueError(
                f"Schema '{schema_name}' does not exist in the PostgreSQL database."
            )

    # Create tables within the specified schema
    model.metadata.create_all(bind=postgres_engine)

    return postgres_engine


def extract_pizzeria_name(endpoint_path: str) -> str:
    """Extract pizzeria slug from URL path, stripping version suffixes like '-4'."""
    slug = endpoint_path.rstrip("/").split("/")[-1]
    if not slug:
        raise ValueError(f"Invalid pizzeria endpoint path: {endpoint_path}")

    # Strip numeric suffix (e.g., "napoli-on-the-road-4" -> "napoli-on-the-road")
    parts = slug.rsplit("-", 1)
    if len(parts) == 2 and parts[-1].isdigit():
        return parts[0]
    return slug
