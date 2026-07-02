"""Ports layer for pizza data storage application."""

from pizza_data_storage.application.ports.category_payload_repository import (
    ICategoryPayloadRepository,
)
from pizza_data_storage.application.ports.html_repository import IHtmlStorageRepository
from pizza_data_storage.application.ports.pizzeria_repository import IPizzeriaRepository
from pizza_data_storage.application.ports.ranking_repository import IRankingsRepository

__all__ = [
    "ICategoryPayloadRepository",
    "IHtmlStorageRepository",
    "IPizzeriaRepository",
    "IRankingsRepository",
]
