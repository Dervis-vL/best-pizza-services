"""Use cases for pizza data storage service."""

from pizza_data_storage.application.use_cases.get_editions import GetEditionsUseCase
from pizza_data_storage.application.use_cases.get_pizzerias import GetPizzeriasUseCase
from pizza_data_storage.application.use_cases.get_webpages import GetWebpagesUseCase
from pizza_data_storage.application.use_cases.mark_edition import (
    MarkEditionAsParsedUseCase,
    MarkEditionAsScrapedUseCase,
)
from pizza_data_storage.application.use_cases.mark_webpage import (
    MarkWebpageAsParsedUseCase,
    MarkWebpageAsScrapedUseCase,
)
from pizza_data_storage.application.use_cases.seed_categories_editions import (
    SeedCategoriesAndEditionsUseCase,
)
from pizza_data_storage.application.use_cases.seed_location import SeedLocationUseCase
from pizza_data_storage.application.use_cases.seed_pizzerias_webpages_rating import (
    SeedPizzeriasWebpagesRatingsUseCase,
)
from pizza_data_storage.application.use_cases.use_edition_storage import (
    EditionHtmlExistsUseCase,
    GetEditionHtmlUseCase,
    ListEditionKeysUseCase,
    StoreEditionHtmlUseCase,
)
from pizza_data_storage.application.use_cases.use_webpage_storage import (
    GetWebpageHtmlUseCase,
    ListWebpageKeysUseCase,
    StoreWebpageHtmlUseCase,
    WebpageHtmlExistsUseCase,
)

__all__ = [
    "EditionHtmlExistsUseCase",
    "GetEditionHtmlUseCase",
    "GetEditionsUseCase",
    "GetPizzeriasUseCase",
    "GetWebpageHtmlUseCase",
    "GetWebpagesUseCase",
    "ListEditionKeysUseCase",
    "ListWebpageKeysUseCase",
    "MarkEditionAsParsedUseCase",
    "MarkEditionAsScrapedUseCase",
    "MarkWebpageAsParsedUseCase",
    "MarkWebpageAsScrapedUseCase",
    "SeedCategoriesAndEditionsUseCase",
    "SeedLocationUseCase",
    "SeedPizzeriasWebpagesRatingsUseCase",
    "StoreEditionHtmlUseCase",
    "StoreWebpageHtmlUseCase",
    "WebpageHtmlExistsUseCase",
]
