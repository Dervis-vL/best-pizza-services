"""The adapter (cli) to fire the maintenance and process all pending job."""

import logging

from pizza_worker import factories

logger = logging.getLogger(__name__)


def run_pending() -> None:
    """Scrape and parse every edition and webpage still pending in DB."""
    engine = factories.create_worker_engine()
    try:
        result = factories.build_process_pending_uc(engine=engine).execute()
    finally:
        engine.dispose()

    logger.info(
        "run-pending done | editions %s / %s | webpages %s / %s",
        result.editions_scraped,
        result.editions_parsed,
        result.webpages_scraped,
        result.webpages_parsed,
    )
