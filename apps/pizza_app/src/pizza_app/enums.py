"""Pizza app enums."""

from enum import StrEnum


class SegmentedControl(StrEnum):
    "Enums controlling the segmented view toggle."

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
