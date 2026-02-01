"""Schema for ranked edition data validation."""

import pydantic as pyd


class RankedEditionSchema(pyd.BaseModel):
    """Schema for validating ranked edition data."""

    category_slug: str = pyd.Field(..., max_length=50, description="URL-friendly slug for the pizza category")
    year: int = pyd.Field(..., description="Year of the ranking edition")
    endpoint_url: str = pyd.Field(..., max_length=500, description="Endpoint URL for the ranking edition data") 

    @pyd.field_validator("category_slug")
    @classmethod
    def slug_lowercase_no_spaces(cls, v: str) -> str:
        """Returns the slug in lowercase and without spaces."""
        return v.lower().replace(" ", "-").strip()

    @pyd.field_validator("year")
    @classmethod
    def year_reasonable(cls, v: int) -> int:
        """Validates that the year is within a reasonable range."""
        if v < 2017 or v > 2030:
            raise ValueError(f"Year {v} is outside reasonable range (2017-2030)")
        return v

    @pyd.field_validator("endpoint_url")
    @classmethod
    def valid_url(cls, v: str) -> str:
        """Validates that the endpoint URL is a valid URL."""
        v = v.strip()

        # Normalize URL
        if v.startswith("http://"):
            v = v.replace("http://", "https://", 1)
        # Ensure URL starts with https://
        if not v.startswith("https://"):
            raise ValueError(f"Endpoint URL is not valid: {v}")
        return v