"""Module for pizza data scraper models."""

from pizza_data_collector.models.parser.patterns import (
    AddressPatterns,
    AwardNamePatterns,
    CardPatterns,
    CoordPatterns,
    PhonePatterns,
    RankingPositionPatterns,
    URLPatterns,
)

adress_patterns = AddressPatterns()
award_name_patterns = AwardNamePatterns()
card_patterns = CardPatterns()
coordinate_patterns = CoordPatterns()
phone_patterns = PhonePatterns()
ranking_position_patterns = RankingPositionPatterns()
url_pattern = URLPatterns()


__all__ = [
    "AwardNamePatterns",
    "CardPatterns",
    "RankingPositionPatterns",
    "URLPatterns",
    "adress_patterns",
    "award_name_patterns",
    "card_patterns",
    "coordinate_patterns",
    "phone_patterns",
    "ranking_position_patterns",
]
