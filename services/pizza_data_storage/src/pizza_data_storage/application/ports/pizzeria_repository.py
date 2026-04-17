"""Pizzeria repository interface."""

from typing import Protocol

from pizza_platform_shared import schemas as shared_schemas

from pizza_data_storage import models


class IPizzeriaRepository(Protocol):
    """Interface for a repository handling pizzerias and their webpages."""

    def seed_pizzerias_webpages_and_rating(
        self, config_schemas: list[shared_schemas.PizzeriaSchema]
    ) -> None:
        """Write pizzerias and webpages from config, inserting or updating."""

    def seed_location(self, location_config: shared_schemas.LocationSchema) -> None:
        """Write a pizzeria location from config, inserting or updating."""

    def get_webpages(self, *, only_unscraped: bool) -> list[models.Webpages]:
        """Return all pizzeria webpages that have not been scraped yet."""

    def get_pizzerias(self, *, only_with_locations: bool) -> list[models.Pizzerias]:
        """Return all pizzerias, optionally filtering on presence of location."""

    def mark_webpage_scraped(self, webpage_id: int) -> None:
        """Mark a pizzeria webpage as scraped."""
