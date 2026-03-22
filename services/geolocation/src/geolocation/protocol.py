"""Port definition for the geolocation service."""

from typing import Protocol

from geolocation.models import LocationResult


class GeolocationProtocol(Protocol):
    """Driven port: reverse-geocode a coordinate into a structured location."""

    def reverse_geocode(self, lat: float, lon: float) -> LocationResult:
        """Return country, city, and address for the given coordinates."""
