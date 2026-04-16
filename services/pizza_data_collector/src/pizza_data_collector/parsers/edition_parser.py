"""Edition parser implementation for pizza data collector service."""

from bs4 import BeautifulSoup
from pizza_platform_shared import schemas

from pizza_data_collector import models, utils


class EditionParser:  # pylint: disable=too-few-public-methods
    """Parser for edition pages in pizza data collector service."""

    def __init__(
        self,
        card_patterns: models.CardPatterns,
        url_pattern: models.URLPatterns,
        position_patterns: models.RankingPositionPatterns,
        awards_patterns: models.AwardNamePatterns,
    ) -> None:
        """Initializes the edition parser with the necessary patterns."""
        self._cards = card_patterns
        self._urls = url_pattern
        self._positions = position_patterns
        self._awards = awards_patterns

    def parse(self, soup: BeautifulSoup, edition_id: int) -> list[schemas.PizzeriaSchema]:
        """Parses the edition page soup and returns structured data."""
        html_cards_list = self._cards.extract(html=str(soup))

        pizzerias: dict[str, schemas.PizzeriaSchema] = {}
        for card in html_cards_list:
            url = self._urls.extract(html=card)
            if url is None:
                continue

            slug = utils.extract_pizzeria_name(endpoint_path=url)

            # see if cards are for awards or ranking
            award_name = self._awards.extract(html=card)
            if award_name:
                award = self._awards.extract(html=card)
                if slug not in pizzerias:
                    pizzerias[slug] = schemas.PizzeriaSchema(
                        slug=slug,
                        rankings=[],
                        awards=[schemas.AwardsSchema(name=award, edition_id=edition_id)],
                        webpages=[schemas.WebpagesSchema(url=url, slug=slug)],
                    )
            else:
                position = self._positions.extract(html=card)
                if slug not in pizzerias:
                    pizzerias[slug] = schemas.PizzeriaSchema(
                        slug=slug,
                        rankings=[schemas.RankingSchema(position=position, edition_id=edition_id, awards=None)],
                        awards=[],
                        webpages=[schemas.WebpagesSchema(url=url, slug=slug)],
                    )
                else:
                    pizzerias[slug].rankings.append(
                        schemas.RankingSchema(position=position, edition_id=edition_id, awards=None)
                    )
                    pizzerias[slug].webpages.append(schemas.WebpagesSchema(url=url, slug=slug))

        return list(pizzerias.values())
