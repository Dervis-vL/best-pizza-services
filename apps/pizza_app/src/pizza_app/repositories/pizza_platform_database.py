"""Data access layer — read pizzeria data from (Postgre)SQL."""

from __future__ import annotations

from typing import Any

import pandas as pd
import sqlalchemy as sa
from pandera import typing as pa_typing

from pizza_app import schemas, models, types


class PizzaPlatformDatabase:
    """Reads pizzeria location data from the pizza platform database.
    
    Args:
        settings: Resolved database settings
    """

    def __init__(self, connection_string: str, schema_name: types.SchemaName | None = None) -> None:
        """Initialization of repo."""
        self._engine: sa.Engine = sa.create_engine(connection_string, pool_pre_ping=True)
        self._schema: types.SchemaName | None = schema_name

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
        query = self._get_query()

        try:
            # must work for postgres and sqlite, so use pandas read_sql which can handle both via SQLAlchemy.
            # When no schema (SQLite) it would still work:
            with self._engine.connect() as conn:
                pizzerias_df = pd.read_sql(query, conn)
        except Exception as e:
            raise RuntimeError(f"Error reading from database: {e}")

        return schemas.PizzeriaSchema.validate(pizzerias_df)
