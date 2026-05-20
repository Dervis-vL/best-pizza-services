"""Settings for the pizza app."""

from pizza_app.settings.application import Application
from pizza_platform_shared.settings import pizza_db

app_settings = Application()

__all__ = ["app_settings", "pizza_db"]
