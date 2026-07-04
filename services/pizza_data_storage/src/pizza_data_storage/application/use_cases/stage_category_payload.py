"""Stage a category-ingestion payload use case."""

from pizza_data_storage.application import ports
from pizza_platform_shared import schemas as shared_schemas


class StageCategoryPayloadUseCase:  # pylint: disable=too-few-public-methods
    """Persist a category payload for hand-off to the worker."""

    def __init__(self, payload_repository: ports.ICategoryPayloadRepository) -> None:
        """Initialize the use case."""
        self._payload_repository = payload_repository

    def execute(self, category_schemas: list[shared_schemas.CategorySchema]) -> int:
        """Stage the payload as pending and return its row id."""
        return self._payload_repository.stage_payload(category_schemas=category_schemas)
