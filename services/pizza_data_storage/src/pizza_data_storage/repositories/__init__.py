"""Database repositories for scraper app."""

from pizza_data_storage.repositories.category_payload_db import CategoryPayloadRepository
from pizza_data_storage.repositories.html_storage import HtmlStorageRepository
from pizza_data_storage.repositories.pizzeria_db import PizzeriaRepository
from pizza_data_storage.repositories.ranking_db import RankingsRepository

__all__ = [
    "CategoryPayloadRepository",
    "HtmlStorageRepository",
    "PizzeriaRepository",
    "RankingsRepository",
]
