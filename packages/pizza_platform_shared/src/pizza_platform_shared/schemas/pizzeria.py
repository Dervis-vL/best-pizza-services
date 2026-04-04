"""Schema for pizzeria data."""

import pydantic as pyd

from pizza_platform_shared.schemas.base import BaseReadSchema


class PizzeriaSchema(pyd.BaseModel):
    """Schema for validating pizzeria data."""

    slug: str = pyd.Field(..., max_length=100, description="Slug for the pizzeria, used in URLs")
    description: str | None = pyd.Field(None, max_length=500, description="Pizzeria description")

    @pyd.computed_field
    @property
    def name(self) -> str:
        """Derive the display name from the slug."""
        return " ".join(word.capitalize() for word in self.slug.split("-"))  # pylint: disable=no-member

    # strip numeric suffic from slug when passed ina as input
    @pyd.model_validator(mode="before")
    @classmethod
    def strip_slug_version_suffix(cls, data: dict) -> dict:
        """Strip numeric version suffixes from slug."""
        if slug := data.get("slug"):
            parts = slug.rsplit("-", 1)
            if len(parts) == 2 and parts[-1].isdigit():
                data["slug"] = parts[0]
        return data


class PizzeriaReadSchema(PizzeriaSchema, BaseReadSchema):
    """Schema for validating pizzeria data."""
