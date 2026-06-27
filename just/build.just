api_config    := "apps/pizza_api/pyproject.toml"
app_config    := "apps/pizza_app/pyproject.toml"
worker_config := "apps/pizza_worker/pyproject.toml"

_github_user  := `git remote get-url origin | sed 's/.*github\.com[:/]\([^/]*\)\/.*/\1/' | tr '[:upper:]' '[:lower:]'`
_api_image    := shell("grep '^name'    $1 | sed 's/.*= \"//' | tr -d '\"'", api_config)
_app_image    := shell("grep '^name'    $1 | sed 's/.*= \"//' | tr -d '\"'", app_config)
_worker_image := shell("grep '^name'    $1 | sed 's/.*= \"//' | tr -d '\"'", worker_config)
_registry_ghcr := "ghcr.io/" + _github_user
_api_version  := shell("grep '^version' $1 | head -1 | sed 's/.*= \"//' | tr -d '\"'", api_config)
_app_version  := shell("grep '^version' $1 | head -1 | sed 's/.*= \"//' | tr -d '\"'", app_config)
_worker_version := shell("grep '^version' $1 | head -1 | sed 's/.*= \"//' | tr -d '\"'", worker_config)

# Run podman compose up
compose env_file=".env":
    podman compose --env-file {{env_file}} up --build

# Run podman compose down
compose-down env_file=".env":
    podman compose --env-file {{env_file}} down

# Alembic upgrade: env_file arg selects the dotenv to load (default .env)
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
alembic-revision m:
    {{run}} alembic revision -m "{{m}}"

# Build the FastAPI image
build-api:
    podman build -f apps/pizza_api/Dockerfile -t {{_registry_ghcr}}/{{_api_image}}:{{_api_version}} .

# Build the Streamlit app image
build-app:
    podman build -f apps/pizza_app/Dockerfile -t {{_registry_ghcr}}/{{_app_image}}:{{_app_version}} .

# Build the batch worker image
build-worker:
    podman build -f apps/pizza_worker/Dockerfile -t {{_registry_ghcr}}/{{_worker_image}}:{{_worker_version}} .

# Build all deployable images (api, app, worker)
build: build-api build-app build-worker

# Build and push dev images to GHCR tagged with a given SHA (e.g. `just push-ghcr-dev abc1234`)
push-ghcr-dev sha:
    podman build -f apps/pizza_api/Dockerfile -t {{_registry_ghcr}}/{{_api_image}}:{{sha}} .
    podman build -f apps/pizza_app/Dockerfile -t {{_registry_ghcr}}/{{_app_image}}:{{sha}} .
    podman build -f apps/pizza_worker/Dockerfile -t {{_registry_ghcr}}/{{_worker_image}}:{{sha}} .
    podman push {{_registry_ghcr}}/{{_api_image}}:{{sha}}
    podman push {{_registry_ghcr}}/{{_app_image}}:{{sha}}
    podman push {{_registry_ghcr}}/{{_worker_image}}:{{sha}}

# Build and push all images to GHCR, also tagging latest
push-ghcr: build
    podman push {{_registry_ghcr}}/{{_api_image}}:{{_api_version}}
    podman push {{_registry_ghcr}}/{{_app_image}}:{{_app_version}}
    podman push {{_registry_ghcr}}/{{_worker_image}}:{{_worker_version}}
    podman tag  {{_registry_ghcr}}/{{_api_image}}:{{_api_version}} {{_registry_ghcr}}/{{_api_image}}:latest
    podman tag  {{_registry_ghcr}}/{{_app_image}}:{{_app_version}} {{_registry_ghcr}}/{{_app_image}}:latest
    podman tag  {{_registry_ghcr}}/{{_worker_image}}:{{_worker_version}} {{_registry_ghcr}}/{{_worker_image}}:latest
    podman push {{_registry_ghcr}}/{{_api_image}}:latest
    podman push {{_registry_ghcr}}/{{_app_image}}:latest
    podman push {{_registry_ghcr}}/{{_worker_image}}:latest
