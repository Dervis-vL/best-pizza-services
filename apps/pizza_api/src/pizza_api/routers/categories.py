"""Router for category management endpoints."""

import logging

from fastapi import APIRouter, status

from pizza_api import dependencies
from pizza_api.schemas import requests, responses

router = APIRouter(prefix="/categories", tags=["Data entry"])

logger = logging.getLogger("pizza_api")


@router.post(
    "/",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=responses.JobTriggerResponse,
    summary="Trigger a worker to add a new category and run the full scrape + parse cycle",
)
def add_category(
    jobs: dependencies.JobsTriggerDep,
    use_case: dependencies.StageCategoryPayloadUCDep,
    body: requests.CategoryCreateRequest,
) -> responses.JobTriggerResponse:
    """Trigger a worker to add a new category and run the full scrape + parse cycle."""
    # Stage the payload to the DB
    payload_id = use_case.execute(category_schemas=body.categories)

    # Trigger the worker to run the add-category job with the payload_id
    run = jobs.start_add_category(payload_id=payload_id)
    logger.info("Triggered add-category job run %s", run.id)
    return responses.JobTriggerResponse(job_run_id=run.id, status=str(run.state))
