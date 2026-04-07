"""HTTP client implementation for pizza data collector service."""

from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from pizza_data_collector.exceptions import URLExtractionError

class HttpClient:  # pylint: disable=too-few-public-methods
    """HTTP client implementation for pizza data collector service."""

    def __init__(self, timeout: int = 10) -> None:
        """Initializes the HTTP client with an optional timeout."""
        self._timeout = timeout

    def fetch(self, url: str) -> bytes:
        """Fetches the content of the given URL."""
        try:
            with urlopen(url, timeout=self._timeout) as response:
                return response.read()
        except HTTPError as e:
            raise URLExtractionError(f"HTTP {e.code} fetching {url}") from e
        except URLError as e:
            raise URLExtractionError(f"URL error fetching {url}: {e.reason}") from e
        except TimeoutError as e:
            raise URLExtractionError(f"Timeout fetching {url}") from e
