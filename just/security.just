# Build all images and scan them with Trivy.
# Mirrors the CI `scan` job: HIGH/CRITICAL only, fixable vulnerabilities only.
[doc("Build all images and scan them with Trivy.")]
[group("Security")]
security: build
    #!/usr/bin/env bash
    set -euo pipefail
    # Empty Docker config avoids a stale docker-credential-* helper breaking the DB pull.
    export DOCKER_CONFIG="$(mktemp -d)"
    scan() {
        local ref="$1"
        local tar; tar="$(mktemp).tar"
        trap 'rm -f "$tar"' RETURN
        {{container}} save "$ref" -o "$tar"
        trivy image --input "$tar" \
            --severity HIGH,CRITICAL --ignore-unfixed \
            --scanners vuln --skip-version-check --exit-code 1
    }
    for dir in {{_deployables}}; do
        name="$(just _meta "$dir" name)"
        version="$(just _meta "$dir" version)"
        echo "{{bold}}{{green}}🔒 Scanning $name:$version...{{nc}}"
        scan "{{_registry}}/$name:$version"
    done
    echo "{{bold}}{{green}}✓ Security scan passed.{{nc}}"
