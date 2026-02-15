"""Schema for pizzeria data."""

import pydantic as pyd


class PizzeriaSchema(pyd.BaseModel):
    """Schema for validating pizzeria data."""

    name: str = pyd.Field(..., max_length=100, description="Name of the pizzeria")
    description: str | None = pyd.Field(None, max_length=500, description="Description of the pizzeria")
