"""Tests for LocationSchema and LocationReadSchema."""

from __future__ import annotations

import pydantic as pyd
import pytest
from hypothesis import given
from hypothesis import strategies as st

from pizza_platform_shared import constants
from pizza_platform_shared.schemas.location import LocationReadSchema, LocationSchema

from .conftest import st_finite_float, st_optional_float, st_optional_text

_PHONE_MAX = constants.ModelColumnLengths.PHONE

_valid_location = st.fixed_dictionaries(
    {
        "pizzaria_id": st.integers(),
        "address": st_optional_text(250),
        "city": st_optional_text(50),
        "country": st_optional_text(50),
        "latitude": st_optional_float(),
        "longitude": st_optional_float(),
        "phone": st.one_of(st.none(), st.text(max_size=_PHONE_MAX)),
    }
)


class TestLocationSchema:
    """Tests for LocationSchema write/create behaviour."""

    @given(_valid_location)
    def test_valid_construction(self, data: dict) -> None:
        """Accepts any valid combination of location fields and preserves pizzaria_id."""
        schema = LocationSchema(**data)
        assert schema.pizzaria_id == data["pizzaria_id"]

    @given(lat=st_finite_float(), lng=st_finite_float())
    def test_has_coordinates_true(self, lat: float, lng: float) -> None:
        """Returns True when both latitude and longitude are finite floats."""
        schema = LocationSchema(pizzaria_id=1, latitude=lat, longitude=lng)
        assert schema.has_coordinates is True

    def test_has_coordinates_false_when_lat_none(self) -> None:
        """Returns False when latitude is None even if longitude is set."""
        schema = LocationSchema(pizzaria_id=1, latitude=None, longitude=0.0)
        assert schema.has_coordinates is False

    def test_has_coordinates_false_when_lng_none(self) -> None:
        """Returns False when longitude is None even if latitude is set."""
        schema = LocationSchema(pizzaria_id=1, latitude=0.0, longitude=None)
        assert schema.has_coordinates is False

    def test_phone_none_passes_through(self) -> None:
        """Preserves None as the phone value without coercion."""
        schema = LocationSchema(pizzaria_id=1, latitude=None, longitude=None, phone=None)
        assert schema.phone is None

    def test_phone_empty_string_passes_through(self) -> None:
        """Preserves an empty string phone value without coercion."""
        schema = LocationSchema(pizzaria_id=1, latitude=None, longitude=None, phone="")
        assert schema.phone == ""

    @given(phone=st.text(min_size=1, max_size=_PHONE_MAX))
    def test_phone_within_limit_passes_through(self, phone: str) -> None:
        """Preserves any phone string at or below the column length limit."""
        schema = LocationSchema(pizzaria_id=1, latitude=None, longitude=None, phone=phone)
        assert schema.phone == phone

    @given(phone=st.text(min_size=_PHONE_MAX + 1))
    def test_phone_over_limit_becomes_none(self, phone: str) -> None:
        """Coerces phone to None when the value exceeds the column length limit."""
        schema = LocationSchema(pizzaria_id=1, latitude=None, longitude=None, phone=phone)
        assert schema.phone is None

    def test_pizzaria_id_required(self) -> None:
        """Raises ValidationError when pizzaria_id is omitted."""
        with pytest.raises(pyd.ValidationError):
            LocationSchema(latitude=None, longitude=None)  # type: ignore[call-arg]

    def test_latitude_required(self) -> None:
        """Raises ValidationError when latitude is omitted."""
        with pytest.raises(pyd.ValidationError):
            LocationSchema(pizzaria_id=1, longitude=None)  # type: ignore[call-arg]

    def test_longitude_required(self) -> None:
        """Raises ValidationError when longitude is omitted."""
        with pytest.raises(pyd.ValidationError):
            LocationSchema(pizzaria_id=1, latitude=None)  # type: ignore[call-arg]


class TestLocationReadSchema:
    """Tests for LocationReadSchema read/response behaviour, including the required id field."""

    @given(
        schema_id=st.integers(),
        pizzaria_id=st.integers(),
        lat=st_optional_float(),
        lng=st_optional_float(),
    )
    def test_valid_construction(
        self,
        schema_id: int,
        pizzaria_id: int,
        lat: float | None,
        lng: float | None,
    ) -> None:
        """Accepts any valid id/pizzaria_id combination and preserves both values."""
        schema = LocationReadSchema(
            id=schema_id,
            pizzaria_id=pizzaria_id,
            latitude=lat,
            longitude=lng,
        )
        assert schema.id == schema_id
        assert schema.pizzaria_id == pizzaria_id

    def test_id_required(self) -> None:
        """Raises ValidationError when id is omitted."""
        with pytest.raises(pyd.ValidationError):
            LocationReadSchema(pizzaria_id=1, latitude=None, longitude=None)
