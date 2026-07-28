api_config    := "apps/pizza_api/pyproject.toml"
app_config    := "apps/pizza_app/pyproject.toml"
worker_config := "apps/pizza_worker/pyproject.toml"


_api_image    := shell("grep '^name'    $1 | sed 's/.*= \"//' | tr -d '\"'", api_config)
_app_image    := shell("grep '^name'    $1 | sed 's/.*= \"//' | tr -d '\"'", app_config)
_worker_image := shell("grep '^name'    $1 | sed 's/.*= \"//' | tr -d '\"'", worker_config)

_api_version  := shell("grep '^version' $1 | head -1 | sed 's/.*= \"//' | tr -d '\"'", api_config)
_app_version  := shell("grep '^version' $1 | head -1 | sed 's/.*= \"//' | tr -d '\"'", app_config)
_worker_version := shell("grep '^version' $1 | head -1 | sed 's/.*= \"//' | tr -d '\"'", worker_config)

# Run podman compose up
[doc("Run podman compose up.")]
[group("Build & Deploy")]
compose env_file=".env":
    {{container}} compose --env-file {{env_file}} up --build

# Run podman compose down
[doc("Run podman compose down.")]
[group("Build & Deploy")]
compose-down env_file=".env":
    {{container}} compose --env-file {{env_file}} down

# Alembic upgrade: env_file arg selects the dotenv to load (default .env)
[doc("Run alembic upgrade head.")]
[group("Build & Deploy")]
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
[group("Build & Deploy")]
alembic-revision m:
    {{run}} alembic revision --autogenerate -m "{{m}}"

# Build one image (e.g. `just build-image apps/pizza_api`); tag defaults to project version
[doc("Build a single deployable image.")]
[group("Build & Deploy")]
build-image dir tag="":
    #!/usr/bin/env bash
    set -euo pipefail
    name="$(just _meta {{dir}} name)"
    tag="{{tag}}"
    if [[ -z "$tag" ]]; then
        tag="$(just _meta {{dir}} version)"
    fi
    echo "{{bold}}{{green}}🐋 {{dir}} → $name:$tag{{nc}}"
    {{container}} build -f "{{dir}}/Dockerfile" -t "{{_registry_ghcr}}/$name:$tag" .

# Build all deployable images
[doc("Build all deployable images.")]
[group("Build & Deploy")]
build:
    @for d in {{_deployables}}; do just build-image "$d"; done

# Build and push dev images to registry tagged with a given SHA
[doc("Build and push dev images to GHCR tagged with a given SHA.")]
[group("Build & Deploy")]
push-ghcr-dev sha:
    #!/usr/bin/env bash
    set -euo pipefail
    for d in {{_deployables}}; do
        just build-image "$d" "{{sha}}"
        {{container}} push "{{_registry_ghcr}}/$(just _meta "$d" name):{{sha}}"
    done

# Build and push all images to GHCR, also tagging latest
[doc("Build and push all images to GHCR, also tagging latest.")]
[group("Build & Deploy")]
push-ghcr: build
    #!/usr/bin/env bash
    set -euo pipefail
    for d in {{_deployables}}; do
        name="$(just _meta "$d" name)"
        version="$(just _meta "$d" version)"
        {{container}} push "{{_registry_ghcr}}/$name:$version"
        {{container}} tag  "{{_registry_ghcr}}/$name:$version" "{{_registry_ghcr}}/$name:latest"
        {{container}} push "{{_registry_ghcr}}/$name:latest"
    done
