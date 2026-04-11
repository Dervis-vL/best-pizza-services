"""Scrape edition url use case."""

import pathlib

from bs4 import BeautifulSoup

from pizza_data_collector.application import ports


class ScrapeEditionUseCase:  # pylint: disable=too-few-public-methods
    """Scrape edition url use case."""

    def __init__(self, scraper: ports.IScraper):
        """Initialize the use case."""
        self._scraper = scraper

    def execute(self, edition_url: pathlib.Path) -> BeautifulSoup:
        """Execute the use case."""
        return self._scraper.scrape(url=edition_url)
