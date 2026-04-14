"""Scrape pizzeria url use case."""

from bs4 import BeautifulSoup
from pizza_platform_shared import schemas as shared_schemas

from pizza_data_collector.application import ports


class ParsePizzeriaUseCase:  # pylint: disable=too-few-public-methods
    """Parse pizzeria data use case."""

    def __init__(self, parser: ports.IPizzaParser):
        """Initialize the use case."""
        self._parser = parser

    def execute(self, soup: BeautifulSoup, pizzeria_id: str) -> shared_schemas.LocationSchema:
        """Execute the use case."""
        return self._parser.parse(soup=soup, pizzeria_id=pizzeria_id)
