api_config    := "apps/pizza_api/pyproject.toml"
app_config    := "apps/pizza_app/pyproject.toml"

_github_user  := `git remote get-url origin | sed 's/.*github\.com[:/]\([^/]*\)\/.*/\1/' | tr '[:upper:]' '[:lower:]'`
_api_image    := shell("grep '^name'    $1 | sed 's/.*= \"//' | tr -d '\"'", api_config)
_app_image    := shell("grep '^name'    $1 | sed 's/.*= \"//' | tr -d '\"'", app_config)
_registry_ghcr := "ghcr.io/" + _github_user
_api_version  := shell("grep '^version' $1 | head -1 | sed 's/.*= \"//' | tr -d '\"'", api_config)
_app_version  := shell("grep '^version' $1 | head -1 | sed 's/.*= \"//' | tr -d '\"'", app_config)

# Run podman compose up
compose env_file=".env":
    podman compose --env-file {{env_file}} up --build

# Run podman compose down
compose-down env_file=".env":
    podman compose --env-file {{env_file}} down

# Alembic upgrade: env_file arg selects the dotenv to load (default .env)
alembic-upgrade env_file=".env":
    set -a && . ./{{env_file}} && set +a && {{run}} alembic upgrade head

# Alembic revision: message arg sets the revision message
alembic-revision m:
    {{run}} alembic revision -m "{{m}}"

# Build the FastAPI image
build-api:
    podman build -f apps/pizza_api/Dockerfile -t {{_registry_ghcr}}/{{_api_image}}:{{_api_version}} .

# Build the Streamlit app image
build-app:
    podman build -f apps/pizza_app/Dockerfile -t {{_registry_ghcr}}/{{_app_image}}:{{_app_version}} .

# Build both app and api service images
build: build-api build-app

# Build and push dev images to GHCR tagged with a given SHA (e.g. `just push-ghcr-dev abc1234`)
push-ghcr-dev sha:
    podman build -f apps/pizza_api/Dockerfile -t {{_registry_ghcr}}/{{_api_image}}:{{sha}} .
    podman build -f apps/pizza_app/Dockerfile -t {{_registry_ghcr}}/{{_app_image}}:{{sha}} .
    podman push {{_registry_ghcr}}/{{_api_image}}:{{sha}}
    podman push {{_registry_ghcr}}/{{_app_image}}:{{sha}}

# Build and push both images to GHCR, also tagging latest
push-ghcr: build
    podman push {{_registry_ghcr}}/{{_api_image}}:{{_api_version}}
    podman push {{_registry_ghcr}}/{{_app_image}}:{{_app_version}}
    podman tag  {{_registry_ghcr}}/{{_api_image}}:{{_api_version}} {{_registry_ghcr}}/{{_api_image}}:latest
    podman tag  {{_registry_ghcr}}/{{_app_image}}:{{_app_version}} {{_registry_ghcr}}/{{_app_image}}:latest
    podman push {{_registry_ghcr}}/{{_api_image}}:latest
    podman push {{_registry_ghcr}}/{{_app_image}}:latest
