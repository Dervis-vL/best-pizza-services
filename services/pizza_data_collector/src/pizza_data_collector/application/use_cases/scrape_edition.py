"""Scrape edition url use case."""

from pizza_platform_shared import schemas as shared_schemas

from pizza_data_collector.application import ports
from pizza_data_collector import parsers, models

class ScrapeEditionUseCase:  # pylint: disable=too-few-public-methods
    """Scrape edition url use case."""

    def __init__(self, scraper: ports.IScraper):
        """Initialize the use case."""
        self._scraper = scraper

    def execute(
        self, edition: shared_schemas.EditionReadSchema) -> list[shared_schemas.PizzeriaSchema
    ]:
        """Execute the use case."""
        soup = self._scraper.scrape(url=edition.url)
        parser = parsers.EditionParser(
            card_patterns=models.card_patterns,
            url_pattern=models.url_pattern,
            position_patterns=models.ranking_position_patterns,
        )
        return parser.parse(soup=soup, edition_id=edition.id)
