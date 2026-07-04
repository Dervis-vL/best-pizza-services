"""Dependencies for the pizza API.

Only dependencies that are used outside of the dependencies folder are defined here.
This is to avoid circular imports and to keep the dependency graph clean.
"""

from pizza_api.dependencies.payload import StageCategoryPayloadUCDep
from pizza_api.dependencies.pizzerias import ReadPizzeriasUCDep
from pizza_api.dependencies.scaleway import JobsTriggerDep
from pizza_api.dependencies.security import RequireApiKeyDep

__all__ = [
    "JobsTriggerDep",
    "ReadPizzeriasUCDep",
    "RequireApiKeyDep",
    "StageCategoryPayloadUCDep",
]
