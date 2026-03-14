"""Geolocation constants and shared types."""

from typing import Final

import yarl


class GeoLocationConstants:  # pylint: disable=too-few-public-methods
    """Constants for the geolocation service."""

    BASE_URL: Final[yarl.URL] = yarl.URL("https://nominatim.openstreetmap.org/reverse")
    MIN_INTERVAL: Final[float] = 1.0  # Nominatim hard limit: 1 req/sec
