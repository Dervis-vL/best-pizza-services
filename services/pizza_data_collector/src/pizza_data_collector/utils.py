"""Utility functions for the scraper."""

import pathlib

import bs4 as bs


def soup_to_file(soup: bs.BeautifulSoup, file_path: pathlib.Path) -> None:
    """Save BeautifulSoup object to an HTML file.

    :param soup: The BeautifulSoup object to save.
    :type soup: bs
    :param file_path: The path to the output HTML file.
    :type file_path: str
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(str(soup))


def extract_pizzeria_name(endpoint_path: str) -> str:
    """Extract pizzeria slug from URL path, stripping version suffixes like '-4'."""
    slug = endpoint_path.rstrip("/").split("/")[-1]
    if not slug:
        raise ValueError(f"Invalid pizzeria endpoint path: {endpoint_path}")

    # Strip numeric suffix (e.g., "napoli-on-the-road-4" -> "napoli-on-the-road")
    parts = slug.rsplit("-", 1)
    if len(parts) == 2 and parts[-1].isdigit():
        return parts[0]
    return slug
