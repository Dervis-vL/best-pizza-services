"""Data access layer — read pizzeria data from (Postgre)SQL."""

from __future__ import annotations

from typing import Any

import sqlalchemy as sa
from pandera import typing as pa_typing

from pizza_platform_shared.repositories.base_database import BaseDatabase

from pizza_app import models, schemas


class PizzaPlatformDatabase(BaseDatabase):
    """Reads pizzeria location data from the pizza platform database.
    
    Args:
        db_settings: Resolved database settings
    """

    def _get_read_query(self) -> sa.Select[Any]:
        """Get a query to read pizzeria names and coordinates."""
        return sa.select(
            models.Pizzerias.name,
            models.Locations.latitude,
            models.Locations.longitude,
        ).join(
            models.Locations,
            models.Locations.pizzeria_id == models.Pizzerias.id,
        ).where(
            models.Locations.latitude.is_not(None)
            & models.Locations.longitude.is_not(None)
        ).order_by(models.Pizzerias.name)

    def read(self) -> pa_typing.DataFrame[schemas.PizzeriaSchema]:
        """Return every pizzeria that has lat lon pupulated."""
        query = self._get_read_query()

        try:
            pizzerias_df = self._read(query)
        except Exception as e:
            raise RuntimeError(f"Error reading from database: {e}") from e
        return schemas.PizzeriaSchema.validate(pizzerias_df)
