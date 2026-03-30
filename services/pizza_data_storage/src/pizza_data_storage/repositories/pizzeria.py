"""Database repository. 

Repository for the following models/schemas:
    pizzerias,
    webpages,
    rankings,
    locations.
"""

from __future__ import annotations

import logging

import sqlalchemy as sa
from sqlalchemy import orm as sa_orm, select

from pizza_platform_shared.repositories.base_database import BaseDatabase
from pizza_platform_shared import schemas as shared_schemas

from pizza_data_storage import constants, models
from pizza_data_storage.utils import extract_pizzeria_name

logger = logging.getLogger(__name__)


class PizzeriaRepository(BaseDatabase):
    """Repository for seeding and querying pizzerias, webpages, rankings, and locations."""

    def seed_pizzerias_and_webpages(
        self,
        config_schema: shared_schemas.PizzeriaEndpointsSchema
    ) -> None:
        """Write pizzerias, their webpages, and ranks from config, inserting or updating."""
        with self._session() as session:
            pizzeria_map: dict[str, models.Pizzerias] = {}

            for pizzeria in config_schema.pizzerias:
                pizzeria_model = self._upsert_pizzeria(session, pizzeria)
                session.flush()
                pizzeria_map[pizzeria.name] = pizzeria_model

            for webpage_config in config_schema.webpages:
                name = extract_pizzeria_name(webpage_config.slug)
                pizzeria = pizzeria_map.get(name)
                if not pizzeria:
                    logger.warning(
                        "Skipping webpage — no pizzeria found for slug '%s'", webpage_config.slug
                    )
                    continue
                self._upsert_webpage(session, webpage_config, pizzeria)

            for ranking_config in config_schema.rankings:
                name = extract_pizzeria_name(ranking_config.pizzeria_slug)
                pizzeria = pizzeria_map.get(name)
                if not pizzeria:
                    logger.warning(
                        "Skipping ranking — no pizzeria found for slug '%s'",
                        ranking_config.pizzeria_slug,
                    )
                    continue
                self._upsert_ranking_entry(session, ranking_config, pizzeria)

    def upsert_location(self, location_config: shared_schemas.LocationSchema) -> None:
        """Write a single pizzeria location, skipping if coordinates already exist nearby."""
        with self._session() as session:
            self._upsert_location(session, location_config)

    def get_unscraped_pizzerias(self) -> list[models.Webpages]:
        """Return all pizzeria webpages that have not yet been scraped."""
        query = select(models.Webpages).where(models.Webpages.scraped_at.is_(None))
        return self._read_orm(query)

    def mark_pizzeria_scraped(self, webpage_id: int) -> None:
        """Set scraped_at to now for the given pizzeria webpage."""
        with self._session() as session:
            webpage = session.get(models.Webpages, webpage_id)
            if not webpage:
                raise ValueError(f"Webpage with id {webpage_id} not found.")
            webpage.scraped_at = sa.func.now()  # pylint: disable=not-callable

    @staticmethod
    def _upsert_pizzeria(
        session: sa_orm.Session, pizzeria_config: shared_schemas.PizzeriaSchema
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
        webpage_config: shared_schemas.WebpagesSchema,
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
    def _upsert_ranking_entry(
        session: sa_orm.Session,
        ranking_config: shared_schemas.RankingPositionSchema,
        pizzeria: models.Pizzerias,
    ) -> models.Rankings:
        existing = session.scalar(
            select(models.Rankings).where(
                models.Rankings.edition_id == ranking_config.edition_id,
                models.Rankings.pizzeria_id == pizzeria.id,
            )
        )
        if existing:
            existing.position = ranking_config.position
            return existing

        entry = models.Rankings(
            edition_id=ranking_config.edition_id,
            pizzeria_id=pizzeria.id,
            position=ranking_config.position,
        )
        session.add(entry)
        return entry

    @staticmethod
    def _upsert_location(
        session: sa_orm.Session, location_config: shared_schemas.LocationSchema
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
