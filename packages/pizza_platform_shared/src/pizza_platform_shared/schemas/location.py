"""Schema for validating pizzeria location data."""

from __future__ import annotations

import pydantic as pyd

from pizza_platform_shared import constants
from pizza_platform_shared.schemas.base import BaseReadSchema


class LocationSchema(pyd.BaseModel):
    """Schema for validating pizzeria location data."""

    pizzaria_id: int = pyd.Field(..., description="Id foreignkey of the pizzeria")
    adress: str | None = pyd.Field(
        default=None,
        max_length=250,
        description="Adress of the pizzeria",
    )
    city: str | None = pyd.Field(
        default=None,
        max_length=50,
        description="City of the pizzeria",
    )
    country: str | None = pyd.Field(
        default=None,
        max_length=50,
        description="Country of the pizzeria",
    )
    latitude: float | None = pyd.Field(..., description="Lat of the pizzeria")
    longitude: float | None = pyd.Field(..., description="Lng of the pizzeria")
    phone: str | None = pyd.Field(
        default=None,
        max_length=constants.ModelColumnLengths.PHONE,
        description="Phone of the pizzeria",
    )

    @property
    def has_coordinates(self) -> bool:
        """True is coordinates are not default."""
        return self.latitude is not None or self.longitude is not None

    @pyd.field_validator("phone", mode="before")
    @classmethod
    def phone_check(cls, v: str | None) -> str | None:
        """Checks if phone is correct, otherwise split."""
        if not v or len(v) <= constants.ModelColumnLengths.PHONE:
            return v

        return None


class LocationReadSchema(LocationSchema, BaseReadSchema):
    """Schema for validating pizzeria location data."""
