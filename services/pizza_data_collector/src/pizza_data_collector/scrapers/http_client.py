"""HTTP client implementation for pizza data collector service."""

import logging
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import urlopen

from pizza_data_collector.exceptions import URLExtractionError

logger = logging.getLogger(__name__)


class HttpClient:  # pylint: disable=too-few-public-methods
    """HTTP client implementation for pizza data collector service."""

    def __init__(self, timeout: int = 10) -> None:
        """Initializes the HTTP client with an optional timeout."""
        self._timeout = timeout

    def fetch(self, url: str) -> Any | None:
        """Fetches the content of the given URL."""
        try:
            parsed_url = urlsplit(url)
            if parsed_url.scheme not in ("http", "https"):
                raise ValueError(f"Unsupported URL schema: {parsed_url.scheme!r}")
            with urlopen(url, timeout=self._timeout) as response:  # noqa: S310
                return response.read()
        except HTTPError as e:
            logger.warning("HTTP %s fetching %s", e.code, url)
        except URLError as e:
            logger.warning("URL error fetching %s: %s", url, e.reason)
        except TimeoutError as e:
            logger.warning("Timeout fetching %s", url)
            raise URLExtractionError(f"Timeout fetching {url}") from e
        return None
