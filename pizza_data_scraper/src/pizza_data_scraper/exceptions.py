"""Custom exceptions for the pizza data scraper."""


class PizzaDataScraperError(Exception):
    """Base exception for the pizza data scraper."""

    message: str

    def __init__(self, message: str = None):
        if message is not None:
            self.message = message
        super().__init__(self.message)


class URLExtractionError(PizzaDataScraperError):
    """Exception raised when URL extraction from a card element fails."""

    def __init__(self, message: str = "Failed to extract URL from card element."):
        super().__init__(message)