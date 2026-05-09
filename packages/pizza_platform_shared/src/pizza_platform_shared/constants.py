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
