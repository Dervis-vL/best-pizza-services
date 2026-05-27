"""Infrastructure module for the pizza app."""

import streamlit as st

from pizza_app import dataclasses, repositories
from pizza_platform_shared import schemas


class PizzaDataAdapter:  # pylint: disable=too-few-public-methods
    """Pizza data adapter class."""

    def __init__(self, repo: repositories.PizzaPlatformAPI) -> None:
        """Class initialization."""
        self._repo = repo

    def load_pizza_data(self) -> dataclasses.PizzaData:
        """Load all pizza app data."""
        pizza_data: dataclasses.PizzaData = PizzaDataAdapter.load_data(_repo=self._repo)

        if pizza_data.locations.empty:
            st.warning("No pizzerias with coordinates found in the database.")
            st.stop()

        if pizza_data.rankings.empty:
            st.warning("No pizzeria rankings found in the database.")
            st.stop()

        return pizza_data

    @staticmethod
    @st.cache_data(ttl=18000, show_spinner="Loading Pizza Data from DB...")
    def load_data(_repo: repositories.PizzaPlatformAPI) -> dataclasses.PizzaData:
        """Load all pizza app data.

        Staticmethod implementation to allow caching of the method without
        the need for an instance of the class.
        """
        pizzerias: list[schemas.PizzeriaReadSchema] = _repo.read_pizzerias()
        return dataclasses.PizzaData(
            locations=[
                pizzeria.locations for pizzeria in pizzerias if pizzeria.locations is not None
            ],
            rankings=[pizzeria.rankings for pizzeria in pizzerias if pizzeria.rankings is not None],
        )
