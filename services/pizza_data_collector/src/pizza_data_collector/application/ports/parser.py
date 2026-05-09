"""Edition parser interface for pizza data collector service."""

from typing import Protocol

from bs4 import BeautifulSoup

from pizza_platform_shared import schemas as shared_schemas


class IEditionParser(Protocol):  # pylint: disable=too-few-public-methods
    """Interface for parser used in pizza data collector service."""

    def parse(
        self, soup: BeautifulSoup, edition_id: str
    ) -> list[shared_schemas.PizzeriaSchema]:
        """Parses the soup object and returns a list of pizzeria schemas."""


class IPizzaParser(Protocol):  # pylint: disable=too-few-public-methods
    """Interface for parser used in pizza data collector service."""

    def parse(
        self, soup: BeautifulSoup, pizzeria_id: str
    ) -> shared_schemas.LocationSchema:
        """Parses the soup object and returns a list of location schemas."""
