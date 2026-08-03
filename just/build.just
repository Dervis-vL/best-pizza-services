# Run dockerpodman compose
[doc("Run images from compose file.")]
[group("Build & Deploy")]
compose env_file=".env":
    {{container}} compose --env-file {{env_file}} up --build

# Stop docker/podman compose
[doc("Stop images from compose file.")]
[group("Build & Deploy")]
compose-down:
    {{container}} compose down

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
    {{container}} build -f "{{dir}}/Dockerfile" -t "{{_registry}}/$name:$tag" .

# Build all deployable images
[doc("Build all deployable images.")]
[group("Build & Deploy")]
build:
    @for d in {{_deployables}}; do just build-image "$d"; done

# Build and push dev images to registry tagged with a given SHA
[doc("Build and push dev images to registry tagged with a given SHA.")]
[group("Build & Deploy")]
push-to-registry-dev sha:
    #!/usr/bin/env bash
    set -euo pipefail
    for d in {{_deployables}}; do
        just build-image "$d" "{{sha}}"
        {{container}} push "{{_registry}}/$(just _meta "$d" name):{{sha}}"
    done

# Build and push all images to registry, also tagging latest
[doc("Build and push all images to registry, also tagging latest.")]
[group("Build & Deploy")]
push-to-registry: build
    #!/usr/bin/env bash
    set -euo pipefail
    for d in {{_deployables}}; do
        name="$(just _meta "$d" name)"
        version="$(just _meta "$d" version)"
        {{container}} push "{{_registry}}/$name:$version"
        {{container}} tag  "{{_registry}}/$name:$version" "{{_registry}}/$name:latest"
        {{container}} push "{{_registry}}/$name:latest"
    done
