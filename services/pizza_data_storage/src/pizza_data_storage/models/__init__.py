"""Module for pizza data scraper models."""

from pizza_data_storage.models.database.base import BaseModel
from pizza_data_storage.models.database.categories import Categories
from pizza_data_storage.models.database.locations import Locations
from pizza_data_storage.models.database.pizzerias import Pizzerias
from pizza_data_storage.models.database.ranking_editions import RankingEditions
from pizza_data_storage.models.database.ranking_entries import RankingEntries
from pizza_data_storage.models.database.webpages import Webpages

__all__ = [
    "BaseModel",
    "Categories",
    "Locations",
    "Pizzerias",
    "RankingEditions",
    "RankingEntries",
    "Webpages",
]
