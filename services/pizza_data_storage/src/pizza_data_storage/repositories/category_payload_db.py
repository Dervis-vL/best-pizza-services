"""Database repository for staging category-ingestion payloads.

Handles the hand-off of a category payload from the API (producer) to the worker
(consumer): the API stages a payload as ``pending`` and passes the row id to the
worker, which reads it back, processes it, and marks it ``consumed`` or ``failed``.
"""

import datetime
import logging

import pydantic
from sqlalchemy import select

from pizza_data_storage import models
from pizza_platform_shared import enums as shared_enums
from pizza_platform_shared import schemas as shared_schemas
from pizza_platform_shared.repositories.base_database import BaseDatabase

logger = logging.getLogger(__name__)

_PAYLOAD_ADAPTER = pydantic.TypeAdapter(list[shared_schemas.CategorySchema])


class CategoryPayloadRepository(BaseDatabase):
    """Repository for the category payload staging table."""

    def stage_payload(
        self,
        category_schemas: list[shared_schemas.CategorySchema],
    ) -> int:
        """Persist the payload as a pending row and return its generated id.

        Args:
            category_schemas (list[CategorySchema]): The list of category schemas to stage.

        Returns:
            int: The id of the staged payload row.
        """
        row = models.CategoryPayloadStaging(
            payload=[schema.model_dump(mode="json") for schema in category_schemas],
            status=shared_enums.PayloadStatus.PENDING,
        )
        with self._session() as session:
            session.add(row)
            session.flush()
            payload_id = row.id
        logger.info("Staged category payload id=%s", payload_id)
        return payload_id

    def get_payload(self, payload_id: int) -> list[shared_schemas.CategorySchema]:
        """Return the deserialized payload for a staging row."""
        row = self._read_orm(
            select(models.CategoryPayloadStaging).where(
                models.CategoryPayloadStaging.id == payload_id,
            ),
            single=True,
        )
        if row is None:
            msg = f"No staged category payload with id {payload_id}"
            raise KeyError(msg)
        return _PAYLOAD_ADAPTER.validate_python(row.payload)

    def mark_consumed(self, payload_id: int) -> None:
        """Mark a staging row as consumed."""
        self._set_status(payload_id, status=shared_enums.PayloadStatus.CONSUMED)

    def mark_failed(self, payload_id: int) -> None:
        """Mark a staging row as failed."""
        self._set_status(payload_id, status=shared_enums.PayloadStatus.FAILED)

    def _set_status(self, payload_id: int, *, status: shared_enums.PayloadStatus) -> None:
        with self._session() as session:
            row = session.get(models.CategoryPayloadStaging, payload_id)
            if row is None:
                msg = f"No staged category payload with id {payload_id}"
                raise KeyError(msg)
            row.status = status
            row.consumed_at = datetime.datetime.now(datetime.UTC)
