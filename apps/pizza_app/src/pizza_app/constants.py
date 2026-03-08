"""Constants for the scraper."""

from typing import Final
import yarl

from pizza_app import types


URL_HOME: Final[yarl.URL] = yarl.URL("https://www.50toppizza.it/")


class PizzaTableNames(types.TableNames):
    """Constants for pizza database table names."""

    categories: types.TableName = "categories"
    pizzerias: types.TableName = "pizzerias"
    ranking_editions: types.TableName = "ranking_editions"
    ranking_entries: types.TableName = "ranking_entries"
    webpages: types.TableName = "webpages"
    locations: types.TableName = "locations"


class Filters:
    """Constants for filter names in the Streamlit app."""

    HEADER: Final[str] = "Filters"
    PLACEHOLDER: Final[str] = "e.g. Pepe in Grani"
    YEARS: Final[str] = "Years"
    CATEGORIES: Final[str] = "Categories"
    EXCELLENT_CATEGORIES: Final[str] = "Excellent Categories"
    SPECIAL_AWARDS: Final[str] = "Special Awards"
