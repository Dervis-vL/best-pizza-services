"""Pizza database settings."""

from typing import Annotated

import pydantic
import pydantic_settings
import sqlalchemy as sa
from sqlalchemy import engine as sa_engine



class PizzaDatabaseSettings(pydantic_settings.BaseSettings):
    """Pizza database settings from env vars."""

    host: Annotated[str, pydantic.Field(...)]
    port: Annotated[int, pydantic.Field(...)]
    username: Annotated[str, pydantic.Field(...)]
    password: Annotated[pydantic.SecretStr, pydantic.Field(...)]
    ssl_enabled: Annotated[bool, pydantic.Field(...)]

    database_name: Annotated[str, pydantic.Field(...)]
    schema_name: Annotated[str, pydantic.Field(...)]

    @property
    def ssl_mode(self) -> str:
        """Construct ssl mode string used in connection string."""
        return "require" if self.ssl_enabled else "prefer"

    @property
    def connection_string(self) -> sa_engine.URL:
        """Construct connection string from fields."""
        return sa.URL.create(
            "postgresql",
            username=self.username,
            password=self.password.get_secret_value(),  # pylint: disable=no-member
            host=self.host,
            port=self.port,
            database=self.database_name,
            query={"sslmode": self.ssl_mode},
        )

    model_config = pydantic_settings.SettingsConfigDict(
        hide_input_in_errors=True,
        env_prefix="DB_",
    )
