[doc("Scan the workspace lock and its resolved dependencies.")]
[group("Security")]
[script]
audit-uv:
    #!/usr/bin/env bash

    echo "{{green}}🔒 Auditing workspace dependencies...{{nc}}"
    if ! {{_uv_audit}} --no-dev; then
        echo "{{style('bold')}}✗ Audit found vulnerabilities or adverse project statuses.{{nc}}" >&2
        echo "  Run 'just audit-blame <package>' to see which members pull it in." >&2
        echo "  Suppress non-actionable findings in [tool.uv.audit]." >&2
        exit 1
    fi
    echo "{{green}}✓ Dependency audit passed.{{nc}}"


[doc("Scan the full git history for committed secrets.")]
[group("Security")]
[script]
audit-secrets *args:
    #!/usr/bin/env bash

    # History, not the working tree. The prek hook already blocks secrets at
    # commit time (gitleaks --staged); this proves none ever landed, including
    # from before the hook existed or from a --no-verify commit. Untracked files
    # (.env, dev/) are gitignored and are meant to hold local secrets, so
    # scanning the working tree would be all noise and no signal.
    echo "{{green}}🔒 Scanning git history for secrets...{{nc}}"

    # Prefer a system gitleaks (CI installs one); otherwise reuse the binary prek
    # already built for the hook, so a contributor needs no second install.
    if command -v gitleaks >/dev/null 2>&1; then
        gitleaks=(gitleaks)
    else
        gitleaks=({{run}} --no-sync prek exec gitleaks -- gitleaks)
    fi

    if ! "${gitleaks[@]}" git . {{_gitleaks_flags}} {{args}}; then
        echo "{{red}}✗ Secrets found in git history.{{nc}}" >&2
        echo "  Rotate the credential first. Scrubbing history does not un-leak it," >&2
        echo "  and anyone who cloned or forked already has it." >&2
        echo "  Then allowlist the commit in .gitleaks.toml, with a comment saying why." >&2
        exit 1
    fi
    echo "{{green}}✓ No secrets in git history.{{nc}}"


# Pre-flight scan that skips the image build entirely.
[doc("Scan base images and resolved prod dependencies without building images.")]
[group("Security")]
[script]
audit-deployables:
    #!/usr/bin/env bash

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
[script]
audit-image: build
    #!/usr/bin/env bash

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
audit-blame member:
    uv tree --invert --package "{{ member }}" --no-dev


[doc("Full security gate.")]
[group("Security")]
audit: audit-uv audit-secrets audit-deployables audit-image
