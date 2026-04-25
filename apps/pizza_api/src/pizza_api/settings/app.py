"""App settings for the pizza API."""

from typing import Annotated

import pydantic as pyd
import pydantic_settings as pyd_settings
from pizza_platform_shared import settings as shared_settings

from pizza_api import __version__, __description__


class ApplicationSettings(pyd_settings.BaseSettings):
    """Application settings for the pizza API."""

    model_config = pyd_settings.SettingsConfigDict(
        env_prefix="PIZZA_API_",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    title: str = "Best Pizza API"
    description: str = __description__
    version: str = __version__
    pizza_db: Annotated[
        shared_settings.PizzaDatabaseSettings,
        pyd.Field(default_factory=shared_settings.PizzaDatabaseSettings)
    ] = shared_settings.pizza_db
    debug: bool = False
