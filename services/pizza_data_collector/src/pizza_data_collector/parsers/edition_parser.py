"""Edition parser implementation for pizza data collector service."""

from bs4 import BeautifulSoup
from pizza_platform_shared.schemas import (
    PizzeriaSchema,
    RankingSchema,
    WebpagesSchema,
)

from pizza_data_collector import utils
from pizza_data_collector.models.parser.patterns import (
    CardPatterns,
    RankingPositionPatterns,
    URLPatterns,
)


class EditionParser:  # pylint: disable=too-few-public-methods
    """Parser for edition pages in pizza data collector service."""

    def __init__(
        self,
        card_patterns: CardPatterns,
        url_pattern: URLPatterns,
        position_patterns: RankingPositionPatterns,
    ) -> None:
        """Initializes the edition parser with the necessary patterns."""
        self._cards = card_patterns
        self._urls = url_pattern
        self._positions = position_patterns

    def parse(self, soup: BeautifulSoup, edition_id: int) -> list[PizzeriaSchema]:
        """Parses the edition page soup and returns structured data."""
        html_cards_list = self._cards.extract(html=str(soup))

        pizzerias: dict[str, PizzeriaSchema] = {}
        for card in html_cards_list:
            url = self._urls.extract(html=card)
            if url is None:
                continue

            slug = utils.extract_pizzeria_name(endpoint_path=url)
            position = self._positions.extract(html=card)

            if slug not in pizzerias:
                pizzerias[slug] = PizzeriaSchema(
                    slug=slug,
                    rankings=[RankingSchema(position=position, edition_id=edition_id, awards=None)],
                    webpages=[WebpagesSchema(url=url, slug=slug)],
                )
            else:
                pizzerias[slug].rankings.append(
                    RankingSchema(position=position, edition_id=edition_id, awards=None)
                )
                pizzerias[slug].webpages.append(WebpagesSchema(url=url, slug=slug))

        return list(pizzerias.values())
