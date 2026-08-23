# Print which projects have changed since their last release tag (<name>/v*).
# A project with no tag yet is treated as needing its first release. The
# release_scope.env is excluded: it is release metadata (and the release flow
# rewrites it after tagging), not a source change that should trigger a release.
[doc("List projects that have changes since their last release tag.")]
[group("Versioning")]
changed-projects:
    #!/usr/bin/env bash
    set -euo pipefail
    for project in {{_members}}; do
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
[doc("List all projects that are affected by changes.")]
[group("Versioning")]
affected-projects:
    #!/usr/bin/env bash
    set -euo pipefail
    changed="$(just changed-projects)"
    if [[ -z "$changed" ]]; then
        exit 0
    fi
    # Resolve a workspace package name to its project dir (empty if not a member), always returns 0
    dir_of_name() {
        local n="$1" dir name
        for dir in {{_members}}; do
            name="$(grep -m1 '^name' "$dir/pyproject.toml" | sed -E 's/^name *= *"//; s/".*//')"
            if [[ "$name" == "$n" ]]; then
                echo "$dir"
                return 0
            fi
        done
        return 0
    }
    # List the workspace-member dirs that a project directly depends on from its [project] dependencies.
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
    # Seed with directly-changed projects, then mark a project affected whenever one of its deps is affected
    affected="$changed"
    progress=1
    while (( progress )); do
        progress=0
        for dir in {{_members}}; do
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
    # Emit in canonical _members order.
    for dir in {{_members}}; do
        if is_in "$dir" "$affected"; then
            echo "$dir"
        fi
    done

# Fail if CHANGELOG.md in project does not contain an [Unreleased] section
[doc("Check that the project's changelog has an [Unreleased] section.")]
[group("Quality Checks")]
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
[doc("Bump the version for a project.")]
[group("Versioning")]
bump-project name:
    #!/usr/bin/env bash
    set -euo pipefail
    env_file="{{name}}/release_scope.env"
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
    echo "Bumping {{name}} ($SCOPE)..."
    # --no-sync: the env is already synced by CI setup; without it, `uv run`
    # rewrites uv.lock (member versions change) and dirties the tree, which
    # makes the next name's bump-my-version abort on its clean-tree check.
    (cd "{{name}}" && uv run --no-sync bump-my-version bump "$SCOPE")


# Validate changelogs and release scopes; no bumping. With no arguments this
# checks every affected project (changed + dependents), which is what CI needs.
# Given explicit project dirs it checks only those, so `check-changed` can be reused with smaller set.
[doc("Validate changelogs and release scopes for the affected (or given) projects.")]
[group("Quality Checks")]
check-version *projects:
    #!/usr/bin/env bash
    set -euo pipefail

    dirs=({{projects}})
    if [[ ${#dirs[@]} -eq 0 ]]; then
        while IFS= read -r line; do
            if [[ -n "$line" ]]; then
                dirs+=("$line")
            fi
        done < <(just affected-projects)
        echo "Affected projects (changed + dependents):"
    else
        echo "Checking projects:"
    fi

    if [[ ${#dirs[@]} -eq 0 ]]; then
        echo "No project changes detected; nothing to check"
        exit 0
    fi
    printf '%s\n' "${dirs[@]}"

    for project in "${dirs[@]}"; do
        just check-changelog "$project"
        env_file="$project/release_scope.env"
        if [[ ! -f "$env_file" ]]; then
            echo "ERROR: $env_file not found; create it with SCOPE=patch|minor|major"
            exit 1
        fi
        # Clear first: `source` leaves SCOPE set, so a project whose env file is
        # missing the line would otherwise silently inherit the previous one.
        unset SCOPE
        # shellcheck source=/dev/null
        source "$env_file"
        if [[ ! "${SCOPE:-}" =~ ^(patch|minor|major)$ ]]; then
            echo "ERROR: SCOPE in $env_file must be patch, minor, or major (got: '${SCOPE:-unset}')"
            exit 1
        fi
        echo "✓ SCOPE=$SCOPE in $env_file"
    done
    echo "{{green}}✓ Version check passed for: ${dirs[*]}{{nc}}"
