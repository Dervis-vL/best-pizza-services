"""A single Pydantic model where each attribute is a compiled regex pattern
for extracting lat/lng coordinates from pizzeria HTML pages.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import Iterator

from pydantic import BaseModel, ConfigDict


class BasePattern(BaseModel, ABC):
    """Base pattern model."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __iter__(self) -> Iterator[tuple[str, re.Pattern[str]]]:
        """Iterate as (name, pattern) pairs — preserves definition order."""
        for name in self.__class__.model_fields:
            yield name, getattr(self, name)

    def all(self) -> list[re.Pattern[str]]:
        """Return all patterns in definition order."""
        return [p for _, p in self]

    def search(self, html: str) -> re.Match[str] | None:
        """Try each pattern in order, return the first match found."""
        for _, pattern in self:
            match = pattern.search(html)
            if match:
                return match
        return None

    @abstractmethod
    def extract(self):
        """Abstract base method"""
        pass


class CoordPatterns(BasePattern):
    """
    Compiled regex patterns for coordinate extraction.
    Each attribute targets a specific HTML structure observed in the wild.
    Both (?P<lat>...) and (?P<lng>...) named groups are required in every pattern.
    """

    js_map_init: re.Pattern[str] = re.compile(
        r"\blat\s*:\s*(?P<lat>-?\d+\.\d+).*?"
        r"\blng\s*:\s*(?P<lng>-?\d+\.\d+)",
        re.DOTALL,
    )
    json_location_object: re.Pattern[str] = re.compile(
        r'"lat"\s*:\s*(?P<lat>-?\d+\.\d+).*?'
        r'"lng"\s*:\s*(?P<lng>-?\d+\.\d+)',
        re.DOTALL,
    )
    maps_destination_link: re.Pattern[str] = re.compile(
        r"destination=(?P<lat>-?\d+\.\d+),(?P<lng>-?\d+\.\d+)",
    )
    generic_fallback: re.Pattern[str] = re.compile(
        r"lat(?:itude)?\s*[=:]\s*(?P<lat>-?\d+\.\d+).*?"
        r"l(?:ng|on)(?:gitude)?\s*[=:]\s*(?P<lng>-?\d+\.\d+)",
        re.DOTALL | re.IGNORECASE,
    )

    def extract(self, html: str) -> tuple[float, float] | None:
        """Return (lat, lng) from the first matching pattern, or None."""
        match = self.search(html)
        if match:
            return float(match.group("lat")), float(match.group("lng"))
        return None


class AddressPatterns(BasePattern):
    """
    Patterns for extracting the raw address string.
    Each pattern must contain an (?P<address>...) named group.
    """

    js_address_field: re.Pattern[str] = re.compile(
        r'address:\s*"(?P<address>[^"]+)"',
    )

    def extract(self, html: str) -> str | None:
        """Return the raw address string, or None."""
        match = self.search(html)
        if match:
            return match.group("address").strip()
        return None


class PhonePatterns(BasePattern):
    """
    Patterns for extracting the phone number.
    Each pattern must contain a (?P<phone>...) named group.
    """

    tel_href: re.Pattern[str] = re.compile(
        r'href="tel:[/]*\s*(?P<phone>\+?[\d][\d\s\-\(\)]+)"',
    )

    def extract(self, html: str) -> str | None:
        """Return the phone number string, or None."""
        match = self.search(html)
        if match:
            return match.group("phone").strip()
        return None