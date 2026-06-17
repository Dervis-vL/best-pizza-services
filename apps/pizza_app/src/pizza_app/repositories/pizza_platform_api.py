"""Data access layer; read pizzeeria data from the API."""

import requests

from pizza_app import constants
from pizza_app.settings.pizza_api import PizzaAPISettings
from pizza_platform_shared import schemas


class PizzaPlatformAPI:
    """Reads pizzeria location data from the pizza platform API."""

    def __init__(self, api_settings: PizzaAPISettings) -> None:
        """Initialize the API client.

        Args:
            api_settings: Resolved API settings

        """
        self.api_settings = api_settings

    def read_pizzerias(self) -> list[schemas.PizzeriaReadSchema]:
        """Read pizzeria location data from the API."""
        # HTTP request using the settings url here with timeout and error handling
        response = requests.get(
            f"{self.api_settings.base_url}{constants.PizzaAPI.PIZZERIAS_ENDPOINT}",
            timeout=constants.PizzaAPI.TIMEOUT,
        )
        response.raise_for_status()
        return [schemas.PizzeriaReadSchema(**pizzeria) for pizzeria in response.json()]
