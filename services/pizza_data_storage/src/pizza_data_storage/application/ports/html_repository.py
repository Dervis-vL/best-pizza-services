"""Repository protocols (ports) for dependency injection."""

from typing import Protocol

from pizza_platform_shared import enums as shared_enums


class IHtmlStorageRepository(Protocol):
    """Port for HTML object storage.

    Any class implementing these methods satisfies this protocol —
    including HtmlStorageRepository (Scaleway) and a MinIO or
    in-memory fake for local testing.
    """

    def save_html(
        self,
        *,
        html: str,
        model_id: int,
        model_name: shared_enums.HtmlModelName,
    ) -> str:
        """Store an HTML string in Glacier object storage."""

    def get_html(self, *, model_name: shared_enums.HtmlModelName, model_id: int) -> str:
        """Retrieve an HTML string from object storage."""

    def list_keys(
        self,
        *,
        model_name: shared_enums.HtmlModelName | None = None,
    ) -> list[str]:
        """List stored HTML keys, optionally filtered by category or year."""

    def html_exists(self, *, model_id: int, model_name: shared_enums.HtmlModelName) -> bool:
        """Check whether an HTML file already exists in storage."""
