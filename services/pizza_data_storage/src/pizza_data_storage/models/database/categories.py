"""Model for pizza categories and their associated data."""

from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm

from pizza_data_storage import settings
from pizza_data_storage.models.database import base

if TYPE_CHECKING:
    from pizza_data_storage.models.database.editions import Editions


class Categories(base.BaseModel):
    """Model for storing pizza category information."""

    # table configuration
    __tablename__ = settings.pizza_db.tables.categories
    __table_args__ = (
        sa.UniqueConstraint("slug", name="uq_category_slug"),
        {"schema": settings.pizza_db.schema_name}
    )

    # columns
    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(50), nullable=False, comment="Name of the pizza category"
    )
    description: orm.Mapped[str] = orm.mapped_column(
        sa.String(500), nullable=True, comment="Description of the pizza category"
    )
    slug: orm.Mapped[str] = orm.mapped_column(
        sa.String(50), nullable=False, comment="URL-friendly slug for the pizza category"
    )

    # relationships
    editions: orm.Mapped[
        list["Editions"]
    ] = orm.relationship(back_populates="category")
