"""Database repository for ranking categories and editions."""

from __future__ import annotations

import logging
from typing import Any

import sqlalchemy as sa
from sqlalchemy import orm as sa_orm, select

from pizza_platform_shared.repositories.base_database import BaseDatabase

from pizza_data_management import models, schemas

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
