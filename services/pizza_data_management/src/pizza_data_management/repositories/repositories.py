"""Database repositories for scraper app."""

from __future__ import annotations

import logging
from typing import Any

import sqlalchemy as sa
from sqlalchemy import orm as sa_orm, select

from pizza_platform_shared.repositories.base_database import BaseDatabase
from pizza_platform_shared import settings as shared_settings

from pizza_data_management import models, schemas
from pizza_data_management.utils import extract_pizzeria_name

logger = logging.getLogger(__name__)


class RankingRepository(BaseDatabase):
    """Repository for seeding and querying categories and ranking editions.

    Handles the first phase of the scraper: writing config-driven categories
    and ranking editions to the DB, then reading back unscraped editions.

    Args:
        db_settings: Database connection settings.
    """

    def _get_read_query(self) -> sa.Select[Any]:
        """Unscraped ranking editions with their category eagerly loaded."""
        return (
            select(models.RankingEditions)
            .where(models.RankingEditions.scraped_at.is_(None))
            .options(sa_orm.joinedload(models.RankingEditions.category))
        )

    def upsert_categories_and_editions(self, config: schemas.RankingEndpointsSchema) -> None:
        """Write categories and ranking editions from config, inserting or updating."""
        with self._session() as session:
            category_map: dict[str, models.Categories] = {}

            for cat_config in config.categories:
                category = self._upsert_category(session, cat_config)
                session.flush()  # ensure id is available for FK references
                category_map[cat_config.slug] = category

            for edition_config in config.editions:
                category = category_map.get(edition_config.slug)
                if not category:
                    logger.warning("Skipping edition — category '%s' not found", edition_config.slug)
                    continue
                self._upsert_edition(session, edition_config, category)

    def get_unscraped_editions(self) -> list[models.RankingEditions]:
        """Return all ranking editions that have not yet been scraped.

        Relationships are eagerly loaded so objects remain usable after
        the session closes.
        """
        with sa_orm.Session(self._engine) as session:
            return session.execute(self._get_read_query()).scalars().all()

    def mark_edition_scraped(self, edition_id: int) -> None:
        """Set scraped_at to now for the given ranking edition."""
        with self._session() as session:
            edition = session.get(models.RankingEditions, edition_id)
            if not edition:
                raise ValueError(f"RankingEdition with id {edition_id} not found.")
            edition.scraped_at = sa.func.now()

    @staticmethod
    def _upsert_category(
        session: sa_orm.Session, cat_config: schemas.CategorySchema
    ) -> models.Categories:
        existing = session.scalar(
            select(models.Categories).where(models.Categories.slug == cat_config.slug)
        )
        if existing:
            existing.name = cat_config.name
            existing.description = cat_config.description
            return existing

        category = models.Categories(
            slug=cat_config.slug,
            name=cat_config.name,
            description=cat_config.description,
        )
        session.add(category)
        return category

    @staticmethod
    def _upsert_edition(
        session: sa_orm.Session,
        edition_config: schemas.RankedEditionSchema,
        category: models.Categories,
    ) -> models.RankingEditions:
        existing = session.scalar(
            select(models.RankingEditions).where(
                models.RankingEditions.category_id == category.id,
                models.RankingEditions.year == edition_config.year,
            )
        )
        if existing:
            existing.url = edition_config.url
            return existing

        edition = models.RankingEditions(
            category_id=category.id,
            year=edition_config.year,
            url=edition_config.url,
        )
        session.add(edition)
        return edition


class PizzeriaRepository(BaseDatabase):
    """Repository for seeding and querying pizzerias, webpages, and locations.

    Handles the second phase of the scraper: writing scraped pizzeria data
    (pizzerias, webpages, locations) and reading back what still needs scraping.

    Args:
        db_settings: Database connection settings.
    """

    def _get_read_query(self) -> sa.Select[Any]:
        """Unscraped pizzeria webpages."""
        return select(models.Webpages).where(models.Webpages.scraped_at.is_(None))

    def upsert_pizzerias_and_webpages(self, config: schemas.PizzeriaEndpointsSchema) -> None:
        """Write pizzerias and their webpages from config, inserting or updating."""
        with self._session() as session:
            pizzeria_map: dict[str, models.Pizzerias] = {}

            for pizzeria_config in config.pizzerias:
                pizzeria = self._upsert_pizzeria(session, pizzeria_config)
                session.flush()
                pizzeria_map[pizzeria_config.name] = pizzeria

            for webpage_config in config.webpages:
                name = extract_pizzeria_name(webpage_config.slug)
                pizzeria = pizzeria_map.get(name)
                if not pizzeria:
                    logger.warning(
                        "Skipping webpage — no pizzeria found for slug '%s'", webpage_config.slug
                    )
                    continue
                self._upsert_webpage(session, webpage_config, pizzeria)

    def upsert_location(self, location_config: schemas.LocationSchema) -> None:
        """Write a single pizzeria location, skipping if coordinates already exist nearby."""
        with self._session() as session:
            self._upsert_location(session, location_config)

    def get_unscraped_pizzerias(self) -> list[models.Webpages]:
        """Return all pizzeria webpages that have not yet been scraped."""
        with sa_orm.Session(self._engine) as session:
            return session.execute(self._get_read_query()).scalars().all()

    def mark_pizzeria_scraped(self, webpage_id: int) -> None:
        """Set scraped_at to now for the given pizzeria webpage."""
        with self._session() as session:
            webpage = session.get(models.Webpages, webpage_id)
            if not webpage:
                raise ValueError(f"Webpage with id {webpage_id} not found.")
            webpage.scraped_at = sa.func.now()

    @staticmethod
    def _upsert_pizzeria(
        session: sa_orm.Session, pizzeria_config: schemas.PizzeriaSchema
    ) -> models.Pizzerias:
        existing = session.scalar(
            select(models.Pizzerias).where(models.Pizzerias.name == pizzeria_config.name)
        )
        if existing:
            existing.description = pizzeria_config.description
            return existing

        pizzeria = models.Pizzerias(
            name=pizzeria_config.name,
            description=pizzeria_config.description,
        )
        session.add(pizzeria)
        return pizzeria

    @staticmethod
    def _upsert_webpage(
        session: sa_orm.Session,
        webpage_config: schemas.WebpagesSchema,
        pizzeria: models.Pizzerias,
    ) -> models.Webpages:
        existing = session.scalar(
            select(models.Webpages).where(
                models.Webpages.slug == webpage_config.slug,
                models.Webpages.pizzeria_id == pizzeria.id,
            )
        )
        if existing:
            existing.url = webpage_config.url
            return existing

        webpage = models.Webpages(
            slug=webpage_config.slug,
            url=webpage_config.url,
            pizzeria_id=pizzeria.id,
        )
        session.add(webpage)
        return webpage

    @staticmethod
    def _upsert_location(
        session: sa_orm.Session, location_config: schemas.LocationSchema
    ) -> models.Locations:
        from pizza_data_management import constants

        if location_config.has_coordinates:
            existing = session.scalar(
                select(models.Locations)
                .where(models.Locations.latitude.between(
                    location_config.latitude - constants.Coordinate.LOC_DELTA,
                    location_config.latitude + constants.Coordinate.LOC_DELTA,
                ))
                .where(models.Locations.longitude.between(
                    location_config.longitude - constants.Coordinate.LOC_DELTA,
                    location_config.longitude + constants.Coordinate.LOC_DELTA,
                ))
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
        session.add(location)
        return location
