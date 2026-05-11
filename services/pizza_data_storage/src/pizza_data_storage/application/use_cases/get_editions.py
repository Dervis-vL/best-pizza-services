"""Get all, unscraped and/or unparsed editions use case."""

from pizza_data_storage.application import ports
from pizza_platform_shared import schemas as shared_schemas


class GetEditionsUseCase:  # pylint: disable=too-few-public-methods
    """Get (unscraped/unparsed) editions use case."""

    def __init__(self, ranking_repository: ports.IRankingsRepository) -> None:
        """Initialize the use case."""
        self._ranking_repository = ranking_repository

    def execute(
        self,
        *,
        only_unscraped: bool = False,
        only_unparsed: bool = False,
    ) -> list[shared_schemas.EditionReadSchema]:
        """Execute the use case."""
        editions_models = self._ranking_repository.get_editions(
            only_unscraped=only_unscraped,
            only_unparsed=only_unparsed,
        )
        return [
            shared_schemas.EditionReadSchema.model_validate(
                edition,
                from_attributes=True,
            )
            for edition in editions_models
        ]
