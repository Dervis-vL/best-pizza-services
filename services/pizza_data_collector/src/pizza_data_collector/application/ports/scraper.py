"""Edition scraper interface for pizza data collector service."""

import pathlib

from typing import Protocol
from bs4 import BeautifulSoup


class IScraper(Protocol):  # pylint: disable=too-few-public-methods
    """Interface for scraper used in pizza data collector service."""

    def scrape(self, url: pathlib.Path) -> BeautifulSoup:
        """Scrapes the content of the given URL and returns a BeautifulSoup object."""
