"""Get reverse geolocation data for locations with lat/lon but missing city/country."""

from geolocation import models
from geolocation.application import ports


class GetReverseGeolocationUseCase:  # pylint: disable=too-few-public-methods
    """Use case for getting reverse geolocation data with lat/lon."""

    def __init__(self, geolocation_service: ports.IGeolocationService):
        """Initialize the use case."""
        self._geo_service = geolocation_service

    def execute(self, latitude: float, longitude: float) -> models.LocationResult:
        """Get reverse geolocation data for a location with lat/lon but missing city/country."""
        return self._geo_service.reverse_geocode(lat=latitude, lon=longitude)
