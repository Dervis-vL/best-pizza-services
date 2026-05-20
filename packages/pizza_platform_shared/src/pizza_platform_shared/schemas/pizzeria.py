"""Schema for pizzeria data."""

import pydantic as pyd

from pizza_platform_shared import constants
from pizza_platform_shared import schemas as shared_schemas
from pizza_platform_shared.schemas.base import BaseReadSchema
from pizza_platform_shared.schemas.ranking import RankingSchema
from pizza_platform_shared.schemas.webpage import WebpageSchema


class PizzeriaBaseSchema(pyd.BaseModel):
    """Schema for validating pizzeria data."""

    description: str | None = pyd.Field(
        None,
        max_length=500,
        description="Pizzeria description",
    )
    rankings: list[RankingSchema] = pyd.Field(
        default_factory=list,
        description="List of rankings linking to this pizzeria",
    )
    webpages: list[WebpageSchema] = pyd.Field(
        default_factory=list,
        description="List of webpages linked to this pizzeria",
    )
    awards: list[shared_schemas.AwardSchema] = pyd.Field(
        default_factory=list,
        description="List of awards received by the pizzeria",
    )


class PizzeriaSchema(PizzeriaBaseSchema):
    """Schema for validating pizzeria data."""

    slug: str = pyd.Field(
        ...,
        max_length=constants.ModelColumnLengths.SLUG,
        description="Slug for the pizzeria",
    )

    @property
    @pyd.computed_field
    def name(self) -> str:
        """Derive the display name from the slug."""
        derived_name = " ".join(word.capitalize() for word in self.slug.split("-"))  # pylint: disable=no-member
        if len(derived_name) > constants.ModelColumnLengths.NAME:
            msg = f"Derived name exceeds maximum length (derived from slug '{self.slug}')"
            raise ValueError(msg)
        return derived_name

    @pyd.field_validator("slug", mode="before")
    @classmethod
    def normalize_slug(cls, v: str) -> str:
        """Soft validation/normalization of the slug value."""
        return v.lower().replace(" ", "-").strip()


class PizzeriaReadSchema(PizzeriaBaseSchema, BaseReadSchema):
    """Schema for validating pizzeria data."""

    name: str = pyd.Field(
        ...,
        max_length=constants.ModelColumnLengths.NAME,
        description="Name for pizzeria",
    )
