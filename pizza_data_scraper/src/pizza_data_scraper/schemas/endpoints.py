"""Endpoints schemas for pizza data scraper."""

import pydantic as pyd

from pizza_data_scraper.schemas.category import CategorySchema
from pizza_data_scraper.schemas.pizzeria import PizzeriaSchema
from pizza_data_scraper.schemas.ranked_edition import RankedEditionSchema
from pizza_data_scraper.schemas.webpages import WebpagesSchema


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
        """Validates that each edition's category.slug exists in the categories list."""
        valid_slugs = {category.slug for category in self.categories}
        for edition in self.editions:
            if edition.slug not in valid_slugs:
                raise ValueError(f"Edition has invalid category_slug: {edition.slug}")
        return self


class PizzeriaEndpointsSchema(pyd.BaseModel):
    """Schema for the endpoints to pizzerias."""

    pizzerias: list[PizzeriaSchema] = pyd.Field(
        ...,
        description="List of pizzerias with their details",
    )
    webpages: list[WebpagesSchema] = pyd.Field(
        ...,
        description="List of webpages for pizzerias on 50 Top Pizza"
    )

    @pyd.model_validator(mode="after")
    def validate(self) -> "PizzeriaEndpointsSchema":
        """Validates that each webpage.slug is in the pizzerias name."""
        for pizzeria in self.pizzerias:
            if not any(webpage.slug.startswith(pizzeria.name) for webpage in self.webpages):
                raise ValueError(f"No matching webpage slug for pizzeria: {pizzeria.name}")
        return self
