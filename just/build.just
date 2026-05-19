github_user    := "Dervis-vL"
api_image      := "pizza-api"
app_image      := "pizza-app"
registry_ghcr  := "ghcr.io/" + github_user
_api_version  := `grep '^version' apps/pizza_api/pyproject.toml | head -1 | sed 's/.*"\(.*\)"/\1/'`
_app_version  := `grep '^version' apps/pizza_app/pyproject.toml | head -1 | sed 's/.*"\(.*\)"/\1/'`

# Run podman compose: action defaults to "up", e.g. `just compose down`
compose action="up" env_file=".env":
    podman compose --env-file {{env_file}} {{action}}

# Alembic upgrade
alembic-upgrade:
    {{run}} alembic upgrade head

# Alembic revision: message arg sets the revision message
alembic-revision m:
    {{run}} alembic revision -m "{{m}}"

# Build both app and api service images
build: build-api build-app

# Build the FastAPI image
build-api:
    podman build -f apps/pizza_api/Dockerfile -t {{registry_ghcr}}/{{api_image}}:{{_api_version}} .

# Build the Streamlit app image
build-app:
    podman build -f apps/pizza_app/Dockerfile -t {{registry_ghcr}}/{{app_image}}:{{_app_version}} .

# Build and push both images to GHCR, also tagging latest
push-ghcr: build
    podman push {{registry_ghcr}}/{{api_image}}:{{_api_version}}
    podman push {{registry_ghcr}}/{{app_image}}:{{_app_version}}
    podman tag  {{registry_ghcr}}/{{api_image}}:{{_api_version}} {{registry_ghcr}}/{{api_image}}:latest
    podman tag  {{registry_ghcr}}/{{app_image}}:{{_app_version}} {{registry_ghcr}}/{{app_image}}:latest
    podman push {{registry_ghcr}}/{{api_image}}:latest
    podman push {{registry_ghcr}}/{{app_image}}:latest