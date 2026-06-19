"""Pizza app enums."""

from enum import StrEnum


class BaseCategories(StrEnum):
    """Base category enum."""

    @classmethod
    def list(cls) -> list[str]:
        """Return a list of all category values."""
        categories = []
        for subclass in cls.__subclasses__():
            categories.extend(subclass.list())
        categories.extend([member.value for member in cls])
        return categories


class Categories(BaseCategories):
    """Enum for best pizza categories."""

    ITALY = "Top Pizza Italia"
    WORLD = "Top Pizza World"
    EUROPE = "Top Pizza Europa"
    LATIN_AMERICA = "Top Pizza Latin America"
    ASIA_PACIFIC = "Top Pizza Asia-Pacific"
    USA = "Top Pizza USA"
    PIZZA_CHAINS = "Top Artisan Pizza Chains"


class CategoriesExcellent(BaseCategories):
    """Enum for best pizza categories with excellent awards."""

    ITALY_EXCELLENT = "Top Pizza Italia Excellent"
    EUROPE_EXCELLENT = "Top Pizza Europa Excellent"
    USA_EXCELLENT = "Top Pizza USA Excellent"
    PIZZA_CHAINS_EXCELLENT = "Excellent Artisan Pizza Chains"


class CategoriesSpecial(BaseCategories):
    """Enum for special awards categories."""

    WORLD_SPECIAL = "World Special Awards"
    LATIN_AMERICA_SPECIAL = "Latin America Special Awards"
    EUROPE_SPECIAL = "European Special Awards"
    ASIA_PACIFIC_SPECIAL = "Asia-Pacific Special Awards"
    ITALY_SPECIAL = "Italy Special Awards"
    USA_SPECIAL = "USA Special Awards"


class SegmentedControl(StrEnum):
    """Enums controlling the segmented view toggle."""

    MAP = "Map"
    LIST = "List"

    @classmethod
    def toggle_label(cls) -> str:
        """Returns the Streamlit toggle label."""
        return "View"

    @classmethod
    def toggle_key(cls) -> str:
        """Returns the Streamlit toggle key."""
        return cls.toggle_label().lower()

    @classmethod
    def values(cls) -> list[str]:
        """Returns all enum values as a list."""
        return [e.value for e in cls]
