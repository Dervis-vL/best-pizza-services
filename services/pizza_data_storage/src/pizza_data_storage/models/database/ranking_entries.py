"""Model for ranking entries and their associated data."""

from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm

from pizza_data_storage import settings
from pizza_data_storage.models.database import base

if TYPE_CHECKING:
    from pizza_data_storage.models.database.pizzerias import Pizzerias
    from pizza_data_storage.models.database.ranking_editions import RankingEditions


class RankingEntries(base.BaseModel):
    """Model for storing ranking entry information."""

    # table configuration
    __tablename__ = settings.pizza_db.tables.ranking_entries
    __table_args__ = (
        sa.UniqueConstraint(
            "edition_id", "pizzeria_id", name="uq_ranking_entry_edition_pizzeria"
        ),
        {"schema": settings.pizza_db.schema_name},
    )

    # foreign key(s)
    edition_id: orm.Mapped[int] = orm.mapped_column(
        sa.BigInteger().with_variant(sa.Integer, "sqlite"),
        sa.ForeignKey(base.BaseModel.create_foreign_key_str(
            schema_name=settings.pizza_db.schema_name,
            table_name=settings.pizza_db.tables.ranking_editions,
        ), ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to the ranking edition",
    )
    pizzeria_id: orm.Mapped[int] = orm.mapped_column(
        sa.BigInteger().with_variant(sa.Integer, "sqlite"),
        sa.ForeignKey(base.BaseModel.create_foreign_key_str(
            schema_name=settings.pizza_db.schema_name,
            table_name=settings.pizza_db.tables.pizzerias,
        ), ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to the pizzeria",
    )

    # columns
    position: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, nullable=True, comment="Position of the pizza in the ranking"
    )

    # relationships
    pizzeria: orm.Mapped["Pizzerias"] = orm.relationship(
        back_populates="rankings"
    )
    edition: orm.Mapped["RankingEditions"] = orm.relationship(
        back_populates="rankings"
    )
