"""Modules containing scraper settings."""

from pizza_platform_shared.settings import PizzaDatabaseSettings

from pizza_data_storage.settings.maintenance_database import MaintenanceDatabaseSettings
from pizza_data_storage.settings.storage import PizzaStorageSettings

__all__ = [
    "MaintenanceDatabaseSettings",
    "PizzaDatabaseSettings",
    "PizzaStorageSettings",
]

maintenance_db = MaintenanceDatabaseSettings()
pizza_db = PizzaDatabaseSettings()
pizza_storage = PizzaStorageSettings()
