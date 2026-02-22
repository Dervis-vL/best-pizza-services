"""Enums for the scraper."""

from enum import StrEnum


class Categories(StrEnum):
    """Enum for best pizza categories."""

    WORLD = "world"
    LATIN_AMERICA = "latin_america"
    EUROPE = "europe"
    ASIA_PACIFIC = "asia_pacific"
    ITALY = "italy"
    USA = "usa"


class Year(StrEnum):
    """Enum for years of pizza rankings."""

    Y2024 = "2024"
    Y2025 = "2025"
