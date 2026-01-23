"""Base model definitions for pizza_data_scraper models."""

import datetime

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import orm


class BaseModel(orm.DeclarativeBase):
    """Base model for pizza data scraper models."""

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
        postgresql.TIMESTAMP(precision=0, timezone=True),
        nullable=False,
        server_default=sa.func.now(),  # pylint: disable=not-callable
    )