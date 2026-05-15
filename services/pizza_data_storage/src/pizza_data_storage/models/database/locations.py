"""Model for pizzerias and their associated locations."""

from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm

from pizza_data_storage import settings
from pizza_data_storage.models.database import base

if TYPE_CHECKING:
    from pizza_data_storage.models.database.pizzerias import Pizzerias


class Locations(base.BaseModel):
    """Model for storing pizzeria locations."""

    # table configuration
    __tablename__ = settings.pizza_db.tables.locations
    __table_args__ = (
        sa.UniqueConstraint(
            "pizzeria_id",
            "latitude",
            "longitude",
            name="uq_location_pizzeria_latitude_longitude",
        ),
        {"schema": settings.pizza_db.schema_name},
    )

    # foreign key(s)
    pizzeria_id: orm.Mapped[int] = orm.mapped_column(
        sa.BigInteger().with_variant(sa.Integer, "sqlite"),
        sa.ForeignKey(
            base.BaseModel.create_foreign_key_str(
                schema_name=settings.pizza_db.schema_name,
                table_name=settings.pizza_db.tables.pizzerias,
            ),
            ondelete="CASCADE",
        ),
        nullable=False,
        comment="Foreign key to the pizzerias table",
    )

    # columns
    adress: orm.Mapped[str | None] = orm.mapped_column(
        sa.String(250),
        nullable=True,
        comment="Pizzeria adress",
    )
    city: orm.Mapped[str | None] = orm.mapped_column(
        sa.String(50),
        nullable=True,
        comment="Pizzeria city",
    )
    country: orm.Mapped[str | None] = orm.mapped_column(
        sa.String(50),
        nullable=True,
        comment="Pizzeria country",
    )
    latitude: orm.Mapped[float | None] = orm.mapped_column(
        sa.Float,
        nullable=True,
        comment="Pizzeria latitude",
    )
    longitude: orm.Mapped[float | None] = orm.mapped_column(
        sa.Float,
        nullable=True,
        comment="Pizzeria longitude",
    )
    phone: orm.Mapped[str | None] = orm.mapped_column(
        sa.String(20),
        nullable=True,
        comment="Pizzeria phonenumber",
    )

    # relationships
    pizzeria: orm.Mapped[Pizzerias] = orm.relationship(
        back_populates=settings.pizza_db.tables.locations,
    )
