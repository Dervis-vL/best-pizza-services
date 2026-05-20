"""Routers for maintenance endpoints."""

import logging

from fastapi import APIRouter, status

from pizza_api import dependencies
from pizza_api.application.logging import WarningCaptureHandler
from pizza_api.schemas import responses

router = APIRouter(prefix="/maintenance", tags=["maintenance"])

_pizza_api_logger = logging.getLogger("pizza_api")


@router.post(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=responses.ProcessPendingResponse,
    summary="Run a full scrape + parse cycle for all pending editions and webpages",
)
def process_pending(
    use_case: dependencies.ProcessPendingUCDep,
) -> responses.ProcessPendingResponse:
    """Scrape and parse all pending editions and pizzeria webpages."""
    handler = WarningCaptureHandler()
    _pizza_api_logger.addHandler(handler)
    try:
        result = use_case.execute()
    finally:
        _pizza_api_logger.removeHandler(handler)

    response = responses.ProcessPendingResponse.model_validate(
        result,
        from_attributes=True,
    )
    response.warnings = handler.warnings
    return response
