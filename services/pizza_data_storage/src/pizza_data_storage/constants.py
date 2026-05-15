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


class StorageKeys:
    """Constants for storage keys."""

    SCRAPES_PREFIX: Final[str] = "scrapes"
    HTML_SUFFIX: Final[str] = "html"
    JSON_SUFFIX: Final[str] = "json"
    STORAGE_TYPE: Final = "s3"
    STORAGE_TIER: Final = "STANDARD"
