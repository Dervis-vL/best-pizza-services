"""Alembic environment configuration for pizza_platform."""

import logging

import psycopg2.errors as pg_errors

logging.basicConfig(
    format="%(levelname)-5.5s [%(name)s] %(message)s",
    datefmt="%H:%M:%S",
    level=logging.WARNING,
)
logging.getLogger("alembic").setLevel(logging.INFO)
from alembic import context
from sqlalchemy import Connection, create_engine, engine_from_config, pool, text
from sqlalchemy import exc as sa_exc

from pizza_data_storage import models
from pizza_platform_shared import settings

logger = logging.getLogger(__name__)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config  # pylint: disable=no-member
config.set_main_option(
    "sqlalchemy.url",
    settings.pizza_db.connection_string.render_as_string(hide_password=False).replace(
        "%",
        "%%",
    ),
)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = models.BaseModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# Database and schema bootstrap


def ensure_database_exists() -> None:
    """Create the target database if it doesn't exist.

    Connects to the default 'postgres' database to execute CREATE DATABASE.
    Uses EAFP pattern - attempts creation and catches duplicate error.
    """
    target_db_name = settings.pizza_db.name

    # Connect to default postgres database
    engine = create_engine(
        url=settings.maintenance_db.connection_string,
        isolation_level="AUTOCOMMIT",
    )

    try:
        with engine.connect() as conn:
            conn.execute(text(f'CREATE DATABASE "{target_db_name}"'))
            logger.info("Database '%s' created successfully.", target_db_name)
    except sa_exc.ProgrammingError as err:
        if isinstance(err.orig, pg_errors.DuplicateDatabase):  # pylint: disable=no-member
            logger.debug("Database '%s' already exists.", target_db_name)
        elif isinstance(err.orig, pg_errors.InsufficientPrivilege):  # pylint: disable=no-member
            logger.debug(
                "No CREATEDB privilege, assuming database '%s' already exists.",
                target_db_name,
            )
        else:
            raise
    finally:
        engine.dispose()


def ensure_schema_exists(connection: Connection) -> None:
    """Create the target schema if it doesn't exist."""
    schema_name = settings.pizza_db.schema_name
    if schema_name is None:
        return
    try:
        connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
        connection.commit()
        logger.info("Schema '%s' ready.", schema_name)
    except sa_exc.ProgrammingError as err:
        logger.error("Error ensuring schema '%s': %s", schema_name, err)
        raise


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(  # pylint: disable=no-member
        url=url,
        target_metadata=target_metadata,
        include_schemas=True,
        version_table_schema=settings.pizza_db.schema_name,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():  # pylint: disable=no-member
        context.run_migrations()  # pylint: disable=no-member


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        ensure_schema_exists(connection=connection)

        context.configure(  # pylint: disable=no-member
            connection=connection,
            include_schemas=True,
            version_table_schema=settings.pizza_db.schema_name,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():  # pylint: disable=no-member
            context.run_migrations()  # pylint: disable=no-member


# Database must exist before running migrations:
ensure_database_exists()

if context.is_offline_mode():  # pylint: disable=no-member
    run_migrations_offline()
else:
    run_migrations_online()
