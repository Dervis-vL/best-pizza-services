"""Enums for the scraper."""

from enum import IntEnum, StrEnum


class HtmlModelName(StrEnum):
    """Enum for HTML model names."""

    EDITIONS = "editions"
    WEBPAGES = "webpages"


class PizzeriaInclude(StrEnum):
    """Pizzeria relationships that can be eagerly loaded."""

    LOCATIONS = "locations"
    RANKINGS = "rankings"
    WEBPAGES = "webpages"
    AWARDS = "awards"


class Year(IntEnum):
    """Enum for years of pizza rankings."""

    Y2026 = 2026
    Y2025 = 2025
    Y2024 = 2024
    Y2023 = 2023
    Y2022 = 2022
    Y2021 = 2021
    Y2020 = 2020


class URLSchemas(StrEnum):
    """Enum for allowed url schemas."""

    HTTP = "http://"
    HTTPS = "https://"
