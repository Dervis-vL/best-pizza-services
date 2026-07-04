"""The adapter (cli) to fire the add category job."""

import logging

import typer

from pizza_data_storage import repositories as storage_repos
from pizza_data_storage.application import use_cases as storage_ucs
from pizza_worker import factories

logger = logging.getLogger(__name__)


def add_category(payload_id: int = typer.Option(..., envvar="WORKER_PAYLOAD_ID")) -> None:
    """Trigger a worker to add a new category and run the full scrape + parse cycle."""
    engine = factories.create_worker_engine()
    try:
        repo = storage_repos.CategoryPayloadRepository.from_engine(engine=engine)
        categories = storage_ucs.GetCategoryPayloadUseCase(payload_repository=repo).execute(
            payload_id=payload_id
        )
        result = factories.build_add_category_uc(engine=engine).execute(category_schemas=categories)
        storage_ucs.MarkCategoryPayloadAsConsumedUseCase(payload_repository=repo).execute(
            payload_id=payload_id
        )
    except Exception:
        storage_ucs.MarkCategoryPayloadAsFailedUseCase(payload_repository=repo).execute(
            payload_id=payload_id
        )
        logger.exception("Error while running add-category job: %s", payload_id)
        raise
    finally:
        engine.dispose()

    logger.info(
        "add-category done | editions %s / %s | webpages %s / %s",
        result.editions_scraped,
        result.editions_parsed,
        result.webpages_scraped,
        result.webpages_parsed,
    )
