"""Utility functions for the pizza app."""

from pathlib import Path
from typing import TYPE_CHECKING

import sqlalchemy as sa
import streamlit as st
from pandera import typing as pa_typing

from pizza_app import constants, repositories, schemas, settings
from pizza_platform_shared import enums as shared_enums

if TYPE_CHECKING:
    from collections.abc import Callable


# create repo
def create_repo() -> repositories.PizzaPlatformDatabase:
    """Create repo instance."""
    if settings.app_settings.database_type == shared_enums.DatabaseType.POSTGRESQL:
        pizza_repo = repositories.PizzaPlatformDatabase.from_settings(
            db_settings=settings.pizza_db,
        )
    elif settings.app_settings.database_type == shared_enums.DatabaseType.SQLITE:
        root_path = Path(__file__).parent.parent.parent
        sqlite_db_path = root_path / "test_rankings_parsing.db"
        sqlite_db_path.exists()
        pizza_repo = repositories.PizzaPlatformDatabase.from_engine(
            engine=sa.create_engine(
                f"sqlite:///{sqlite_db_path}",
                poolclass=sa.pool.StaticPool,
            ),
        )
    else:
        msg = "Unsupported database type."
        raise ValueError(msg)

    return pizza_repo


def on_country_change() -> None:
    """Check country column again after a change."""
    st.session_state[constants.QueryParam.CITY] = constants.Filters.DEFAULT


def make_on_city_change(
    relevant_locations: pa_typing.DataFrame[schemas.LocationSchema],
    city_col: str,
    country_col: str,
) -> Callable[[], None]:
    """Factory to return the on change callback"""

    def on_city_change() -> None:
        city = st.session_state[constants.QueryParam.CITY]
        if city != constants.Filters.DEFAULT:
            match = relevant_locations[relevant_locations[city_col] == city]
            if not match.empty:
                st.session_state[constants.QueryParam.COUNTRY] = match.iloc[0][country_col]

    return on_city_change
