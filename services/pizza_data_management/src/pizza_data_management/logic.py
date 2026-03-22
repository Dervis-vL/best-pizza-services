"""Main logic for the pizza data scraper.

This script is a web scraper. It fetches information from 50toppizza.it,
concerning the best pizza's in the world. The web scraper collects:
Rank, name, country, region, place, address. 

The information is linked to an object.
"""

import logging
from typing import Generator
from urllib import request as url_request
from urllib.error import HTTPError, URLError

import bs4 as bs

from pizza_data_management import repositories, schemas, settings, utils

logger = logging.getLogger(__name__)


def seed_categories_and_editions(config: schemas.RankingEndpointsSchema) -> None:
    """Seed the database with the ranking categories and editions from a schema."""

    ranking_repo = repositories.RankingRepository.from_settings(
        db_settings=settings.pizza_db
    )
    ranking_repo.upsert_categories_and_editions(config=config)


def scrape_editions() -> Generator[schemas.PizzeriaEndpointsSchema, None, None]:
    """Scrape the ranking categories editions html pages."""
    ranking_repo = repositories.RankingRepository.from_settings(
        db_settings=settings.pizza_db
    )
    unscraped_editions = ranking_repo.get_unscraped_editions()
    for edition in unscraped_editions:
        soup = scrape_data_from_url(edition.url)
        if soup is None:
            continue

        ranking_repo.mark_edition_scraped(edition_id=edition.id)
        yield utils.create_pizzeria_schema(soup=soup, edition_id=edition.id)


def parse_pizzerias_and_webpages(config: schemas.PizzeriaEndpointsSchema) -> None:
    """Seed the database with the pizzerias and webpages from a schema."""

    pizzeria_repo = repositories.PizzeriaRepository.from_settings(
        db_settings=settings.pizza_db
    )
    pizzeria_repo.upsert_pizzerias_and_webpages(config=config)


def seed_pizzeria_pages() -> None:
    """Scrape the ranking categories editions html pages and seed the DB with pizzerias and webpages."""
    for pizzeria_schema_config in scrape_editions():
        parse_pizzerias_and_webpages(config=pizzeria_schema_config)


def scrape_pizzeria_pages() -> Generator[schemas.LocationSchema, None, None]:
    """Scrape the pizzeria pages for all pizzerias in the DB."""
    pizzeria_repo = repositories.PizzeriaRepository.from_settings(
        db_settings=settings.pizza_db
    )
    for webpage in pizzeria_repo.get_unscraped_pizzerias():
        soup = scrape_data_from_url(webpage.url)
        if soup is None:
            continue

        pizzeria_repo.mark_pizzeria_scraped(webpage_id=webpage.id)
        yield utils.create_location_schema(soup=soup, pizzeria_id=webpage.pizzeria_id)


def parse_pizzeria_page(location_schema: schemas.LocationSchema) -> None:
    """Parse a pizzeria page and update the database with the location data."""
    pizzeria_repo = repositories.PizzeriaRepository.from_settings(
        db_settings=settings.pizza_db
    )
    pizzeria_repo.upsert_location(location_config=location_schema)


def seed_pizzeria_locations() -> None:
    """Scrape the pizzeria pages for all pizzerias in the DB and update the DB with location data."""
    for location_schema in scrape_pizzeria_pages():
        parse_pizzeria_page(location_schema=location_schema)


def scrape_data_from_url(url: str) -> bs.BeautifulSoup:
    """Function for scraping data from the best pizza's website.

    :param url: The URL to scrape.
    :type url: str

    :return: The parsed HTML content.
    :rtype: BeautifulSoup
    """
    req = url_request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; pizza-scraper/1.0)"},
    )

    try:
        page = url_request.urlopen(req, timeout=10)
        return bs.BeautifulSoup(page, features="html.parser")

    except HTTPError as e:
        logging.warning(f"HTTP {e.code} fetching {url}: {e.reason} — skipping")
    except URLError as e:
        logging.warning(f"Failed to reach {url}: {e.reason} — skipping")
    except TimeoutError:
        logging.warning(f"Timeout fetching {url} — skipping")

    return None

