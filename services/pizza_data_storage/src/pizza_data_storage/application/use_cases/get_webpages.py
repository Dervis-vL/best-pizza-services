"""Get all, unscraped and/or unparsed webpages use case."""

from pizza_data_storage.application import ports
from pizza_platform_shared import schemas as shared_schemas


class GetWebpagesUseCase:  # pylint: disable=too-few-public-methods
    """Get (unscraped/unparsed) webpages use case."""

    def __init__(self, pizza_repository: ports.IPizzeriaRepository):
        """Initialize the use case."""
        self._pizza_repository = pizza_repository

    def execute(
        self,
        *,
        only_unscraped: bool = False,
        only_unparsed: bool = False,
    ) -> list[shared_schemas.WebpageReadSchema]:
        """Execute the use case."""
        webpages_models = self._pizza_repository.get_webpages(
            only_unscraped=only_unscraped,
            only_unparsed=only_unparsed,
        )
        return [
            shared_schemas.WebpageReadSchema.model_validate(
                webpage,
                from_attributes=True,
            )
            for webpage in webpages_models
        ]
