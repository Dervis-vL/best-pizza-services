# --- SETTINGS -------------------------------------------
set shell := ["bash", "-euo", "pipefail", "-c"]
set minimum-version := '1.58.0'
set default-list
set lazy

# --- IMPORTS --------------------------------------------
import '.just/vars.just'
import '.just/build.just'
import '.just/check.just'
import '.just/database.just'
import '.just/git.just'
import '.just/security.just'
import '.just/setup.just'
import '.just/test.just'
import '.just/version.just'

# --- VARIABLES ------------------------------------------
_uv := require('uv')
_workspaces := quote(_uv) + ' run --script ' +  quote(justfile_directory() / '.just/scripts/workspaces.py') \
    + ' ' + quote(justfile_directory())
_members     := shell(_workspaces + ' members')
_modules     := shell(_workspaces + ' modules')
_deployables := shell(_workspaces + ' deployables')
run  := quote(_uv) + ' run'
green := style('bold') + style('green')
yellow := style('yellow')
nc   := NORMAL

# --- TARGETS -------------------------------------
# Read a field out of a member's pyproject.toml
[private]
_meta dir field:
    @grep -m1 '^{{field}}' {{dir}}/pyproject.toml | sed -E 's/^{{field}} *= *"//; s/".*//'


[doc("Show all available targets/members.")]
[group("Setup")]
show:
    @echo "{{yellow}}⚙ Workspace members:{{nc}}"
    @for m in {{_members}}; do \
        echo "{{green}}  - $m{{nc}}"; \
    done
    @echo "{{yellow}}⚙ Workspace modules:{{nc}}"
    @for m in {{_modules}}; do \
        echo "{{green}}  - $m{{nc}}"; \
    done
    @echo "{{yellow}}⚙ Workspace deployables:{{nc}}"
    @for m in {{_deployables}}; do \
        echo "{{green}}  - $m{{nc}}"; \
    done


[doc("Fix all auto-fixable issues")]
[group("Local")]
fix: fmt lint-fix
    @echo "{{yellow}}✓ All fixing done.{{nc}}"


[doc("Run all quality checks")]
[group("Quality Checks")]
check: check-lock check-type check-lint check-deps check-spelling test check-version
    @echo "{{yellow}}✓ All checks passed.{{nc}}"


[doc("Full security gate")]
[group("Security")]
audit: audit-uv audit-secrets audit-deployables audit-image
    #!/usr/bin/env bash
    set -euo pipefail
    echo "{{yellow}}✓ Security gate passed.{{nc}}"


# CI entry point: detect changed projects, validate changelogs, bump versions
[doc("Run versioning flow for changed projects.")]
[group("Versioning")]
version:
    #!/usr/bin/env bash
    set -euo pipefail
    changed=$(just affected-projects)
    if [[ -z "$changed" ]]; then
        echo "No project changes detected; nothing to bump"
        exit 0
    fi
    echo "Affected projects (changed + dependents):"
    echo "$changed"
    # Validate all changelogs before touching anything
    while IFS= read -r project; do
        just check-version "$project"
    done <<< "$changed"
    # Bump all projects (each makes its own clean commit + tag)
    while IFS= read -r project; do
        just bump-project "$project"
    done <<< "$changed"

    uv lock
    git add uv.lock
    git commit --no-verify -m "chore: reset release scopes and refresh lockfile"

    @echo "{{yellow}}✓ Versioning flow completed.{{nc}}"


[doc("Build and push all images to registry, also tagging latest")]
[group("Build & Deploy")]
publish: build push-to-registry
    @echo "{{yellow}}✓ All images built and pushed to registry.{{nc}}"
