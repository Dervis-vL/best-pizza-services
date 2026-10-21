"""Base schema for pizza data scraper."""

import pydantic as pyd


class BaseReadSchema(pyd.BaseModel):
    """Base schema for reading pizza data."""

    id: int = pyd.Field(..., description="Unique identifier of the resource")
