"""Pizza platform API."""

from pathlib import Path

import tomllib


_pyproject = tomllib.loads((Path(__file__).parent.parent.parent / "pyproject.toml").read_text())
__version__ = _pyproject["project"]["version"]
__description__ = _pyproject["project"]["description"]
