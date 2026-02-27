"""Database repositories for scraper app."""

from pizza_data_management.repositories.pizzerias import PizzeriaRepository
from pizza_data_management.repositories.ranking import RankingRepository

__all__ = [
    "PizzeriaRepository",
    "RankingRepository",
]