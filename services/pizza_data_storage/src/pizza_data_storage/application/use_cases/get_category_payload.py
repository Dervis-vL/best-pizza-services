"""Get a staged category-ingestion payload use case."""

from pizza_data_storage.application import ports
from pizza_platform_shared import schemas as shared_schemas


class GetCategoryPayloadUseCase:  # pylint: disable=too-few-public-methods
    """Read a staged category payload back by its row id."""

    def __init__(self, payload_repository: ports.ICategoryPayloadRepository) -> None:
        """Initialize the use case."""
        self._payload_repository = payload_repository

    def execute(self, payload_id: int) -> list[shared_schemas.CategorySchema]:
        """Return the deserialized payload for a staging row."""
        return self._payload_repository.get_payload(payload_id=payload_id)
