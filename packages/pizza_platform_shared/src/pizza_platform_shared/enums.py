"""Enums for the scraper."""

from enum import IntEnum, StrEnum


class DatabaseType(StrEnum):
    """Supported database types."""

    POSTGRESQL = "postgresql"
    SQLITE = "sqlite"


class BaseCategories(StrEnum):
    """Base category enum."""

    @classmethod
    def list(cls) -> list[str]:
        """Return a list of all category values."""
        categories = []
        for subclass in cls.__subclasses__():
            categories.extend(subclass.list())
        categories.extend([member.value for member in cls])
        return categories


class Categories(BaseCategories):
    """Enum for best pizza categories."""

    ITALY = "50 Top Pizza Italia"
    WORLD = "50 Top World"
    EUROPE = "50 Top Pizza Europa"
    LATIN_AMERICA = "50 Top Pizza Latin America"
    ASIA_PACIFIC = "50 Top Pizza Asia-Pacific"
    USA = "50 Top Pizza USA"
    PIZZA_CHAINS = "50 Top Artisan Pizza Chains"


class CategoriesExcellent(BaseCategories):
    """Enum for best pizza categories with excellent awards."""

    ITALY_EXCELLENT = "50 Top Pizza Italia Excellent"
    EUROPE_EXCELLENT = "50 Top Pizza Europa Excellent"
    USA_EXCELLENT = "50 Top Pizza USA Excellent"
    PIZZA_CHAINS_EXCELLENT = "Excellent Artisan Pizza Chains"


class CategoriesSpecial(BaseCategories):
    """Enum for special awards categories."""

    WORLD_SPECIAL = "World Special Awards"
    LATIN_AMERICA_SPECIAL = "Latin America Special Awards"
    EUROPE_SPECIAL = "European Special Awards"
    ASIA_PACIFIC_SPECIAL = "Asia-Pacific Special Awards"
    ITALY_SPECIAL = "Italy Special Awards"
    USA_SPECIAL = "USA Special Awards"


class Year(IntEnum):
    """Enum for years of pizza rankings."""

    Y2025 = 2025
    Y2024 = 2024
    Y2023 = 2023
    Y2022 = 2022
    Y2021 = 2021
    Y2020 = 2020
