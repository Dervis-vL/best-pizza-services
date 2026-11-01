"""Category payload staging repository interface."""

from typing import Protocol

from pizza_platform_shared import schemas as shared_schemas


class ICategoryPayloadRepository(Protocol):
    """Interface for staging category-ingestion payloads between the API and worker."""

    def stage_payload(
        self,
        category_schemas: list[shared_schemas.CategorySchema],
    ) -> int:
        """Persist a payload as pending and return its staging row id."""

    def get_payload(self, payload_id: int) -> list[shared_schemas.CategorySchema]:
        """Return the deserialized payload for a staging row by id."""

    def mark_consumed(self, payload_id: int) -> None:
        """Mark a staging row as consumed."""

    def mark_failed(self, payload_id: int) -> None:
        """Mark a staging row as failed."""
