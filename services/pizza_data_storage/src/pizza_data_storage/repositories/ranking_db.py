"""Database repository.

Repository for the following models/schemas:
    categories,
    editions.
"""

from __future__ import annotations

import logging

import sqlalchemy as sa
from sqlalchemy import orm as sa_orm
from sqlalchemy import select

from pizza_data_storage import models
from pizza_platform_shared import schemas as shared_schemas
from pizza_platform_shared.repositories.base_database import BaseDatabase

logger = logging.getLogger(__name__)


class RankingsRepository(BaseDatabase):
    """Repository for seeding and querying categories and editions tables."""

    def seed_categories_and_editions(
        self,
        category_schemas: list[shared_schemas.CategorySchema],
    ) -> None:
        """Write categories and editions from config, inserting or updating."""
        # read all existing slugs from db using self._read_orm()
        existing_slugs = {category.slug for category in self._read_orm(select(models.Categories))}

        with self._session() as session:
            for category in category_schemas:
                if category.slug not in existing_slugs and not category.allow_create:
                    logger.warning(
                        "Skip category '%s', doesn't exist and create is not allowed.",
                        category.slug,
                    )
                    continue
                category_model = self._upsert_category(session, category)
                session.flush()
                for edition in category.editions:
                    self._upsert_edition(session, edition, category_model)

    def get_editions(
        self,
        *,
        only_unscraped: bool = False,
        only_unparsed: bool = False,
    ) -> list[models.Editions]:
        """Return all editions, optionally filtering on scraped and parsed status.

        Relationships are eagerly loaded so objects remain usable after
        the session closes.
        """
        query = select(models.Editions).options(
            sa_orm.joinedload(models.Editions.category),
            sa_orm.joinedload(models.Editions.rankings),
            sa_orm.joinedload(models.Editions.awards),
        )
        if only_unscraped:
            query = query.where(models.Editions.scraped_at.is_(None))
        if only_unparsed:
            query = query.where(models.Editions.parsed_at.is_(None))

        return self._read_orm(query)

    def get_edition(self, edition_id: int) -> models.Editions | None:
        """Return a single edition by id."""
        query = (
            select(models.Editions)
            .where(models.Editions.id == edition_id)
            .options(
                sa_orm.joinedload(models.Editions.category),
                sa_orm.joinedload(models.Editions.rankings),
                sa_orm.joinedload(models.Editions.awards),
            )
        )
        return self._read_orm(query, single=True)

    def get_category(self, category_id: int) -> models.Categories | None:
        """Return a single category by id."""
        query = (
            select(models.Categories)
            .where(models.Categories.id == category_id)
            .options(sa_orm.joinedload(models.Categories.editions))
        )
        return self._read_orm(query, single=True)

    def mark_edition_scraped(self, edition_id: int) -> None:
        """Set scraped_at to now for the given edition."""
        with self._session() as session:
            edition = session.get(models.Editions, edition_id)
            if not edition:
                msg = f"Edition with id {edition_id} not found."
                raise ValueError(msg)
            edition.scraped_at = sa.func.now()  # pylint: disable=not-callable

    def mark_edition_parsed(self, edition_id: int) -> None:
        """Set parsed_at to now for the given edition."""
        with self._session() as session:
            edition = session.get(models.Editions, edition_id)
            if not edition:
                msg = f"Edition with id {edition_id} not found."
                raise ValueError(msg)
            edition.parsed_at = sa.func.now()  # pylint: disable=not-callable

    @staticmethod
    def _upsert_category(
        session: sa_orm.Session,
        cat_config: shared_schemas.CategorySchema,
    ) -> models.Categories:
        """Upsert a category by slug, updating name, description if already exists."""
        existing = session.scalar(
            select(models.Categories).where(models.Categories.slug == cat_config.slug),
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
        edition_config: shared_schemas.EditionSchema,
        category: models.Categories,
    ) -> models.Editions:
        """Upsert an edition by category and year, updating url if it already exists."""
        existing = session.scalar(
            select(models.Editions).where(
                models.Editions.category_id == category.id,
                models.Editions.year == edition_config.year,
            ),
        )
        if existing:
            existing.url = edition_config.url
            return existing

        edition = models.Editions(
            category_id=category.id,
            year=edition_config.year,
            url=edition_config.url,
        )
        session.add(edition)
        return edition
