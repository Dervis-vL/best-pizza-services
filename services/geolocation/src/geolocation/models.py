"""Data models for the geolocation service."""

import pydantic as pyd


class LocationResult(pyd.BaseModel):
    """Structured location data returned by the geolocation service."""

    country: str = pyd.Field(description="Country name, e.g., 'Italy'")
    city: str = pyd.Field(description="City name, e.g., 'Rome'")
    address: str = pyd.Field(description="Full display address, e.g., 'Piazza Navona, Rome, Italy'")
