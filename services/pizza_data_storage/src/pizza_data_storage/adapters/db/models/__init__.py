"""Module for pizza data scraper models."""

from pizza_data_storage.adapters.db.models.awards import Awards
from pizza_data_storage.adapters.db.models.base import BaseModel
from pizza_data_storage.adapters.db.models.categories import Categories
from pizza_data_storage.adapters.db.models.category_payload import CategoryPayloadStaging
from pizza_data_storage.adapters.db.models.editions import Editions
from pizza_data_storage.adapters.db.models.locations import Locations
from pizza_data_storage.adapters.db.models.pizzerias import Pizzerias
from pizza_data_storage.adapters.db.models.rankings import Rankings
from pizza_data_storage.adapters.db.models.webpages import Webpages

__all__ = [
    "Awards",
    "BaseModel",
    "Categories",
    "CategoryPayloadStaging",
    "Editions",
    "Locations",
    "Pizzerias",
    "Rankings",
    "Webpages",
]
