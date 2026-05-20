"""Edition scraper implementation for pizza data collector service."""

from bs4 import BeautifulSoup

from pizza_data_collector.application.ports.http_client import IHttpClient


class Scraper:  # pylint: disable=too-few-public-methods
    """Scraper implementation for pizza data collector service."""

    def __init__(self, http_client: IHttpClient) -> None:
        """Initializes the edition scraper with an HTTP client."""
        self._client = http_client

    def scrape(self, url: str) -> BeautifulSoup | None:
        """Scrapes the content of the given URL and returns a BeautifulSoup object."""
        html = self._client.fetch(url)
        if html is None:
            return None
        return BeautifulSoup(html, features="html.parser")
