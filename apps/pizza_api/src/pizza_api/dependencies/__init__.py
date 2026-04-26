"""Dependencies for the pizza API."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.engine import Engine
from pizza_data_storage import repositories as storage_repos

from pizza_api.application import use_cases
from pizza_api.dependencies.categories import get_add_category_uc
from pizza_api.dependencies.engine import get_engine
from pizza_api.dependencies.maintenance import get_process_pending_uc
from pizza_api.dependencies.repositories import (
    get_html_repo,
    get_pizzeria_repo,
    get_ranking_repo,
)


EngineDep = Annotated[Engine, Depends(get_engine)]
RankingRepoDep = Annotated[storage_repos.RankingsRepository, Depends(get_ranking_repo)]
PizzeriaRepoDep = Annotated[storage_repos.PizzeriaRepository, Depends(get_pizzeria_repo)]
HtmlRepoDep = Annotated[storage_repos.HtmlStorageRepository, Depends(get_html_repo)]
AddCategoryUCDep = Annotated[use_cases.AddCategoryUseCase, Depends(get_add_category_uc)]
ProcessPendingUCDep = Annotated[use_cases.ProcessPendingUseCase, Depends(get_process_pending_uc)]
