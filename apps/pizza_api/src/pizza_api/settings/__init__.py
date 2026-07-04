"""Settings for the pizza API."""

from pizza_api.settings.app import ApplicationSettings
from pizza_api.settings.engine_pool import ApiPoolSettings
from pizza_api.settings.scaleway import ScalewaySettings

app_settings = ApplicationSettings()
pool = ApiPoolSettings()
scw = ScalewaySettings()

__all__ = ["app_settings", "pool", "scw"]
