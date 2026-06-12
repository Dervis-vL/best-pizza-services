"""Settings for the pizza app."""

from pizza_app.settings.pizza_api import PizzaAPISettings
from pizza_platform_shared.settings import pizza_db

pizza_api = PizzaAPISettings()

__all__ = ["pizza_api", "pizza_db"]
