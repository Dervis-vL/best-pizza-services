"""Pizzeria model dependencies for the API."""

from typing import Annotated

from fastapi import Depends

from pizza_api.dependencies.repositories import PizzeriaRepoDep
from pizza_data_storage.application import use_cases as storage_use_cases


def get_read_pizzerias_uc(
    pizzeria_repo: PizzeriaRepoDep,
) -> storage_use_cases.GetPizzeriasUseCase:
    """Get use case for reading pizzerias."""
    return storage_use_cases.GetPizzeriasUseCase(pizzeria_repo)


ReadPizzeriasUCDep = Annotated[
    storage_use_cases.GetPizzeriasUseCase,
    Depends(get_read_pizzerias_uc),
]
