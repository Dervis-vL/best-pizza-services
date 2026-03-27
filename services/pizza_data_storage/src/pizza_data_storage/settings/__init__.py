"""Modules containing scraper settings."""

from pizza_platform_shared.settings import PizzaDatabaseSettings

from pizza_data_storage.settings.maintenance_database import MaintenanceDatabaseSettings

__all__ = [
    "MaintenanceDatabaseSettings",
    "PizzaDatabaseSettings",
]

pizza_db = PizzaDatabaseSettings()
maintenance_db = MaintenanceDatabaseSettings()
