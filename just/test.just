# Test all workspace members with parallel argument
test:
    @echo "{{bold}}{{green}}🔍 Running tests...{{nc}}"
    {{run}} pytest
    @echo "{{bold}}{{green}}✓ All tests passed.{{nc}}"
