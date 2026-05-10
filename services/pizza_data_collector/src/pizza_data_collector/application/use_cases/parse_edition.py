"""Scrape edition url use case."""

from bs4 import BeautifulSoup

from pizza_data_collector.application import ports
from pizza_platform_shared import schemas as shared_schemas


class ParseEditionUseCase:  # pylint: disable=too-few-public-methods
    """Parse edition data use case."""

    def __init__(self, parser: ports.IEditionParser) -> None:
        """Initialize the use case."""
        self._parser = parser

    def execute(
        self,
        soup: BeautifulSoup,
        edition_id: str,
    ) -> list[shared_schemas.PizzeriaSchema]:
        """Execute the use case."""
        return self._parser.parse(soup=soup, edition_id=edition_id)
