"""Tests for the settings module."""

from pizza_data_collector import settings


def test_pizza_db_settings():
    """Test that pizza DB settings are loaded correctly."""
    assert settings.pizza_db.host == "localhost"
    assert settings.pizza_db.port == 5432
    assert settings.pizza_db.username == "best-pizzas-ever"
    assert settings.pizza_db.database_name == "pizza"
    assert settings.pizza_db.ssl_enabled is False