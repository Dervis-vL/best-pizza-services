"""Get all, with or without location, pizzerias use case."""

from pizza_platform_shared import schemas as shared_schemas

from pizza_data_storage.application import ports


class GetPizzeriasUseCase:  # pylint: disable=too-few-public-methods
    """Get pizzerias use case."""

    def __init__(self, pizza_repository: ports.IPizzeriaRepository):
        """Initialize the use case."""
        self._pizza_repository = pizza_repository

    def execute(
        self, *, only_with_locations: bool
    ) -> list[shared_schemas.PizzeriaReadSchema]:
        """Execute the use case."""
        pizzerias_models = self._pizza_repository.get_pizzerias(
            only_with_locations=only_with_locations,
        )
        return [
            shared_schemas.PizzeriaReadSchema.model_validate(
                edition, from_attributes=True
            )
            for edition in pizzerias_models
        ]
