"""Pizza API Constants."""

import pathlib
from typing import Final


class ApiConstants:
    """Constants for the pizza API."""

    # Absolute path to the static directory
    STATIC_DIR: Final[pathlib.Path] = pathlib.Path(__file__).parent / "static"

    # URL path the static files are mounted at, and the favicon's URL.
    STATIC_URL: Final[str] = "/static"
    FAVICON_URL: Final[str] = f"{STATIC_URL}/pizza_slice.png"
