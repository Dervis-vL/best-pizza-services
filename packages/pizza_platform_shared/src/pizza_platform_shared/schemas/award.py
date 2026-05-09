"""Schema for special awards data validation."""

import pydantic as pyd

from pizza_platform_shared.schemas.base import BaseReadSchema


class AwardSchema(pyd.BaseModel):
    """Schema for validating special awards data."""

    award: str = pyd.Field(
        max_length=255, description="Awards or specials for the pizzeria"
    )
    sponsor: str = pyd.Field(max_length=200, description="Sponsor of the award")
    edition_id: int = pyd.Field(..., description="Foreign key to the editions table")


class AwardReadSchema(AwardSchema, BaseReadSchema):
    """Schema for validating special awards data."""

    pizzeria_id: int = pyd.Field(..., description="Foreign key to the pizzerias table")
