"""Model for pizza categories and their associated data."""

import sqlalchemy as sa
from sqlalchemy import orm

from pizza_data_scraper.models import base


class Categories(base.BaseModel):
    """Model for storing pizza category information."""

    __tablename__ = "categories"

    name: orm.Mapped[str] = orm.mapped_column(sa.String, nullable=False, unique=True, comment="Name of the pizza category")
    description: orm.Mapped[str] = orm.mapped_column(sa.String, nullable=True, comment="Description of the pizza category")

    __table_args__ = (
        sa.UniqueConstraint(
            "name", name="uq_category_name"
        ), 
        {"schema": "pizza"}
    )