"""Router for getting pizzeria data endpoints."""

from fastapi import APIRouter, status

from pizza_api import dependencies
from pizza_platform_shared import schemas as shared_schemas

router = APIRouter(prefix="/pizzerias", tags=["Data read"])


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=list[shared_schemas.PizzeriaReadSchema],
    summary="Get the Pizzerias data from the database.",
)
def get_pizzerias(
    use_case: dependencies.ReadPizzeriasUCDep,
) -> list[shared_schemas.PizzeriaReadSchema]:
    """Get all the pizzeria data from the DB with all relationships."""
    return use_case.execute()
