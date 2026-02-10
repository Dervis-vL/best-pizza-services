"""Utility functions for the scraper."""

import json
import pathlib
from venv import logger

import bs4 as bs
import yarl
import sqlalchemy as sa
from sqlalchemy import select, event
from sqlalchemy import orm
from bs4 import element as bs_element

from pizza_data_scraper import enums, constants, schemas, models


def create_endpoint(category: enums.Categories, year: enums.Year) -> str:
    """Create an endpoint URL based on category and year.

    :param category: The category for the endpoint.
    :type category: enums.Categories
    :param year: The year for the endpoint.
    :type year: enums.Year

    :return: The constructed endpoint URL.
    :rtype: str
    """
    endpoint_part = getattr(constants.CategoryEndpoints, category.name)
    return f"{constants.CategoryEndpoints.SELECTION_TYPE}-{endpoint_part}-{year.value}/"


def get_pizzeria_url_from_card(card: bs_element.Tag, attr: str) -> yarl.URL:
    """Get the URL from a pizzeria card element.

    :param card: The pizzeria card element.
    :type card: bs4.element.Tag
    :param attr: The attribute to extract the URL from.
    :type attr: str

    :return: The URL extracted from the card element.
    :rtype: yarl.URL
    """
    url_str = card.get(attr)
    if url_str is None:
        raise ValueError(f"The attribute '{attr}' is not found in the card element.")
    return yarl.URL(url_str)


def soup_to_file(soup: bs.BeautifulSoup, file_path: pathlib.Path) -> None:
    """Save BeautifulSoup object to an HTML file.

    :param soup: The BeautifulSoup object to save.
    :type soup: bs
    :param file_path: The path to the output HTML file.
    :type file_path: str
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(str(soup))


def load_ranking_config(config_path: pathlib.Path) -> schemas.RankingEndpointsSchema:
    """Load ranking configuration from a JSON file.

    :param config_path: The path to the configuration JSON file.
    :type config_path: pathlib.Path
    :return: The ranking endpoints configuration schema.
    :rtype: schemas.RankingEndpointsSchema
    """
    with open(config_path, "r", encoding="utf-8") as file:
        config_data = json.load(file)

    return schemas.RankingEndpointsSchema.model_validate(config_data)


def upsert_category(db: orm.Session, category_config: schemas.CategorySchema) -> models.Categories:
    """Insert or update a category."""
    existing = db.scalar(select(models.Categories).where(models.Categories.slug == category_config.slug))

    if existing:
        existing.name = category_config.name
        existing.description = category_config.description
        return existing
    else:
        category = models.Categories(
            slug=category_config.slug,
            name=category_config.name,
            description=category_config.description,
        )
        db.add(category)
        return category


def upsert_edition(
    db: orm.Session,
    edition_config: schemas.RankedEditionSchema,
    category_map: dict[str, models.Categories],
) -> models.RankingEditions:
    """Insert or update a ranking edition."""
    category = category_map.get(edition_config.category_slug)
    if not category:
        raise ValueError(f"Category '{edition_config.category_slug}' not found")

    existing = db.scalar(
        select(models.RankingEditions).where(
            models.RankingEditions.category_id == category.id,
            models.RankingEditions.year == edition_config.year,
        )
    )

    if existing:
        existing.endpoint_url = edition_config.endpoint_url
        return existing
    else:
        edition = models.RankingEditions(
            category_id=category.id,
            year=edition_config.year,
            endpoint_url=edition_config.endpoint_url,
        )
        db.add(edition)
        return edition


def seed_database(db: orm.Session, config: schemas.RankingEndpointsSchema) -> dict[str, int]:
    """Seed the database with categories and editions from config.

    Returns statistics about what was created/updated.
    """
    stats = {
        "categories_created": 0,
        "categories_updated": 0,
        "editions_created": 0,
        "editions_updated": 0,
    }

    # First pass: upsert all categories
    category_map: dict[str, models.Categories] = {}

    for cat_config in config.categories:
        existing = db.scalar(select(models.Categories).where(models.Categories.slug == cat_config.slug))
        is_new = existing is None

        category = upsert_category(db, cat_config)
        db.flush()  # Get ID for new categories

        category_map[cat_config.slug] = category

        if is_new:
            stats["categories_created"] += 1
        else:
            stats["categories_updated"] += 1

    # Second pass: upsert all editions
    for edition_config in config.editions:
        category = category_map.get(edition_config.category_slug)
        if not category:
            logger.warning(
                f"Skipping edition - category '{edition_config.category_slug}' not found"
            )
            continue

        existing = db.scalar(
            select(models.RankingEditions).where(
                models.RankingEditions.category_id == category.id,
                models.RankingEditions.year == edition_config.year,
            )
        )
        is_new = existing is None

        upsert_edition(db, edition_config, category_map)

        if is_new:
            stats["editions_created"] += 1
        else:
            stats["editions_updated"] += 1

    db.commit()
    return stats


def get_sqlite_engine(db_path: pathlib.Path | None, model: orm.DeclarativeBase) -> sa.engine.Engine:
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

    # raise an error if schema does not exist
    with postgres_engine.connect() as connection:
        result = connection.execute(
            sa.text("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'pizza_data'")
        )
        if result.first() is None:
            raise ValueError("Schema 'pizza_data' does not exist in the PostgreSQL database.")

    # Create tables within the specified schema
    model.metadata.create_all(bind=postgres_engine, schema="pizza_data")

    return postgres_engine


def read_from_db(engine: sa.engine.Engine, model: orm.DeclarativeBase, table_name: str) -> schemas.RankingEndpointsSchema:
    """Read data from the database and return it as a schema."""
    with orm.Session(engine) as session:
        categories = session.execute(select(models.Categories)).scalars().all()
        editions = session.execute(select(models.RankingEditions)).scalars().all()

    category_schemas = [
        schemas.CategorySchema(
            slug=cat.slug,
            name=cat.name,
            description=cat.description,
        )
        for cat in categories
    ]

    edition_schemas = [
        schemas.RankedEditionSchema(
            category_slug=next((c.slug for c in categories if c.id == ed.category_id), None),
            year=ed.year,
            endpoint_url=ed.endpoint_url,
        )
        for ed in editions
    ]

    return schemas.RankingEndpointsSchema(categories=category_schemas, editions=edition_schemas)


def query_not_scraped_ranking_editions(engine: sa.engine.Engine) -> list[models.RankingEditions]:
    """Eager query the database for ranking editions pages that have not been scraped yet."""
    # Eager load ranking editions and category data
    with orm.Session(engine) as session:
        return session.execute(
            select(models.RankingEditions).where(models.RankingEditions.scraped_at.is_(None)).options(
                orm.joinedload(models.RankingEditions.category)
            )
        ).scalars().all()
