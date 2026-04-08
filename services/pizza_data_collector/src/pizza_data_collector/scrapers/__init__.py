"""Scrapers module for pizza data collection."""

from pizza_data_collector.scrapers.http_client import HttpClient
from services.pizza_data_collector.src.pizza_data_collector.scrapers.scraper import (
    Scraper,
)

__all__ = ["Scraper", "HttpClient"]
