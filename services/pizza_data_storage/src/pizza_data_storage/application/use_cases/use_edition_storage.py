"""Save, get, list and check existence of edition HTML use case."""

import logging

import bs4

from pizza_data_storage.application import ports
from pizza_platform_shared import enums as shared_enums

logger = logging.getLogger(__name__)


class StoreEditionHtmlUseCase:  # pylint: disable=too-few-public-methods
    """Store a scraped edition's HTML to object storage."""

    def __init__(self, html_repository: ports.IHtmlStorageRepository) -> None:
        """Initialize the use case."""
        self._html_repository = html_repository

    def execute(
        self,
        *,
        soup: bs4.BeautifulSoup,
        model_id: int,
    ) -> str | None:
        """Convert soup to HTML string and store it."""
        html = soup.prettify()
        return self._html_repository.save_html(
            html=html,
            model_id=model_id,
            model_name=shared_enums.HtmlModelName.EDITIONS,
        )


class GetEditionHtmlUseCase:  # pylint: disable=too-few-public-methods
    """Get a scraped edition's HTML from storage, as Beautifulsoup."""

    def __init__(self, html_repository: ports.IHtmlStorageRepository) -> None:
        """Initialize the use case."""
        self._html_repository = html_repository

    def execute(self, *, model_id: int) -> bs4.BeautifulSoup:
        """Get the edition's HTML string from storage as soup."""
        html = self._html_repository.get_html(
            model_name=shared_enums.HtmlModelName.EDITIONS,
            model_id=model_id,
        )
        return bs4.BeautifulSoup(html, "html.parser")


class EditionHtmlExistsUseCase:  # pylint: disable=too-few-public-methods
    """Check whether an edition's HTML already exists in storage."""

    def __init__(self, html_repository: ports.IHtmlStorageRepository) -> None:
        """Initialize the use case."""
        self._html_repository = html_repository

    def execute(self, *, model_id: int) -> bool:
        """Return True if the edition's HTML already exists in storage."""
        return self._html_repository.html_exists(
            model_id=model_id,
            model_name=shared_enums.HtmlModelName.EDITIONS,
        )


class ListEditionKeysUseCase:  # pylint: disable=too-few-public-methods
    """List stored edition HTML keys, optionally filtered."""

    def __init__(self, html_repository: ports.IHtmlStorageRepository) -> None:
        """Initialize the use case."""
        self._html_repository = html_repository

    def execute(self) -> list[str]:
        """List and return stored edition HTML keys."""
        return self._html_repository.list_keys(model_name=shared_enums.HtmlModelName.EDITIONS)
