"""Model for pizzerias and their associated locations."""

import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import orm

from pizza_data_scraper import settings
from pizza_data_scraper.models.database import base

if TYPE_CHECKING:
    from pizza_data_scraper.models.database.pizzerias import Pizzerias


class Locations(base.BaseModel):
    """Model for storing pizzeria locations."""

    # table configuration
    __tablename__ = settings.pizza_db.tables.locations
    __table_args__ = (
        sa.UniqueConstraint(
            "latitude", "longitude", name="uq_location_latitude_longitude"
        ),
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
    adress: orm.Mapped[str] = orm.mapped_column(sa.String(250), nullable=False, comment="")
    city: orm.Mapped[str] = orm.mapped_column(sa.String(50), nullable=False, comment="")
    country: orm.Mapped[str] = orm.mapped_column(sa.String(50), nullable=False, comment="")
    latitude: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=False, comment="")
    longitude: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=False, comment="")
    phone: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=False, comment="")

    # relationships
    pizzeria: orm.Mapped["Pizzerias"] = orm.relationship(
        back_populates=settings.pizza_db.tables.locations
    )