"""Edition scraper interface for pizza data collector service."""

from typing import Protocol
from bs4 import BeautifulSoup

class IEditionScraper(Protocol):  # pylint: disable=too-few-public-methods
    """Interface for edition scraper used in pizza data collector service."""

    def scrape(self, url: str) -> BeautifulSoup:
        """Scrapes the content of the given URL and returns a BeautifulSoup object."""
