"""Module for pizza data scraper models."""

from pizza_data_collector.models.database.base import BaseModel
from pizza_data_collector.models.database.categories import Categories
from pizza_data_collector.models.database.locations import Locations
from pizza_data_collector.models.database.pizzerias import Pizzerias
from pizza_data_collector.models.database.ranking_editions import RankingEditions
from pizza_data_collector.models.database.ranking_entries import RankingEntries
from pizza_data_collector.models.database.webpages import Webpages
from pizza_data_collector.models.parser.patterns import (
    AddressPatterns,
    CardPatterns,
    CoordPatterns,
    PhonePatterns,
    RankingPositionPatterns,
    URLPattern,
)

adress_patterns = AddressPatterns()
card_patterns = CardPatterns()
coordinate_patterns = CoordPatterns()
phone_patterns = PhonePatterns()
ranking_position_patterns = RankingPositionPatterns()
url_pattern = URLPattern()


__all__ = [
    "adress_patterns",
    "BaseModel",
    "Categories",
    "card_patterns",
    "coordinate_patterns",
    "Locations",
    "phone_patterns",
    "Pizzerias",
    "RankingEditions",
    "RankingEntries",
    "ranking_position_patterns",
    "URLPattern",
    "Webpages",
]