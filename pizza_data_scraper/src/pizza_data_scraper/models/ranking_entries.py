"""Model for ranking entries and their associated data."""

import sqlalchemy as sa
from sqlalchemy import orm

from pizza_data_scraper.models import base


class RankingEntries(base.BaseModel):
    """Model for storing ranking entry information."""

    __tablename__ = "ranking_entries"

    edition_id: orm.Mapped[int] = orm.mapped_column(sa.Integer, sa.ForeignKey("pizza.ranking_editions.id"), nullable=False, comment="Foreign key to the ranking edition")
    pizzeria_id: orm.Mapped[int] = orm.mapped_column(sa.Integer, sa.ForeignKey("pizza.pizzerias.id"), nullable=False, comment="Foreign key to the pizzeria")

    position: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=False, comment="Position of the pizza in the ranking")
    award: orm.Mapped[str] = orm.mapped_column(sa.String, nullable=True, comment="Award received by the pizza, if any")

    __table_args__ = (
        sa.UniqueConstraint(
            "edition_id", "position", name="uq_ranking_entry_edition_position"
        ), 
        {"schema": "pizza"}
    )