"""Application use cases for the pizza API."""

from pizza_api.application.use_cases.add_category import AddCategoryUseCase
from pizza_api.application.use_cases.parse_editions import ParseEditionsUseCase
from pizza_api.application.use_cases.parse_webpages import ParseWebpagesUseCase
from pizza_api.application.use_cases.process_pending import ProcessPendingUseCase
from pizza_api.application.use_cases.scrape_editions import ScrapeEditionsUseCase
from pizza_api.application.use_cases.scrape_webpages import ScrapeWebpagesUseCase

__all__ = [
    "AddCategoryUseCase",
    "ParseEditionsUseCase",
    "ParseWebpagesUseCase",
    "ProcessPendingUseCase",
    "ScrapeEditionsUseCase",
    "ScrapeWebpagesUseCase",
]
