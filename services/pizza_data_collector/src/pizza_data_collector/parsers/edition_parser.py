"""Edition parser implementation for pizza data collector service."""

from bs4 import BeautifulSoup

from pizza_data_collector import models, utils
from pizza_platform_shared import schemas


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

    def parse(
        self,
        soup: BeautifulSoup,
        edition_id: int,
    ) -> list[schemas.PizzeriaSchema]:
        """Parses the edition page soup and returns structured data."""
        html_cards_list = self._cards.extract(html=str(soup))

        pizzerias: dict[str, schemas.PizzeriaSchema] = {}
        for card in html_cards_list:
            # Extract data from card
            url = self._urls.extract(html=card)
            raw_award, sponsor = self._awards.extract(html=card)
            position = self._positions.extract(html=card)
            if url is None:
                continue

            award = utils.standardize_award_name(raw_award) if raw_award else None
            slug = utils.extract_pizzeria_name(endpoint_path=url)
            webpage_schema = schemas.WebpageSchema(url=url, slug=slug)

            if award is not None:
                award_schema = schemas.AwardSchema(
                    award=award,
                    sponsor=sponsor,
                    edition_id=edition_id,
                )
                if slug not in pizzerias:
                    pizzerias[slug] = schemas.PizzeriaSchema(
                        slug=slug,
                        awards=[award_schema],
                        webpages=[webpage_schema],
                    )
                else:
                    pizzerias[slug].awards.append(award_schema)
                    pizzerias[slug].webpages.append(webpage_schema)
            elif position is not None:
                ranking_schema = schemas.RankingSchema(
                    position=position,
                    edition_id=edition_id,
                )
                if slug not in pizzerias:
                    pizzerias[slug] = schemas.PizzeriaSchema(
                        slug=slug,
                        rankings=[ranking_schema],
                        webpages=[webpage_schema],
                    )
                else:
                    pizzerias[slug].rankings.append(ranking_schema)
                    pizzerias[slug].webpages.append(webpage_schema)
            elif slug not in pizzerias:
                pizzerias[slug] = schemas.PizzeriaSchema(
                    slug=slug,
                    webpages=[webpage_schema],
                )
            else:
                pizzerias[slug].webpages.append(webpage_schema)

        return list(pizzerias.values())
