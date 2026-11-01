"""Seed pizzerias and webpages use case."""

from pizza_data_storage.application import ports
from pizza_platform_shared import schemas as shared_schemas


class SeedPizzeriasWebpagesRatingsUseCase:  # pylint: disable=too-few-public-methods
    """Seed pizzerias, webpages and rankings use case."""

    def __init__(self, pizzeria_repository: ports.IPizzeriaRepository) -> None:
        """Initialize the use case."""
        self._pizzeria_repository = pizzeria_repository

    def execute(self, config_schema: list[shared_schemas.PizzeriaSchema]) -> None:
        """Execute the use case."""
        self._pizzeria_repository.seed_pizzerias_webpages_and_rating(
            config_schemas=config_schema,
        )
