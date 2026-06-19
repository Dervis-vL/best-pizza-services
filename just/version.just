# Projects tracked for per-project versioning
_projects := "apps/pizza_api apps/pizza_app packages/pizza_platform_shared services/geolocation services/pizza_data_collector services/pizza_data_storage"

# Print which projects have changed since their last release tag (<name>/v*).
# A project with no tag yet is treated as needing its first release. The
# release_scope.env is excluded: it is release metadata (and the release flow
# rewrites it after tagging), not a source change that should trigger a release.
changed-projects:
    #!/usr/bin/env bash
    set -euo pipefail
    for project in {{_projects}}; do
        name="$(grep -m1 '^name' "$project/pyproject.toml" | sed -E 's/^name *= *"//; s/".*//')"
        last_tag="$(git describe --tags --match "$name/v*" --abbrev=0 2>/dev/null || true)"
        if [[ -z "$last_tag" ]]; then
            echo "$project"
        elif git diff --name-only "$last_tag" HEAD -- "$project" ":(exclude)$project/release_scope.env" | grep -q .; then
            echo "$project"
        fi
    done

# Projects that need a release: the directly-changed ones plus any project whose
# (transitive) workspace dependencies changed. Dependencies are read from each
# project's [project] dependencies, so this stays in sync with the tomls.
affected-projects:
    #!/usr/bin/env bash
    # No associative arrays here so this also runs on macOS's default bash 3.2.
    set -euo pipefail
    changed="$(just changed-projects)"
    if [[ -z "$changed" ]]; then
        exit 0
    fi
    # Resolve a workspace package name to its project dir (empty if not a member).
    # Always returns 0 so a "not found" does not trip set -e via `d=$(...)`.
    dir_of_name() {
        local n="$1" dir name
        for dir in {{_projects}}; do
            name="$(grep -m1 '^name' "$dir/pyproject.toml" | sed -E 's/^name *= *"//; s/".*//')"
            if [[ "$name" == "$n" ]]; then
                echo "$dir"
                return 0
            fi
        done
        return 0
    }
    # List the workspace-member dirs that a project directly depends on, parsed
    # from its [project] dependencies.
    deps_of_dir() {
        local dir="$1" block entry base d
        block="$(awk '/^dependencies *= *\[/{f=1;next} /^[[:space:]]*\]/{f=0} f{print}' "$dir/pyproject.toml")"
        while IFS= read -r entry; do
            base="$(sed -E 's/[][<>=!~ ].*//' <<<"$entry")"
            d="$(dir_of_name "$base")"
            if [[ -n "$d" ]]; then
                echo "$d"
            fi
        done < <(grep -oE '"[^"]+"' <<<"$block" | tr -d '"')
    }
    is_in() { grep -qxF "$1" <<<"$2"; }
    # Seed with directly-changed projects, then mark a project affected whenever
    # one of its deps is affected. Repeat to a fixpoint for transitive chains.
    affected="$changed"
    progress=1
    while (( progress )); do
        progress=0
        for dir in {{_projects}}; do
            if is_in "$dir" "$affected"; then
                continue
            fi
            for d in $(deps_of_dir "$dir"); do
                if is_in "$d" "$affected"; then
                    affected="$affected"$'\n'"$dir"
                    progress=1
                    break
                fi
            done
        done
    done
    # Emit in canonical _projects order.
    for dir in {{_projects}}; do
        if is_in "$dir" "$affected"; then
            echo "$dir"
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
version-check:
    #!/usr/bin/env bash
    set -euo pipefail
    changed=$(just affected-projects)
    if [[ -z "$changed" ]]; then
        echo "No project changes detected; nothing to check"
        exit 0
    fi
    echo "Affected projects (changed + dependents):"
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
    echo "{{bold}}{{green}}✓ Version check passed for all changed projects.{{nc}}"

# CI entry point: detect changed projects, validate changelogs, bump versions
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
