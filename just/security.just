# Build both images and scan them with Trivy.
# Mirrors the CI `scan` job: HIGH/CRITICAL only, fixable vulnerabilities only.
security: build
    #!/usr/bin/env bash
    set -euo pipefail
    # Empty Docker config avoids a stale docker-credential-* helper breaking the DB pull.
    export DOCKER_CONFIG="$(mktemp -d)"
    scan() {
        local ref="$1"
        local tar; tar="$(mktemp).tar"
        trap 'rm -f "$tar"' RETURN
        podman save "$ref" -o "$tar"
        trivy image --input "$tar" \
            --severity HIGH,CRITICAL --ignore-unfixed \
            --scanners vuln --skip-version-check --exit-code 1
    }
    scan {{_registry_ghcr}}/{{_api_image}}:{{_api_version}}
    scan {{_registry_ghcr}}/{{_app_image}}:{{_app_version}}
    @echo "{{bold}}{{green}}✓ Security scan passed.{{nc}}"
