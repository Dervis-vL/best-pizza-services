# Pre-flight scan that skips the image build entirely.
[doc("Scan base images and resolved prod dependencies without building images.")]
[group("Security")]
audit:
    #!/usr/bin/env bash
    set -euo pipefail
    # Empty Docker config avoids a stale docker-credential-* helper breaking the DB pull.
    export DOCKER_CONFIG="$(mktemp -d)"
    failed=0

    bases="$(grep -h '^FROM' {{ append('/Dockerfile', _deployables) }} | awk '{print $2}' | sort -u)"
    for base in $bases; do
        echo "{{bold}}{{green}}🔒 Scanning base image $base...{{nc}}"
        trivy image "$base" {{_trivy_flags}} || failed=1
    done

    for dir in {{_deployables}}; do
        name="$(just _meta "$dir" name)"
        echo "{{bold}}{{green}}🔒 Scanning $name dependencies...{{nc}}"
        out="$(mktemp -d)"
        uv export --package "$name" --no-dev --frozen \
            --no-emit-project --no-hashes -q -o "$out/requirements.txt"
        trivy fs "$out" {{_trivy_flags}} || failed=1
        rm -rf "$out"
    done

    if [[ "$failed" -ne 0 ]]; then
        echo "{{bold}}✗ Audit found HIGH/CRITICAL fixable vulnerabilities.{{nc}}" >&2
        exit 1
    fi
    echo "{{bold}}{{green}}✓ Audit passed. Run 'just audit-image' for the full image scan.{{nc}}"

# Build all images and scan them with Trivy.
[doc("Build all images and scan them with Trivy.")]
[group("Security")]
audit-image: build
    #!/usr/bin/env bash
    set -euo pipefail
    # Empty Docker config avoids a stale docker-credential-* helper breaking the DB pull.
    export DOCKER_CONFIG="$(mktemp -d)"
    scan() {
        local ref="$1"
        local tar; tar="$(mktemp).tar"
        trap 'rm -f "$tar"' RETURN
        {{container}} save "$ref" -o "$tar"
        trivy image --input "$tar" {{_trivy_flags}}
    }
    for dir in {{_deployables}}; do
        name="$(just _meta "$dir" name)"
        version="$(just _meta "$dir" version)"
        echo "{{bold}}{{green}}🔒 Scanning $name:$version...{{nc}}"
        scan "{{_registry}}/$name:$version"
    done
    echo "{{bold}}{{green}}✓ Security scan passed.{{nc}}"
