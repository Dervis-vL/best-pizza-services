"""Settings for maintenance database (used for Alembic migrations)."""

from pizza_data_management import config, settings


class MaintenanceDatabaseSettings(settings.DatabaseSettings):
    """Maintenance database settings for Alembic migrations. 

    Inherits from DatabaseSettings but does not require tables to be defined, 
    since it's only used for connection info during migrations.
    """

    model_config = config.DatabaseSettingsConfigDict(
        requires_tables=False,
        env_file=".env",
        env_prefix="MAINTENANCE_DB_",
    )
