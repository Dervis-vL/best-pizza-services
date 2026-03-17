"""Geolocation service: reverse-geocodes lat/lon via Nominatim (OpenStreetMap).

Nominatim is completely free with no API token required.
Hard rate limit: 1 request/second — enforced here to stay compliant.
Attribution requirement: must display "© OpenStreetMap contributors" where results are shown.

Docs: https://nominatim.org/release-docs/latest/api/Reverse/
"""

import json
import time
import urllib.parse
import urllib.request
from urllib.error import HTTPError, URLError

import yarl

from geolocation import constants, models


class GeolocationService:
    """Reverse-geocoding adapter backed by Nominatim (OpenStreetMap).

    Usage::

        service = GeolocationService(user_agent="best-pizza-services/1.0")
        result = service.reverse_geocode(lat=41.9028, lon=12.4964)
        # LocationResult(country='Italy', city='Rome', address='...')
    """

    _BASE_URL: yarl.URL = constants.GeoLocationConstants.BASE_URL
    _MIN_INTERVAL: float = constants.GeoLocationConstants.MIN_INTERVAL

    def __init__(self, user_agent: str) -> None:
        """
        :param user_agent: Identifies your app to Nominatim (required by their policy).
                           Use something like "best-pizza-services/1.0 contact@example.com".
        """
        self._user_agent = user_agent
        self._last_request_at: float = 0.0

    def reverse_geocode(self, lat: float, lon: float) -> models.LocationResult:
        """Return country, city, and full display address for the given coordinates.

        :raises RuntimeError: If the API returns an unexpected response.
        :raises urllib.error.HTTPError: On non-2xx HTTP responses.
        :raises urllib.error.URLError: On network errors.
        """
        self._throttle()
        data = self._fetch(lat=lat, lon=lon)
        return self._parse(data)

    def _throttle(self) -> None:
        elapsed = time.monotonic() - self._last_request_at
        if elapsed < self._MIN_INTERVAL:
            time.sleep(self._MIN_INTERVAL - elapsed)
        self._last_request_at = time.monotonic()

    def _fetch(self, lat: float, lon: float) -> dict:
        params = urllib.parse.urlencode({"lat": lat, "lon": lon, "format": "json"})
        url_str = f"{self._BASE_URL}?{params}"
        req = urllib.request.Request(
            url_str, 
            headers={"User-Agent": self._user_agent, "Accept-Language": "en"},
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read())
        except HTTPError as e:
            raise HTTPError(e.url, e.code, f"Nominatim error for ({lat}, {lon}): {e.reason}", e.headers, e.fp)
        except URLError as e:
            raise URLError(f"Failed to reach Nominatim for ({lat}, {lon}): {e.reason}")

    @staticmethod
    def _parse(data: dict) -> models.LocationResult:
        if "error" in data:
            raise RuntimeError(f"Nominatim returned an error: {data['error']}")

        addr = data.get("address", {})
        city = (
            addr.get("city")
            or addr.get("town")
            or addr.get("village")
            or addr.get("municipality")
            or ""
        )
        return models.LocationResult(
            country=addr.get("country", ""),
            city=city,
            address=data.get("display_name", ""),
        )
