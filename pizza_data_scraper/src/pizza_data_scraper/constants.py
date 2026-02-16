"""Constants for the scraper."""

from typing import Final
import yarl

from pizza_data_scraper import types

URL_HOME: Final = yarl.URL("https://www.50toppizza.it/")


class CategoryEndpoints:
    """Constants for category endpoints."""

    WORLD: Final[str] = "world"
    LATIN_AMERICA: Final[str] = "pizza-latin-america"
    EUROPE: Final[str] = "europe"
    ASIA_PACIFIC: Final[str] = "pizza-asia-pacific"
    ITALY: Final[str] = "pizza-italia"
    USA: Final[str] = "usa"
    SELECTION_TYPE: Final[str] = "50-top"


class ColumnLengths:
    """Constants for column lengths."""

    NAME: Final[int] = 100
    DESCRIPTION: Final[int] = 500
    URL: Final[int] = 500
    SLUG: Final[int] = 200


class PizzaTableNames(types.TableNames):
    """Constants for pizza database table names."""

    categories: types.TableName = "categories"
    pizzerias: types.TableName = "pizzerias"
    ranking_editions: types.TableName = "ranking_editions"
    ranking_entries: types.TableName = "ranking_entries"
    webpages: types.TableName = "webpages"
    locations: types.TableName = "locations"