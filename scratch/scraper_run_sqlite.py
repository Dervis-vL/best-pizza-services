"""Scratch file to test changes before committing."""

import pathlib

from local_database_settings import get_sqlite_engine
from pizza_data_storage import utils, repositories, models


if __name__ == "__main__":
    # FLAGS
    SCRAPE_RANKING_DATA = True
    SCRAPE_PIZZERIA_DATA = True
    WRITE_TO_FILE = False

    # PATHS
    ROOT_PATH = pathlib.Path(__file__).parent.parent
    DEV_FOLDER_PATH = ROOT_PATH / "dev"
    RANKINGS_JSON_PATH = DEV_FOLDER_PATH / "JSON" / "yearly_categories.json"
    DEFAULT_DB_PATH = DEV_FOLDER_PATH / "db" / "test_new_rankings_parsing.db"
    HTML_OUTPUT_PATH = DEV_FOLDER_PATH / "HTML"


    # Load config
    config = utils.load_ranking_config(config_path=RANKINGS_JSON_PATH)

    # create sqlite engine and tables
    engine = get_sqlite_engine(
        db_path=DEFAULT_DB_PATH,
        model=models.BaseModel,
    )

    # seed categories and editions from config
    ranking_repo: repositories.RankingsRepository = repositories.RankingsRepository.from_engine(
        engine=engine,
    )
    ranking_repo.seed_categories_and_editions(config=config)

    if SCRAPE_RANKING_DATA:
        # Create repository instance
        pizzeria_repo: repositories.PizzeriaRepository = repositories.PizzeriaRepository.from_engine(
                engine=engine,
            )
        # Scrape, parse and seed pages of pizzerias
        unscraped_editions = ranking_repo.get_editions()
    #     for edition in unscraped_editions:
    #         soup = logic.scrape_data_from_url(edition.url)
    #         if soup is None:
    #             continue

    #         ranking_repo.mark_edition_scraped(edition_id=edition.id)
    #         pizzeria_schema = utils.create_pizzeria_schema(soup=soup, edition_id=edition.id)
    #         pizzeria_repo.upsert_pizzerias_and_webpages(config=pizzeria_schema)

    #         if WRITE_TO_FILE and soup:
    #             # Write to file
    #             output_path = HTML_OUTPUT_PATH / f"{edition.category.slug}_{edition.year}.html"
    #             if not output_path.exists():
    #                 utils.soup_to_file(soup, output_path)

    # if SCRAPE_PIZZERIA_DATA:
    #     # Scrape, parse and seed locations
    #     for webpage in pizzeria_repo.get_unscraped_pizzerias():
    #         soup = logic.scrape_data_from_url(webpage.url)
    #         if soup is None:
    #             continue

    #         pizzeria_repo.mark_pizzeria_scraped(webpage_id=webpage.id)
    #         location_schema = utils.create_location_schema(
    #             soup=soup, pizzeria_id=webpage.pizzeria_id
    #         )
    #         pizzeria_repo.upsert_location(location_config=location_schema)

    #         if WRITE_TO_FILE:
    #             # Write to file
    #             pizzeria_output_path = HTML_OUTPUT_PATH / f"{webpage.slug}.html"
    #             # Check if file exists
    #             if not pizzeria_output_path.exists():
    #                 utils.soup_to_file(soup, pizzeria_output_path)
