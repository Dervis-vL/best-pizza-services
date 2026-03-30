"""Endpoints schemas for pizza data scraper."""

import pydantic as pyd

from pizza_platform_shared.schemas.category import CategorySchema
from pizza_platform_shared.schemas.pizzeria import PizzeriaSchema
from pizza_platform_shared.schemas.edition import EditionSchema
from pizza_platform_shared.schemas.ranking import RankingSchema
from pizza_platform_shared.schemas.webpages import WebpagesSchema


class RankedCategoriesSchema(pyd.BaseModel):
    """Schema for the endpoints to rankings."""

    categories: list[CategorySchema] = pyd.Field(
        ...,
        description="List of pizza categories with their details",
    )
    editions: list[EditionSchema] = pyd.Field(
        ...,
        description="List of ranking editions with their details",
    )

    @pyd.model_validator(mode="after")
    def validate_edition_slugs(self) -> "RankedCategoriesSchema":
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
    rankings: list[RankingSchema] = pyd.Field(
        default_factory=list,
        description="List of ranking entries linking pizzerias to their edition positions",
    )

    @pyd.model_validator(mode="after")
    def validate_webpage_slugs(self) -> "PizzeriaEndpointsSchema":
        """Validates that each webpage.slug is in the pizzerias name."""
        for pizzeria in self.pizzerias:
            if not any(webpage.slug.startswith(pizzeria.slug) for webpage in self.webpages):
                raise ValueError(f"No matching webpage slug for pizzeria: {pizzeria.name}")
        return self

    @pyd.model_validator(mode="after")
    def validate_ranking_editions(self) -> "PizzeriaEndpointsSchema":
        """Validates that each ranking's edition_id is a positive integer."""
        for ranking in self.rankings:
            if ranking.edition_id <= 0:
                raise ValueError(f"Ranking has invalid edition_id: {ranking.edition_id}")
            if not any(
                pizzeria.slug.startswith(ranking.pizzeria_slug) for pizzeria in self.pizzerias
            ):
                raise ValueError(f"No matching pizzeria slug for ranking: {ranking.pizzeria_slug}")
        return self
