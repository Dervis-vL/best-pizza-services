"""Process all unscraped and unparsed items use case."""

from dataclasses import dataclass

from pizza_api.application.use_cases.parse_editions import ParseEditionsResult, ParseEditionsUseCase
from pizza_api.application.use_cases.parse_webpages import ParseWebpagesResult, ParseWebpagesUseCase
from pizza_api.application.use_cases.scrape_editions import ScrapeEditionsResult, ScrapeEditionsUseCase
from pizza_api.application.use_cases.scrape_webpages import ScrapeWebpagesResult, ScrapeWebpagesUseCase


@dataclass
class ProcessPendingResult:
    """Result summary of a pending-items processing run."""

    editions_scraped: ScrapeEditionsResult
    editions_parsed: ParseEditionsResult
    webpages_scraped: ScrapeWebpagesResult
    webpages_parsed: ParseWebpagesResult


class ProcessPendingUseCase:
    """Retry all unscraped and unparsed editions and webpages already in the database."""

    def __init__(
        self,
        scrape_editions_uc: ScrapeEditionsUseCase,
        parse_editions_uc: ParseEditionsUseCase,
        scrape_webpages_uc: ScrapeWebpagesUseCase,
        parse_webpages_uc: ParseWebpagesUseCase,
    ) -> None:
        """Initialize the use case."""
        self._scrape_editions_uc = scrape_editions_uc
        self._parse_editions_uc = parse_editions_uc
        self._scrape_webpages_uc = scrape_webpages_uc
        self._parse_webpages_uc = parse_webpages_uc

    def execute(self) -> ProcessPendingResult:
        """Execute the use case."""
        return ProcessPendingResult(
            editions_scraped=self._scrape_editions_uc.execute(),
            editions_parsed=self._parse_editions_uc.execute(),
            webpages_scraped=self._scrape_webpages_uc.execute(),
            webpages_parsed=self._parse_webpages_uc.execute(),
        )
