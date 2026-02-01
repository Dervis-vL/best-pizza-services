"""Model for ranking editions and their associated data."""

import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import orm

from pizza_data_scraper.models import base

if TYPE_CHECKING:
    from pizza_data_scraper.models.categories import Categories


class RankingEditions(base.BaseModel):
    """Model for storing ranking edition information."""

    __tablename__ = "ranking_editions"

    category_id: orm.Mapped[int] = orm.mapped_column(
        sa.BigInteger().with_variant(sa.Integer, "sqlite"),
        sa.ForeignKey("pizza.categories.id", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to the categories table",
    )
    year: orm.Mapped[int] = orm.mapped_column(sa.SmallInteger, nullable=False, comment="Year of the ranking edition")
    endpoint_url: orm.Mapped[str] = orm.mapped_column(sa.String(500), nullable=False, comment="Endpoint URL for the ranking edition data")
    scraped_at: orm.Mapped[datetime.datetime | None] = orm.mapped_column(
        postgresql.TIMESTAMP(precision=0, timezone=True).with_variant(
            sa.DateTime(timezone=True),
            "sqlite"
        ),
        nullable=True,
        comment="Timestamp when the data was scraped"
    )

    # relationships
    category: orm.Mapped["Categories"] = orm.relationship(back_populates="ranked_editions")

    __table_args__ = (
        sa.UniqueConstraint(
            "category_id", "year", name="uq_ranking_edition_category_year"
        ),
        sa.UniqueConstraint(
            "endpoint_url", name="uq_ranking_edition_endpoint_url"
        ), 
        {"schema": "pizza"}
    )