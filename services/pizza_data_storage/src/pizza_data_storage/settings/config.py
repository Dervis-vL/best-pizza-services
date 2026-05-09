"""Module containing database settings config for the pizza app."""

import pydantic_settings


class DatabaseSettingsConfigDict(pydantic_settings.SettingsConfigDict, total=False):
    """Config dict for database settings, with field to indicate if required tables."""

    requires_tables: bool
