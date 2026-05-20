"""Schema for ranked edition data validation."""

import pydantic as pyd

from pizza_platform_shared import constants
from pizza_platform_shared.schemas.base import BaseReadSchema


class EditionSchema(pyd.BaseModel):
    """Schema for validating ranked edition data."""

    year: int = pyd.Field(..., description="Year of the ranking edition")
    url: str = pyd.Field(..., max_length=500, description="URL of the resource")

    @pyd.field_validator("year")
    @classmethod
    def year_reasonable(cls, v: int) -> int:
        """Validates that the year is within a reasonable range."""
        if v < constants.YearRange.MIN or v > constants.YearRange.MAX:
            msg = f"Year {v} is outside reasonable range ({constants.YearRange.MAX})"
            raise ValueError(msg)
        return v

    @pyd.model_validator(mode="after")
    def year_in_url(self) -> EditionSchema:
        """Validates that the year appears in the URL."""
        if str(self.year) not in self.url:
            msg = f"Year {self.year} must appear in the URL"
            raise ValueError(msg)
        return self


class EditionReadSchema(EditionSchema, BaseReadSchema):
    """Schema for validating ranked edition data."""

    category_id: int = pyd.Field(..., description="Foreign key to the categories table")
