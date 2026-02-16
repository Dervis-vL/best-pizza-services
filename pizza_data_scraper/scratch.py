"""Scratch file to test changes before committing."""

import pathlib
import re

from sqlalchemy import orm
import yarl

from pizza_data_scraper import logic, utils, schemas, settings
from pizza_data_scraper.models.base import BaseModel

if __name__ == "__main__":
    # FLAGS
    SCRAPE_RANKING_DATA = True
    SCRAPE_PIZZERIA_DATA = True
    WRITE_TO_FILE = False

    # CONSTANTS
    URL_PATTERN = re.compile(r'href="(https://www\.50toppizza\.it/(?:referenza|recensione)/[^"]+)"')
    DATABASE = "POSTGRESQL"

    # PATHS
    ROOT_PATH = pathlib.Path(__file__).parent.parent
    HTML_OUTPUT_PATH = ROOT_PATH / "dev" / "HTML" / "EUROPE_2025.html"
    RANKINGS_JSON_PATH = ROOT_PATH / "dev" / "JSON" / "yearly_categories.json"
    DEFAULT_DB_PATH = ROOT_PATH / "dev" / "db" / "test_pizza.db"


    # Load config
    config = utils.load_ranking_config(config_path=RANKINGS_JSON_PATH)

    # Setup database
    if DATABASE == "SQLITE":
        engine = utils.get_sqlite_engine(
            db_path=DEFAULT_DB_PATH,
            model=BaseModel,
            )
    elif DATABASE == "POSTGRESQL":
        engine = utils.get_postgres_engine(
            db_url=settings.pizza_db.connection_string,
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
            utils.update_rankings_scraped_at(engine=engine, edition_id=edition.id)

            if WRITE_TO_FILE:
                # Write to file
                output_path = ROOT_PATH / "dev" / "HTML" / f"{edition.category.slug}_{edition.year}.html"
                if not output_path.exists():
                    utils.soup_to_file(scraped_ranked_data, output_path)

            # Scrape pizzeria data
            pizzerria_urls = list(set(URL_PATTERN.findall(scraped_ranked_data.prettify())))
            yarl_pizzeria_urls = [yarl.URL(url) for url in pizzerria_urls]

            pizzerias_schemas = [
                schemas.PizzeriaSchema(
                    name=utils.extract_pizzeria_name(endpoint_path=url.path),
                    slug=url.path.rstrip("/").split("/")[-1],
                    description=None
                )
                for url in yarl_pizzeria_urls
            ]

            webpages_schemas = [
                schemas.WebpagesSchema(
                    slug=url.path.rstrip("/").split("/")[-1],
                    url=url.human_repr()
                )
                for url in yarl_pizzeria_urls
            ]

            pizzeria_endpoints_schema = schemas.PizzeriaEndpointsSchema(
                pizzerias=pizzerias_schemas,
                webpages=webpages_schemas
            )

            # seed pizzeria db
            with SessionLocal() as db:
                utils.seed_pizzeria_database(db=db, config=pizzeria_endpoints_schema)

    if SCRAPE_PIZZERIA_DATA:
        # Get all pizzerias from db which have 'scraped_at' as null
        not_scraped_pizzerias = utils.query_not_scraped_pizzerias(engine=engine)
        
        # Scrape html data for each pizzeria page
        for i, pizzeria_webpage in enumerate(not_scraped_pizzerias):
            url = yarl.URL(pizzeria_webpage.url)
            print(url)
            pizzeria_soup = logic.scrape_data_from_url(url=url.human_repr())
            utils.update_pizzerias_scraped_at(engine=engine, pizzeria_id=pizzeria_webpage.id)

            if WRITE_TO_FILE:
                # Write to file
                pizzeria_output_path = ROOT_PATH / "dev" / "HTML" / f"{pizzeria_webpage.slug}.html"
                print(f"Scraped {i+1}/{len(not_scraped_pizzerias)}: {pizzeria_webpage.slug}")
                # Check if file exists
                if not pizzeria_output_path.exists():
                    utils.soup_to_file(pizzeria_soup, pizzeria_output_path)