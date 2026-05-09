"""Constants for the Streamlit app."""

from typing import Final


class AppContext:
    """Constants for the config names of the Streamlit app."""

    TAB_TITLE: Final[str] = "🍕 Top Pizzerias Platform"
    TAB_ICON: Final[str] = "🍕"
    PAGE_TITLE: Final[str] = "🍕 Pizzerias — World Map"
    LAYOUT: Final[str] = "wide"
    CAPTION: Final[str] = "Locations sourced from 50 Top Pizza rankings."
    HEADER: Final[str] = """Explore the world's best pizzerias, ranked and reviewed by
        [50 Top Pizza](https://www.50toppizza.com). Use the sidebar filters to narrow
        down by year and/or category — whether you're after the global top 50, a
        regional list, or special awards. You might just find an acclaimed slice closer
        to home than you'd expect.
        """
    DISCLAIMER: Final[str] = """
        **Disclaimer:**\n
        All ranking data displayed in this application is sourced exclusively from
        [50 Top Pizza](https://www.50toppizza.com) and remains the intellectual property
        of its respective owners. This application does not claim any rights over the
        data. The data has not been altered, manipulated, or editorially modified in any
        way. It is reproduced as published. This application is an independent,
        non-commercial project and is not affiliated with, endorsed by, or officially
        connected to 50 Top Pizza or any of its associated organisations.
        """


class Filters:
    """Constants for filter names in the Streamlit app."""

    DEFAULT: Final[str] = "All"
    HEADER: Final[str] = "Filters"
    PLACEHOLDER: Final[str] = "e.g. Pepe in Grani"
    YEARS: Final[str] = "Years"
    CATEGORIES: Final[str] = "Categories"
    EXCELLENT_CATEGORIES: Final[str] = "Excellent Categories"
    SPECIAL_AWARDS: Final[str] = "Special Awards"


class QueryParam:
    """Constants for the query params."""

    COUNTRY: Final[str] = "selected_country"
    CITY: Final[str] = "selected_city"
    YEAR: Final[str] = "year_"
    CATEGORY: Final[str] = "cat_"
    BIND: Final[str] = "query-params"
