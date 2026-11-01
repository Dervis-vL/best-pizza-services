"""Seed categories and editions use case."""

from pizza_data_storage.application import ports
from pizza_platform_shared import schemas as shared_schemas


class SeedCategoriesAndEditionsUseCase:  # pylint: disable=too-few-public-methods
    """Seed categories and editions use case."""

    def __init__(self, ranking_repository: ports.IRankingsRepository) -> None:
        """Initialize the use case."""
        self._ranking_repository = ranking_repository

    def execute(self, category_schemas: list[shared_schemas.CategorySchema]) -> None:
        """Execute the use case."""
        self._ranking_repository.seed_categories_and_editions(
            category_schemas=category_schemas,
        )
