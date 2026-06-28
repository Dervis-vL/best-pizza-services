"""Process all unscraped and unparsed items use case."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pizza_api.application import results

if TYPE_CHECKING:
    from pizza_api.application.use_cases.parse_editions import ParseEditionsUseCase
    from pizza_api.application.use_cases.parse_webpages import ParseWebpagesUseCase
    from pizza_api.application.use_cases.scrape_editions import ScrapeEditionsUseCase
    from pizza_api.application.use_cases.scrape_webpages import ScrapeWebpagesUseCase


class ProcessPendingUseCase:  # pylint: disable=too-few-public-methods
    """Retry all unscraped and unparsed editions/webpages already in the database."""

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

    def execute(self) -> results.ProcessPendingResult:
        """Execute the use case."""
        return results.ProcessPendingResult(
            editions_scraped=self._scrape_editions_uc.execute(),
            editions_parsed=self._parse_editions_uc.execute(),
            webpages_scraped=self._scrape_webpages_uc.execute(),
            webpages_parsed=self._parse_webpages_uc.execute(),
        )
