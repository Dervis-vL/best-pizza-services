"""Schema for pizzeria websites data."""

import pydantic as pyd

from pizza_platform_shared.schemas.base import BaseSchema, BaseReadSchema


class WebpagesSchema(BaseSchema):
    """Schema for validating pizzeria websites data."""

    @pyd.model_validator(mode="before")
    @classmethod
    def strip_slug_version_suffix(cls, data: dict) -> dict:
        """Strip numeric version suffixes from slug."""
        if slug := data.get("slug"):
            parts = slug.rsplit("-", 1)
            if len(parts) == 2 and parts[-1].isdigit():
                data["slug"] = parts[0]
        return data


class WebpagesReadSchema(BaseReadSchema):
    """Schema for validating pizzeria websites data."""

    url: str = pyd.Field(..., max_length=500, description="URL of the resource")
    pizzeria_id: int = pyd.Field(..., description="Foreign key to the pizzerias table")

    @pyd.model_validator(mode="before")
    @classmethod
    def strip_slug_version_suffix(cls, data: dict) -> dict:
        """Strip numeric version suffixes from slug."""
        if slug := data.get("slug"):
            parts = slug.rsplit("-", 1)
            if len(parts) == 2 and parts[-1].isdigit():
                data["slug"] = parts[0]
        return data