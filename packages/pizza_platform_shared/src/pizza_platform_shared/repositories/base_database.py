"""Base database repository."""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from typing import Any, Literal, overload

import pandas as pd
import sqlalchemy as sa
from sqlalchemy import orm as sa_orm

from pizza_platform_shared import settings


class BaseDatabase:
    """Base database repository.

    Owns the engine and exposes a session in context manager.

    Args:
        db_settings: Database settings.

    """

    def __init__(
        self, connection_string: str | sa.engine.URL, schema_name: str | None = None
    ) -> None:
        """Initialize the database repository."""
        self._engine = sa.create_engine(connection_string, pool_pre_ping=True)
        self._schema = schema_name

    @classmethod
    def from_engine(cls, engine: sa.Engine) -> BaseDatabase:
        """Create a database instance from an existing engine, without db settings.

        schema_name will be None — queries must not rely on it.
        """
        instance = cls.__new__(cls)
        instance._engine = engine  # noqa: SLF001
        instance._schema = None  # noqa: SLF001
        return instance

    @classmethod
    def from_settings(cls, db_settings: settings.DatabaseSettings) -> BaseDatabase:
        """Create a database repo instance from settings."""
        return cls(
            connection_string=db_settings.connection_string,
            schema_name=db_settings.schema_name,
        )

    @contextmanager
    def _session(self) -> Generator[sa_orm.Session]:
        """ORM session with commit/rollback. Use for writes and ORM reads."""
        with sa_orm.Session(self._engine) as session:
            try:
                yield session
                session.commit()
            except Exception:
                session.rollback()
                raise

    @overload
    def _read_orm[T](self, query: sa.Select[tuple[T]], *, single: Literal[True]) -> T | None: ...
    @overload
    def _read_orm[T](
        self,
        query: sa.Select[tuple[T]],
        *,
        single: Literal[False] = ...,
    ) -> list[T]: ...
    def _read_orm[T](
        self,
        query: sa.Select[tuple[T]],
        *,
        single: bool = False,
    ) -> list[T] | T | None:
        """Execute an ORM query and return mapped model instances.

        Uses a bare session (no commit) since this is read-only.
        Eager-load any relationships in the query if you need them
        after this method returns.
        """
        with sa_orm.Session(self._engine) as session:
            if single:
                return session.execute(query).scalars().first()
            return list(session.execute(query).scalars().unique().all())

    def _read_df(self, query: sa.Select[Any]) -> pd.DataFrame:
        """Execute a query and return a pandas DataFrame.

        Bypasses the ORM — use for projections across multiple tables
        or when the result feeds a data pipeline rather than entity logic.
        """
        try:
            with self._engine.connect() as conn:
                df = pd.read_sql(query, conn)
        except Exception as e:
            msg = f"Failed to read data from the database: {e}"
            raise RuntimeError(msg) from e

        return df
