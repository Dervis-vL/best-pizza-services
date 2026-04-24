"""Parse all unparsed editions use case."""

from dataclasses import dataclass

from pizza_data_collector.application import use_cases as collector_use_cases
from pizza_data_storage.application import use_cases as storage_use_cases


@dataclass
class ParseEditionsResult:
    """Result of parsing all unparsed editions."""

    parsed: int
    skipped: int  # HTML not in storage yet


class ParseEditionsUseCase:
    """Parse stored HTML for every unparsed edition and seed the resulting pizzerias."""

    def __init__(
        self,
        get_editions_uc: storage_use_cases.GetEditionsUseCase,
        html_exists_uc: storage_use_cases.EditionHtmlExistsUseCase,
        get_html_uc: storage_use_cases.GetEditionHtmlUseCase,
        parse_edition_uc: collector_use_cases.ParseEditionUseCase,
        mark_parsed_uc: storage_use_cases.MarkEditionAsParsedUseCase,
        seed_pizzerias_uc: storage_use_cases.SeedPizzeriasWebpagesRatingsUseCase,
    ) -> None:
        """Initialize the use case."""
        self._get_editions_uc = get_editions_uc
        self._html_exists_uc = html_exists_uc
        self._get_html_uc = get_html_uc
        self._parse_edition_uc = parse_edition_uc
        self._mark_parsed_uc = mark_parsed_uc
        self._seed_pizzerias_uc = seed_pizzerias_uc

    def execute(self) -> ParseEditionsResult:
        """Execute the use case."""
        unparsed = self._get_editions_uc.execute(only_unparsed=True)
        parsed, skipped = 0, 0
        for edition in unparsed:
            if not self._html_exists_uc.execute(model_id=edition.id):
                skipped += 1
                continue
            soup = self._get_html_uc.execute(model_id=edition.id)
            pizzerias = self._parse_edition_uc.execute(soup=soup, edition_id=edition.id)
            self._mark_parsed_uc.execute(edition_id=edition.id)
            self._seed_pizzerias_uc.execute(config_schema=pizzerias)
            parsed += 1
        return ParseEditionsResult(parsed=parsed, skipped=skipped)
