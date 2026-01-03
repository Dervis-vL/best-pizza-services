"""Scratch file to test changes before committing."""

from scraper import enums, logic

if __name__ == "__main__":
    # Example usage
    location = enums.Location.ITALY
    year = enums.Year.Y2025
    scraped_data = logic.get_scraped_data(location, year)
    print(scraped_data)