[doc("Scan the workspace lock and its resolved dependencies.")]
[group("Security")]
audit-uv:
    #!/usr/bin/env bash
    set -euo pipefail

    echo "{{green}}🔒 Auditing workspace dependencies...{{nc}}"
    if ! {{_uv_audit}} --no-dev; then
        echo "{{style('bold')}}✗ Audit found vulnerabilities or adverse project statuses.{{nc}}" >&2
        echo "  Run 'just audit-blame <package>' to see which members pull it in." >&2
        echo "  Suppress non-actionable findings in [tool.uv.audit]." >&2
        exit 1
    fi
    echo "{{green}}✓ Dependency audit passed.{{nc}}"


[doc("Scan committed tree for secrets.")]
[group("Security")]
audit-secrets:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "{{green}}🔒 Scanning committed tree for secrets...{{nc}}"
    tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
    git archive HEAD | tar -x -C "$tmp"
    trivy fs "$tmp" --scanners secret --exit-code 1 -q
    echo "{{green}}✓ No secrets found.{{nc}}"


# Pre-flight scan that skips the image build entirely.
[doc("Scan base images and resolved prod dependencies without building images.")]
[group("Security")]
audit-deployables:
    #!/usr/bin/env bash
    set -euo pipefail
    # Empty Docker config avoids a stale docker-credential-* helper breaking the DB pull.
    export DOCKER_CONFIG="$(mktemp -d)"
    failed=0

    bases="$(grep -h '^FROM' {{ append('/Dockerfile', _deployables) }} | awk '{print $2}' | sort -u)"
    for base in $bases; do
        echo "{{green}}🔒 Scanning base image $base...{{nc}}"
        trivy image "$base" {{_trivy_flags}} || failed=1
    done

    for dir in {{_deployables}}; do
        name="$(just _meta "$dir" name)"
        echo "{{green}}🔒 Scanning $name dependencies...{{nc}}"
        out="$(mktemp -d)"
        uv export --package "$name" --no-dev --frozen \
            --no-emit-project --no-hashes -q -o "$out/requirements.txt"
        trivy fs "$out" {{_trivy_flags}} || failed=1
        rm -rf "$out"
    done

    if [[ "$failed" -ne 0 ]]; then
        echo "✗ Audit found HIGH/CRITICAL fixable vulnerabilities.{{nc}}" >&2
        exit 1
    fi
    echo "{{green}}✓ Audit passed. Run 'just audit-image' for the full image scan.{{nc}}"

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
        echo "{{green}}🔒 Scanning $name:$version...{{nc}}"
        scan "{{_registry}}/$name:$version"
    done
    echo "{{green}}✓ Security scan passed.{{nc}}"


[doc("Show which workspace members depend on a package.")]
[group("Security")]
audit-blame package:
    uv tree --invert --package "{{package}}" --no-dev
