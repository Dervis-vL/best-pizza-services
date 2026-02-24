"""Modules containing scraper settings."""

from pizza_platform_shared.settings.base_database import DatabaseSettings
from pizza_platform_shared.settings.pizza_database import PizzaDatabaseSettings

__all__ = [
    "DatabaseSettings",
    "PizzaDatabaseSettings",
]

pizza_db = PizzaDatabaseSettings()
