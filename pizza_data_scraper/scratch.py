"""Scratch file to test changes before committing."""

import pathlib

from pizza_data_scraper import enums, logic, utils

if __name__ == "__main__":
    # CONFIG
    WRITE_TO_FILE = False
    ROOT_PATH = pathlib.Path(__file__).parent.parent
    HTML_OUTPUT_PATH = ROOT_PATH / "dev" / "HTML" / "EUROPE_2024.html"
    location = enums.Categories.EUROPE
    year = enums.Year.Y2025

    # Scrape html data
    scraped_data = logic.get_scraped_data(location, year)

    if WRITE_TO_FILE:
        # Write to file
        utils.soup_to_file(scraped_data, HTML_OUTPUT_PATH)
