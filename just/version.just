# Projects tracked for per-project versioning
_projects := "apps/pizza_api apps/pizza_app packages/pizza_platform_shared services/geolocation services/pizza_data_collector services/pizza_data_storage"

# Print which projects have changes between base_sha and HEAD (default: HEAD^)
changed-projects base_sha="HEAD^":
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ "{{base_sha}}" == "0000000000000000000000000000000000000000" ]]; then
        exit 0
    fi
    for project in {{_projects}}; do
        if git diff --name-only "{{base_sha}}" HEAD -- "$project" | grep -q .; then
            echo "$project"
        fi
    done

# Fail if CHANGELOG.md in project does not contain an [Unreleased] section
check-changelog project:
    #!/usr/bin/env bash
    set -euo pipefail
    changelog="{{project}}/CHANGELOG.md"
    if [[ ! -f "$changelog" ]]; then
        echo "ERROR: $changelog not found"
        exit 1
    fi
    if ! grep -q '\[Unreleased\]' "$changelog"; then
        echo "ERROR: No [Unreleased] section in $changelog; add changelog entries before merging"
        exit 1
    fi
    echo "✓ [Unreleased] found in $changelog"

# Bump version for a project — reads scope from project's release_scope.env
bump-project project:
    #!/usr/bin/env bash
    set -euo pipefail
    env_file="{{project}}/release_scope.env"
    if [[ ! -f "$env_file" ]]; then
        echo "ERROR: $env_file not found; create it with SCOPE=patch|minor|major"
        exit 1
    fi
    # shellcheck source=/dev/null
    source "$env_file"
    if [[ ! "${SCOPE:-}" =~ ^(patch|minor|major)$ ]]; then
        echo "ERROR: SCOPE is not set in $env_file; set it to patch, minor, or major"
        exit 1
    fi
    echo "Bumping {{project}} ($SCOPE)..."
    # --no-sync: the env is already synced by CI setup; without it, `uv run`
    # rewrites uv.lock (member versions change) and dirties the tree, which
    # makes the next project's bump-my-version abort on its clean-tree check.
    (cd "{{project}}" && uv run --no-sync bump-my-version bump "$SCOPE")

# Reset SCOPE to placeholder after a successful bump
reset-scope project:
    #!/usr/bin/env bash
    set -euo pipefail
    env_file="{{project}}/release_scope.env"
    perl -i -pe 's/^SCOPE=.*/SCOPE=placeholder/' "$env_file"
    echo "✓ Reset SCOPE to placeholder in $env_file"

# Validate changelogs and release scopes for changed projects; no bumping
version-check base_sha="":
    #!/usr/bin/env bash
    set -euo pipefail
    base="{{base_sha}}"
    if [[ -z "$base" ]]; then
        base=$(git merge-base HEAD main 2>/dev/null || echo "HEAD^")
    fi
    changed=$(just changed-projects "$base")
    if [[ -z "$changed" ]]; then
        echo "No project changes detected; nothing to check"
        exit 0
    fi
    echo "Changed projects:"
    echo "$changed"
    while IFS= read -r project; do
        just check-changelog "$project"
        env_file="$project/release_scope.env"
        if [[ ! -f "$env_file" ]]; then
            echo "ERROR: $env_file not found; create it with SCOPE=patch|minor|major"
            exit 1
        fi
        # shellcheck source=/dev/null
        source "$env_file"
        if [[ ! "${SCOPE:-}" =~ ^(patch|minor|major)$ ]]; then
            echo "ERROR: SCOPE in $env_file must be patch, minor, or major (got: '${SCOPE:-unset}')"
            exit 1
        fi
        echo "✓ SCOPE=$SCOPE in $env_file"
    done <<< "$changed"
    @echo "{{bold}}{{green}}✓ Version check passed for all changed projects.{{nc}}"

# CI entry point: detect changed projects, validate changelogs, bump versions
version base_sha="HEAD^":
    #!/usr/bin/env bash
    set -euo pipefail
    changed=$(just changed-projects "{{base_sha}}")
    if [[ -z "$changed" ]]; then
        echo "No project changes detected; nothing to bump"
        exit 0
    fi
    echo "Changed projects:"
    echo "$changed"
    # Validate all changelogs before touching anything
    while IFS= read -r project; do
        just check-changelog "$project"
    done <<< "$changed"
    # Bump all projects (each makes its own clean commit + tag)
    while IFS= read -r project; do
        just bump-project "$project"
    done <<< "$changed"
    # Reset scopes and refresh the lockfile once, in a single follow-up commit.
    # Doing this inside the bump loop would dirty the tree and abort the next bump.
    while IFS= read -r project; do
        just reset-scope "$project"
        git add "$project/release_scope.env"
    done <<< "$changed"
    uv lock
    git add uv.lock
    git commit --no-verify -m "chore: reset release scopes and refresh lockfile"
