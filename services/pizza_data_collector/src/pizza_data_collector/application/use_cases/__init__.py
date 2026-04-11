"""Use cases for pizza data collector service."""

from pizza_data_collector.application.use_cases.scrape_edition import (
    ScrapeEditionUseCase
)
from pizza_data_collector.application.use_cases.parse_edition import (
    ParseEditionUseCase
)

__all__ = ["ParseEditionUseCase", "ScrapeEditionUseCase"]
