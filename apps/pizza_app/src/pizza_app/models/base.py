"""Base model definitions for pizza_data_scraper models."""

from __future__ import annotations

import datetime

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import orm


class BaseModel(orm.DeclarativeBase):
    """Base model with common fields for all tables.

    Columns:
        id (int): Auto-incrementing primary key.
        created_at (datetime): Timestamp of record creation.
        updated_at (datetime): Timestamp of last record update.

    Provides:
        - Auto-incrementing ID (BigInt for Postgres, Int for SQLite)
        - created_at timestamp with timezone
        - updated_at timestamp with timezone (auto-updates)"""

    __abstract__ = True

    id: orm.Mapped[int] = orm.mapped_column(
        sa.BigInteger().with_variant(sa.Integer, "sqlite"),
        sa.Identity(
            always=True,
            start=1,
            increment=1,
            minvalue=1,
            maxvalue=9223372036854775807,
            cycle=False,
            cache=1,
        ),
        primary_key=True,
    )
    created_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        postgresql.TIMESTAMP(precision=0, timezone=True).with_variant(
            sa.DateTime(timezone=True),
            "sqlite",
        ),
        nullable=False,
        server_default=sa.func.now(),  # pylint: disable=not-callable
    )
    updated_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        postgresql.TIMESTAMP(precision=0, timezone=True).with_variant(
            sa.DateTime(timezone=True),
            "sqlite",
        ),
        nullable=False,
        server_default=sa.func.now(),  # pylint: disable=not-callable
        onupdate=sa.func.now(),  # pylint: disable=not-callable
    )

    @staticmethod
    def create_foreign_key_str(schema_name: str, table_name: str) -> str:
        """Returns the str of the foreign key name with dot separation."""
        if schema_name is None:
            return f"{table_name}.id"
        return ".".join((schema_name, table_name, "id"))
