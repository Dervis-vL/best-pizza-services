"""Settings for the pizza app."""

from pizza_platform_shared.settings import pizza_db

from pizza_app.settings.pizza_api import APIRetrySettings, PizzaAPISettings

pizza_api = PizzaAPISettings()
retry_api = APIRetrySettings()

__all__ = [
    "pizza_api",
    "pizza_db",
    "retry_api",
]
