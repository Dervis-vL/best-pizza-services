"""App settings for the pizza API."""

from typing import Annotated

import pydantic as pyd
import pydantic_settings as pyd_settings

from pizza_api import __description__, __version__


class ApplicationSettings(pyd_settings.BaseSettings):
    """Application settings for the pizza API."""

    model_config = pyd_settings.SettingsConfigDict(
        env_prefix="PIZZA_API_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    title: Annotated[
        str,
        pyd.Field(description="The title of the API.", default="Best Pizza API"),
    ]
    description: Annotated[
        str,
        pyd.Field(description="The description of the API.", default=__description__),
    ]
    version: Annotated[
        str,
        pyd.Field(description="The version of the API.", default=__version__),
    ]
    debug: Annotated[
        bool,
        pyd.Field(description="Whether to enable debug mode.", default=False),
    ]
