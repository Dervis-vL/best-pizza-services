"""Utility functions for the pizza app."""

from typing import TYPE_CHECKING

import streamlit as st
from pandera import typing as pa_typing

from pizza_app import constants, schemas

if TYPE_CHECKING:
    from collections.abc import Callable


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
