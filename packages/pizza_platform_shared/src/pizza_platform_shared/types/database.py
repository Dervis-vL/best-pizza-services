"""Database types used across the pizza app/services."""

from typing import Annotated

import pydantic

PostgresName = Annotated[
    str,
    pydantic.StringConstraints(
        pattern=r"^[a-z_][a-z0-9_]*$",
        max_length=63,
    ),
]

SchemaName = Annotated[
    PostgresName | None,
    pydantic.BeforeValidator(lambda x: None if (x == "" or x.lower() == "none") else x),
]

TableName = PostgresName

BucketName = Annotated[
    str,
    pydantic.StringConstraints(
        pattern=r"^[a-z0-9][a-z0-9\-]*[a-z0-9]$",
        min_length=3,
        max_length=63,
    ),
]

Region = Annotated[
    str,
    pydantic.StringConstraints(
        pattern=r"^[a-z]{2}-[a-z]{3}$",
        max_length=6,
    ),
]


class TableNames(pydantic.BaseModel):
    """Base model for table names.

    Subclasses should define fields for each table name,
    and validation will ensure at least one is defined.
    """

    model_config = pydantic.ConfigDict(frozen=True, extra="forbid")

    def __getitem__(self, key: str) -> str:
        """Allow dict-like access to table names."""
        return getattr(self, key)

    def __contains__(self, key: str) -> bool:
        """Check if table name exists."""
        return hasattr(self, key)

    def values(self) -> list[TableName]:
        """Get all table names."""
        return [
            field_info.default for field_info in self.__class__.model_fields.values()
        ]

    @pydantic.model_validator(mode="after")
    def validate_at_least_one_table(self) -> TableNames:
        """Ensure at least one table is defined."""
        if not self.__class__.model_fields:
            raise ValueError(
                f"{self.__class__.__name__} must define at least one table name field."
            )
        return self
