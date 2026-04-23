"""Modules containing scraper settings."""

from pizza_platform_shared.settings import pizza_db

from pizza_data_storage.settings.storage import PizzaStorageSettings

__all__ = [
    "pizza_db",
    "PizzaStorageSettings",
]

pizza_storage = PizzaStorageSettings()
