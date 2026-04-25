"""Pizza platform API."""

from importlib.metadata import metadata 


meta = metadata("pizza_api")
__version__ = meta["version"]
__description__ = meta["description"]
