"""Enums for the scraper."""

from enum import StrEnum


class Location(StrEnum):
    """Enum for pizza locations."""

    WORLD = "world"
    LATIN_AMERICA = "latin-america"
    EUROPE = "europe"
    ASIA_PACIFIC = "asia-pacific"
    ITALY = "italia"
    USA = "usa"


class Year(StrEnum):
    """Enum for years of pizza rankings."""

    Y2022 = "2022"
    Y2023 = "2023"
    Y2024 = "2024"
    Y2025 = "2025"
