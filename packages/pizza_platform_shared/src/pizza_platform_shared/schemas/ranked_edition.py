"""Schema for ranked edition data validation."""

import pydantic as pyd

from pizza_platform_shared.schemas.base import BaseSchema


class EditionSchema(BaseSchema):
    """Schema for validating ranked edition data."""

    year: int = pyd.Field(..., description="Year of the ranking edition")

    @pyd.field_validator("year")
    @classmethod
    def year_reasonable(cls, v: int) -> int:
        """Validates that the year is within a reasonable range."""
        if v < 2017 or v > 2030:
            raise ValueError(f"Year {v} is outside reasonable range (2017-2030)")
        return v
