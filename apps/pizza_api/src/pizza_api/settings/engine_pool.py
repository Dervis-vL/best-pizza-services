"""App engine pool settings for the pizza API."""

from typing import Annotated

import pydantic as pyd
import pydantic_settings as pyd_settings


class ApiPoolSettings(pyd_settings.BaseSettings):
    """Application engine pool settings for the pizza API."""

    model_config = pyd_settings.SettingsConfigDict(env_file=".env", env_prefix="API_DB_POOL_")

    size: Annotated[
        int,
        pyd.Field(
            description="Per-instance number of connections kept open for (re-)use.", default=5
        ),
    ]
    max_overflow: Annotated[
        int,
        pyd.Field(
            description="Amount of connections the pool may open temp. when all are checked out.",
            default=5,
        ),
    ]
    recycle_seconds: Annotated[
        int,
        pyd.Field(
            description="Older connections that are silently discarded, and ready for next use.",
            default=1800,
        ),
    ]
    timeout_seconds: Annotated[
        int,
        pyd.Field(
            description="Wait when all connections are taken, before retry.",
            default=10,
        ),
    ]
