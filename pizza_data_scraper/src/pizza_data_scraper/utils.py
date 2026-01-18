"""Utility functions for the scraper."""

import bs4 as bs
import yarl
import pathlib
from bs4 import element as bs_element

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


def get_pizzeria_url_from_card(card: bs_element.Tag, attr: str) -> yarl.URL:
    """Get the URL from a pizzeria card element.

    :param card: The pizzeria card element.
    :type card: bs4.element.Tag
    :param attr: The attribute to extract the URL from.
    :type attr: str

    :return: The URL extracted from the card element.
    :rtype: yarl.URL
    """
    url_str = card.get(attr)
    if url_str is None:
        raise ValueError(f"The attribute '{attr}' is not found in the card element.")
    return yarl.URL(url_str)


def soup_to_file(soup: bs.BeautifulSoup, file_path: pathlib.Path) -> None:
    """Save BeautifulSoup object to an HTML file.

    :param soup: The BeautifulSoup object to save.
    :type soup: bs
    :param file_path: The path to the output HTML file.
    :type file_path: str
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(str(soup))