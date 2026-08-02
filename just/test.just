# Test all workspace members with parallel argument
[doc("Run tests for all workspace members; optionally pass pytest args, e.g. --integration")]
[group("Quality Checks")]
test *flag:
    @echo "{{bold}}{{green}}🔍 Running tests...{{nc}}"
    {{run}} pytest {{flag}} {{ prepend('--cov=', _modules) }} --cov-report=term-missing
    @echo "{{bold}}{{green}}✓ All tests passed.{{nc}}"
