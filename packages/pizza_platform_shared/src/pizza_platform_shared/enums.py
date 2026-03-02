"""Enums for the scraper."""

from enum import StrEnum


class Categories(StrEnum):
    """Enum for best pizza categories."""

    WORLD = "world"
    WORLD_SPECIAL = "world-special"
    LATIN_AMERICA = "latin_america"
    LATIN_AMERICA_SPECIAL = "latin-america-special"
    EUROPE = "europe"
    EUROPE_SPECIAL = "europe-special"
    EUROPE_EXCELLENT = "europe-excellent"
    ASIA_PACIFIC = "asia_pacific"
    ASIA_PACIFIC_SPECIAL = "asia-pacific-special"
    ITALY = "italy"
    ITALY_SPECIAL = "italy-special"
    ITALY_EXCELLENT = "italy-excellent"
    USA = "usa"
    USA_SPECIAL = "usa-special"
    USA_EXCELLENT = "usa-excellent"
    PIZZA_CHAINS = "pizza-chains"
    PIZZA_CHAINS_EXCELLENT = "pizza-chains-excellent"


class Year(StrEnum):
    """Enum for years of pizza rankings."""

    Y2020 = "2020"
    Y2021 = "2021"
    Y2022 = "2022"
    Y2023 = "2023"
    Y2024 = "2024"
    Y2025 = "2025"
