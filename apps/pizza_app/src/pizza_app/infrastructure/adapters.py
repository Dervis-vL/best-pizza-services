"""Infrastructure module for the pizza app."""

import streamlit as st

from pizza_app import dataclasses, repositories


class PizzaDataAdapter:  # pylint: disable=too-few-public-methods
    """Pizza data adapter class."""

    def __init__(self, repo: repositories.PizzaPlatformDatabase):
        """Class initialization."""
        self._repo = repo

    @st.cache_data(ttl=18000, show_spinner="Loading Pizzerias from DB...")
    def load_pizza_data(_self) -> dataclasses.PizzaData:  # pylint: disable=no-self-argument
        """Load all pizza app data."""
        pizza_data = dataclasses.PizzaData(
            locations=_self._repo.read_pizzerias(),
            rankings=_self._repo.read_rankings(),
        )

        if pizza_data.locations.empty:
            st.warning("No pizzerias with coordinates found in the database.")
            st.stop()

        if pizza_data.rankings.empty:
            st.warning("No pizzeria rankings found in the database.")
            st.stop()

        return pizza_data
