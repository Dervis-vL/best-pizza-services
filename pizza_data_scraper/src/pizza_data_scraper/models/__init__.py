"""Module for pizza data scraper models."""

from pizza_data_scraper.models.base import BaseModel
from pizza_data_scraper.models.categories import Categories
from pizza_data_scraper.models.pizzerias import Pizzerias
from pizza_data_scraper.models.ranking_editions import RankingEditions
from pizza_data_scraper.models.webpages import Webpages

__all__ = [
    "BaseModel",
    "Categories",
    "Pizzerias",
    "RankingEditions",
    "Webpages",
]