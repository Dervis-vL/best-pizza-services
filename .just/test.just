# Test all workspace members with parallel argument
[doc("Run tests for all workspace members; optionally pass pytest args, e.g. --integration")]
[group("Quality Checks")]
test *flag:
    @echo "{{green}}🔍 Running tests...{{nc}}"
    {{run}} pytest {{flag}} {{ prepend('--cov=', _modules) }} --cov-report=term-missing
    @echo "{{green}}✓ All tests passed.{{nc}}"
