"""Pizza app enums."""

from enum import StrEnum


class DatabaseType(StrEnum):
    """Supported database types."""

    POSTGRESQL = "postgresql"
    SQLITE = "sqlite"