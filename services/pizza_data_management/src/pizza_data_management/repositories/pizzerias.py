"""Database repository for ranking categories and editions."""

from __future__ import annotations

import logging
from typing import Any

import sqlalchemy as sa
from sqlalchemy import orm as sa_orm, select

from pizza_platform_shared.repositories.base_database import BaseDatabase

from pizza_data_management import constants, models, schemas
from pizza_data_management.utils import extract_pizzeria_name

logger = logging.getLogger(__name__)

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
            webpage.scraped_at = sa.func.now()  # pylint: disable=not-callable

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
        """Upsert a pizzeria location, skipping if coordinates already exist nearby."""
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
