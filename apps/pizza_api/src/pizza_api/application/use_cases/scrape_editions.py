"""Scrape all unscraped editions use case."""

from dataclasses import dataclass

from pizza_data_collector.application import use_cases as collector_use_cases
from pizza_data_storage.application import use_cases as storage_use_cases


@dataclass
class ScrapeEditionsResult:
    """Result of scraping all unscraped editions."""

    scraped: int
    failed: int


class ScrapeEditionsUseCase:
    """Fetch and store HTML for every unscraped edition."""

    def __init__(
        self,
        get_editions_uc: storage_use_cases.GetEditionsUseCase,
        scrape_uc: collector_use_cases.ScrapeUseCase,
        store_html_uc: storage_use_cases.StoreEditionHtmlUseCase,
        mark_scraped_uc: storage_use_cases.MarkEditionAsScrapedUseCase,
    ) -> None:
        """Initialize the use case."""
        self._get_editions_uc = get_editions_uc
        self._scrape_uc = scrape_uc
        self._store_html_uc = store_html_uc
        self._mark_scraped_uc = mark_scraped_uc

    def execute(self) -> ScrapeEditionsResult:
        """Execute the use case."""
        unscraped = self._get_editions_uc.execute(only_unscraped=True)
        scraped, failed = 0, 0
        for edition in unscraped:
            soup = self._scrape_uc.execute(url=edition.url)
            if not soup:
                failed += 1
                continue
            self._store_html_uc.execute(soup=soup, model_id=edition.id)
            self._mark_scraped_uc.execute(edition_id=edition.id)
            scraped += 1
        return ScrapeEditionsResult(scraped=scraped, failed=failed)
