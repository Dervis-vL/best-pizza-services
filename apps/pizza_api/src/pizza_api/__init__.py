"""Pizza platform API."""

from importlib.metadata import metadata

_metadata = metadata("pizza-api")
__version__ = _metadata["Version"]
__description__ = _metadata["Summary"]
