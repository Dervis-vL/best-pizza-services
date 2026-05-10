"""Parse all unparsed editions use case."""

import logging

from pizza_api.application import results
from pizza_data_collector.application import use_cases as collector_use_cases
from pizza_data_storage.application import use_cases as storage_use_cases

logger = logging.getLogger(__name__)

_MIN_PIZZERIAS_THRESHOLD = 35


class ParseEditionsUseCase:  # pylint: disable=too-few-public-methods
    """Parse stored HTML for every unparsed edition and seed the resulting pizzerias."""

    def __init__(
        self,
        get_editions_uc: storage_use_cases.GetEditionsUseCase,
        get_html_uc: storage_use_cases.GetEditionHtmlUseCase,
        parse_edition_uc: collector_use_cases.ParseEditionUseCase,
        mark_parsed_uc: storage_use_cases.MarkEditionAsParsedUseCase,
        seed_pizzerias_uc: storage_use_cases.SeedPizzeriasWebpagesRatingsUseCase,
    ) -> None:
        """Initialize the use case."""
        self._get_editions_uc = get_editions_uc
        self._get_html_uc = get_html_uc
        self._parse_edition_uc = parse_edition_uc
        self._mark_parsed_uc = mark_parsed_uc
        self._seed_pizzerias_uc = seed_pizzerias_uc

    def execute(self) -> results.ParseEditionsResult:
        """Execute the use case."""
        unparsed = self._get_editions_uc.execute(only_unparsed=True)
        unscraped_ids = [
            edition.id for edition in self._get_editions_uc.execute(only_unscraped=True)
        ]
        # Tracker for response
        parsed, skipped, failed = 0, 0, 0
        for edition in unparsed:
            if edition.id in unscraped_ids:
                skipped += 1
                continue

            soup = self._get_html_uc.execute(model_id=edition.id)
            pizzerias = self._parse_edition_uc.execute(soup=soup, edition_id=edition.id)

            if not pizzerias:
                logger.warning("No pizzerias parsed for edition %s", edition.id)
                failed += 1
                continue

            if len(pizzerias) < _MIN_PIZZERIAS_THRESHOLD:
                logger.warning(
                    "Only %s pizzerias parsed for edition %s",
                    len(pizzerias),
                    edition.id,
                )
                failed += 1
                continue

            self._seed_pizzerias_uc.execute(config_schema=pizzerias)
            self._mark_parsed_uc.execute(edition_id=edition.id)
            parsed += 1

        return results.ParseEditionsResult(
            parsed=parsed,
            skipped=skipped,
            failed=failed,
        )
