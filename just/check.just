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
typecheck:
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
deps-check:
    @echo "{{bold}}{{green}}🔍 Checking dependencies...{{nc}}"
    @for d in {{_members}}; do echo "→ $d"; {{run}} --directory "$d" deptry .; done
    @echo "{{bold}}{{green}}✓ All dependencies are valid.{{nc}}"


# Spell check
[doc("Run spell checking.")]
[group("Quality Checks")]
spell-check:
    @echo "{{bold}}{{green}}🔍 Spell checking...{{nc}}"
    {{run}} codespell apps packages services README.md
    @echo "{{bold}}{{green}}✓ All spelling is valid.{{nc}}"

# Check for stale lock files
[doc("Check for stale lock files.")]
[group("Quality Checks")]
lock-check:
    uv lock --check
