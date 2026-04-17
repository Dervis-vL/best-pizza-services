"""Module for pizza data scraper models."""

from pizza_data_storage.models.database.awards import Awards
from pizza_data_storage.models.database.base import BaseModel
from pizza_data_storage.models.database.categories import Categories
from pizza_data_storage.models.database.locations import Locations
from pizza_data_storage.models.database.pizzerias import Pizzerias
from pizza_data_storage.models.database.editions import Editions
from pizza_data_storage.models.database.rankings import Rankings
from pizza_data_storage.models.database.webpages import Webpages

__all__ = [
    "Awards",
    "BaseModel",
    "Categories",
    "Locations",
    "Pizzerias",
    "Editions",
    "Rankings",
    "Webpages",
]
