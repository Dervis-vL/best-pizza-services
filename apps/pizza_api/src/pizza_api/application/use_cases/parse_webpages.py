"""Parse all unparsed pizzeria webpages use case."""

import logging

from geolocation.application import use_cases as geo_use_cases
from pizza_data_collector.application import use_cases as collector_use_cases
from pizza_data_storage.application import use_cases as storage_use_cases

from pizza_api.application import results

logger = logging.getLogger(__name__)


class ParseWebpagesUseCase:  # pylint: disable=too-few-public-methods
    """Parse stored HTML for every unparsed webpage, enrich with geolocation, seed location."""

    def __init__(
        self,
        get_webpages_uc: storage_use_cases.GetWebpagesUseCase,
        get_html_uc: storage_use_cases.GetWebpageHtmlUseCase,
        parse_pizzeria_uc: collector_use_cases.ParsePizzeriaUseCase,
        enrich_geo_uc: geo_use_cases.EnrichGeolocationUseCase,
        mark_parsed_uc: storage_use_cases.MarkWebpageAsParsedUseCase,
        seed_location_uc: storage_use_cases.SeedLocationUseCase,
    ) -> None:
        """Initialize the use case."""
        self._get_webpages_uc = get_webpages_uc
        self._get_html_uc = get_html_uc
        self._parse_pizzeria_uc = parse_pizzeria_uc
        self._enrich_geo_uc = enrich_geo_uc
        self._mark_parsed_uc = mark_parsed_uc
        self._seed_location_uc = seed_location_uc

    def execute(self) -> results.ParseWebpagesResult:
        """Execute the use case."""
        unparsed = self._get_webpages_uc.execute(only_unparsed=True)
        unscraped_ids = [
            webpage.id for webpage in self._get_webpages_uc.execute(only_unscraped=True)
        ]
        # Tracker for response
        parsed, skipped, failed = 0, 0, 0
        for webpage in unparsed:
            if webpage.id in unscraped_ids:
                skipped += 1
                continue

            soup = self._get_html_uc.execute(model_id=webpage.id)
            location = self._parse_pizzeria_uc.execute(
                soup=soup, pizzeria_id=webpage.pizzeria_id
            )

            if not location:
                logger.warning("No location parsed for webpage %s", webpage.id)
                failed += 1
                continue

            enriched = self._enrich_geo_uc.execute(location=location)
            self._seed_location_uc.execute(location_config=enriched)
            self._mark_parsed_uc.execute(webpage_id=webpage.id)
            parsed += 1

        return results.ParseWebpagesResult(
            parsed=parsed, skipped=skipped, failed=failed
        )
