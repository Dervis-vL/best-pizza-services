"""Custom exceptions for the pizza data scraper."""


class PizzaDataScraperError(Exception):
    """Base exception for the pizza data scraper."""

    message: str

    def __init__(self, message: str) -> None:
        if message is not None:
            self.message = message
        super().__init__(self.message)


class TransientFetchError(Exception):
    """Retryable upstream failure (5xx / timeout)."""


class URLExtractionError(PizzaDataScraperError):
    """Exception raised when URL extraction from a card element fails."""

    def __init__(
        self,
        message: str = "Failed to extract URL from card element.",
    ) -> None:
        super().__init__(message)
