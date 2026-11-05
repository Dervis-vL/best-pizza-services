"""Aggregations over the rankings."""

from importlib.metadata import metadata

_metadata = metadata("pizza-data-stats")
__version__ = _metadata["Version"]
__description__ = _metadata["Summary"]

__all__ = [
    "__description__",
    "__version__",
]
