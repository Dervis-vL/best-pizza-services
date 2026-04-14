"""Use cases for pizza data storage service."""

from pizza_data_storage.application.use_cases.seed_categories_editions import (
    SeedCategoriesAndEditionsUseCase
)
from pizza_data_storage.application.use_cases.seed_pizzerias_webpages_rankings import (
    SeedPizzeriasWebpagesRankingsUseCase
)
from pizza_data_storage.application.use_cases.seed_location import (
    SeedLocationUseCase
)
from pizza_data_storage.application.use_cases.get_unscraped_webpages import (
    GetUnscrapedWebpagesUseCase
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
    "SeedPizzeriasWebpagesRankingsUseCase",
    "SeedLocationUseCase",
    "GetUnscrapedEditionsUseCase",
    "GetUnscrapedWebpagesUseCase",
    "MarkEditionAsScrapedUseCase",
    "MarkWebpageAsScrapedUseCase",
]
