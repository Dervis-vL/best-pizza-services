"""Engine dependencies for the pizza API."""

from fastapi import Request
from sqlalchemy.engine import Engine


def get_engine(request: Request) -> Engine:
    """Return the shared SQLAlchemy engine stored on app state."""
    return request.app.state.engine
