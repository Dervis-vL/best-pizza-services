"""Edition parser implementation for pizza data collector service."""

from bs4 import BeautifulSoup
from pizza_platform_shared.schemas import (
    PizzeriaEndpointsSchema,
    PizzeriaSchema,
    RankingSchema,
    WebpagesSchema,
)

from pizza_data_collector.models.parser.patterns import (
    CardPatterns,
    RankingPositionPatterns,
    URLPattern,
)


class EditionParser:  # pylint: disable=too-few-public-methods
    """Parser for edition pages in pizza data collector service."""

    def __init__(
        self,
        card_patterns: CardPatterns,
        url_pattern: URLPattern,
        position_patterns: RankingPositionPatterns,
    ) -> None:
        """Initializes the edition parser with the necessary patterns."""
        self._cards = card_patterns
        self._urls = url_pattern
        self._positions = position_patterns

    def parse(self, soup: BeautifulSoup, edition_id: int) -> PizzeriaEndpointsSchema:
        """Parses the edition page soup and returns structured data."""
        pizzerias: list[PizzeriaSchema] = []
        webpages: list[WebpagesSchema] = []
        rankings: list[RankingSchema] = []

        for card in soup.find_all("div", class_=self._cards.altezza_class):
            url = self._urls.extract(str(card))
            if url is None:
                continue

            slug = url.rstrip("/").split("/")[-1]
            position = self._positions.extract(str(card))

            pizzerias.append(PizzeriaSchema(slug=slug, rankings=[], webpages=[]))
            webpages.append(WebpagesSchema(url=url, slug=slug))
            rankings.append(
                RankingSchema(position=position, edition_id=edition_id, awards=None)
            )

        return PizzeriaEndpointsSchema(
            pizzerias=pizzerias, webpages=webpages, rankings=rankings
        )
