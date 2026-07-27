# Test all workspace members with parallel argument
[doc("Run tests for all workspace members.")]
[group("Quality Checks")]
test:
    @echo "{{bold}}{{green}}🔍 Running tests...{{nc}}"
    {{run}} pytest
    @echo "{{bold}}{{green}}✓ All tests passed.{{nc}}"
