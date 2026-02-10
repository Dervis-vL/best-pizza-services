"""Scratch file to test changes before committing."""

import pathlib

from sqlalchemy import orm
import yarl

from pizza_data_scraper import enums, logic, utils
from pizza_data_scraper.models.base import BaseModel

if __name__ == "__main__":
    # FLAGS
    SCRAPE_RANKING_DATA = True
    WRITE_TO_FILE = True

    # CONSTANTS
    CARDS_SELECTOR = "a#scheda"

    # PATHS
    ROOT_PATH = pathlib.Path(__file__).parent.parent
    HTML_OUTPUT_PATH = ROOT_PATH / "dev" / "HTML" / "EUROPE_2025.html"
    RANKINGS_JSON_PATH = ROOT_PATH / "dev" / "JSON" / "yearly_categories.json"
    DEFAULT_DB_PATH = ROOT_PATH / "dev" / "db" / "test_pizza.db"


    # Load config
    config = utils.load_ranking_config(config_path=RANKINGS_JSON_PATH)

    # Setup database
    engine = utils.get_sqlite_engine(
        db_path=DEFAULT_DB_PATH,
        model=BaseModel,
        )

    # Seed database
    SessionLocal = orm.sessionmaker(bind=engine)
    with SessionLocal() as db:
        stats = utils.seed_database(
            db=db,
            config=config
        )

if SCRAPE_RANKING_DATA:
    # Get all urls from db which have 'scraped_at' as null
    not_scraped_rankings = utils.query_not_scraped_ranking_editions(engine=engine)

    # Scrape html ranked categories data
    for edition in not_scraped_rankings:
        url = yarl.URL(edition.endpoint_url)
        print(url)
        scraped_ranked_data = logic.scrape_ranked_categories_data(url=str(url))

        if WRITE_TO_FILE:
            # Write to file
            output_path = ROOT_PATH / "dev" / "HTML" / f"{edition.category.slug}_{edition.year}.html"
            if not output_path.exists():
                utils.soup_to_file(scraped_ranked_data, output_path)

        # # Scrape pizzeria data from cards
        # cards = scraped_ranked_data.select(CARDS_SELECTOR)
        # for i, card in enumerate(cards):
        #     name = card.select_one("h3").get_text(strip=True).lower().replace(" ", "_")
        #     pizzeria_soup = logic.get_scraped_pizzeria_data(card)

        #     if WRITE_TO_FILE:
        #         # Write to file
        #         pizzeria_output_path = ROOT_PATH / "dev" / "HTML" / f"pizzeria_{name}.html"
        #         # Check if file exists
        #         if not pizzeria_output_path.exists():
        #             utils.soup_to_file(pizzeria_soup, pizzeria_output_path)