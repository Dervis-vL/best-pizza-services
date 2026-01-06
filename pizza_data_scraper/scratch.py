"""Scratch file to test changes before committing."""

import pathlib

from pizza_data_scraper import enums, logic, utils

if __name__ == "__main__":
    # CONFIG
    ROOT_PATH = pathlib.Path(__file__).parent
    HTML_OUTPUT_PATH = ROOT_PATH / "local" / "HTML" / "USA_2024.html"
    location = enums.Categories.USA
    year = enums.Year.Y2024

    # Scrape html data
    scraped_data = logic.get_scraped_data(location, year)

    # Write to file
    utils.soup_to_file(scraped_data, HTML_OUTPUT_PATH)
