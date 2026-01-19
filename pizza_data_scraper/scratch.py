"""Scratch file to test changes before committing."""

import pathlib

from pizza_data_scraper import enums, logic, utils

if __name__ == "__main__":
    # CONFIG
    WRITE_TO_FILE = True
    ROOT_PATH = pathlib.Path(__file__).parent.parent
    HTML_OUTPUT_PATH = ROOT_PATH / "dev" / "HTML" / "EUROPE_2025.html"
    CARDS_SELECTOR = "a#scheda"
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
