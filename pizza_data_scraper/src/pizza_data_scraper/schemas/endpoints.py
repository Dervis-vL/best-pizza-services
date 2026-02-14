"""Endpoints schemas for pizza data scraper."""

import pydantic as pyd

from pizza_data_scraper.schemas import CategorySchema, RankedEditionSchema


class RankingEndpointsSchema(pyd.BaseModel):
    """Schema for the endpoints to rankings."""

    categories: list[CategorySchema] = pyd.Field(
        ...,
        description="List of pizza categories with their details",
    )
    editions: list[RankedEditionSchema] = pyd.Field(
        ...,
        description="List of ranking editions with their details",
    )

    @pyd.model_validator(mode="after")
    def validate(self) -> "RankingEndpointsSchema":
        """Validates that each edition's category_slug exists in the categories list."""
        valid_slugs = {category.slug for category in self.categories}
        for edition in self.editions:
            if edition.slug not in valid_slugs:
                raise ValueError(f"Edition has invalid category_slug: {edition.slug}")
        return self