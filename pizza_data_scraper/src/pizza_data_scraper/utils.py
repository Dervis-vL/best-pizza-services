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

from pizza_data_scraper import (
    enums,
    constants,
    schemas,
    models,
    settings,
    patterns,
)


def extract_coords(soup: bs.BeautifulSoup) -> dict | None:
    """
    Try each pattern in priority order and return the FIRST match.
    Returns {'lat': float, 'lng': float} or None if nothing found.
    """
    for pat in (patterns.PAT_JS, patterns.PAT_JSON, patterns.PAT_FALLBACK):
        m = pat.search(str(soup))
        if m:
            return {
                'lat': float(m.group('lat')),
                'lng': float(m.group('lng'))
            }
    return None



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
    category = category_map.get(edition_config.slug)
    if not category:
        raise ValueError(f"Category '{edition_config.slug}' not found")

    existing = db.scalar(
        select(models.RankingEditions).where(
            models.RankingEditions.category_id == category.id,
            models.RankingEditions.year == edition_config.year,
        )
    )

    if existing:
        existing.url = edition_config.url
        return existing
    else:
        edition = models.RankingEditions(
            category_id=category.id,
            year=edition_config.year,
            url=edition_config.url,
        )
        db.add(edition)
        return edition


def upsert_pizzeria(
    db: orm.Session,
    pizzeria_config: schemas.PizzeriaSchema
) -> models.Pizzerias:
    """Insert or update a pizzeria."""
    existing = db.scalar(select(models.Pizzerias).where(models.Pizzerias.name == pizzeria_config.name))

    if existing:
        existing.description = pizzeria_config.description
        return existing
    else:
        pizzeria = models.Pizzerias(
            name=pizzeria_config.name,
            description=pizzeria_config.description,
        )
        db.add(pizzeria)
        return pizzeria


def upsert_webpage(
    db: orm.Session,
    webpage_config: schemas.WebpagesSchema,
    pizzeria_map: dict[str, models.Pizzerias]
) -> models.Webpages:
    """Insert or update a webpage."""
    slug_to_name = extract_pizzeria_name(endpoint_path=webpage_config.slug)
    pizzeria = pizzeria_map.get(slug_to_name)
    if not pizzeria:
        raise ValueError(f"Pizzeria for slug '{webpage_config.slug}' not found")

    existing = db.scalar(
        select(models.Webpages).where(
            models.Webpages.slug == webpage_config.slug,
            models.Webpages.pizzeria_id == pizzeria.id,
        )
    )

    if existing:
        existing.url = webpage_config.url
        return existing
    else:
        webpage = models.Webpages(
            slug=webpage_config.slug,
            url=webpage_config.url,
            pizzeria_id=pizzeria.id,
        )
        db.add(webpage)
        return webpage


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
        category = category_map.get(edition_config.slug)
        if not category:
            logger.warning(
                f"Skipping edition - category '{edition_config.slug}' not found"
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


def seed_pizzeria_database(db: orm.Session, config: schemas.PizzeriaEndpointsSchema) -> dict[str, int]:
    """Seed the database with pizzeria data."""
    stats = {
        "pizzerias_created": 0,
        "pizzerias_updated": 0,
        "webpages_created": 0,
        "webpages_updated": 0,
    }

    # First pass: upsert all pizzerias
    pizzeria_map: dict[str, models.Pizzerias] = {}

    for pizzeria_config in config.pizzerias:
        existing = db.scalar(select(models.Pizzerias).where(models.Pizzerias.name == pizzeria_config.name))
        is_new = existing is None

        pizzeria = upsert_pizzeria(db, pizzeria_config)
        db.flush()  # Get ID for new pizzerias

        pizzeria_map[pizzeria_config.name] = pizzeria

        if is_new:
            stats["pizzerias_created"] += 1
        else:
            stats["pizzerias_updated"] += 1

    # Second pass: upsert all webpages
    for webpage_config in config.webpages:
        slug_to_name = extract_pizzeria_name(endpoint_path=webpage_config.slug)
        pizzeria = pizzeria_map.get(slug_to_name)
        if not pizzeria:
            logger.warning(
                f"Skipping webpage - pizzeria for slug '{webpage_config.slug}' not found"
            )
            continue

        existing = db.scalar(
            select(models.Webpages).where(
                models.Webpages.slug == webpage_config.slug,
                models.Webpages.pizzeria_id == pizzeria.id,
            )
        )
        is_new = existing is None

        upsert_webpage(db, webpage_config, pizzeria_map)

        if is_new:
            stats["webpages_created"] += 1
        else:
            stats["webpages_updated"] += 1

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
    schema_name = settings.pizza_db.schema_name

    # raise an error if schema does not exist
    with postgres_engine.connect() as connection:
        result = connection.execute(
            sa.text(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{schema_name}'")
        )
        if result.first() is None:
            raise ValueError(f"Schema '{schema_name}' does not exist in the PostgreSQL database.")

    # Create tables within the specified schema
    model.metadata.create_all(bind=postgres_engine)

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
            slug=next((c.slug for c in categories if c.id == ed.category_id), None),
            year=ed.year,
            url=ed.url,
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


def query_not_scraped_pizzerias(engine: sa.engine.Engine) -> list[models.Webpages]:
    """Lazy query the database for pizzerias that have not been scraped yet."""
    with orm.Session(engine) as session:
        return session.execute(
            select(models.Webpages).where(models.Webpages.scraped_at.is_(None))
        ).scalars().all()


def update_rankings_scraped_at(engine: sa.engine.Engine, edition_id: int) -> None:
    """Update the 'scraped_at' timestamp for a given ranking edition."""
    try:
        with orm.Session(engine) as session:
            edition = session.get(models.RankingEditions, edition_id)
            if edition:
                now = sa.func.now()
                edition.scraped_at = now
                session.commit()
            else:
                raise ValueError(f"RankingEdition with id {edition_id} not found.")
    except Exception as e:
        logger.error(f"Error updating scraped_at for edition_id {edition_id}: {e}")
        raise


def update_pizzerias_scraped_at(engine: sa.engine.Engine, pizzeria_id: int) -> None:
    """Update the 'scraped_at' timestamp for a given pizzeria."""
    try:
        with orm.Session(engine) as session:
            pizzeria = session.get(models.Webpages, pizzeria_id)
            if pizzeria:
                now = sa.func.now()
                pizzeria.scraped_at = now
                session.commit()
            else:
                raise ValueError(f"Pizzerias with id {pizzeria_id} not found.")
    except Exception as e:
        logger.error(f"Error updating scraped_at for pizzeria_id {pizzeria_id}: {e}")
        raise


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
