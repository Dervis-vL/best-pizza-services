"""Pizza parser implementation for pizza data collector service."""

from bs4 import BeautifulSoup

from pizza_data_collector.models.parser.patterns import (
    AddressPatterns,
    CoordPatterns,
    PhonePatterns,
)
from pizza_platform_shared.schemas import LocationSchema


class PizzeriaParser:  # pylint: disable=too-few-public-methods
    """Parser for pizzeria pages in pizza data collector service."""

    def __init__(
        self,
        coord_patterns: CoordPatterns,
        address_patterns: AddressPatterns,
        phone_patterns: PhonePatterns,
    ) -> None:
        """Initializes the pizzeria parser with the necessary patterns."""
        self._coords = coord_patterns
        self._addresses = address_patterns
        self._phones = phone_patterns

    def parse(self, soup: BeautifulSoup, pizzeria_id: int) -> LocationSchema:
        """Parses the pizzeria page soup and returns structured location data."""
        html = str(soup)
        coords = self._coords.extract(html)
        address = self._addresses.extract(html)
        phone = self._phones.extract(html)

        return LocationSchema(
            pizzaria_id=pizzeria_id,
            address=address,
            city=None,
            country=None,
            latitude=coords[0],
            longitude=coords[1],
            phone=phone,
        )
