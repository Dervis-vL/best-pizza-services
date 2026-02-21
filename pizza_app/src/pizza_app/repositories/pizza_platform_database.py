"""Data access layer — read pizzeria data from (Postgre)SQL."""

from __future__ import annotations

from typing import Any

import pandas as pd
import sqlalchemy as sa
from pandera import typing as pa_typing

from pizza_app import settings, schemas, models


class PizzaPlatformDatabase:
    """Reads pizzeria location data from the pizza platform database.
    
    Args:
        settings: Resolved database settings
    """

    def __init__(self, settings: settings.DatabaseSettings) -> None:
        """Initialization of repo."""
        self._engine = sa.create_engine(settings.connection_string, pool_pre_ping=True)
        self._schema = settings.schema_name

    def _get_query(self) -> sa.Select[Any]:
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
        query = self.get_query()

        with self._engine.connect() as conn:
            pizzerias_df = pd.read_sql(sql=query, con=conn)

        return schemas.PizzeriaSchema.validate(pizzerias_df)