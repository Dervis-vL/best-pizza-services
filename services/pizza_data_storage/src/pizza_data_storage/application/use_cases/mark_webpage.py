"""Mark webpage as scraped use case."""

from pizza_data_storage.application import ports


class MarkWebpageAsScrapedUseCase:
    """Mark webpage as scraped use case."""

    def __init__(self, pizza_repository: ports.IPizzeriaRepository) -> None:
        """Initialize the use case."""
        self._pizza_repository = pizza_repository

    def execute(self, webpage_id: int) -> bool:
        """Execute the use case."""
        self._pizza_repository.mark_webpage_scraped(webpage_id=webpage_id)
        return True
