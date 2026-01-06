"""Constants for the scraper."""

from typing import Final
import yarl


URL_HOME: Final = yarl.URL("https://www.50toppizza.it/")


class CategoryEndpoints:
    """Constants for category endpoints."""

    WORLD: Final = "world"
    LATIN_AMERICA: Final = "pizza-latin-america"
    EUROPE: Final = "europe"
    ASIA_PACIFIC: Final = "pizza-asia-pacific"
    ITALY: Final = "pizza-italia"
    USA: Final = "usa"
    SELECTION_TYPE: Final = "50-top"