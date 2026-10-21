"""Schema for pizzeria data."""

import pydantic as pyd

from pizza_platform_shared import constants
from pizza_platform_shared.schemas.award import AwardReadSchema, AwardSchema
from pizza_platform_shared.schemas.base import BaseReadSchema
from pizza_platform_shared.schemas.location import LocationReadSchema
from pizza_platform_shared.schemas.ranking import RankingReadSchema, RankingSchema
from pizza_platform_shared.schemas.webpage import WebpageReadSchema, WebpageSchema


class PizzeriaBaseSchema(pyd.BaseModel):
    """Schema for validating pizzeria data."""

    description: str | None = pyd.Field(
        None,
        max_length=500,
        description="Pizzeria description",
    )


class PizzeriaSchema(PizzeriaBaseSchema):
    """Schema for validating pizzeria data."""

    slug: str = pyd.Field(
        ...,
        max_length=constants.ModelColumnLengths.SLUG,
        description="Slug for the pizzeria",
    )
    rankings: list[RankingSchema] = pyd.Field(
        default_factory=list,
        description="List of rankings linking to this pizzeria",
    )
    webpages: list[WebpageSchema] = pyd.Field(
        default_factory=list,
        description="List of webpages linked to this pizzeria",
    )
    awards: list[AwardSchema] = pyd.Field(
        default_factory=list,
        description="List of awards received by the pizzeria",
    )

    @pyd.computed_field  # type: ignore[prop-decorator]
    @property
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

    webpages: list[WebpageReadSchema] = pyd.Field(
        default_factory=list,
        description="List of webpages linked to this pizzeria",
    )
    locations: list[LocationReadSchema] = pyd.Field(
        default_factory=list,
        description="List of locations for the pizzeria",
    )
    rankings: list[RankingReadSchema] = pyd.Field(
        default_factory=list,
        description="List of rankings linking to this pizzeria",
    )
    awards: list[AwardReadSchema] = pyd.Field(
        default_factory=list,
        description="List of awards received by the pizzeria",
    )
