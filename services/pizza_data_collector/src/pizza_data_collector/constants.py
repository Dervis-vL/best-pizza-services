"""Constants for the scraper."""

from typing import Final

import yarl

URL_HOME: Final = yarl.URL("https://www.50toppizza.it/")


class Coordinate:
    """Coordinate constant values for models."""

    LOC_DELTA: Final[float] = 0.0003


class CategoryEndpoints:
    """Constants for category endpoints."""

    WORLD: Final[str] = "world"
    LATIN_AMERICA: Final[str] = "pizza-latin-america"
    EUROPE: Final[str] = "europe"
    ASIA_PACIFIC: Final[str] = "pizza-asia-pacific"
    ITALY: Final[str] = "pizza-italia"
    USA: Final[str] = "usa"
    SELECTION_TYPE: Final[str] = "50-top"


class ColumnLengths:
    """Constants for column lengths."""

    NAME: Final[int] = 100
    DESCRIPTION: Final[int] = 500
    URL: Final[int] = 500
    SLUG: Final[int] = 200


class PizzaNameRules:
    """Constants for pizza name rules."""

    HAS_TWO_PARTS: Final[int] = 2
    HAS_THREE_PARTS: Final[int] = 3
    PART_FIVE: Final[int] = 5
    PART_ELEVEN: Final[int] = 11
    PART_FOURTEEN: Final[int] = 14
