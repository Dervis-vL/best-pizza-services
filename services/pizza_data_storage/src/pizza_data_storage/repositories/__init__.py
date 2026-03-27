"""Database repositories for scraper app."""

from pizza_data_storage.repositories.pizzerias import PizzeriaRepository
from pizza_data_storage.repositories.ranking import RankingRepository

__all__ = [
    "PizzeriaRepository",
    "RankingRepository",
]
