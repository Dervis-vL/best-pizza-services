# Auto-fix formatting and safe lint fixes
[doc("Run and auto-fix formatting and safe linting checks.")]
[group("Quality Checks")]
fmt:
    @echo "{{bold}}{{green}}🔍 Ruff format...{{nc}}"
    {{run}} ruff format .
    @echo "{{bold}}{{green}}🔍 Ruff check fix...{{nc}}"
    {{run}} ruff check . --fix
    @echo "{{bold}}{{green}}✓ All formatting done.{{nc}}"


# Type check all workspace members (strict)
[doc("Run type checking for all workspace members.")]
[group("Quality Checks")]
check-type:
    @echo "{{bold}}{{green}}🔍 Type checking...{{nc}}"
    {{run}} mypy {{ prepend('-p ', _modules) }}
    @echo "{{bold}}{{green}}✓ All type checks passed.{{nc}}"


# Lint all workspace members
[doc("Run linting checks for all workspace members.")]
[group("Quality Checks")]
lint:
    @echo "{{bold}}{{green}}🔍 Ruff check...{{nc}}"
    {{run}} ruff check .
    @echo "{{bold}}{{green}}✓ All lint checks passed.{{nc}}"


# Check dependencies for all workspace members
[doc("Check dependencies for all workspace members.")]
[group("Quality Checks")]
check-deps:
    @echo "{{bold}}{{green}}🔍 Checking dependencies...{{nc}}"
    @for d in {{_members}}; do echo "→ $d"; {{run}} --directory "$d" deptry .; done
    @echo "{{bold}}{{green}}✓ All dependencies are valid.{{nc}}"


# Spell check
[doc("Run spell checking.")]
[group("Quality Checks")]
check-spelling:
    @echo "{{bold}}{{green}}🔍 Spell checking...{{nc}}"
    {{run}} codespell apps packages services README.md
    @echo "{{bold}}{{green}}✓ All spelling is valid.{{nc}}"

# Check for stale lock files
[doc("Check for stale lock files.")]
[group("Quality Checks")]
check-lock:
    uv lock --check


# Run fmt / mypy / deptry / pytest scoped to a subset of projects given as arg or from changed-projects.
[doc("Run formatting, type, dependency and test checks for the changed (or given) projects.")]
[group("Quality Checks")]
check-changed *projects: check-lock
    #!/usr/bin/env bash
    set -euo pipefail

    dirs=({{projects}})
    if [[ ${#dirs[@]} -eq 0 ]]; then
        while IFS= read -r line; do
            if [[ -n "$line" ]]; then
                dirs+=("$line")
            fi
        done < <(just affected-projects)
    fi

    if [[ ${#dirs[@]} -eq 0 ]]; then
        echo "{{bold}}{{green}}✓ No changed projects; nothing to check.{{nc}}"
        exit 0
    fi

    # pass validation recipe when ready
    mypy_args=()
    for d in "${dirs[@]}"; do
        if [[ ! -f "$d/pyproject.toml" ]]; then
            echo "ERROR: '$d' is not a workspace member directory" >&2
            exit 1
        fi
        mypy_args+=(-p "$(basename "$d")")
    done

    echo "{{bold}}{{green}}⚙ Checking: ${dirs[*]}{{nc}}"

    echo "{{bold}}{{green}}🔍 Ruff format + check fix...{{nc}}"
    {{run}} ruff format "${dirs[@]}"
    {{run}} ruff check "${dirs[@]}" --fix

    echo "{{bold}}{{green}}🔍 Type checking...{{nc}}"
    {{run}} mypy "${mypy_args[@]}"

    echo "{{bold}}{{green}}🔍 Checking dependencies...{{nc}}"
    for d in "${dirs[@]}"; do
        echo "→ $d"
        {{run}} --directory "$d" deptry .
    done

    echo "{{bold}}{{green}}🔍 Checking spelling...{{nc}}"
    for d in "${dirs[@]}"; do
        echo "→ $d"
        {{run}} codespell "$d"
    done

    echo "→ README.md"
    {{run}} codespell README.md

    echo "{{bold}}{{green}}🔍 Checking versions...{{nc}}"
    just check-version "${dirs[@]}"

    # Every project must carry tests; pytest alone would not catch this, because
    # one test-less project is masked by the others in a combined run.
    for d in "${dirs[@]}"; do
        if ! find "$d/tests" -name '__pycache__' -prune -o -name 'test_*.py' -print 2>/dev/null | grep -q .; then
            echo "ERROR: '$d' has no test_*.py files under tests/" >&2
            exit 1
        fi
    done

    echo "{{bold}}{{green}}🔍 Running tests...{{nc}}"
    # --cov takes the module name, not the path: --cov=apps/pizza_app would
    test_dirs=()
    cov_args=()
    for d in "${dirs[@]}"; do
        echo "→ $d"
        test_dirs+=("$d/tests")
        cov_args+=("--cov=$(basename "$d")")
    done
    {{run}} pytest "${test_dirs[@]}" "${cov_args[@]}" --cov-report=term-missing

    echo "{{bold}}{{green}}✓ All checks passed for: ${dirs[*]}{{nc}}"
