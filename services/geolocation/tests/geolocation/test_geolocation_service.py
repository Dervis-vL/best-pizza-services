"""Tests for the geolocation service."""

from unittest.mock import MagicMock, patch

import pytest

from geolocation import GeolocationService, models


COLOSSEUM_RESPONSE = {
    "display_name": "Colosseum, Via Sacra, Celio, Rome, Roma Capitale, Lazio, 00184, Italy",
    "address": {
        "city": "Rome",
        "country": "Italy",
        "country_code": "it",
        "postcode": "00184",
    },
}


@patch.object(GeolocationService, "_fetch", return_value=COLOSSEUM_RESPONSE)
def test_reverse_geocode(mock_fetch: MagicMock) -> None:
    service = GeolocationService(user_agent="test-agent")
    result = service.reverse_geocode(41.8902, 12.4922)

    mock_fetch.assert_called_once_with(lat=41.8902, lon=12.4922)
    assert isinstance(result, models.LocationResult)
    assert result.country == "Italy"
    assert result.city == "Rome"


@patch.object(GeolocationService, "_fetch", return_value={"error": "Unable to geocode"})
def test_reverse_geocode_nominatim_error(_mock_fetch: MagicMock) -> None:
    service = GeolocationService(user_agent="test-agent")
    with pytest.raises(RuntimeError, match="Nominatim returned an error"):
        service.reverse_geocode(0.0, 0.0)
