"""Modules containing scraper settings."""

from functools import cache
from typing import TYPE_CHECKING

from pizza_platform_shared.settings.base_database import DatabaseSettings
from pizza_platform_shared.settings.pizza_database import PizzaDatabaseSettings
from pizza_platform_shared.settings.maintenance_database import MaintenanceDatabaseSettings

if TYPE_CHECKING:
    pizza_db: PizzaDatabaseSettings
    maintenance_db: MaintenanceDatabaseSettings


@cache
def _pizza_db() -> PizzaDatabaseSettings:
    return PizzaDatabaseSettings()


@cache
def _maintenance_db() -> MaintenanceDatabaseSettings:
    return MaintenanceDatabaseSettings()


_loaders = {
    "pizza_db": _pizza_db,
    "maintenance_db": _maintenance_db,
}


def __getattr__(name: str):
    if name in _loaders:
        return _loaders[name]()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "DatabaseSettings",
    "pizza_db",
    "maintenance_db",
]