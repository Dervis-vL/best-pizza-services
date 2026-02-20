"""Schema for validating pizzeria location data."""

import pydantic as pyd


class LocationSchema(pyd.BaseModel):
    """Schema for validating pizzeria location data."""

    pizzaria_id: int = pyd.Field(..., description="Id foreignkey of the pizzeria")
    adress: str | None = pyd.Field(default=None, max_length=100, description="Adress of the pizzeria")
    city: str | None = pyd.Field(default=None, max_length=100, description="City of the pizzeria")
    country: str | None = pyd.Field(default=None, max_length=100, description="Country of the pizzeria")
    latitude: float = pyd.Field(..., description="Lat of the pizzeria")
    longitude: float = pyd.Field(..., description="Lng of the pizzeria")
    phone: str | None = pyd.Field(default=None, max_length=20, description="Phone of the pizzeria")
