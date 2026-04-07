"""Tests for the settings module."""

import os

from pizza_data_collector import settings


def test_pizza_db_settings():
    """Test that pizza DB settings are loaded correctly."""
    assert settings.pizza_db.host == os.environ["PIZZA_DB_HOST"]
    assert settings.pizza_db.port == int(os.environ["PIZZA_DB_PORT"])
    assert settings.pizza_db.username == os.environ["PIZZA_DB_USERNAME"]
    assert settings.pizza_db.database_name == os.environ["PIZZA_DB_DATABASE_NAME"]
    assert isinstance(settings.pizza_db.ssl_enabled, bool)