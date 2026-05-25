"""Get all, with or without location, pizzerias use case."""

from pizza_data_storage.application import ports
from pizza_platform_shared import schemas as shared_schemas


class GetPizzeriasUseCase:  # pylint: disable=too-few-public-methods
    """Get pizzerias use case."""

    def __init__(self, pizza_repository: ports.IPizzeriaRepository) -> None:
        """Initialize the use case."""
        self._pizza_repository = pizza_repository

    def execute(self) -> list[shared_schemas.PizzeriaReadSchema]:
        """Execute the use case."""
        pizzerias_models = self._pizza_repository.get_pizzerias()
        return [
            shared_schemas.PizzeriaReadSchema.model_validate(
                edition,
                from_attributes=True,
            )
            for edition in pizzerias_models
        ]
