"""Schema for ranking position data validation."""

import pydantic as pyd

from pizza_platform_shared.schemas.base import BaseReadSchema



class RankingSchema(pyd.BaseModel):
    """Schema for validating ranking position data."""

    position: int | None = pyd.Field(default=None, description="Ranking position of the pizzeria")
    edition_id: int = pyd.Field(..., description="Foreign key to the editions table")
    awards: str | None = pyd.Field(
        default=None, max_length=500, description="Awards or special mentions for the pizzeria"
    )

    @pyd.field_validator("position")
    @classmethod
    def position_positive(cls, v: int | None) -> int | None:
        """Validates that the ranking position is a positive integer."""
        if v is None:
            return v
        if v < 1:
            raise ValueError(f"Ranking position {v} is not a positive integer")
        return v


class RankingReadSchema(RankingSchema, BaseReadSchema):
    """Schema for validating ranking position data."""

    pizzeria_id: int = pyd.Field(..., description="Foreign key to the pizzerias table")
