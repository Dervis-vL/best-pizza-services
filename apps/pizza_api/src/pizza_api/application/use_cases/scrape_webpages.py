"""Scrape all unscraped pizzeria webpages use case."""

from pizza_data_collector.application import use_cases as collector_use_cases
from pizza_data_storage.application import use_cases as storage_use_cases

from pizza_api.application import results


class ScrapeWebpagesUseCase:  # pylint: disable=too-few-public-methods
    """Fetch and store HTML for every unscraped pizzeria webpage."""

    def __init__(
        self,
        get_webpages_uc: storage_use_cases.GetWebpagesUseCase,
        scrape_uc: collector_use_cases.ScrapeUseCase,
        store_html_uc: storage_use_cases.StoreWebpageHtmlUseCase,
        mark_scraped_uc: storage_use_cases.MarkWebpageAsScrapedUseCase,
    ) -> None:
        """Initialize the use case."""
        self._get_webpages_uc = get_webpages_uc
        self._scrape_uc = scrape_uc
        self._store_html_uc = store_html_uc
        self._mark_scraped_uc = mark_scraped_uc

    def execute(self) -> results.ScrapeWebpagesResult:
        """Execute the use case."""
        unscraped_list = self._get_webpages_uc.execute(only_unscraped=True)
        scraped, failed = 0, 0
        for webpage in unscraped_list:
            soup = self._scrape_uc.execute(url=webpage.url)
            if soup is None:
                failed += 1
                continue
            self._store_html_uc.execute(soup=soup, model_id=webpage.id)
            self._mark_scraped_uc.execute(webpage_id=webpage.id)
            scraped += 1
        return results.ScrapeWebpagesResult(scraped=scraped, failed=failed)
