"""Scratch file to test changes before committing."""

import pathlib
import re

from sqlalchemy import orm
import yarl

from pizza_data_scraper import logic, utils
from pizza_data_scraper.models.base import BaseModel

if __name__ == "__main__":
    # FLAGS
    SCRAPE_RANKING_DATA = True
    WRITE_TO_FILE = True

    # CONSTANTS
    URL_PATTERN = re.compile(r'href="(https://www\.50toppizza\.it/(?:referenza|recensione)/[^"]+)"')

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
            url = yarl.URL(edition.url)
            print(url)
            scraped_ranked_data = logic.scrape_data_from_url(url=url.human_repr())
            utils.update_scraped_at(engine=engine, edition_id=edition.id)

            if WRITE_TO_FILE:
                # Write to file
                output_path = ROOT_PATH / "dev" / "HTML" / f"{edition.category.slug}_{edition.year}.html"
                if not output_path.exists():
                    utils.soup_to_file(scraped_ranked_data, output_path)

            # Scrape pizzeria data from cards
            pizzerria_urls = list(set(URL_PATTERN.findall(scraped_ranked_data.prettify())))
            yarl_pizzeria_urls = [yarl.URL(url) for url in pizzerria_urls]
            for i, url in enumerate(yarl_pizzeria_urls):
                name = url.path.split("/")[-2]

                # seed pizzeria db
                

                pizzeria_soup = logic.scrape_data_from_url(url=url.human_repr())

                if WRITE_TO_FILE:
                    # Write to file
                    pizzeria_output_path = ROOT_PATH / "dev" / "HTML" / f"{name}.html"
                    print(f"Scraped {i+1}/{len(yarl_pizzeria_urls)}: {name}")
                    # Check if file exists
                    if not pizzeria_output_path.exists():
                        utils.soup_to_file(pizzeria_soup, pizzeria_output_path)