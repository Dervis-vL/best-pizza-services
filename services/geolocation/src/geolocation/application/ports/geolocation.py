"""Port definition for the geolocation service."""

from typing import Protocol

from geolocation import models


class IGeolocationService(Protocol):  # pylint: disable=too-few-public-methods
    """Driven port: reverse-geocode a coordinate into a structured location."""

    def reverse_geocode(self, lat: float, lon: float) -> models.LocationResult:
        """Return country, city, and address for the given coordinates."""
