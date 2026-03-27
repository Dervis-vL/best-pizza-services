"""Utility functions for the scraper."""

import json
import pathlib
from venv import logger

import bs4 as bs
import sqlalchemy as sa
from pizza_platform_shared import schemas as shared_schemas
from sqlalchemy import event, orm, select

from pizza_data_storage import (
    constants,
    models,
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


def load_ranking_config(
    config_path: pathlib.Path,
) -> shared_schemas.RankingEndpointsSchema:
    """Load ranking configuration from a JSON file.

    :param config_path: The path to the configuration JSON file.
    :type config_path: pathlib.Path
    :return: The ranking endpoints configuration schema.
    :rtype: schemas.RankingEndpointsSchema
    """
    with open(config_path, "r", encoding="utf-8") as file:
        config_data = json.load(file)

    return shared_schemas.RankingEndpointsSchema.model_validate(config_data)


def upsert_category(
    db: orm.Session, category_config: shared_schemas.CategorySchema
) -> models.Categories:
    """Insert or update a category."""
    existing = db.scalar(
        select(models.Categories).where(models.Categories.slug == category_config.slug)
    )

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
    edition_config: shared_schemas.RankedEditionSchema,
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
    db: orm.Session, pizzeria_config: shared_schemas.PizzeriaSchema
) -> models.Pizzerias:
    """Insert or update a pizzeria."""
    existing = db.scalar(
        select(models.Pizzerias).where(models.Pizzerias.name == pizzeria_config.name)
    )

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


def upsert_location(
    db: orm.Session, location_config: shared_schemas.LocationSchema
) -> models.Locations:
    """Insert or update a pizzeria location."""
    if location_config.has_coordinates:
        existing = db.scalar(
            select(models.Locations)
            .where(
                models.Locations.latitude.between(
                    location_config.latitude - constants.Coordinate.LOC_DELTA,
                    location_config.latitude + constants.Coordinate.LOC_DELTA,
                )
            )
            .where(
                models.Locations.longitude.between(
                    location_config.longitude - constants.Coordinate.LOC_DELTA,
                    location_config.longitude + constants.Coordinate.LOC_DELTA,
                )
            )
        )

        if existing:
            return existing

    location = models.Locations(
        pizzeria_id=location_config.pizzaria_id,
        adress=location_config.adress,
        city=location_config.city,
        country=location_config.country,
        latitude=location_config.latitude,
        longitude=location_config.longitude,
        phone=location_config.phone,
    )
    db.add(location)
    return location


def upsert_webpage(
    db: orm.Session,
    webpage_config: shared_schemas.WebpagesSchema,
    pizzeria_map: dict[str, models.Pizzerias],
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


def seed_database(
    db: orm.Session, config: shared_schemas.RankingEndpointsSchema
) -> dict[str, int]:
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
        existing = db.scalar(
            select(models.Categories).where(models.Categories.slug == cat_config.slug)
        )
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
                "Skipping edition - category '%s' not found", edition_config.slug
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


def seed_pizzeria_database(
    db: orm.Session, config: shared_schemas.PizzeriaEndpointsSchema
) -> dict[str, int]:
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
        existing = db.scalar(
            select(models.Pizzerias).where(
                models.Pizzerias.name == pizzeria_config.name
            )
        )
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
                "Skipping webpage - pizzeria for slug '%s' not found",
                webpage_config.slug,
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


def seed_location_database(
    db: orm.Session, config: shared_schemas.LocationSchema
) -> None:
    """Seed the database with pizzeria location data."""
    stats = {
        "locations_created": 0,
        "locations_updated": 0,
    }

    # upsert all pizzerias
    existing = db.scalar(
        select(models.Locations).where(
            models.Locations.pizzeria_id == config.pizzaria_id
        )
    )
    is_new = existing is None

    upsert_location(db, config)
    db.flush()  # Get ID for new Location

    if is_new:
        stats["locations_created"] += 1
    else:
        stats["locations_updated"] += 1

    db.commit()
    return stats


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
    def set_sqlite_pragma(dbapi_connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    # Remove schema for SQLite
    for table in model.metadata.tables.values():
        table.schema = None

    # Create tables
    model.metadata.create_all(bind=sqlite_engine)

    return sqlite_engine
