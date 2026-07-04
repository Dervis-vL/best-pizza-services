"""Reset the pizza database schema: drop it ``CASCADE`` and recreate it empty.

Wipes every table and row in the configured ``PIZZA_DB_SCHEMA_NAME`` schema. Interactive —
you must retype the schema name to confirm. Destructive; never run against data you need.
"""

import sqlalchemy as sa

from pizza_platform_shared import settings

if __name__ == "__main__":
    db = settings.pizza_db
    schema = db.schema_name
    if schema is None:
        msg = "pizza_db.schema_name is not set, refusing to run."  # pylint: disable=invalid-name
        raise SystemExit(msg)

    print(f"About to DROP SCHEMA {schema} CASCADE on {db.host}:{db.port}/{db.name}")  # noqa: T201
    if input("Type the schema name to confirm: ").strip() != schema:
        msg = "Aborted."  # pylint: disable=invalid-name
        raise SystemExit(msg)

    engine = sa.create_engine(db.connection_string)
    with engine.connect() as connection:
        connection.execute(sa.text(f"DROP SCHEMA IF EXISTS {schema} CASCADE;"))
        connection.execute(sa.text(f"CREATE SCHEMA {schema};"))
        connection.commit()
    print(f"Schema {schema} reset.")  # noqa: T201
