"""Schema for category data validation."""

import pydantic as pyd


class CategorySchema(pyd.BaseModel):
    """Schema for validating category data."""

    slug: str = pyd.Field(..., max_length=200, description="URL-friendly slug for the pizza category")
    name: str = pyd.Field(..., max_length=100, description="Name of the pizza category")
    description: str | None = pyd.Field(None, max_length=500, description="Description of the pizza category")

    @pyd.field_validator("slug")
    @classmethod
    def slug_lowercase_no_spaces(cls, v: str) -> str:
        """Returns the slug in lowercase and without spaces."""
        return v.lower().replace(" ", "-").strip()
