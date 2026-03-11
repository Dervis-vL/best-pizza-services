"""Application settings for the pizza app."""

from typing import Annotated

import pydantic as pyd
import pydantic_settings as pyd_settings

from pizza_platform_shared import enums


class Application(pyd_settings.BaseSettings):
    """Application settings."""

    database_type: Annotated[
        enums.DatabaseType,
        pyd.Field(description="Type of database to connect to."),
    ]

    class Config:
        """Pydantic config."""

        extra="ignore"
        env_file = ".env"
        env_file_encoding = "utf-8"
