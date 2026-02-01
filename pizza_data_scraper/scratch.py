"""Scratch file to test changes before committing."""

import pathlib

from sqlalchemy import orm

from pizza_data_scraper import enums, logic, utils
from pizza_data_scraper.models.base import BaseModel

if __name__ == "__main__":
    # CONFIG
    SCRAPE_RANKING_DATA = False
    WRITE_TO_FILE = True
    ROOT_PATH = pathlib.Path(__file__).parent.parent
    HTML_OUTPUT_PATH = ROOT_PATH / "dev" / "HTML" / "EUROPE_2025.html"
    CARDS_SELECTOR = "a#scheda"
    RANKINGS_JSON_PATH = ROOT_PATH / "dev" / "JSON" / "yearly_categories.json"
    DEFAULT_DB_URL = "sqlite:///./test_pizza.db"

    if SCRAPE_RANKING_DATA:
        location = enums.Categories.EUROPE
        year = enums.Year.Y2025

        # Scrape html ranked data
        scraped_ranked_data = logic.get_scraped_ranked_data(location, year)

        if WRITE_TO_FILE:
            # Write to file
            if not HTML_OUTPUT_PATH.exists():
                utils.soup_to_file(scraped_ranked_data, HTML_OUTPUT_PATH)

        # Scrape pizzeria data from cards
        cards = scraped_ranked_data.select(CARDS_SELECTOR)
        for i, card in enumerate(cards):
            name = card.select_one("h3").get_text(strip=True).lower().replace(" ", "_")
            pizzeria_soup = logic.get_scraped_pizzeria_data(card)

            if WRITE_TO_FILE:
                # Write to file
                pizzeria_output_path = ROOT_PATH / "dev" / "HTML" / f"pizzeria_{name}.html"
                # Check if file exists
                if not pizzeria_output_path.exists():
                    utils.soup_to_file(pizzeria_soup, pizzeria_output_path)

    rankings_schema = utils.load_ranking_config(config_path=RANKINGS_JSON_PATH)

    engine = utils.get_engine(DEFAULT_DB_URL)

    # Handle SQLite schema issue - create tables without schema for SQLite
    if "sqlite" in DEFAULT_DB_URL:
        # Temporarily remove schema for SQLite
        for table in BaseModel.metadata.tables.values():
            table.schema = None

    # Load config
    config = utils.load_ranking_config(config_path=RANKINGS_JSON_PATH)

    # Seed database
    SessionLocal = orm.sessionmaker(bind=engine)
    with SessionLocal() as db:
        stats = utils.seed_database(db, config)
