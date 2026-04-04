"""Schema for ranked edition data validation."""

import pydantic as pyd

from pizza_platform_shared.schemas.base import BaseReadSchema


class EditionSchema(pyd.BaseModel):
    """Schema for validating ranked edition data."""

    year: int = pyd.Field(..., description="Year of the ranking edition")
    url: str = pyd.Field(..., max_length=500, description="URL of the resource")

    @pyd.field_validator("year")
    @classmethod
    def year_reasonable(cls, v: int) -> int:
        """Validates that the year is within a reasonable range."""
        if v < 2017 or v > 2030:
            raise ValueError(f"Year {v} is outside reasonable range (2017-2030)")
        return v

    # @pyd.field_validator("url")
    # @classmethod
    # def url_contains_year(cls, v: str, info: pyd.FieldValidationInfo) -> str:
    #     """Validates that the URL contains the year."""
    #     year = info.data.get("year")
    #     if year and str(year) not in v:
    #         raise ValueError(f"URL '{v}' does not contain the year {year}")
    #     return v


class EditionReadSchema(EditionSchema, BaseReadSchema):
    """Schema for validating ranked edition data."""

    category_id: int = pyd.Field(..., description="Foreign key to the categories table")
