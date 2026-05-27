"""Pizza API settings."""

import pydantic as pd
import pydantic_settings as pd_settings


class PizzaAPISettings(pd_settings.BaseSettings):
    """Pizza API settings from env vars."""

    model_config = pd_settings.SettingsConfigDict(
        env_file=".env",
        env_prefix="API_",
        extra="ignore",
    )

    base_url: pd.AnyHttpUrl = pd.Field(..., description="Base URL of the pizza platform API")
