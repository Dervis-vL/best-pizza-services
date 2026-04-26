"""Routers for maintenance endpoints."""

from fastapi import APIRouter, status

from pizza_api.dependencies.dep_types import ProcessPendingUCDep
from pizza_api.schemas.responses import ProcessPendingResponse

router = APIRouter(prefix="/maintenance", tags=["maintenance"])


@router.post(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=ProcessPendingResponse,
    summary="Run a full scrape + parse cycle for all pending editions and webpages",
)
def process_pending(
    use_case: ProcessPendingUCDep,
) -> ProcessPendingResponse:
    """Scrape and parse all pending editions and pizzeria webpages."""
    result = use_case.execute()
    return ProcessPendingResponse.model_validate(result, from_attributes=True)
