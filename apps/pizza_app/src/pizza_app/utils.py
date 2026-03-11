"""Utility functions for the pizza app."""

from pathlib import Path

import sqlalchemy as sa
import streamlit as st
from pizza_platform_shared import enums as shared_enums
from pandera import typing as pa_typing

from pizza_app import repositories, schemas, settings


# create repo
def create_repo() -> repositories.PizzaPlatformDatabase:
    """Create repo instance."""
    if settings.app_settings.database_type == shared_enums.DatabaseType.POSTGRESQL:
        pizza_repo = repositories.PizzaPlatformDatabase.from_settings(
            db_settings=settings.pizza_db
        )
    elif settings.app_settings.database_type == shared_enums.DatabaseType.SQLITE:
        root_path = Path(__file__).parent.parent.parent
        sqlite_db_path = root_path / "test_rankings_parsing.db"
        sqlite_db_path.exists()
        pizza_repo = repositories.PizzaPlatformDatabase.from_engine(
            engine=sa.create_engine(
                f"sqlite:///{sqlite_db_path}",
                poolclass=sa.pool.StaticPool,
            ),
        )
    else:
        raise ValueError("Unsupported database type.")

    return pizza_repo

# Data LOAD
@st.cache_data(ttl=300, show_spinner="Loading Pizzerias from DB...")
def load_locations(
    db_repo: repositories.PizzaPlatformDatabase
) -> pa_typing.DataFrame[schemas.PizzeriaSchema]:
    """Load data from db."""
    return db_repo.read_pizzerias()


@st.cache_data(ttl=300, show_spinner="Loading Rankings from DB...")
def load_rankings(
    db_repo: repositories.PizzaPlatformDatabase
) -> pa_typing.DataFrame[schemas.RankingSchema]:
    """Load data from db."""
    return db_repo.read_rankings()