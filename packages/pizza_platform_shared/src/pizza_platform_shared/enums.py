"""Enums for the scraper."""

from enum import IntEnum, StrEnum


class DatabaseType(StrEnum):
    """Supported database types."""

    POSTGRESQL = "postgresql"
    SQLITE = "sqlite"


class Categories(StrEnum):
    """Enum for best pizza categories."""

    ITALY = "50 Top Pizza Italia"
    WORLD = "50 Top World"
    EUROPE = "50 Top Pizza Europa"
    LATIN_AMERICA = "50 Top Pizza Latin America"
    ASIA_PACIFIC = "50 Top Pizza Asia-Pacific"
    USA = "50 Top Pizza USA"
    ITALY_EXCELLENT = "50 Top Pizza Italia Excellent"
    EUROPE_EXCELLENT = "50 Top Pizza Europa Excellent"
    USA_EXCELLENT = "50 Top Pizza USA Excellent"
    WORLD_SPECIAL = "World Special Awards"
    LATIN_AMERICA_SPECIAL = "Latin America Special Awards"
    EUROPE_SPECIAL = "European Special Awards"
    ASIA_PACIFIC_SPECIAL = "Asia-Pacific Special Awards"
    ITALY_SPECIAL = "Italy Special Awards"
    USA_SPECIAL = "USA Special Awards"
    PIZZA_CHAINS = "50 Top Artisan Pizza Chains"
    PIZZA_CHAINS_EXCELLENT = "Excellent Artisan Pizza Chains"


class Year(IntEnum):
    """Enum for years of pizza rankings."""

    Y2025 = 2025
    Y2024 = 2024
    Y2023 = 2023
    Y2022 = 2022
    Y2021 = 2021
    Y2020 = 2020
