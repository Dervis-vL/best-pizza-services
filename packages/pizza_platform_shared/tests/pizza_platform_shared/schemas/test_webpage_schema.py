"""Tests for WebpageSchema and WebpageReadSchema."""

from __future__ import annotations

import pydantic as pyd
import pytest
from hypothesis import given
from hypothesis import strategies as st

from pizza_platform_shared.schemas.webpage import WebpageReadSchema, WebpageSchema

_URL_MAX = 500
_SLUG_MAX = 200
_HTTPS = "https://"


def _st_https_url() -> st.SearchStrategy[str]:
    """URL starting with https:// that stays within the column length limit."""
    return st.text(max_size=_URL_MAX - len(_HTTPS)).map(lambda s: _HTTPS + s)


_valid_webpage = st.fixed_dictionaries(
    {
        "url": _st_https_url(),
        "slug": st.text(max_size=_SLUG_MAX),
    }
)


class TestWebpageSchema:
    """Tests for WebpageSchema write/create behaviour."""

    @given(_valid_webpage)
    def test_valid_construction(self, data: dict) -> None:
        """Accepts any https URL and slug within the length limits."""
        schema = WebpageSchema(**data)
        assert schema.url.startswith(_HTTPS)

    @given(suffix=st.text(max_size=100))
    def test_http_url_normalized_to_https(self, suffix: str) -> None:
        """Rewrites http:// URLs to https:// instead of rejecting them."""
        schema = WebpageSchema(url="http://" + suffix, slug="slug")
        assert schema.url.startswith(_HTTPS)

    def test_url_whitespace_stripped(self) -> None:
        """Strips surrounding whitespace before validating the URL."""
        schema = WebpageSchema(url="  https://example.com  ", slug="slug")
        assert schema.url == "https://example.com"

    @given(
        url=st.text(max_size=_URL_MAX).filter(
            lambda s: not s.strip().startswith(("https://", "http://"))
        )
    )
    def test_url_without_scheme_raises(self, url: str) -> None:
        """Raises ValidationError for any URL that lacks an http(s) scheme."""
        with pytest.raises(pyd.ValidationError):
            WebpageSchema(url=url, slug="slug")

    @given(url=st.text(min_size=_URL_MAX + 1, max_size=_URL_MAX + 10))
    def test_url_over_limit_raises(self, url: str) -> None:
        """Raises ValidationError when the URL exceeds the column length limit."""
        with pytest.raises(pyd.ValidationError):
            WebpageSchema(url=url, slug="slug")

    @given(slug=st.text(max_size=_SLUG_MAX))
    def test_slug_lowercase_without_spaces(self, slug: str) -> None:
        """Returns the slug lowercased and with no spaces left in it."""
        schema = WebpageSchema(url="https://example.com", slug=slug)
        assert schema.slug == schema.slug.lower()
        assert " " not in schema.slug

    def test_slug_spaces_become_dashes(self) -> None:
        """Replaces spaces with dashes and lowercases the slug."""
        schema = WebpageSchema(url="https://example.com", slug="Best Pizza NYC")
        assert schema.slug == "best-pizza-nyc"

    @given(slug=st.text(min_size=_SLUG_MAX + 1, max_size=_SLUG_MAX + 10))
    def test_slug_over_limit_raises(self, slug: str) -> None:
        """Raises ValidationError when the slug exceeds the column length limit."""
        with pytest.raises(pyd.ValidationError):
            WebpageSchema(url="https://example.com", slug=slug)

    def test_url_required(self) -> None:
        """Raises ValidationError when url is omitted."""
        with pytest.raises(pyd.ValidationError):
            WebpageSchema(slug="slug")  # type: ignore[call-arg]

    def test_slug_required(self) -> None:
        """Raises ValidationError when slug is omitted."""
        with pytest.raises(pyd.ValidationError):
            WebpageSchema(url="https://example.com")  # type: ignore[call-arg]


class TestWebpageReadSchema:
    """Tests for WebpageReadSchema read/response behaviour, with required id and pizzeria_id."""

    @given(
        schema_id=st.integers(),
        pizzeria_id=st.integers(),
        url=_st_https_url(),
    )
    def test_valid_construction(self, schema_id: int, pizzeria_id: int, url: str) -> None:
        """Accepts any valid id/pizzeria_id combination and preserves both values."""
        schema = WebpageReadSchema(
            id=schema_id,
            pizzeria_id=pizzeria_id,
            url=url,
            slug="slug",
        )
        assert schema.id == schema_id
        assert schema.pizzeria_id == pizzeria_id

    def test_id_required(self) -> None:
        """Raises ValidationError when id is omitted."""
        with pytest.raises(pyd.ValidationError):
            WebpageReadSchema(pizzeria_id=1, url="https://example.com", slug="slug")  # type: ignore[call-arg]

    def test_pizzeria_id_required(self) -> None:
        """Raises ValidationError when pizzeria_id is omitted."""
        with pytest.raises(pyd.ValidationError):
            WebpageReadSchema(id=1, url="https://example.com", slug="slug")  # type: ignore[call-arg]
