"""Schema for pizzeria websites data."""

import pydantic as pyd

from pizza_platform_shared.schemas.base import BaseReadSchema


class WebpageSchema(pyd.BaseModel):
    """Schema for validating pizzeria websites data."""

    url: str = pyd.Field(..., max_length=500, description="URL of the resource")
    slug: str = pyd.Field(..., max_length=200, description="URL-friendly slug for the resource")

    @pyd.field_validator("url")
    @classmethod
    def valid_url(cls, v: str) -> str:
        """Validates that the URL is a valid URL."""
        v = v.strip()

        # Normalize URL
        if v.startswith("http://"):
            v = v.replace("http://", "https://", 1)
        # Ensure URL starts with https://
        if not v.startswith("https://"):
            raise ValueError(f"URL is not valid: {v}")
        return v

    @pyd.field_validator("slug")
    @classmethod
    def slug_lowercase_no_spaces(cls, v: str) -> str:
        """Returns the slug in lowercase and without spaces."""
        return v.lower().replace(" ", "-").strip()


class WebpageReadSchema(WebpageSchema, BaseReadSchema):
    """Schema for validating pizzeria websites data."""

    pizzeria_id: int = pyd.Field(..., description="Foreign key to the pizzerias table")
