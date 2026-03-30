"""Database repository. 

Repository for the following models/schemas:
    categories,
    editions.
"""

from __future__ import annotations

import logging

import sqlalchemy as sa
from sqlalchemy import orm as sa_orm, select

from pizza_platform_shared.repositories.base_database import BaseDatabase
from pizza_platform_shared import schemas as shared_schemas

from pizza_data_storage import models

logger = logging.getLogger(__name__)


class RankingsRepository(BaseDatabase):
    """Repository for seeding and querying categories and editions tables."""

    def seed_categories_and_editions(
        self,
        config_schema: shared_schemas.RankedCategoriesSchema,
    ) -> None:
        """Write categories and ranking editions from config, inserting or updating."""
        with self._session() as session:
            category_map: dict[str, models.Categories] = {}

            for category in config_schema.categories:
                category_model = self._upsert_category(session, category)
                session.flush()
                category_map[category.slug] = category_model

            for edition in config_schema.editions:
                category = category_map.get(edition.slug)
                if not category:
                    logger.warning(
                        "Skipping edition — category '%s' not found", edition.slug
                    )
                    continue
                self._upsert_edition(session, edition, category)

    def get_editions(self, *, only_unscraped: bool) -> list[models.Editions]:
        """Return all ranking editions, optionally filtering on scraped status.

        Relationships are eagerly loaded so objects remain usable after
        the session closes.
        """
        query = (
            select(models.Editions)
            .options(
                sa_orm.joinedload(models.Editions.category),
                sa_orm.joinedload(models.Editions.rankings),
            )
        )
        if only_unscraped:
            query = query.where(models.Editions.scraped_at.is_(None))

        return self._read_orm(query)

    def get_edition(self, edition_id: int) -> models.Editions | None:
        """Return a single edition by id."""
        query = (
            select(models.Editions)
            .where(models.Editions.id == edition_id)
            .options(
                sa_orm.joinedload(models.Editions.category),
                sa_orm.joinedload(models.Editions.rankings),
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
        """Set scraped_at to now for the given ranking edition."""
        with self._session() as session:
            edition = session.get(models.Editions, edition_id)
            if not edition:
                raise ValueError(f"Edition with id {edition_id} not found.")
            edition.scraped_at = sa.func.now()  # pylint: disable=not-callable

    @staticmethod
    def _upsert_category(
        session: sa_orm.Session, cat_config: shared_schemas.CategorySchema
    ) -> models.Categories:
        """Upsert a category by slug, updating name and description if it already exists."""
        existing = session.scalar(
            select(models.Categories)
            .where(models.Categories.slug == cat_config.slug)
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
            select(models.Editions)
            .where(
                models.Editions.category_id == category.id,
                models.Editions.year == edition_config.year,
            )
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
