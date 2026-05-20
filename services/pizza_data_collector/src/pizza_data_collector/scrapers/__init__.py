"""Scrapers module for pizza data collection."""

from pizza_data_collector.scrapers.http_client import HttpClient
from pizza_data_collector.scrapers.scraper import Scraper

__all__ = ["HttpClient", "Scraper"]
