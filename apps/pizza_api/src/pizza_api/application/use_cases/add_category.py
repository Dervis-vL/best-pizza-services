"""Add a new category and run the full scrape + parse cycle use case."""

from dataclasses import dataclass

from pizza_data_storage.application import use_cases as storage_use_cases
from pizza_platform_shared import schemas as shared_schemas

from pizza_api.application.use_cases.parse_editions import ParseEditionsResult, ParseEditionsUseCase
from pizza_api.application.use_cases.parse_webpages import ParseWebpagesResult, ParseWebpagesUseCase
from pizza_api.application.use_cases.scrape_editions import (
    ScrapeEditionsResult,
    ScrapeEditionsUseCase
)
from pizza_api.application.use_cases.scrape_webpages import (
    ScrapeWebpagesResult,
    ScrapeWebpagesUseCase
)


@dataclass
class AddCategoryResult:
    """Result summary of a full add-category cycle."""

    editions_scraped: ScrapeEditionsResult
    editions_parsed: ParseEditionsResult
    webpages_scraped: ScrapeWebpagesResult
    webpages_parsed: ParseWebpagesResult


class AddCategoryUseCase:
    """Seed a new category and run the full scrape + parse cycle."""

    def __init__(
        self,
        seed_uc: storage_use_cases.SeedCategoriesAndEditionsUseCase,
        scrape_editions_uc: ScrapeEditionsUseCase,
        parse_editions_uc: ParseEditionsUseCase,
        scrape_webpages_uc: ScrapeWebpagesUseCase,
        parse_webpages_uc: ParseWebpagesUseCase,
    ) -> None:
        """Initialize the use case."""
        self._seed_uc = seed_uc
        self._scrape_editions_uc = scrape_editions_uc
        self._parse_editions_uc = parse_editions_uc
        self._scrape_webpages_uc = scrape_webpages_uc
        self._parse_webpages_uc = parse_webpages_uc

    def execute(self, category_schemas: list[shared_schemas.CategorySchema]) -> AddCategoryResult:
        """Seed categories and editions, then run the full scrape + parse cycle."""
        self._seed_uc.execute(category_schemas=category_schemas)
        return AddCategoryResult(
            editions_scraped=self._scrape_editions_uc.execute(),
            editions_parsed=self._parse_editions_uc.execute(),
            webpages_scraped=self._scrape_webpages_uc.execute(),
            webpages_parsed=self._parse_webpages_uc.execute(),
        )
