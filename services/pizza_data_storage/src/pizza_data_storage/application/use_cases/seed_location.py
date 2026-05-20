"""Seed location use case."""

from pizza_data_storage.application import ports
from pizza_platform_shared import schemas as shared_schemas


class SeedLocationUseCase:  # pylint: disable=too-few-public-methods
    """Seed location use case."""

    def __init__(self, pizzeria_repository: ports.IPizzeriaRepository) -> None:
        """Initialize the use case."""
        self._pizzeria_repository = pizzeria_repository

    def execute(self, location_config: shared_schemas.LocationSchema) -> None:
        """Execute the use case."""
        self._pizzeria_repository.seed_location(location_config=location_config)
