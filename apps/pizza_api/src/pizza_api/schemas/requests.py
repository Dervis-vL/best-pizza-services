"""Request schemas for the pizza API."""

from typing import TYPE_CHECKING

import pydantic as pyd

if TYPE_CHECKING:
    from pizza_platform_shared import schemas as shared_schemas


class CategoryCreateRequest(pyd.BaseModel):
    """Request body for adding a new category with its editions."""

    categories: list[shared_schemas.CategorySchema]
