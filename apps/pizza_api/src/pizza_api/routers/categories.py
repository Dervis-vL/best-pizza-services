"""Router for category management endpoints."""

from fastapi import APIRouter, status

from pizza_api.dependencies.dep_types import AddCategoryUCDep
from pizza_api.schemas.requests import CategoryCreateRequest
from pizza_api.schemas.responses import AddCategoryResponse

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=AddCategoryResponse,
    summary="Add a new category and run the full scrape + parse cycle",
)
def add_category(
    body: CategoryCreateRequest,
    use_case: AddCategoryUCDep,
) -> AddCategoryResponse:
    """Seed a new category, scrape all its editions and pizzeria webpages, and parse the results."""
    result = use_case.execute(category_schemas=body.categories)
    return AddCategoryResponse.model_validate(result, from_attributes=True)
