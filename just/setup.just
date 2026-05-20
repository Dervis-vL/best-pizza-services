# Setup the development environment
setup:
    @echo "{{bold}}{{green}}⚙ Installing dependencies...{{nc}}"
    uv sync
    @echo "{{bold}}{{green}}⚙ Installing pre-commit hooks...{{nc}}"
    {{run}} pre-commit install
    @if [ ! -f .env ]; then \
        cp .env.example .env; \
        echo "{{bold}}{{green}}⚙ Created .env from .env.example; update credentials as needed.{{nc}}"; \
    fi
    @echo "{{bold}}{{green}}✓ Environment ready.{{nc}}"
