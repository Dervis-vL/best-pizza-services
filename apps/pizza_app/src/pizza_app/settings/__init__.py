"""Settings for the pizza app."""

from pizza_platform_shared.settings import pizza_db

from pizza_app.settings.application import Application

app_settings = Application()

__all__ = ["pizza_db", "app_settings"]
