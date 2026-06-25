"""Settings for the pizza API."""

from pizza_api.settings.app import ApplicationSettings
from pizza_api.settings.engine_pool import ApiPoolSettings

app_settings = ApplicationSettings()
pool = ApiPoolSettings()

__all__ = ["app_settings", "pool"]
