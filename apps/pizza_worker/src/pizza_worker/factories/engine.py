"""Engine factory for the pizza worker."""

import sqlalchemy as sa
from sqlalchemy.engine import Engine

from pizza_platform_shared import settings as shared_settings


def create_worker_engine() -> Engine:
    """Create a non-pooled engine for worker."""
    return sa.create_engine(
        shared_settings.pizza_db.connection_string,
        poolclass=sa.NullPool,
        pool_pre_ping=True,
    )
