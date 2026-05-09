"""Model for ranking entries and their associated data."""

from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm

from pizza_data_storage import settings
from pizza_data_storage.models.database import base

if TYPE_CHECKING:
    from pizza_data_storage.models.database.editions import Editions
    from pizza_data_storage.models.database.pizzerias import Pizzerias


class Rankings(base.BaseModel):  # pylint: disable=too-few-public-methods
    """Model for storing ranking entry information."""

    # table configuration
    __tablename__ = settings.pizza_db.tables.rankings
    __table_args__ = (
        sa.UniqueConstraint(
            "edition_id", "pizzeria_id", name="uq_ranking_entry_edition_pizzeria"
        ),
        {"schema": settings.pizza_db.schema_name},
    )

    # foreign key(s)
    edition_id: orm.Mapped[int] = orm.mapped_column(
        sa.BigInteger().with_variant(sa.Integer, "sqlite"),
        sa.ForeignKey(
            base.BaseModel.create_foreign_key_str(
                schema_name=settings.pizza_db.schema_name,
                table_name=settings.pizza_db.tables.editions,
            ),
            ondelete="CASCADE",
        ),
        nullable=False,
        comment="Foreign key to the ranking edition",
    )
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
        comment="Foreign key to the pizzeria",
    )

    # columns
    position: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, nullable=False, comment="Position of the pizza in the ranking"
    )

    # relationships
    pizzeria: orm.Mapped[Pizzerias] = orm.relationship(back_populates="rankings")
    edition: orm.Mapped[Editions] = orm.relationship(back_populates="rankings")
