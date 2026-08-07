"""Pizza API specific settings."""

import pydantic as pyd
import pydantic_settings as pyd_settings


class APIRetrySettings(pyd_settings.BaseSettings):
    """API retry settings."""

    model_config = pyd_settings.SettingsConfigDict(
        env_prefix="API_",
        env_file=".env",
        extra="ignore",
    )

    timeout: int = pyd.Field(default=5, description="Per-request timeout [s].")
    max_attempts: int = pyd.Field(default=3, description="Total tries incl. first [n].")
    backoff_base: float = pyd.Field(default=1.0, description="Base for exponential backoff [s].")
    backoff_max: float = pyd.Field(default=10.0, description="Max backoff [s].")


class PizzaAPISettings(pyd_settings.BaseSettings):
    """Pizza API settings from env vars."""

    model_config = pyd_settings.SettingsConfigDict(
        env_file=".env",
        env_prefix="API_",
        extra="ignore",
    )

    base_url: pyd.AnyHttpUrl = pyd.Field(..., description="Base URL of the pizza platform API")
