"""Base database settings."""

from typing import ClassVar

import pydantic
import pydantic_settings
import sqlalchemy as sa

from pizza_app import types


class DatabaseSettings(pydantic_settings.BaseSettings):
    """Base database settings from env vars. 

    Subclasses should define 'tables' ClassVar if they require tables to 
    be defined. Validation will ensure that any subclass that requires
    tables has them defined, but the base class itself can be used without 
    defining tables for cases where it's not needed (e.g., alembic 
    maintenance settings).

    Attributes:
        host: Database host.
        port: Database port.
        username: Database username.
        password: Database password (hidden in errors).
        ssl_enabled: Whether SSL is enabled for the database connection.
        database_name: Name of the database to connect to.
        schema_name: Name of the schema to use within the database.
        tables: ClassVar containing table names relevant to the settings, if required.
    """

    model_config = pydantic_settings.SettingsConfigDict(
        extra="ignore",
        hide_input_in_errors=True,
    )

    host: str = pydantic.Field(..., description="Database host")
    port: int = pydantic.Field(..., description="Database port")
    username: str = pydantic.Field(..., description="Database username")
    password: pydantic.SecretStr = pydantic.Field(..., description="Database password")
    ssl_enabled: bool = pydantic.Field(..., description="Whether SSL is enabled for the database connection")

    database_name: types.PostgresName = pydantic.Field(
        ..., description="Name of the database to connect to"
    )
    schema_name: types.SchemaName = pydantic.Field(..., description="Name of the schema to use within the database")

    # Database tables if required. Must be defined in subclasses, and is not an env var.
    tables: ClassVar[types.TableNames | None]

    @pydantic.model_validator(mode="after")
    def validate_tables_defined(self) -> "DatabaseSettings":
        """Validate that if 'requires_tables' is True in the config, then 'tables' ClassVar is defined in the subclass.

        This allows us to enforce that subclasses that need to define tables do so, 
        while still allowing the base class to be used without tables for cases like alembic settings.
        """
        config = self.model_config
        requires_tables: bool = config.get("requires_tables", True)  # type: ignore[assignment]

        # Skip validation for base class and classes that don't require tables
        if self.__class__ == DatabaseSettings or not requires_tables:
            return self

        if not hasattr(self.__class__, "tables") or self.__class__.tables is None:
            raise ValueError(
                f"{self.__class__.__name__} must define 'tables' ClassVar when 'requires_tables' is True."
            )
        return self

    @property
    def ssl_mode(self) -> str:
        """Construct ssl mode string used in connection string."""
        return "require" if self.ssl_enabled else "prefer"

    @property
    def connection_string(self) -> sa.engine.URL:
        """Return connection string from fields."""
        return sa.URL.create(
            "postgresql",
            username=self.username,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.database_name,
            query={"sslmode": self.ssl_mode},
        )
