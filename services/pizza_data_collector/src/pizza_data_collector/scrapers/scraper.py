"""Edition scraper implementation for pizza data collector service."""

import pathlib

from bs4 import BeautifulSoup
from pizza_data_collector.application.ports.http_client import IHttpClient


class Scraper:  # pylint: disable=too-few-public-methods
    """Edition scraper implementation for pizza data collector service."""

    def __init__(self, http_client: IHttpClient) -> None:
        """Initializes the edition scraper with an HTTP client."""
        self._client = http_client

    def scrape(self, url: pathlib.Path) -> BeautifulSoup:
        """Scrapes the content of the given URL and returns a BeautifulSoup object."""
        html = self._client.fetch(url)
        return BeautifulSoup(html, features="html.parser")
