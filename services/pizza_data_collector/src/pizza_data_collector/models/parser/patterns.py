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
    def extract(self, html: str):
        """Abstract base method"""


class CardPatterns(BasePattern):
    """
    Patterns for extracting individual ranking card HTML chunks from a full ranking page.
    Each pattern targets the outer <a> wrapping a single ranking entry.

    Use extract() to get all card chunks, then run URLPattern and
    RankingPositionPatterns or AwarsNamePatterns on each chunk to extract URL and position.
    """

    # Special awards (2022+): must be first pattern since award pages also have id="scheda" anchors
    testo_card: re.Pattern[str] = re.compile(
        r'<div\b[^>]*\bid="sponsor_speciali testo-card"[^>]*>.*?</div>',
        re.DOTALL,
    )

    # Modern (2022+): <a id="scheda" href="...referenza/...">...</a>
    scheda_id: re.Pattern[str] = re.compile(
        r'<a\b[^>]*id="scheda"[^>]*>.*?</a>',
        re.DOTALL,
    )

    # Older (2020): <a class="...altezza-NNN-desktop..." href="...recensione/...">...</a>
    altezza_class: re.Pattern[str] = re.compile(
        r'<a\b[^>]*\baltezza-\d+-desktop\b[^>]*>.*?</a>',
        re.DOTALL,
    )

    def extract(self, html: str) -> list[str]:
        """Return all card HTML chunks using the first pattern that yields results."""
        for _, pattern in self:
            cards = pattern.findall(html)
            if cards:
                return cards
        return []


class URLPatterns(BasePattern):
    """
    Pattern for extracting the raw url string.
    """

    pizzeria_url: re.Pattern[str] =re.compile(
        r'href="(https://www\.50toppizza\.it/(?:referenza|recensione)/[^"]+)"'
    )

    def extract(self, html: str) -> str:
        """Return the raw url string from each cards html, or None."""
        match = self.search(html)
        if match:
            return match.group(1)
        return None


class RankingPositionPatterns(BasePattern):
    """
    Patterns for extracting a ranked position (1–100) from a ranking-list card's HTML.
    Run on each individual card/entry's HTML extracted from a ranking page.
    Each pattern must contain a (?P<position>...) named group.

    Returns None for special-award and excellent pages, which have no numeric position.
    """

    # Modern format (2022+):
    # <h2 class="mt-2 posizione scotchmodern rosso caps">13°</h2>
    posizione_class: re.Pattern[str] = re.compile(
        r'class="[^"]*\bposizione\b[^"]*"[^>]*>\s*(?P<position>\d+)°',
    )

    # Older format (2020):
    # <h2 class="oro margin-bottom-30" style="...">1°</h2>
    oro_class: re.Pattern[str] = re.compile(
        r'<h2\b[^>]*class="[^"]*\boro\b[^"]*"[^>]*>\s*(?P<position>\d+)°',
    )

    def extract(self, html: str) -> int | None:
        """Return the rank position as an integer, or None if not a ranked entry."""
        match = self.search(html)
        if match:
            return int(match.group("position"))
        return None


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

    def extract(self, html: str) -> tuple[float, float] | tuple[None, None]:
        """Return (lat, lng) from the first matching pattern, or None."""
        match = self.search(html)
        if match:
            return float(match.group("lat")), float(match.group("lng"))
        return None, None


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


class AwardNamePatterns(BasePattern):
    """
    Pattern for extracting the award name and sponsor from a special awards card.
    Run on each individual card HTML chunk extracted by AwardCardPatterns.

    The source element looks like:
        <h2 class="grigioscuro scotchmodern ...">
            Best Fried Food 2025<br/>
            Il Fritturista - Oleificio Zucchi Award
        </h2>

    The (?P<award>...) group captures the text before <br/> (the award name).
    The (?P<sponsor>...) group captures the text after <br/> (the sponsor).
    Both are stripped of whitespace in extract().
    """

    grigioscuro_h2: re.Pattern[str] = re.compile(
        r'<h2\b[^>]*\bgrigioscuro\b[^>]*>'
        r'\s*(?P<award>.+?)<br\s*/?>'
        r'(?P<sponsor>.+?)\s*</h2>',
        re.DOTALL,
    )

    def extract(self, html: str) -> tuple[str, str] | tuple[None, None]:
        """Return (award_name, sponsor) stripped of whitespace, or (None, None)."""
        match = self.search(html)
        if match:
            return match.group("award").strip(), match.group("sponsor").strip()
        return None, None
