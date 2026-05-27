"""Settings for the pizza app."""

from pizza_app.settings.application import Application
from pizza_app.settings.pizza_api import PizzaAPISettings
from pizza_platform_shared.settings import pizza_db

app_settings = Application()
pizza_api = PizzaAPISettings()

__all__ = ["app_settings", "pizza_api", "pizza_db"]
