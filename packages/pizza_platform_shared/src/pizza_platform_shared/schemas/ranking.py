"""Schema for ranking position data validation."""

import pydantic as pyd

from pizza_platform_shared.schemas.base import BaseReadSchema
from pizza_platform_shared.schemas.edition import EditionReadSchema


class RankingSchema(pyd.BaseModel):
    """Schema for validating ranking position data."""

    position: int = pyd.Field(..., description="Ranking position of the pizzeria")
    edition_id: int = pyd.Field(..., description="Foreign key to the editions table")

    @pyd.field_validator("position")
    @classmethod
    def position_positive(cls, v: int | None) -> int | None:
        """Validates that the ranking position is a positive integer."""
        if v is None:
            return v
        if v < 1:
            msg = f"Ranking position {v} is not a positive integer"
            raise ValueError(msg)
        return v


class RankingReadSchema(RankingSchema, BaseReadSchema):
    """Schema for validating ranking position data."""

    pizzeria_id: int = pyd.Field(..., description="Foreign key to the pizzerias table")
    edition: EditionReadSchema = pyd.Field(..., description="Nested edition data for the ranking")
