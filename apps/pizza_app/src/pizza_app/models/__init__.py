"""Module for pizza data scraper models."""

from pizza_app.models.base import BaseModel
from pizza_app.models.categories import Categories
from pizza_app.models.locations import Locations
from pizza_app.models.pizzerias import Pizzerias
from pizza_app.models.ranking_editions import RankingEditions
from pizza_app.models.webpages import Webpages

__all__ = [
    "BaseModel",
    "Categories",
    "Locations",
    "Pizzerias",
    "RankingEditions",
    "Webpages",
]