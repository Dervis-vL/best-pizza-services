"""Schema for validating pizzeria location data."""

import pydantic as pyd


class LocationSchema(pyd.BaseModel):
    """Schema for validating pizzeria location data."""

    pizzaria_id: int = pyd.Field(..., max_length=200, description="Id foreignkey of the pizzeria")
    adress: str = pyd.Field(..., max_length=100, description="Adress of the pizzeria")
    city: str = pyd.Field(..., max_length=100, description="City of the pizzeria")
    country: str = pyd.Field(..., max_length=100, description="Country of the pizzeria")
    latitude: int = pyd.Field(..., description="Lat of the pizzeria")
    longitude: int = pyd.Field(..., description="Lng of the pizzeria")
    phone: int = pyd.Field(..., description="Phone of the pizzeria")
