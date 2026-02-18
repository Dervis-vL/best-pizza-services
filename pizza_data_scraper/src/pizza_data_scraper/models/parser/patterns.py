"""A single Pydantic model where each attribute is a compiled regex pattern
for extracting lat/lng coordinates from pizzeria HTML pages.
"""

from __future__ import annotations

import re
from typing import Iterator

from pydantic import BaseModel, ConfigDict


class CoordPatterns(BaseModel):
    """
    Compiled regex patterns for coordinate extraction.
    Each attribute targets a specific HTML structure observed in the wild.
    Both (?P<lat>...) and (?P<lng>...) named groups are required in every pattern.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

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

    def extract_coords(self, html: str) -> tuple[float, float] | None:
        """Return (lat, lng) from the first matching pattern, or None."""
        match = self.search(html)
        if match:
            return float(match.group("lat")), float(match.group("lng"))
        return None
