"""Scrape url use case."""

import pathlib

from bs4 import BeautifulSoup

from pizza_data_collector.application import ports


class ScrapeUseCase:  # pylint: disable=too-few-public-methods
    """Scrape url use case."""

    def __init__(self, scraper: ports.IScraper) -> None:
        """Initialize the use case."""
        self._scraper = scraper

    def execute(self, url: pathlib.Path) -> BeautifulSoup:
        """Execute the use case."""
        return self._scraper.scrape(url=url)
