"""Scratch file to test changes before committing."""

import pathlib

from pizza_data_management import logic, utils


if __name__ == "__main__":
    # FLAGS
    SCRAPE_RANKING_DATA = True
    SCRAPE_PIZZERIA_DATA = True
    WRITE_TO_FILE = True

    # PATHS
    ROOT_PATH = pathlib.Path(__file__).parent.parent
    RANKINGS_JSON_PATH = ROOT_PATH / "dev" / "JSON" / "yearly_categories_test_set.json"


    # Load config
    config = utils.load_ranking_config(config_path=RANKINGS_JSON_PATH)

    # seed
    logic.seed_categories_and_editions(config=config)

    if SCRAPE_RANKING_DATA:
        # Scrape, parse and seed
        logic.seed_pizzeria_pages()

    if SCRAPE_PIZZERIA_DATA:
        # Scrape, parse and seed
        logic.seed_pizzeria_locations()
