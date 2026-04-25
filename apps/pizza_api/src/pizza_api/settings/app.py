"""App settings for the pizza API."""

from pydantic_settings import BaseSettings, SettingsConfigDict

from pizza_api import __version__, __description__


class ApplicationSettings(BaseSettings):
    """Application settings for the pizza API."""

    model_config = SettingsConfigDict(
        env_prefix="PIZZA_API_",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    title: str = "Best Pizza API"
    description: str = __description__
    version: str = __version__
    host: str = ""
    port: int = 8000
    debug: bool = False
