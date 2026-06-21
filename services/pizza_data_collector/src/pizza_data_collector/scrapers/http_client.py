"""HTTP client implementation for pizza data collector service."""

import logging
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import urlopen

from tenacity import (
    RetryError,
    Retrying,
    before_sleep_log,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from pizza_data_collector import constants, settings
from pizza_data_collector.exceptions import TransientFetchError

logger = logging.getLogger(__name__)


class HttpClient:  # pylint: disable=too-few-public-methods
    """HTTP client implementation for pizza data collector service."""

    def __init__(self, cfg: settings.ScraperSettings | None = None) -> None:
        """Initializes the HTTP client with an optional timeout."""
        self._cfg = cfg or settings.ScraperSettings()

    def _fetch_once(self, url: str) -> bytes:
        """Private method fetching a given URL with retries setup."""
        try:
            with urlopen(url, timeout=self._cfg.timeout) as response:  # noqa: S310
                content: bytes = response.read()
                return content
        except HTTPError as e:
            if e.code in constants.RETRYABLE_STATUS:
                msg = f"{e.code} fetching {url}"
                raise TransientFetchError(msg) from e
            logger.warning("Non-retryable HTTP %s fetching %s", e.code, url)
            raise  # 4xx etc. so do not retry
        except URLError as e:
            msg = f"connection error fetching {url}: {e.reason}"
            raise TransientFetchError(msg) from e
        except TimeoutError as e:
            msg = f"Timeout fetching {url}"
            raise TransientFetchError(msg) from e

    def fetch(self, url: str) -> bytes | None:
        """Fetches the content of the given URL."""
        parsed_url = urlsplit(url)
        if parsed_url.scheme not in ("http", "https"):
            msg = f"Unsupported URL schema: {parsed_url.scheme!r}"
            raise ValueError(msg)
        retrying = Retrying(
            stop=stop_after_attempt(self._cfg.max_attempts),
            wait=wait_random_exponential(
                multiplier=self._cfg.backoff_base, max=self._cfg.backoff_max
            ),
            retry=retry_if_exception_type(TransientFetchError),
            before_sleep=before_sleep_log(logger, logging.WARNING),
            reraise=False,
        )
        try:
            return retrying(self._fetch_once, url)
        except RetryError:
            logger.warning("Giving up on %s after %d attempts", url, self._cfg.max_attempts)
            return None
        except HTTPError:
            return None
