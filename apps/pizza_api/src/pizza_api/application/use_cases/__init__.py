"""Application use cases for the pizza API."""

from pizza_api.application.use_cases.add_category import AddCategoryResult, AddCategoryUseCase
from pizza_api.application.use_cases.parse_editions import ParseEditionsResult, ParseEditionsUseCase
from pizza_api.application.use_cases.parse_webpages import ParseWebpagesResult, ParseWebpagesUseCase
from pizza_api.application.use_cases.process_pending import ProcessPendingResult, ProcessPendingUseCase
from pizza_api.application.use_cases.scrape_editions import ScrapeEditionsResult, ScrapeEditionsUseCase
from pizza_api.application.use_cases.scrape_webpages import ScrapeWebpagesResult, ScrapeWebpagesUseCase

__all__ = [
    "AddCategoryUseCase",
    "AddCategoryResult",
    "ParseEditionsUseCase",
    "ParseEditionsResult",
    "ParseWebpagesUseCase",
    "ParseWebpagesResult",
    "ProcessPendingUseCase",
    "ProcessPendingResult",
    "ScrapeEditionsUseCase",
    "ScrapeEditionsResult",
    "ScrapeWebpagesUseCase",
    "ScrapeWebpagesResult",
]
