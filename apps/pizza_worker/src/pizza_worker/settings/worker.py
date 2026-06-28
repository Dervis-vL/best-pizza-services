"""Worker specific settings module."""

import pydantic as pyd
import pydantic_settings as pyd_settings


class WorkerSettings(pyd_settings.BaseSettings):
    """Worker level settings."""

    model_config = pyd_settings.SettingsConfigDict(
        env_prefix="WORKER_",
        env_file=".env",
        extra="ignore",
    )

    log_level: str = pyd.Field(default="INFO", description="Logging level for the worker run.")
