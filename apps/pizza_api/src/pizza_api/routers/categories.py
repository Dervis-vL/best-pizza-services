"""Router for category management endpoints."""

import logging

from fastapi import APIRouter, status

from pizza_api import dependencies
from pizza_api.application.logging import WarningCaptureHandler
from pizza_api.schemas import requests, responses

router = APIRouter(prefix="/categories", tags=["categories"])

_pizza_api_logger = logging.getLogger("pizza_api")


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=responses.AddCategoryResponse,
    summary="Add a new category and run the full scrape + parse cycle",
)
def add_category(
    body: requests.CategoryCreateRequest,
    use_case: dependencies.AddCategoryUCDep,
) -> responses.AddCategoryResponse:
    """Seed a new category, scrape all its editions/pizzeria/webpages, and parse."""
    handler = WarningCaptureHandler()
    _pizza_api_logger.addHandler(handler)
    try:
        result = use_case.execute(category_schemas=body.categories)
    finally:
        _pizza_api_logger.removeHandler(handler)

    response = responses.AddCategoryResponse.model_validate(
        result, from_attributes=True
    )
    response.warnings = handler.warnings
    return response
