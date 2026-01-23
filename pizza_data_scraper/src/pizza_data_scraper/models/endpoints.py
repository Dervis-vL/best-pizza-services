"""Module with the endpoint models for pizza data scraper."""

import sqlalchemy as sa
from sqlalchemy import orm

from pizza_data_scraper.models import base


class Endpoints(base.BaseModel):
    """Model for storing endpoint information."""

    __tablename__ = "endpoints"

    year: orm.Mapped[str] = orm.mapped_column(sa.String, nullable=False, comment="Year of the ranked data endpoint")
    category: orm.Mapped[str] = orm.mapped_column(sa.String, nullable=False, comment="Category of the ranked data endpoint")
    endpoint: orm.Mapped[str] = orm.mapped_column(sa.String, nullable=False, comment="Endpoint URL to the ranked data")

    __table_args__ = ({"schema": "pizza"})    