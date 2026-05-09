# Auto-fix formatting and safe lint fixes
fmt:
    @echo "{{bold}}{{green}}🔍 Ruff format...{{nc}}"
    {{run}} ruff format .
    @echo "{{bold}}{{green}}🔍 Ruff check fix...{{nc}}"
    {{run}} ruff check . --fix


# Type check all workspace members
typecheck:
    @echo "{{bold}}{{green}}🔍 Type checking...{{nc}}"
    {{run}} mypy --package pizza_data_collector
    {{run}} mypy --package pizza_data_storage
    {{run}} mypy --package geolocation
    {{run}} mypy --package pizza_platform_shared
    {{run}} mypy --package pizza_app
    {{run}} mypy --package pizza_api