"""Model for pizzerias and their associated data."""

import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import orm

from pizza_data_storage import settings
from pizza_data_storage.models.database import base

if TYPE_CHECKING:
    from pizza_data_storage.models.database.pizzerias import Pizzerias


class Webpages(base.BaseModel):
    """Model for storing webpages linked to the pizzerias information."""

    # table configuration
    __tablename__ = settings.pizza_db.tables.webpages
    __table_args__ = (
        sa.UniqueConstraint("pizzeria_id", "url", name="uq_webpage_pizzeria_url"),
        {"schema": settings.pizza_db.schema_name}
    )

    # foreign key(s)
    pizzeria_id: orm.Mapped[int] = orm.mapped_column(
        sa.BigInteger().with_variant(sa.Integer, "sqlite"),
        sa.ForeignKey(base.BaseModel.create_foreign_key_str(
            schema_name=settings.pizza_db.schema_name,
            table_name=settings.pizza_db.tables.pizzerias,
        ), ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to the pizzerias table",
    )

    # columns
    url: orm.Mapped[str] = orm.mapped_column(
        sa.String(500), nullable=False, comment="URL of the pizzeria's page on 50 Top Pizza"
    )
    slug: orm.Mapped[str] = orm.mapped_column(
        sa.String(200), nullable=False, comment="URL-friendly slug for the pizzeria"
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
    pizzeria: orm.Mapped["Pizzerias"] = orm.relationship(
        back_populates=settings.pizza_db.tables.webpages
    )
