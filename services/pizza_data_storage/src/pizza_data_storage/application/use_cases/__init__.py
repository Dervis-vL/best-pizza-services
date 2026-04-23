"""Use cases for pizza data storage service."""

from pizza_data_storage.application.use_cases.seed_categories_editions import (
    SeedCategoriesAndEditionsUseCase
)
from pizza_data_storage.application.use_cases.seed_pizzerias_webpages_rating import (
    SeedPizzeriasWebpagesRatingsUseCase
)
from pizza_data_storage.application.use_cases.seed_location import (
    SeedLocationUseCase
)
from pizza_data_storage.application.use_cases.get_pizzerias import (
    GetPizzeriasUseCase
)
from pizza_data_storage.application.use_cases.get_webpages import (
    GetWebpagesUseCase
)
from pizza_data_storage.application.use_cases.get_editions import (
    GetEditionsUseCase
)
from pizza_data_storage.application.use_cases.mark_edition import (
    MarkEditionAsScrapedUseCase,
    MarkEditionAsParsedUseCase,
)
from pizza_data_storage.application.use_cases.mark_webpage import (
    MarkWebpageAsScrapedUseCase,
    MarkWebpageAsParsedUseCase,
)
from pizza_data_storage.application.use_cases.use_webpage_storage import (
    StoreWebpageHtmlUseCase,
    GetWebpageHtmlUseCase,
    WebpageHtmlExistsUseCase,
    ListWebpageKeysUseCase,
)
from pizza_data_storage.application.use_cases.use_edition_storage import (
    StoreEditionHtmlUseCase,
    GetEditionHtmlUseCase,
    EditionHtmlExistsUseCase,
    ListEditionKeysUseCase,
)

__all__ = [
    "SeedCategoriesAndEditionsUseCase",
    "SeedPizzeriasWebpagesRatingsUseCase",
    "SeedLocationUseCase",
    "GetEditionsUseCase",
    "GetPizzeriasUseCase",
    "GetWebpagesUseCase",
    "MarkEditionAsScrapedUseCase",
    "MarkEditionAsParsedUseCase",
    "MarkWebpageAsScrapedUseCase",
    "MarkWebpageAsParsedUseCase",
    "StoreWebpageHtmlUseCase",
    "GetWebpageHtmlUseCase",
    "WebpageHtmlExistsUseCase",
    "ListWebpageKeysUseCase",
    "StoreEditionHtmlUseCase",
    "GetEditionHtmlUseCase",
    "EditionHtmlExistsUseCase",
    "ListEditionKeysUseCase",
]
