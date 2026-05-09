"""Dependencies for the pizza API.

Only dependencies that are used outside of the dependencies folder are defined here.
This is to avoid circular imports and to keep the dependency graph clean.
"""

from pizza_api.dependencies.categories import AddCategoryUCDep
from pizza_api.dependencies.maintenance import ProcessPendingUCDep

__all__ = [
    "AddCategoryUCDep",
    "ProcessPendingUCDep",
]
