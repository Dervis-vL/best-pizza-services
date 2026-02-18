"""Module for pizza data scraper models."""

from pizza_data_scraper.models.database.base import BaseModel
from pizza_data_scraper.models.database.categories import Categories
from pizza_data_scraper.models.database.pizzerias import Pizzerias
from pizza_data_scraper.models.database.ranking_editions import RankingEditions
from pizza_data_scraper.models.database.webpages import Webpages
from pizza_data_scraper.models.parser.patterns import CoordPatterns, AddressPatterns, PhonePatterns
from pizza_data_scraper.models.dataclass.coordinates import CoordResult

adress_patterns = AddressPatterns()
coordinate_patterns = CoordPatterns()
phone_patterns = PhonePatterns()

__all__ = [
    "adress_patterns",
    "BaseModel",
    "Categories",
    "coordinate_patterns",
    "CoordResult",
    "phone_patterns",
    "Pizzerias",
    "RankingEditions",
    "Webpages",
]