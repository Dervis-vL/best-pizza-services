"""Schema for ranking position data validation."""

import pydantic as pyd


class RankingSchema(pyd.BaseModel):
    """Schema for validating ranking position data."""

    position: int | None = pyd.Field(..., description="Ranking position of the pizzeria")
    pizzeria_slug: str = pyd.Field(..., max_length=200, description="Slug of the ranked pizzeria")
    edition_id: int = pyd.Field(..., description="ID of the ranked edition")

    @pyd.field_validator("position")
    @classmethod
    def position_positive(cls, v: int | None) -> int | None:
        """Validates that the ranking position is a positive integer."""
        if v is None:
            return v
        if v < 1:
            raise ValueError(f"Ranking position {v} is not a positive integer")
        return v
