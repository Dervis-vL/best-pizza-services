github_user    := "Dervis-vL"
api_image      := "pizza-api"
app_image      := "pizza-app"
registry_ghcr  := "ghcr.io/" + github_user
docker_tag     := `git describe --tags --always --dirty 2>/dev/null || git rev-parse --short HEAD`

# Run podman compose: action defaults to "up", e.g. `just compose down`
compose action="up" env_file=".env":
    podman compose --env-file {{env_file}} {{action}}

# Alembic upgrade
alembic-upgrade:
    {{run}} alembic upgrade head

# Alembic revision: message arg sets the revision message
alembic-revision m:
    {{run}} alembic revision -m "{{m}}"

# Build both service images
build: build-api build-app

# Build the API image
build-api:
    podman build -f apps/pizza_api/Dockerfile -t {{registry_ghcr}}/{{api_image}}:{{docker_tag}} .

# Build the Streamlit app image
build-app:
    podman build -f apps/pizza_app/Dockerfile -t {{registry_ghcr}}/{{app_image}}:{{docker_tag}} .

# Build and push both images to GHCR, also tagging latest
push-ghcr: build
    podman push {{registry_ghcr}}/{{api_image}}:{{docker_tag}}
    podman push {{registry_ghcr}}/{{app_image}}:{{docker_tag}}
    podman tag  {{registry_ghcr}}/{{api_image}}:{{docker_tag}} {{registry_ghcr}}/{{api_image}}:latest
    podman tag  {{registry_ghcr}}/{{app_image}}:{{docker_tag}} {{registry_ghcr}}/{{app_image}}:latest
    podman push {{registry_ghcr}}/{{api_image}}:latest
    podman push {{registry_ghcr}}/{{app_image}}:latest