"""Module for pizza data scraper models."""

from pizza_data_storage.models.awards import Awards
from pizza_data_storage.models.base import BaseModel
from pizza_data_storage.models.categories import Categories
from pizza_data_storage.models.editions import Editions
from pizza_data_storage.models.locations import Locations
from pizza_data_storage.models.pizzerias import Pizzerias
from pizza_data_storage.models.rankings import Rankings
from pizza_data_storage.models.webpages import Webpages

__all__ = [
    "Awards",
    "BaseModel",
    "Categories",
    "Editions",
    "Locations",
    "Pizzerias",
    "Rankings",
    "Webpages",
]
