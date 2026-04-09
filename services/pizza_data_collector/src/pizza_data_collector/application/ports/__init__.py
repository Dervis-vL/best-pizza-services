"""Ports layer for pizza data collector application."""

from pizza_data_collector.application.ports.http_client import IHttpClient
from services.pizza_data_collector.src.pizza_data_collector.application.ports.scraper import (
    IScraper,
)

__all__ = ["IScraper", "IHttpClient"]
