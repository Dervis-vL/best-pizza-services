# Alembic upgrade: env_file arg selects the dotenv to load (default .env)
[doc("Run alembic upgrade head.")]
[group("Database")]
alembic-upgrade env_file=".env":
    #!/usr/bin/env bash
    set -euo pipefail
    # Source the env file when present (local dev); in CI the vars are already
    # injected into the environment, so a missing file is not an error.
    set -a
    if [[ -f "{{env_file}}" ]]; then
        source "{{env_file}}"
    fi
    set +a
    {{run}} alembic upgrade head

# Alembic revision: message arg sets the revision message
[doc("Create a new alembic revision.")]
[group("Database")]
alembic-revision m:
    {{run}} alembic revision --autogenerate -m "{{m}}"
