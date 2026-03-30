"""Schema for pizzeria data."""

import pydantic as pyd


class PizzeriaSchema(pyd.BaseModel):
    """Schema for validating pizzeria data."""

    slug: str = pyd.Field(..., max_length=100, description="Slug for the pizzeria, used in URLs")
    description: str | None = pyd.Field(None, max_length=500, description="Pizzeria description")

    @pyd.computed_field
    @property
    def name(self) -> str:
        """Derive the display name from the slug."""
        return " ".join(word.capitalize() for word in self.slug.split("-"))  # pylint: disable=no-member

    # strip numeric suffic from slug when passed ina as input (e.g. 'napoli-on-the-road-4' -> 'napoli-on-the-road')
    @pyd.model_validator(mode="before")
    @classmethod
    def strip_slug_version_suffix(cls, data: dict) -> dict:
        """Strip numeric version suffixes from slug (e.g. 'napoli-on-the-road-4' -> 'napoli-on-the-road')."""
        if slug := data.get("slug"):
            parts = slug.rsplit("-", 1)
            if len(parts) == 2 and parts[-1].isdigit():
                data["slug"] = parts[0]
        return data