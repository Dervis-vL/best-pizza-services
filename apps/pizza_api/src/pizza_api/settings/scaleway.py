"""Scaleway settings for triggering worker jobs."""

import pydantic as pyd
import pydantic_settings as pyd_settings


class ScalewaySettings(pyd_settings.BaseSettings):
    """Credentials and job-definition IDs for triggering the job."""

    model_config = pyd_settings.SettingsConfigDict(
        env_prefix="SCW_",
        env_file=".env",
        extra="ignore",
    )

    access_key: pyd.SecretStr = pyd.Field(description="Scaleway API access key.")
    secret_key: pyd.SecretStr = pyd.Field(description="Scaleway API secret key.")
    default_project_id: str = pyd.Field(description="Scaleway project id.")
    default_region: str = pyd.Field(default="fr-par", description="Scaleway region.")
    run_pending_job_id: str = pyd.Field(
        description="Job Definition id for the worker run-pending job.",
    )
