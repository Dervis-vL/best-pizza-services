"""Process all unscraped and unparsed items use case."""

from pizza_api.application import use_cases, results


class ProcessPendingUseCase:  # pylint: disable=too-few-public-methods
    """Retry all unscraped and unparsed editions and webpages already in the database."""

    def __init__(
        self,
        scrape_editions_uc: use_cases.ScrapeEditionsUseCase,
        parse_editions_uc: use_cases.ParseEditionsUseCase,
        scrape_webpages_uc: use_cases.ScrapeWebpagesUseCase,
        parse_webpages_uc: use_cases.ParseWebpagesUseCase,
    ) -> None:
        """Initialize the use case."""
        self._scrape_editions_uc = scrape_editions_uc
        self._parse_editions_uc = parse_editions_uc
        self._scrape_webpages_uc = scrape_webpages_uc
        self._parse_webpages_uc = parse_webpages_uc

    def execute(self) -> results.ProcessPendingResult:
        """Execute the use case."""
        return results.ProcessPendingResult(
            editions_scraped=self._scrape_editions_uc.execute(),
            editions_parsed=self._parse_editions_uc.execute(),
            webpages_scraped=self._scrape_webpages_uc.execute(),
            webpages_parsed=self._parse_webpages_uc.execute(),
        )
