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

    job_id: int = pyd.Field(..., description="Worker job execution ID.")
