"""Modules containing scraper settings."""

from pizza_data_storage.settings.storage import PizzaStorageSettings
from pizza_platform_shared.settings import pizza_db

__all__ = [
    "PizzaStorageSettings",
    "pizza_db",
]

pizza_storage = PizzaStorageSettings()
