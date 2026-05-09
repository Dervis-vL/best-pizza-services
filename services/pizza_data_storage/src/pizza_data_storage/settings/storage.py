"""Pizza object storage settings."""

import pydantic as pyd
import pydantic_settings as pyd_settings

from pizza_platform_shared import types


class PizzaStorageSettings(pyd_settings.BaseSettings):
    """Pizza object storage settings from env vars."""

    model_config = pyd_settings.SettingsConfigDict(
        env_file=".env",
        env_prefix="STORAGE_",
        extra="ignore",
        hide_input_in_errors=True,
    )

    endpoint: pyd.AnyHttpUrl = pyd.Field(
        ..., description="Scaleway object storage endpoint"
    )
    key_id: str = pyd.Field(
        min_length=20, pattern=r"^SCW[A-Z0-9]+$", description="Access key"
    )
    secret: pyd.SecretStr = pyd.Field(min_length=32, description="Scaleway secret key")
    bucket: types.BucketName = pyd.Field(..., description="Storage bucket name")
    region: types.Region = pyd.Field(..., description="Storage bucket region")
