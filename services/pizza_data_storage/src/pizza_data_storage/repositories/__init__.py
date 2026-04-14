"""Database repositories for scraper app."""

from pizza_data_storage.repositories.pizzeria import PizzeriaRepository
from pizza_data_storage.repositories.ranking import RankingsRepository

__all__ = [
    "PizzeriaRepository",
    "RankingsRepository",
]
