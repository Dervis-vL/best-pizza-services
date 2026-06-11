"""Ranking repository interface."""

from typing import Protocol

from pizza_data_storage import models
from pizza_platform_shared import schemas as shared_schemas


class IRankingsRepository(Protocol):
    """Interface for a repository handling ranking categories and editions."""

    def seed_categories_and_editions(
        self,
        category_schemas: list[shared_schemas.CategorySchema],
    ) -> None:
        """Write categories and editions from config, inserting or updating."""

    def get_editions(
        self,
        *,
        only_unscraped: bool = False,
        only_unparsed: bool = False,
    ) -> list[models.Editions]:
        """Return all ranking editions, optional if not been scraped or parsed yet."""

    def get_edition(self, edition_id: int) -> models.Editions | None:
        """Return a single edition by id."""

    def mark_edition_scraped(self, edition_id: int) -> None:
        """Mark an edition as scraped."""

    def mark_edition_parsed(self, edition_id: int) -> None:
        """Mark an edition as parsed."""
