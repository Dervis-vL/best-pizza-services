"""Ports layer for pizza data collector application."""

from pizza_data_collector.application.ports.edition_scraper import IEditionScraper
from pizza_data_collector.application.ports.http_client import IHttpClient
from pizza_data_collector.application.ports.pizza_scraper import IPizzeriaScraper

__all__ = ["IEditionScraper", "IPizzeriaScraper", "IHttpClient"]
