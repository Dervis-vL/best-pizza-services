"""Utility functions for the scraper."""

import json
import pathlib
from venv import logger

import bs4 as bs
import yarl
from sqlalchemy import select, event, create_engine
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


def get_engine(db_url: str):
    """Create engine with SQLite schema handling."""
    engine = create_engine(db_url, echo=False)
    
    if "sqlite" in db_url:
        # SQLite doesn't support schemas - use schema translation
        # This maps 'pizza.table_name' to just 'table_name'
        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
    
    return engine