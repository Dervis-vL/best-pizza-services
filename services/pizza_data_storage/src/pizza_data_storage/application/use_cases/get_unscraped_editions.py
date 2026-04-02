"""Get unscraped editions use case."""

from pizza_platform_shared import schemas as shared_schemas

from pizza_data_storage.application import ports


class GetUnscrapedEditionsUseCase:  # pylint: disable=too-few-public-methods
    """Get unscraped editions use case."""

    def __init__(self, ranking_repository: ports.IRankingsRepository):
        """Initialize the use case."""
        self._ranking_repository = ranking_repository

    def execute(self, *, only_unscraped: bool = True) -> list[shared_schemas.EditionSchema]:
        """Execute the use case."""
        editions_models = self._ranking_repository.get_editions(only_unscraped=only_unscraped)
        return [shared_schemas.EditionSchema.model_validate(
            edition, from_attributes=True
        ) for edition in editions_models]
