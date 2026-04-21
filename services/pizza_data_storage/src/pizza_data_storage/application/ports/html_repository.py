"""Repository protocols (ports) for dependency injection."""

from typing import Protocol


class IHtmlStorageRepository(Protocol):
    """Port for HTML object storage.

    Any class implementing these methods satisfies this protocol —
    including HtmlStorageRepository (Scaleway) and a MinIO or
    in-memory fake for local testing.
    """

    def save_edition_html(
        self,
        *,
        html: str,
        category_id: str,
        year: int,
    ) -> str:
        """."""

    def get_edition_html(self, *, key: str) -> str:
        """."""

    def list_edition_keys(
        self,
        *,
        category_id: str | None = None,
        year: int | None = None,
    ) -> list[str]:
        """."""

    def edition_html_exists(self, *, category_id: str, year: int) -> bool:
        """."""
