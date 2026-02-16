"""Pizza database settings."""

from typing import ClassVar

import pydantic_settings

from pizza_data_scraper import constants, settings, types


class PizzaDatabaseSettings(settings.DatabaseSettings):
    """Pizza database settings from env vars."""

    model_config = pydantic_settings.SettingsConfigDict(
        env_prefix="PIZZA_DB_",
    )

    tables: ClassVar[types.TableNames] = constants.PizzaTableNames()
