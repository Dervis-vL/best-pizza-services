# Auto-fix formatting and safe lint fixes
fmt:
    @echo "{{bold}}{{green}}🔍 Ruff format...{{nc}}"
    {{run}} ruff format .
    @echo "{{bold}}{{green}}🔍 Ruff check fix...{{nc}}"
    {{run}} ruff check . --fix


# Type check all workspace members (strict)
typecheck:
    @echo "{{bold}}{{green}}🔍 Type checking...{{nc}}"
    {{run}} mypy --package pizza_data_collector --strict
    {{run}} mypy --package pizza_data_storage --strict
    {{run}} mypy --package geolocation --strict
    {{run}} mypy --package pizza_platform_shared --strict
    {{run}} mypy --package pizza_app --strict
    {{run}} mypy --package pizza_api --strict
    @echo "{{bold}}{{green}}✓ All type checks passed.{{nc}}"


# Lint all workspace members
lint:
    @echo "{{bold}}{{green}}🔍 Ruff check...{{nc}}"
    {{run}} ruff check .
    @echo "{{bold}}{{green}}✓ All lint checks passed.{{nc}}"


# Check dependecies for all workspace members
deps-check:
    @echo "{{bold}}{{green}}🔍 Checking dependencies...{{nc}}"
    {{run}} --directory apps/pizza_api deptry .
    {{run}} --directory apps/pizza_app deptry .
    {{run}} --directory packages/pizza_platform_shared deptry .
    {{run}} --directory services/geolocation deptry .
    {{run}} --directory services/pizza_data_collector deptry .
    {{run}} --directory services/pizza_data_storage deptry .
    @echo "{{bold}}{{green}}✓ All dependencies are valid.{{nc}}"