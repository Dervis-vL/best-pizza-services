"""Scaleway Jobs trigger; driven adapter for starting worker runs."""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from scaleway import Client
from scaleway.jobs.v1alpha2 import JobRun, JobsV1Alpha2API

from pizza_api import settings


class WorkerJobsTrigger:
    """Starts pizza_worker job runs on Scaleway Serverless Jobs."""

    def __init__(self) -> None:
        client = Client(
            api_url=settings.scw.api_url,
            api_allow_insecure=settings.scw.api_allow_insecure,
            access_key=settings.scw.access_key.get_secret_value(),  # pylint: disable=no-member
            secret_key=settings.scw.secret_key.get_secret_value(),  # pylint: disable=no-member
            default_project_id=settings.scw.default_project_id,
            default_region=settings.scw.default_region,
        )
        self._api = JobsV1Alpha2API(client)
        self._run_pending_job_id = settings.scw.run_pending_job_id

    def start_run_pending(self) -> JobRun:
        """Start a worker run that scrapes + parses all pending items."""
        response = self._api.start_job_definition(
            job_definition_id=self._run_pending_job_id,
        )
        return response.job_runs[0]


@lru_cache
def get_jobs_trigger() -> WorkerJobsTrigger:
    """Provide a cached Scaleway jobs trigger (client is reusable across requests)."""
    return WorkerJobsTrigger()


JobsTriggerDep = Annotated[WorkerJobsTrigger, Depends(get_jobs_trigger)]
