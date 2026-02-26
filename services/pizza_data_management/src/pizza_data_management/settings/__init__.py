"""Modules containing scraper settings."""

from pizza_data_management.settings.maintenance_database import MaintenanceDatabaseSettings

from pizza_platform_shared.settings import PizzaDatabaseSettings

__all__ = [
    "MaintenanceDatabaseSettings",
    "PizzaDatabaseSettings",
]

pizza_db = PizzaDatabaseSettings()
maintenance_db = MaintenanceDatabaseSettings()