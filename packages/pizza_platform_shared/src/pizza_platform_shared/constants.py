"""Constants for the scraper."""

from typing import Final

import yarl

from pizza_platform_shared import types

URL_HOME: Final = yarl.URL("https://www.50toppizza.it/")


class PizzaTableNames(types.TableNames):
    """Constants for pizza database table names."""

    awards: types.TableName = "awards"
    categories: types.TableName = "categories"
    pizzerias: types.TableName = "pizzerias"
    editions: types.TableName = "editions"
    rankings: types.TableName = "rankings"
    webpages: types.TableName = "webpages"
    locations: types.TableName = "locations"


class ModelColumnLengths:
    """Constants for model column lengths."""

    NAME: Final[int] = 100
    DESCRIPTION: Final[int] = 500
    URL: Final[int] = 500
    SLUG: Final[int] = 100
    PHONE: Final[int] = 20


class YearRange:
    """Constants for year range validation."""

    MIN: Final[int] = 2017
    MAX: Final[int] = 2030
