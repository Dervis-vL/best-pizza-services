"""Module for pizza data scraper models."""

from pizza_data_scraper.models.database.base import BaseModel
from pizza_data_scraper.models.database.categories import Categories
from pizza_data_scraper.models.database.pizzerias import Pizzerias
from pizza_data_scraper.models.database.ranking_editions import RankingEditions
from pizza_data_scraper.models.database.webpages import Webpages
from pizza_data_scraper.models.parser.patterns import CoordPatterns
from pizza_data_scraper.models.dataclass.coordinates import CoordResult

coordinate_patterns = CoordPatterns()

__all__ = [
    "BaseModel",
    "Categories",
    "coordinate_patterns",
    "CoordResult",
    "Pizzerias",
    "RankingEditions",
    "Webpages",
]