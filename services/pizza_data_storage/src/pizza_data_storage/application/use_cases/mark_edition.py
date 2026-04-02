"""Mark edition as scraped use case."""

from pizza_data_storage.application import ports


class MarkEditionAsScrapedUseCase:  # pylint: disable=too-few-public-methods
    """Mark edition as scraped use case."""

    def __init__(self, ranking_repository: ports.IRankingsRepository) -> None:
        """Initialize the use case."""
        self._ranking_repository = ranking_repository

    def execute(self, edition_id: int) -> bool:
        """Execute the use case."""
        self._ranking_repository.mark_edition_scraped(edition_id=edition_id)
        return True
