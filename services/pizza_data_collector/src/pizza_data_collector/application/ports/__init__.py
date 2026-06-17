"""Ports layer for pizza data collector application."""

from pizza_data_collector.application.ports.http_client import IHttpClient
from pizza_data_collector.application.ports.parser import (
    IEditionParser,
    IPizzaParser,
)
from pizza_data_collector.application.ports.scraper import (
    IScraper,
)

__all__ = ["IEditionParser", "IHttpClient", "IPizzaParser", "IScraper"]
