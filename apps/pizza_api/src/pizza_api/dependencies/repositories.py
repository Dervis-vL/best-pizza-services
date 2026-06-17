"""Repository dependencies for the pizza API."""

from typing import Annotated

from fastapi import Depends

from pizza_api.dependencies.engine import EngineDep
from pizza_data_storage import repositories as storage_repos
from pizza_platform_shared import settings as shared_settings


def get_ranking_repo(engine: EngineDep) -> storage_repos.RankingsRepository:
    """Return a RankingsRepository bound to the request-scoped engine."""
    return storage_repos.RankingsRepository.from_engine(engine=engine)


def get_pizzeria_repo(engine: EngineDep) -> storage_repos.PizzeriaRepository:
    """Return a PizzeriaRepository bound to the request-scoped engine."""
    return storage_repos.PizzeriaRepository.from_engine(engine=engine)


def get_html_repo() -> storage_repos.HtmlStorageRepository:
    """Return an HtmlStorageRepository from the configured object storage settings."""
    return storage_repos.HtmlStorageRepository.from_settings(
        storage_settings=shared_settings.pizza_strg,
    )


RankingRepoDep = Annotated[storage_repos.RankingsRepository, Depends(get_ranking_repo)]
PizzeriaRepoDep = Annotated[
    storage_repos.PizzeriaRepository,
    Depends(get_pizzeria_repo),
]
HtmlRepoDep = Annotated[storage_repos.HtmlStorageRepository, Depends(get_html_repo)]
