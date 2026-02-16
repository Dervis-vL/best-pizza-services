"""Model for pizzerias and their associated data."""

from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm

from pizza_data_scraper import settings
from pizza_data_scraper.models import base

if TYPE_CHECKING:
    from pizza_data_scraper.models.webpages import Webpages


class Pizzerias(base.BaseModel):
    """Model for storing pizza category information."""

    # table configuration
    __tablename__ = settings.pizza_db.tables.pizzerias
    __table_args__ = (
        sa.UniqueConstraint("name", name="uq_pizzeria_name"),
        {"schema": settings.pizza_db.schema_name}
    )

    # columns
    name: orm.Mapped[str] = orm.mapped_column(sa.String(100), nullable=False, comment="Name of the pizzeria")
    description: orm.Mapped[str] = orm.mapped_column(sa.String(500), nullable=True, comment="Description of the pizzeria")

    # relationships
    webpages: orm.Mapped[list["Webpages"]] = orm.relationship(back_populates="pizzeria")
