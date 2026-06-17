"""Tests for the settings module."""

from pizza_data_storage import settings


def test_pizza_db_settings() -> None:
    """Test that pizza DB settings are loaded correctly."""
    assert settings.pizza_db.host == "localhost"
    assert settings.pizza_db.port == 5432
    assert settings.pizza_db.user_name == "best_pizza_user"
    assert settings.pizza_db.name == "pizza_platform"
    assert settings.pizza_db.ssl_enabled is False
