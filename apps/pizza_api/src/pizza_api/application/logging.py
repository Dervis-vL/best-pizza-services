"""Logging utilities for the pizza API."""

import logging


class WarningCaptureHandler(logging.Handler):
    """Captures WARNING-level log records into a list for inclusion in API responses."""

    def __init__(self) -> None:
        super().__init__(level=logging.WARNING)
        self.warnings: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.warnings.append(self.format(record))
