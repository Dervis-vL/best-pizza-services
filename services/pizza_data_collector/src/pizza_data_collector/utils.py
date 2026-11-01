"""Utility functions for the scraper."""

from pizza_data_collector import constants
from pizza_platform_shared import enums as shared_enums


def standardize_award_name(raw_award_name: str) -> str:
    """Standardize award name by:
    - Stripping "-" and everything after it (e.g. "Best Pizza - Italy" -> "Best Pizza")
    - Stripping leading and trailing whitespace
    - Removing trailing year (e.g. "Best Pizza 2023" -> "Best Pizza")
    - Uppercasing first letter of each word (e.g. "best pizza" -> "Best Pizza")
    """
    # Strip "-" and everything after it
    award_name = raw_award_name.split("-", maxsplit=1)[0]
    # Strip whitespace
    award_name = award_name.strip()
    # Remove trailing year
    words = award_name.split()
    if words and words[-1] in map(str, shared_enums.Year):
        award_name = " ".join(words[:-1])
    # Uppercase first letter of each word
    return award_name.title()


def extract_pizzeria_name(endpoint_path: str) -> str:
    """Extract pizzeria name from URL path, stripping date and version suffixes.

    Stripping rules (applied in order):
    - All parts are digits (e.g. 2023-10-15) → return as-is
    - Last 2 >= 2022, third-to-last 1-11 → strip last 3 (e.g. name-5-2023-2024 → name)
    - Last >= 2022, second-to-last 1-11  → strip last 2 (e.g. name-5-2023      → name)
    - Last >= 2022, 2+ parts             → strip last 1 (e.g. name-foo-2023  → name-foo)
    - Last 1-14, second-to-last >= 2022  → strip last 2 (e.g. name-2023-4      → name)
    - Last 1-14                          → strip last 1 (e.g. name-4           → name)
    - Post-pass: last two parts digits   → merge with dot (e.g. name-2-0     → name-2.0)
    """
    slug = endpoint_path.rstrip("/").split("/")[-1]
    if not slug:
        msg = f"Invalid pizzeria endpoint path: {endpoint_path}"
        raise ValueError(msg)

    parts = slug.split("-")
    # Last two values >= 2022, third-to-last between 1-11  ->  strip last 3
    if (  # pylint: disable=too-many-boolean-expressions
        len(parts) > constants.PizzaNameRules.HAS_THREE_PARTS
        and parts[-1].isdigit()
        and int(parts[-1]) >= shared_enums.Year.Y2022.value
        and parts[-2].isdigit()
        and int(parts[-2]) >= shared_enums.Year.Y2022.value
        and parts[-3].isdigit()
        and 0 < int(parts[-3]) <= constants.PizzaNameRules.PART_ELEVEN
    ):
        parts = parts[:-3]
    # last two values >= 2022, 2+ parts  ->  strip both
    elif (  # pylint: disable=too-many-boolean-expressions
        len(parts) >= constants.PizzaNameRules.HAS_TWO_PARTS
        and parts[-1].isdigit()
        and int(parts[-1]) >= shared_enums.Year.Y2022.value
        and parts[-2].isdigit()
        and int(parts[-2]) >= shared_enums.Year.Y2022.value
    ) or (
        len(parts) > constants.PizzaNameRules.HAS_TWO_PARTS
        and parts[-1].isdigit()
        and int(parts[-1]) >= shared_enums.Year.Y2022.value
        and parts[-2].isdigit()
        and 0 < int(parts[-2]) <= constants.PizzaNameRules.PART_FIVE
    ):
        parts = parts[:-2]
    # Last value >= 2022, 2+ parts  ->  strip last
    elif (
        len(parts) >= constants.PizzaNameRules.HAS_TWO_PARTS
        and parts[-1].isdigit()
        and int(parts[-1]) >= shared_enums.Year.Y2022.value
    ):
        parts = parts[:-1]
    # Last value between 1-14, second-to-last >= 2022  -> strip last 2
    elif (  # pylint: disable=too-many-boolean-expressions
        len(parts) > constants.PizzaNameRules.HAS_TWO_PARTS
        and parts[-1].isdigit()
        and 0 < int(parts[-1]) < constants.PizzaNameRules.PART_FOURTEEN
        and parts[-2].isdigit()
        and int(parts[-2]) >= shared_enums.Year.Y2022.value
    ) or (
        len(parts) > constants.PizzaNameRules.HAS_TWO_PARTS
        and parts[-1].isdigit()
        and 0 < int(parts[-1]) < constants.PizzaNameRules.PART_ELEVEN
        and parts[-2].isdigit()
        and 0 < int(parts[-2]) < constants.PizzaNameRules.PART_ELEVEN
    ):
        parts = parts[:-2]
    # last value between 1-14  ->  strip last 1
    elif parts[-1].isdigit() and 0 < int(parts[-1]) < constants.PizzaNameRules.PART_FOURTEEN:
        parts = parts[:-1]

    # Post-pass: When last two parts are digits  ->  merge with dot separator
    if (
        len(parts) >= constants.PizzaNameRules.HAS_TWO_PARTS
        and parts[-1].isdigit()
        and parts[-2].isdigit()
    ):
        parts = [*parts[:-2], f"{parts[-2]}.{parts[-1]}"]

    parsed_slug = "-".join(parts)
    return parsed_slug.lower().replace(" ", "-").strip()
