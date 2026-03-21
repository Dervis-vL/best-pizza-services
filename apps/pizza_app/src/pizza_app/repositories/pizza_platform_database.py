"""Data access layer — read pizzeria data from (Postgre)SQL."""

from __future__ import annotations

from typing import Any

import sqlalchemy as sa
from pandera import typing as pa_typing

from pizza_platform_shared.repositories.base_database import BaseDatabase
from pizza_platform_shared import models
from pizza_app import schemas


class PizzaPlatformDatabase(BaseDatabase):
    """Reads pizzeria location data from the pizza platform database.
    
    Args:
        db_settings: Resolved database settings
    """

    def _get_read_query(self) -> sa.Select[Any]:
        """Get a query to read pizzeria names and coordinates."""
        return sa.select(
            models.Pizzerias.name.label("slug"),
            models.Locations.latitude,
            models.Locations.longitude,
            models.Locations.country,
            models.Locations.city,
        ).join(
            models.Locations,
            models.Locations.pizzeria_id == models.Pizzerias.id,
        ).where(
            models.Locations.latitude.is_not(None)
            & models.Locations.longitude.is_not(None)
        ).order_by(models.Pizzerias.name)

    def _get_rankings_query(self) -> sa.Select[Any]:
        """Get a query for all pizzeria rankings with year and category."""
        return (
            sa.select(
                models.Pizzerias.name.label("pizzeria_name"),
                models.RankingEntries.position,
                models.RankingEditions.year,
                models.Categories.name.label("category"),
            )
            .join(models.RankingEntries, models.RankingEntries.pizzeria_id == models.Pizzerias.id)
            .join(models.RankingEditions, models.RankingEditions.id == models.RankingEntries.edition_id)
            .join(models.Categories, models.Categories.id == models.RankingEditions.category_id)
            .order_by(
                models.Pizzerias.name,
                models.RankingEditions.year.desc(),
                models.Categories.name,
            )
        )

    def read_pizzerias(self) -> pa_typing.DataFrame[schemas.PizzeriaSchema]:
        """Return every pizzeria that has lat lon pupulated."""
        query = self._get_read_query()

        try:
            pizzerias_df = self._read(query)
        except Exception as e:
            raise RuntimeError(f"Error reading from database: {e}") from e
        return schemas.PizzeriaSchema.validate(pizzerias_df)


    def read_rankings(self) -> pa_typing.DataFrame[schemas.RankingSchema]:
        """Return all rankings for every pizzeria."""
        query = self._get_rankings_query()
        try:
            df = self._read(query)
        except Exception as e:
            raise RuntimeError(f"Error reading rankings from database: {e}") from e
        return schemas.RankingSchema.validate(df)
