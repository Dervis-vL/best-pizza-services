"""Model for pizzerias and their associated data."""

import datetime

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import orm

from pizza_data_scraper.models import base


class Pizzerias(base.BaseModel):
    """Model for storing pizza category information."""

    __tablename__ = "pizzerias"

    name: orm.Mapped[str] = orm.mapped_column(sa.String(100), nullable=False, comment="Name of the pizzeria")
    url: orm.Mapped[str] = orm.mapped_column(sa.String(200), nullable=False, comment="URL of the pizzeria's page on 50 Top Pizza")
    description: orm.Mapped[str] = orm.mapped_column(sa.String(500), nullable=True, comment="Description of the pizzeria")
    slug: orm.Mapped[str] = orm.mapped_column(sa.String(50), nullable=False, comment="URL-friendly slug for the pizzeria")
    scraped_at: orm.Mapped[datetime.datetime | None] = orm.mapped_column(
        postgresql.TIMESTAMP(precision=0, timezone=True).with_variant(
            sa.DateTime(timezone=True),
            "sqlite"
        ),
        nullable=True,
        comment="Timestamp when the data was scraped"
    )

    # relationships

    __table_args__ = (
        sa.UniqueConstraint("slug", name="uq_pizzeria_slug"),
        {"schema": "pizza"}
    )