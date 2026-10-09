"""Constants for the scraper."""

from typing import Final

import yarl

URL_HOME: Final = yarl.URL("https://www.50toppizza.it/")


class Coordinate:
    """Coordinate constant values for models."""

    LOC_DELTA: Final[float] = 0.0003
