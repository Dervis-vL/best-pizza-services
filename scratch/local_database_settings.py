"""Settings for local database access."""

from __future__ import annotations

import pathlib

import sqlalchemy as sa
from sqlalchemy import event as sa_event
from sqlalchemy import orm as sa_orm


def get_sqlite_engine(
    db_path: pathlib.Path | None, model: sa_orm.DeclarativeBase
) -> sa.engine.Engine:
    """Create engine with SQLite schema handling."""
    if db_path:
        url = f"sqlite:///{db_path}"
        poolclass = sa.pool.StaticPool
    else:
        url = "sqlite:///:memory:"
        poolclass = sa.pool.NullPool

    # Create engine with appropriate pool class for SQLite
    sqlite_engine = sa.create_engine(
        url,
        connect_args={"check_same_thread": False},
        poolclass=poolclass,
    )

    # Enable foreign key enforcement for SQLite
    @sa_event.listens_for(sqlite_engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):  # pylint: disable=unused-argument
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    # Remove schema for SQLite
    for table in model.metadata.tables.values():
        table.schema = None

    # Create tables
    model.metadata.create_all(bind=sqlite_engine)

    return sqlite_engine
