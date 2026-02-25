"""Modules containing scraper settings."""

from pizza_app.settings.base_database import DatabaseSettings
from pizza_app.settings.pizza_database import PizzaDatabaseSettings

__all__ = [
    "DatabaseSettings",
    "PizzaDatabaseSettings",
]

pizza_db = PizzaDatabaseSettings()
