"""Model for staging category-ingestion payloads handed from the API to the worker."""

import datetime
from typing import Any

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.dialects import postgresql

from pizza_data_storage import settings
from pizza_data_storage.models import base
from pizza_platform_shared import enums as shared_enums


class CategoryPayloadStaging(base.BaseModel):
    """Staging row holding a submitted category-ingestion payload.

    The API validates a category payload, writes it here as JSONB, and triggers a
    worker run with this row's id. The worker reads the payload back, runs the
    add-category pipeline, and flips ``pending`` to ``consumed`` (or ``failed``) — so
    the table doubles as a queryable ingestion history rather than an ephemeral queue.
    """

    __tablename__ = settings.pizza_db.tables.payload_staging
    __table_args__ = ({"schema": settings.pizza_db.schema_name},)

    payload: orm.Mapped[list[dict[str, Any]]] = orm.mapped_column(
        postgresql.JSONB().with_variant(sa.JSON(), "sqlite"),
        nullable=False,
        comment="Serialized list[CategorySchema] submitted for ingestion.",
    )
    status: orm.Mapped[shared_enums.PayloadStatus] = orm.mapped_column(
        sa.Enum(
            shared_enums.PayloadStatus,
            name="payload_status",
            native_enum=True,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
        default=shared_enums.PayloadStatus.PENDING,
        comment="Lifecycle status: pending -> consumed | failed.",
    )
    consumed_at: orm.Mapped[datetime.datetime | None] = orm.mapped_column(
        postgresql.TIMESTAMP(precision=0, timezone=True).with_variant(
            sa.DateTime(timezone=True),
            "sqlite",
        ),
        nullable=True,
        comment="When the worker finished processing this payload.",
    )
