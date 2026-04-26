"""Router for category management endpoints."""

from fastapi import APIRouter, status

from pizza_api import dependencies
from pizza_api.schemas import requests, responses

router = APIRouter(prefix="/categories", tags=["categories"])


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
    """Seed a new category, scrape all its editions and pizzeria webpages, and parse the results."""
    result = use_case.execute(category_schemas=body.categories)
    return responses.AddCategoryResponse.model_validate(result, from_attributes=True)
