"""Repository dependencies for the pizza API."""

from typing import Annotated

from fastapi import Depends

from pizza_api.dependencies.engine import EngineDep
from pizza_data_storage.adapters import storage as storage_repos
from pizza_data_storage.adapters.db import repos as db_repos
from pizza_platform_shared import settings as shared_settings


def get_category_payload_repo(engine: EngineDep) -> db_repos.CategoryPayloadRepository:
    """Return a CategoryPayloadRepository from the request-scoped engine."""
    return db_repos.CategoryPayloadRepository.from_engine(engine=engine)


def get_html_repo() -> storage_repos.HtmlStorageRepository:
    """Return an HtmlStorageRepository from the configured object storage settings."""
    return storage_repos.HtmlStorageRepository.from_settings(
        storage_settings=shared_settings.pizza_strg,
    )


def get_pizzeria_repo(engine: EngineDep) -> db_repos.PizzeriaRepository:
    """Return a PizzeriaRepository bound to the request-scoped engine."""
    return db_repos.PizzeriaRepository.from_engine(engine=engine)


def get_ranking_repo(engine: EngineDep) -> db_repos.RankingsRepository:
    """Return a RankingsRepository bound to the request-scoped engine."""
    return db_repos.RankingsRepository.from_engine(engine=engine)


CategoryPayloadRepoDep = Annotated[
    db_repos.CategoryPayloadRepository,
    Depends(get_category_payload_repo),
]
HtmlRepoDep = Annotated[storage_repos.HtmlStorageRepository, Depends(get_html_repo)]
PizzeriaRepoDep = Annotated[
    db_repos.PizzeriaRepository,
    Depends(get_pizzeria_repo),
]
RankingRepoDep = Annotated[db_repos.RankingsRepository, Depends(get_ranking_repo)]
