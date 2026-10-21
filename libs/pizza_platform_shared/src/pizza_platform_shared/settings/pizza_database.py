"""Pizza database settings."""

from typing import ClassVar

import pydantic_settings

from pizza_platform_shared import constants
from pizza_platform_shared.settings.base_database import DatabaseSettings


class PizzaDatabaseSettings(DatabaseSettings):
    """Pizza database settings from env vars."""

    model_config = pydantic_settings.SettingsConfigDict(
        env_file=".env",
        env_prefix="PIZZA_DB_",
    )

    tables: ClassVar[constants.PizzaTableNames] = constants.PizzaTableNames()
