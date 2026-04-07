"""Scrapers module for pizza data collection."""

from pizza_data_collector.scrapers.edition_scraper import EditionScraper
from pizza_data_collector.scrapers.http_client import HttpClient

__all__ = ["EditionScraper", "HttpClient"]
