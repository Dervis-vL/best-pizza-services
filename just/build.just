# Run podman compose: action defaults to "up", e.g. `just compose down`
compose action="up" env_file=".env":
    podman compose --env-file {{env_file}} {{action}}

# Alembic upgrade
alembic-upgrade:
    {{run}} alembic upgrade head

# Alembic revision: message arg sets the revision message
alembic-revision m:
    {{run}} alembic revision "{{m}}"