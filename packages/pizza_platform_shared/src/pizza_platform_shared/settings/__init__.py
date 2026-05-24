"""Modules containing scraper settings."""

from functools import cache
from typing import TYPE_CHECKING

import pydantic_settings as pyd_settings

from pizza_platform_shared.settings.base_database import DatabaseSettings
from pizza_platform_shared.settings.maintenance_database import (
    MaintenanceDatabaseSettings,
)
from pizza_platform_shared.settings.pizza_database import PizzaDatabaseSettings
from pizza_platform_shared.settings.pizza_storage import PizzaStorageSettings

if TYPE_CHECKING:
    pizza_db: PizzaDatabaseSettings
    maintenance_db: MaintenanceDatabaseSettings
    pizza_strg: PizzaStorageSettings


@cache
def _pizza_db() -> PizzaDatabaseSettings:
    """Load (lazy) the pizza database settings."""
    return PizzaDatabaseSettings()


@cache
def _maintenance_db() -> MaintenanceDatabaseSettings:
    """Load (lazy) the maintenance database settings."""
    return MaintenanceDatabaseSettings()


@cache
def _pizza_storage() -> PizzaStorageSettings:
    """Load (lazy) the pizza object storage settings."""
    return PizzaStorageSettings()


_loaders = {
    "pizza_db": _pizza_db,
    "maintenance_db": _maintenance_db,
    "pizza_strg": _pizza_storage,
}


def __getattr__(name: str) -> pyd_settings.BaseSettings:
    """Lazy load the settings when they are accessed."""
    if name in _loaders:
        return _loaders[name]()
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)


__all__ = ["DatabaseSettings", "maintenance_db", "pizza_db", "pizza_strg"]
