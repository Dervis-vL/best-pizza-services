"""Modules containing scraper settings."""

from pizza_data_management.settings.base_database import DatabaseSettings
from pizza_data_management.settings.maintenance_database import MaintenanceDatabaseSettings
from pizza_data_management.settings.pizza_database import PizzaDatabaseSettings

__all__ = [
    "DatabaseSettings",
    "MaintenanceDatabaseSettings",
    "PizzaDatabaseSettings",
]

pizza_db = PizzaDatabaseSettings()
maintenance_db = MaintenanceDatabaseSettings()