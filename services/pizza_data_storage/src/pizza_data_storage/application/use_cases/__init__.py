"""Use cases for pizza data storage service."""

from pizza_data_storage.application.use_cases.seed_categories_and_editions import (
    SeedCategoriesAndEditionsUseCase
)
from pizza_data_storage.application.use_cases.get_unscraped_editions import (
    GetUnscrapedEditionsUseCase
)
from pizza_data_storage.application.use_cases.mark_edition import (
    MarkEditionAsScrapedUseCase
)
from pizza_data_storage.application.use_cases.mark_webpage import (
    MarkWebpageAsScrapedUseCase
)

__all__ = [
    "SeedCategoriesAndEditionsUseCase",
    "GetUnscrapedEditionsUseCase", 
    "MarkEditionAsScrapedUseCase",
    "MarkWebpageAsScrapedUseCase",
]
