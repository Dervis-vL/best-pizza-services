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
