"""Routers for maintenance endpoints."""

from fastapi import APIRouter, status

from pizza_api.dependencies.dep_types import ProcessPendingUCDep
from pizza_api.schemas.responses import ProcessPendingResponse

router = APIRouter(prefix="/maintenance", tags=["maintenance"])

