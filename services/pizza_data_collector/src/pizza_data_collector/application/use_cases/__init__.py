"""Use cases for pizza data collector service."""

from pizza_data_collector.application.use_cases.parse_edition import ParseEditionUseCase
from pizza_data_collector.application.use_cases.parse_pizzeria import (
    ParsePizzeriaUseCase,
)
from pizza_data_collector.application.use_cases.scrape_url import ScrapeUseCase

__all__ = ["ParseEditionUseCase", "ParsePizzeriaUseCase", "ScrapeUseCase"]
