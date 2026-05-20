"""Edition scraper interface for pizza data collector service."""

from typing import Protocol

from bs4 import BeautifulSoup


class IScraper(Protocol):  # pylint: disable=too-few-public-methods
    """Interface for scraper used in pizza data collector service."""

    def scrape(self, url: str) -> BeautifulSoup | None:
        """Scrapes the content of the given URL and returns a BeautifulSoup object."""
