"""Payload dependencies for the api pizza platform."""

from typing import Annotated

from fastapi import Depends

from pizza_api.dependencies.repositories import CategoryPayloadRepoDep
from pizza_data_storage.application import use_cases as storage_use_cases


def get_stage_category_payload_uc(
    category_payload_repo: CategoryPayloadRepoDep,
) -> storage_use_cases.StageCategoryPayloadUseCase:
    """Get use case for staging a new category payload."""
    return storage_use_cases.StageCategoryPayloadUseCase(category_payload_repo)


StageCategoryPayloadUCDep = Annotated[
    storage_use_cases.StageCategoryPayloadUseCase,
    Depends(get_stage_category_payload_uc),
]
