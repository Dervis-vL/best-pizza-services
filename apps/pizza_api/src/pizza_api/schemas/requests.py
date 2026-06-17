"""Request schemas for the pizza API."""

import pydantic as pyd

from pizza_platform_shared import schemas as shared_schemas


class CategoryCreateRequest(pyd.BaseModel):
    """Request body for adding a new category with its editions."""

    categories: list[shared_schemas.CategorySchema]
