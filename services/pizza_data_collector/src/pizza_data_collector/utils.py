"""Utility functions for the scraper."""


def extract_pizzeria_name(endpoint_path: str) -> str:
    """Extract pizzeria name from URL path, stripping date and version suffixes.

    Stripping rules (applied in order):
    - All parts are digits (e.g. 2023-10-15)   → return as-is
    - Last 2 >= 2022, third-to-last 1-11       → strip last 3 (e.g. name-5-2023-2024  → name)
    - Last >= 2022, second-to-last 1-11        → strip last 2 (e.g. name-5-2023       → name)
    - Last >= 2022, 2+ parts                   → strip last 1 (e.g. name-foo-2023     → name-foo)
    - Last 1-14, second-to-last >= 2022        → strip last 2 (e.g. name-2023-4       → name)
    - Last 1-14                                → strip last 1 (e.g. name-4            → name)
    - Post-pass: last two remaining parts digits → merge with dot (e.g. name-2-0      → name-2.0)
    """
    slug = endpoint_path.rstrip("/").split("/")[-1]
    if not slug:
        raise ValueError(f"Invalid pizzeria endpoint path: {endpoint_path}")

    parts = slug.split("-")

    # All parts are digits (e.g. 2023-10-15)  ->  return as-is
    if all(p.isdigit() for p in parts):
        return slug

    # Last two values >= 2022, third-to-last between 1-11  ->  strip last 3
    if (
        len(parts) > 3
        and parts[-1].isdigit() and int(parts[-1]) >= 2022
        and parts[-2].isdigit() and int(parts[-2]) >= 2022
        and parts[-3].isdigit() and 0 < int(parts[-3]) <= 11
    ):
        parts = parts[:-3]
    # Last value >= 2022, second-to-last 1-11  ->  strip last 2
    elif (
        len(parts) > 2
        and parts[-1].isdigit() and int(parts[-1]) >= 2022
        and parts[-2].isdigit() and 0 < int(parts[-2]) <= 11
    ):
        parts = parts[:-2]
    # Last value >= 2022, 2+ parts  ->  strip last
    elif (
        len(parts) >= 2
        and parts[-1].isdigit() and int(parts[-1]) >= 2022
    ):
        parts = parts[:-1]
    # Last value between 1-14, second-to-last >= 2022  -> strip last 2
    elif (
        len(parts) > 2
        and parts[-1].isdigit() and 0 < int(parts[-1]) < 14
        and parts[-2].isdigit() and int(parts[-2]) > 2022
    ):
        parts = parts[:-2]
    # last value between 1-14  ->  strip last 1
    elif parts[-1].isdigit() and 0 < int(parts[-1]) < 14:
        parts = parts[:-1]

    # Post-pass: When last two parts are digits  ->  merge with dot separator
    if len(parts) >= 2 and parts[-1].isdigit() and parts[-2].isdigit():
        parts = parts[:-2] + [f"{parts[-2]}.{parts[-1]}"]

    parsed_slug = "-".join(parts)
    return parsed_slug.lower().replace(" ", "-").strip()
