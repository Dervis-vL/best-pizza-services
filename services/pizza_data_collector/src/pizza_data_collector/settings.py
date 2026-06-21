"""Scraper specific settings."""

import pydantic as pyd
import pydantic_settings as pyd_settings


class ScraperSettings(pyd_settings.BaseSettings):
    """Scraper retry settings."""

    model_config = pyd.ConfigDict(
        env_prefix="SCRAPER_",
        env_file=".env",
        extra="ignore",
    )

    timeout: int = pyd.Field(default=30, description="Per-request timeout [s].")
    max_attempts: int = pyd.Field(default=3, description="Total tries incl. first [n].")
    backoff_base: float = pyd.Field(default=1.0, description="Base for exponential backoff [s].")
    backoff_max: float = pyd.Field(default=60.0, description="Max backoff [s].")
