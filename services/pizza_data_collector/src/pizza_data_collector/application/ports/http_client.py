"""HTTP client interface for pizza data collector service."""

from typing import Protocol


class IHttpClient(Protocol):  # pylint: disable=too-few-public-methods
    """Interface for HTTP client used in pizza data collector service."""

    def fetch(self, url: str) -> bytes | None:
        """Fetches the content of the given URL."""
