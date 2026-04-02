"""Seed pizzerias and webpages use case."""

from pizza_platform_shared import schemas as shared_schemas

from pizza_data_storage.application import ports


class SeedPizzeriasAndWebpagesUseCase:
    """Seed pizzerias and webpages use case."""

    def __init__(self, pizzeria_repository: ports.IPizzeriaRepository):
        self._pizzeria_repository = pizzeria_repository

    def execute(self, config_schema):
        """Execute the use case."""
        self._pizzeria_repository.seed_pizzerias_webpages_and_rankings(
            config_schema=config_schema
        )
