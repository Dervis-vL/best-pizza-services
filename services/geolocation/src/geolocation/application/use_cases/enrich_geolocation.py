"""Get reverse geolocation data for locations with lat/lon but missing city/country."""

from geolocation.application import ports
from pizza_platform_shared import schemas as shared_schemas


class EnrichGeolocationUseCase:  # pylint: disable=too-few-public-methods
    """Enrich a parsed location schema with reverse geolocation data."""

    def __init__(self, geolocation_service: ports.IGeolocationService):
        """Initialize the use case."""
        self._geo_service = geolocation_service

    def execute(
        self,
        location: shared_schemas.LocationSchema,
    ) -> shared_schemas.LocationSchema:
        """GReturn the location schema, enriched with city and country if missing."""
        needs_enrichment = (
            (location.latitude is not None)
            and (location.longitude is not None)
            and (location.city is None or location.country is None)
        )
        if not needs_enrichment:
            return location

        reverse_location = self._geo_service.reverse_geocode(
            lat=location.latitude,
            lon=location.longitude,
        )
        location.country = reverse_location.country
        location.city = reverse_location.city
        return location
