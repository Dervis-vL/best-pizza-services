"""Custom exceptions for the pizza data scraper."""


class TransientAPIError(Exception):
    """Retryable pizza platform API failure (connection error, timeout, 5xx)."""
