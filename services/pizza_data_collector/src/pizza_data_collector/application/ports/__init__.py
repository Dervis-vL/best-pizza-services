"""Ports layer for pizza data collector application."""

from pizza_data_collector.application.ports.parser import (
    IEditionParser,
    IPizzaParser,
)
from pizza_data_collector.application.ports.scraper import (
    IScraper,
)
from pizza_data_collector.application.ports.http_client import IHttpClient

__all__ = ["IScraper", "IHttpClient", "IEditionParser", "IPizzaParser"]
