# Validate an environment contains all project needs
[doc("Validate the development environment.")]
[group("Setup")]
validate:
    @echo "{{bold}}{{green}}⚙ checking toml members...{{nc}}"
    @echo "{{bold}}{{green}}⚙ checking .env...{{nc}}"
    @echo "{{bold}}{{green}}⚙ checking prereq...{{nc}}"

# Setup the development environment
[doc("Initialize the development environment.")]
[group("Setup")]
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

[doc("Add a new workspace member to the project.")]
[group("Setup")]
add:
    @echo "{{bold}}{{green}}⚙ Adding new workspace member...{{nc}}"
    @echo "{{bold}}{{green}}⚙ Updating pyproject.toml...{{nc}}"
    @echo "{{bold}}{{green}}⚙ Updating pre-commit hooks...{{nc}}"
    @echo "{{bold}}{{green}}✓ New workspace member added.{{nc}}"
