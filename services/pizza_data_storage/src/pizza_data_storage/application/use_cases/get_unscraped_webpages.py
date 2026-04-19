"""Get unscraped webpages use case."""

from pizza_platform_shared import schemas as shared_schemas

from pizza_data_storage.application import ports


class GetUnscrapedWebpagesUseCase:  # pylint: disable=too-few-public-methods
    """Get unscraped webpages use case."""

    def __init__(self, pizza_repository: ports.IPizzeriaRepository):
        """Initialize the use case."""
        self._pizza_repository = pizza_repository

    def execute(self, *, only_unscraped: bool = True) -> list[shared_schemas.WebpageReadSchema]:
        """Execute the use case."""
        webpages_models = self._pizza_repository.get_webpages(only_unscraped=only_unscraped)
        return [shared_schemas.WebpageReadSchema.model_validate(
            webpage, from_attributes=True
        ) for webpage in webpages_models]
