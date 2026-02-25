"""Module for pizza data scraper models."""

from pizza_data_management.models.database.base import BaseModel
from pizza_data_management.models.database.categories import Categories
from pizza_data_management.models.database.locations import Locations
from pizza_data_management.models.database.pizzerias import Pizzerias
from pizza_data_management.models.database.ranking_editions import RankingEditions
from pizza_data_management.models.database.webpages import Webpages
from pizza_data_management.models.parser.patterns import CoordPatterns, AddressPatterns, PhonePatterns

adress_patterns = AddressPatterns()
coordinate_patterns = CoordPatterns()
phone_patterns = PhonePatterns()

__all__ = [
    "adress_patterns",
    "BaseModel",
    "Categories",
    "coordinate_patterns",
    "Locations",
    "phone_patterns",
    "Pizzerias",
    "RankingEditions",
    "Webpages",
]