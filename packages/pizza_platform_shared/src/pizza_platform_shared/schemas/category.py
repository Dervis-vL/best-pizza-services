"""Schema for category data validation."""

import pydantic as pyd

from pizza_platform_shared.schemas.edition import EditionSchema


class CategorySchema(pyd.BaseModel):
    """Schema for validating category data."""

    slug: str = pyd.Field(..., max_length=200, description="URL-friendly slug")
    name: str = pyd.Field(..., max_length=100, description="Name of the pizza category")
    description: str | None = pyd.Field(
        None, max_length=500, description="Description of the category"
    )
    editions: list[EditionSchema] = pyd.Field(
        default_factory=list,
        description="List of ranking editions associated with this category",
    )

    @pyd.field_validator("slug")
    @classmethod
    def slug_lowercase_no_spaces(cls, v: str) -> str:
        """Returns the slug in lowercase and without spaces."""
        return v.lower().replace(" ", "-").strip()
