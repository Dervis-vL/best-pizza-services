"""Engine dependencies for the pizza API."""

import sqlalchemy as sa
from fastapi import Request
from pizza_platform_shared import settings as shared_settings
from sqlalchemy.engine import Engine


def create_engine() -> Engine:
    """Create a SQLAlchemy engine using the configured database URL."""
    return sa.create_engine(shared_settings.pizza_db.connection_string, pool_pre_ping=True)


def get_engine(request: Request) -> Engine:
    """Return the shared SQLAlchemy engine stored on app state."""
    return request.app.state.engine
