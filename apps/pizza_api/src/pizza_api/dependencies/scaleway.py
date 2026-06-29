"""Scaleway Jobs trigger; driven adapter for starting worker runs."""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from scaleway import Client
from scaleway.jobs.v1alpha1 import JobRun, JobsV1Alpha1API

from pizza_api import settings


class WorkerJobsTrigger:
    """Starts pizza_worker job runs on Scaleway Serverless Jobs."""

    def __init__(self) -> None:
        cfg = settings.scw
        client = Client(
            access_key=cfg.access_key.get_secret_value(),  # pylint: disable=no-member
            secret_key=cfg.secret_key.get_secret_value(),  # pylint: disable=no-member
            default_project_id=cfg.default_project_id,
            default_region=cfg.default_region,
        )
        self._api = JobsV1Alpha1API(client)
        self._run_pending_job_def_id = cfg.run_pending_job_id

    def start_run_pending(self) -> JobRun:
        """Start a worker run that scrapes + parses all pending items."""
        return self._api.start_job_definition(
            job_definition_id=self._run_pending_job_def_id,
        )


@lru_cache
def get_jobs_trigger() -> WorkerJobsTrigger:
    """Provide a cached Scaleway jobs trigger (client is reusable across requests)."""
    return WorkerJobsTrigger()


JobsTriggerDep = Annotated[WorkerJobsTrigger, Depends(get_jobs_trigger)]
