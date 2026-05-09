"""Database repository.

Repository for the following models/schemas:
    pizzerias,
    webpages,
    rankings,
    awards,
    locations.
"""

from __future__ import annotations

import logging

import sqlalchemy as sa
from sqlalchemy import orm as sa_orm
from sqlalchemy import select

from pizza_data_storage import constants, models
from pizza_platform_shared import schemas as shared_schemas
from pizza_platform_shared.repositories.base_database import BaseDatabase

logger = logging.getLogger(__name__)


class PizzeriaRepository(BaseDatabase):
    """Repository for seeding and querying pizzerias, webpages, rankings, and locations."""

    def seed_pizzerias_webpages_and_rating(
        self, config_schemas: list[shared_schemas.PizzeriaSchema]
    ) -> None:
        """Write pizzerias, their webpages, and rating from config, inserting or updating."""
        with self._session() as session:
            for pizzeria in config_schemas:
                pizzeria_model = self._upsert_pizzeria(session, pizzeria)
                session.flush()
                for webpage in pizzeria.webpages:
                    self._upsert_webpage(
                        session=session,
                        webpage_config=webpage,
                        pizzeria_id=pizzeria_model.id,
                    )

                for ranking in pizzeria.rankings:
                    self._upsert_ranking(
                        session=session,
                        ranking_config=ranking,
                        pizzeria_id=pizzeria_model.id,
                    )

                for award in pizzeria.awards:
                    self._upsert_award(
                        session=session,
                        award_config=award,
                        pizzeria_id=pizzeria_model.id,
                    )

    def seed_location(self, location_config: shared_schemas.LocationSchema) -> None:
        """Write location from config schema, inserting or updating."""
        with self._session() as session:
            self._upsert_location(session, location_config)

    def get_webpages(
        self, *, only_unscraped: bool = False, only_unparsed: bool = False
    ) -> list[models.Webpages]:
        """Return all webpages of pizzerias, optionally filtering on scraped and parsed status.

        Relationships are eagerly loaded so objects remain usable after
        the session closes.
        """
        query = select(models.Webpages).options(
            sa_orm.joinedload(models.Webpages.pizzeria)
        )
        if only_unscraped:
            query = query.where(models.Webpages.scraped_at.is_(None))
        if only_unparsed:
            query = query.where(models.Webpages.parsed_at.is_(None))

        return self._read_orm(query)

    def get_pizzerias(self, *, only_with_locations: bool) -> list[models.Pizzerias]:
        """Return all pizzerias, optionally filtering to only those with locations."""
        query = select(models.Pizzerias).options(
            sa_orm.joinedload(models.Pizzerias.webpages),
            sa_orm.joinedload(models.Pizzerias.rankings),
            sa_orm.joinedload(models.Pizzerias.awards),
            sa_orm.joinedload(models.Pizzerias.locations),
        )
        if only_with_locations:
            # Where locations list is not empty
            query = query.where(models.Pizzerias.locations.any())

        return self._read_orm(query)

    def mark_webpage_scraped(self, webpage_id: int) -> None:
        """Set scraped_at to now for the given pizzeria webpage."""
        with self._session() as session:
            webpage = session.get(models.Webpages, webpage_id)
            if not webpage:
                raise ValueError(f"Webpage with id {webpage_id} not found.")
            webpage.scraped_at = sa.func.now()  # pylint: disable=not-callable

    def mark_webpage_parsed(self, webpage_id: int) -> None:
        """Set parsed_at to now for the given pizzeria webpage."""
        with self._session() as session:
            webpage = session.get(models.Webpages, webpage_id)
            if not webpage:
                raise ValueError(f"Webpage with id {webpage_id} not found.")
            webpage.parsed_at = sa.func.now()  # pylint: disable=not-callable

    @staticmethod
    def _upsert_pizzeria(
        session: sa_orm.Session, pizzeria_config: shared_schemas.PizzeriaSchema
    ) -> models.Pizzerias:
        """Upsert pizzeria, skipping if name already exists."""
        existing = session.scalar(
            select(models.Pizzerias).where(
                models.Pizzerias.name == pizzeria_config.name
            )
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
        webpage_config: shared_schemas.WebpageSchema,
        pizzeria_id: int,
    ) -> models.Webpages:
        """Upsert webpage for the pizzeria, skipping if the url already exists."""
        existing = session.scalar(
            select(models.Webpages).where(
                models.Webpages.pizzeria_id == pizzeria_id,
                models.Webpages.url == webpage_config.url,
            )
        )
        if existing:
            existing.slug = webpage_config.slug
            return existing

        webpage = models.Webpages(
            slug=webpage_config.slug,
            url=webpage_config.url,
            pizzeria_id=pizzeria_id,
        )
        session.add(webpage)
        return webpage

    @staticmethod
    def _upsert_ranking(
        session: sa_orm.Session,
        ranking_config: shared_schemas.RankingSchema,
        pizzeria_id: int,
    ) -> models.Rankings:
        """Upsert rank for top pizzerias, skipping if position already exists."""
        existing = session.scalar(
            select(models.Rankings).where(
                models.Rankings.edition_id == ranking_config.edition_id,
                models.Rankings.pizzeria_id == pizzeria_id,
            )
        )
        if existing:
            existing.position = ranking_config.position
            return existing

        ranking = models.Rankings(
            edition_id=ranking_config.edition_id,
            pizzeria_id=pizzeria_id,
            position=ranking_config.position,
        )
        session.add(ranking)
        return ranking

    @staticmethod
    def _upsert_award(
        session: sa_orm.Session,
        award_config: shared_schemas.AwardSchema,
        pizzeria_id: int,
    ) -> models.Awards:
        """Upsert awards for special pizzerias, skipping if award already exists."""
        existing = session.scalar(
            select(models.Awards).where(
                models.Awards.edition_id == award_config.edition_id,
                models.Awards.pizzeria_id == pizzeria_id,
            )
        )
        if existing:
            existing.award = award_config.award
            return existing

        award = models.Awards(
            edition_id=award_config.edition_id,
            pizzeria_id=pizzeria_id,
            award=award_config.award,
            sponsor=award_config.sponsor,
        )
        session.add(award)
        return award

    @staticmethod
    def _upsert_location(
        session: sa_orm.Session, location_config: shared_schemas.LocationSchema
    ) -> models.Locations:
        """Upsert a pizzeria location, skipping if coordinates already exist nearby."""
        if location_config.has_coordinates:
            existing = session.scalar(
                select(models.Locations)
                .where(models.Locations.pizzeria_id == location_config.pizzaria_id)
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
                existing.adress = location_config.adress
                existing.city = location_config.city
                existing.country = location_config.country
                existing.phone = location_config.phone
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
