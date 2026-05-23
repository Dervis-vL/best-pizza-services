"""Router for getting pizzeria data endpoints."""

from typing import Annotated

from fastapi import APIRouter, Query, status

from pizza_api import dependencies
from pizza_platform_shared import enums as shared_enums
from pizza_platform_shared import schemas as shared_schemas

router = APIRouter(prefix="/pizzerias", tags=["pizzerias"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[shared_schemas.PizzeriaReadSchema],
    summary="Get the Pizzerias data from the database.",
)
def get_pizzerias(
    use_case: dependencies.ReadPizzeriasUCDep,
    include: Annotated[list[shared_enums.PizzeriaInclude] | None, Query()] = None,
) -> list[shared_schemas.PizzeriaReadSchema]:
    """Get all the pizzeria data from the DB, and optionally include relationships."""
    return use_case.execute(include_relationships=include)
