"""HTTP client implementation for pizza data collector service."""

import logging
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

    def fetch(self, url: str) -> bytes | None:
        """Fetches the content of the given URL."""
        try:
            parsed_url = urlsplit(url)
            if parsed_url.scheme not in ("http", "https"):
                msg = f"Unsupported URL schema: {parsed_url.scheme!r}"
                raise ValueError(msg)
            with urlopen(url, timeout=self._timeout) as response:  # noqa: S310
                content: bytes = response.read()
                return content
        except HTTPError as e:
            logger.warning("HTTP %s fetching %s", e.code, url)
        except URLError as e:
            logger.warning("URL error fetching %s: %s", url, e.reason)
        except TimeoutError as e:
            logger.warning("Timeout fetching %s", url)
            msg = f"Timeout fetching {url}"
            raise URLExtractionError(msg) from e
        return None
