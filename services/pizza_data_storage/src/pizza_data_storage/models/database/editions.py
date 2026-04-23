"""Model for ranked editions and their associated data."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import orm

from pizza_data_storage import settings
from pizza_data_storage.models.database import base

if TYPE_CHECKING:
    from pizza_data_storage.models.database.awards import Awards
    from pizza_data_storage.models.database.categories import Categories
    from pizza_data_storage.models.database.rankings import Rankings


class Editions(base.BaseModel):
    """Model for storing ranked edition information."""

    # table configuration
    __tablename__ = settings.pizza_db.tables.editions
    __table_args__ = (
        sa.UniqueConstraint(
            "category_id", "year", name="uq_ranking_edition_category_year"
        ),
        sa.UniqueConstraint(
            "url", name="uq_ranking_edition_url"
        ), 
        {"schema": settings.pizza_db.schema_name}
    )

    # foreign key(s)
    category_id: orm.Mapped[int] = orm.mapped_column(
        sa.BigInteger().with_variant(sa.Integer, "sqlite"),
        sa.ForeignKey(base.BaseModel.create_foreign_key_str(
            schema_name=settings.pizza_db.schema_name,
            table_name=settings.pizza_db.tables.categories,
        ), ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to the categories table",
    )

    # columns
    year: orm.Mapped[int] = orm.mapped_column(
        sa.SmallInteger, nullable=False, comment="Year of the ranked edition"
    )
    url: orm.Mapped[str] = orm.mapped_column(
        sa.String(500), nullable=False, comment="Endpoint URL for the ranked edition data"
    )
    scraped_at: orm.Mapped[datetime.datetime | None] = orm.mapped_column(
        postgresql.TIMESTAMP(precision=0, timezone=True).with_variant(
            sa.DateTime(timezone=True),
            "sqlite"
        ),
        nullable=True,
        comment="Timestamp when the data was scraped"
    )
    parsed_at: orm.Mapped[datetime.datetime | None] = orm.mapped_column(
        postgresql.TIMESTAMP(precision=0, timezone=True).with_variant(
            sa.DateTime(timezone=True),
            "sqlite"
        ),
        nullable=True,
        comment="Timestamp when the data was parsed"
    )

    # relationships
    category: orm.Mapped["Categories"] = orm.relationship(back_populates="editions")
    rankings: orm.Mapped[list["Rankings"]] = orm.relationship(back_populates="edition")
    awards: orm.Mapped[list["Awards"]] = orm.relationship(back_populates="edition")
