"""Add a new category and run the full scrape + parse cycle use case."""

from pizza_data_storage.application import use_cases as storage_use_cases
from pizza_platform_shared import schemas as shared_schemas

from pizza_api.application import use_cases, results


class AddCategoryUseCase:  # pylint: disable=too-few-public-methods
    """Seed a new category and run the full scrape + parse cycle."""

    def __init__(
        self,
        seed_uc: storage_use_cases.SeedCategoriesAndEditionsUseCase,
        scrape_editions_uc: use_cases.ScrapeEditionsUseCase,
        parse_editions_uc: use_cases.ParseEditionsUseCase,
        scrape_webpages_uc: use_cases.ScrapeWebpagesUseCase,
        parse_webpages_uc: use_cases.ParseWebpagesUseCase,
    ) -> None:
        """Initialize the use case."""
        self._seed_uc = seed_uc
        self._scrape_editions_uc = scrape_editions_uc
        self._parse_editions_uc = parse_editions_uc
        self._scrape_webpages_uc = scrape_webpages_uc
        self._parse_webpages_uc = parse_webpages_uc

    def execute(
        self, category_schemas: list[shared_schemas.CategorySchema]
    ) -> results.AddCategoryResult:
        """Seed categories and editions, then run the full scrape + parse cycle."""
        self._seed_uc.execute(category_schemas=category_schemas)
        return results.AddCategoryResult(
            editions_scraped=self._scrape_editions_uc.execute(),
            editions_parsed=self._parse_editions_uc.execute(),
            webpages_scraped=self._scrape_webpages_uc.execute(),
            webpages_parsed=self._parse_webpages_uc.execute(),
        )
