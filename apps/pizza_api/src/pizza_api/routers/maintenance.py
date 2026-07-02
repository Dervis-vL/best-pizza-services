"""Routers for maintenance endpoints."""

import logging

from fastapi import APIRouter, status

from pizza_api import dependencies
from pizza_api.schemas import responses

router = APIRouter(prefix="/maintenance", tags=["Data entry"])

logger = logging.getLogger("pizza_api")


@router.post(
    "/all",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=responses.JobTriggerResponse,
    summary="Trigger a worker run that scrapes + parses all pending items",
)
def process_pending(
    jobs: dependencies.JobsTriggerDep,
) -> responses.JobTriggerResponse:
    """Start a pizza_worker job to scrape and parse all pending editions and pizzeria webpages."""
    run = jobs.start_run_pending()
    logger.info("Triggered run-pending job run %s", run.id)
    return responses.JobTriggerResponse(job_run_id=run.id, status=str(run.state))
