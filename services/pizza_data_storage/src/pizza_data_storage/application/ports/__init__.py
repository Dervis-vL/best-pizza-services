"""Ports layer for pizza data storage application."""

from pizza_data_storage.application.ports.category_payload_repo import (
    ICategoryPayloadRepository,
)
from pizza_data_storage.application.ports.html_repo import IHtmlStorageRepository
from pizza_data_storage.application.ports.pizzeria_repo import IPizzeriaRepository
from pizza_data_storage.application.ports.ranking_repo import IRankingsRepository

__all__ = [
    "ICategoryPayloadRepository",
    "IHtmlStorageRepository",
    "IPizzeriaRepository",
    "IRankingsRepository",
]
