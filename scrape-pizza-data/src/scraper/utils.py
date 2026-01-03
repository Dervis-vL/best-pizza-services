"""Utility functions for the scraper."""

from scraper import enums, constants


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