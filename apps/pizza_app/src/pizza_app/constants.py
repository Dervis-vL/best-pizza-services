"""Constants for the Streamlit app."""

from typing import Final


class Filters:
    """Constants for filter names in the Streamlit app."""

    HEADER: Final[str] = "Filters"
    PLACEHOLDER: Final[str] = "e.g. Pepe in Grani"
    YEARS: Final[str] = "Years"
    CATEGORIES: Final[str] = "Categories"
    EXCELLENT_CATEGORIES: Final[str] = "Excellent Categories"
    SPECIAL_AWARDS: Final[str] = "Special Awards"


class AppContext:
    """Constants for the config names of the Streamlit app."""

    TAB_TITLE: Final[str] = "🍕 Top Pizzerias Platform"
    TAB_ICON: Final[str] = "🍕"
    PAGE_TITLE: Final[str] = "🍕 Pizzerias — World Map"
    LAYOUT: Final[str] = "wide"
    CAPTION: Final[str] = "Locations sourced from 50 Top Pizza rankings."
    BIND: Final[str] = "query-params"
