"""Model for ranking editions and their associated data."""

import sqlalchemy as sa
from sqlalchemy import orm

from pizza_data_scraper.models import base


class RankingEditions(base.BaseModel):
    """Model for storing ranking edition information."""

    __tablename__ = "ranking_editions"

    year: orm.Mapped[str] = orm.mapped_column(sa.String, nullable=False, comment="Year of the ranking edition")
    endpoint_url: orm.Mapped[str] = orm.mapped_column(sa.String, nullable=False, comment="Endpoint URL for the ranking edition data")
    scraped_at: orm.Mapped[sa.DateTime] = orm.mapped_column(sa.DateTime, nullable=False, comment="Timestamp when the data was scraped")

    __table_args__ = (
        sa.UniqueConstraint(
            "endpoint_url", name="uq_ranking_edition_endpoint_url"
        ), 
        {"schema": "pizza"}
    )