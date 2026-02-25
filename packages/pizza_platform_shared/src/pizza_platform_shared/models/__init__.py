"""Module for pizza data scraper models."""

from pizza_platform_shared.models.database.base import BaseModel
from pizza_platform_shared.models.database.categories import Categories
from pizza_platform_shared.models.database.locations import Locations
from pizza_platform_shared.models.database.pizzerias import Pizzerias
from pizza_platform_shared.models.database.ranking_editions import RankingEditions
from pizza_platform_shared.models.database.webpages import Webpages

__all__ = [
    "BaseModel",
    "Categories",
    "Locations",
    "Pizzerias",
    "RankingEditions",
    "Webpages",
]