"""Infrastructure module for the pizza app."""

import streamlit as st

from pizza_app import dataclasses, repositories, schemas


class PizzaDataAdapter:  # pylint: disable=too-few-public-methods
    """Maps API read models (pydantic) to the app's flat analytical frames (pandera)."""

    def __init__(self, repo: repositories.PizzaPlatformAPI) -> None:
        """Class initialization."""
        self._repo = repo

    def load_pizza_data(self) -> dataclasses.PizzaData:
        """Load all pizza app data."""
        pizza_data: dataclasses.PizzaData = PizzaDataAdapter.load_data(_repo=self._repo)

        if pizza_data.locations.empty:
            st.warning("No pizzerias with coordinates found.")
            st.stop()

        if pizza_data.rankings.empty:
            st.warning("No pizzeria rankings found.")
            st.stop()

        return pizza_data

    @staticmethod
    @st.cache_data(ttl=18000, show_spinner="Loading Pizza Data from API...")
    def load_data(_repo: repositories.PizzaPlatformAPI) -> dataclasses.PizzaData:
        """Load all pizza app data.

        Staticmethod implementation to allow caching of the method without
        the need for an instance of the class.
        """
        pizzerias = _repo.read_pizzerias()
        return dataclasses.PizzaData(
            locations=schemas.LocationSchema.from_pizzeria_schema(pizzerias),
            rankings=schemas.RankingSchema.from_pizzeria_schema(pizzerias),
            awards=schemas.AwardSchema.from_pizzeria_schema(pizzerias),
        )
