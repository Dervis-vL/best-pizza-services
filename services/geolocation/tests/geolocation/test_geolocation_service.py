"""Tests for the geolocation service."""

from geolocation import logic, models


def test_reverse_geocode():
    """Test reverse geocoding for a known coordinate."""
    # GIVEN a geolocation service object
    service = logic.GeolocationService(user_agent="test-agent")
    # WHEN we reverse-geocode the Colosseum in Rome
    result = service.reverse_geocode(41.8902, 12.4922)
    # THEN we get the expected country, city, and address
    assert isinstance(result, models.LocationResult)
    assert result.country == "Italia"
    assert result.city == "Roma"
