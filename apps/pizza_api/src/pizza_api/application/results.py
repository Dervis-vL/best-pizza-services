"""Pizza API use case dataclasses."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ScrapeEditionsResult:
    """Result of scraping all unscraped editions."""

    scraped: int
    failed: int


@dataclass
class ParseEditionsResult:
    """Result of parsing all unparsed editions."""

    parsed: int
    skipped: int  # HTML not in storage yet
    failed: int = 0  # Parsed but yielded too few results; not marked as parsed


@dataclass
class ScrapeWebpagesResult:
    """Result of scraping all unscraped pizzeria webpages."""

    scraped: int
    failed: int


@dataclass
class ParseWebpagesResult:
    """Result of parsing all unparsed pizzeria webpages."""

    parsed: int
    skipped: int  # HTML not in storage yet
    failed: int = 0


@dataclass
class AddCategoryResult:
    """Result summary of a full add-category cycle."""

    editions_scraped: ScrapeEditionsResult
    editions_parsed: ParseEditionsResult
    webpages_scraped: ScrapeWebpagesResult
    webpages_parsed: ParseWebpagesResult


@dataclass
class ProcessPendingResult:
    """Result summary of a pending-items processing run."""

    editions_scraped: ScrapeEditionsResult
    editions_parsed: ParseEditionsResult
    webpages_scraped: ScrapeWebpagesResult
    webpages_parsed: ParseWebpagesResult
