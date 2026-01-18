"""Utility functions for the scraper."""

from bs4 import BeautifulSoup as bs
import pathlib

from pizza_data_scraper import enums, constants


def create_endpoint(category: enums.Categories, year: enums.Year) -> str:
    """Create an endpoint URL based on category and year.

    :param category: The category for the endpoint.
    :type category: enums.Categories
    :param year: The year for the endpoint.
    :type year: enums.Year

    :return: The constructed endpoint URL.
    :rtype: str
    """
    endpoint_part = getattr(constants.CategoryEndpoints, category.name)
    return f"{constants.CategoryEndpoints.SELECTION_TYPE}-{endpoint_part}-{year.value}/" 


def soup_to_file(soup: bs, file_path: pathlib.Path) -> None:
    """Save BeautifulSoup object to an HTML file.

    :param soup: The BeautifulSoup object to save.
    :type soup: bs
    :param file_path: The path to the output HTML file.
    :type file_path: str
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(str(soup))