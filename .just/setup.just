# WIP
# Validate an environment contains all project needs
[doc("WIP: Validate the development environment.")]
[group("Setup")]
validate:
    @echo "{{green}}⚙ checking toml members...{{nc}}"
    @echo "{{green}}⚙ checking .env...{{nc}}"
    @echo "{{green}}⚙ checking prereq...{{nc}}"


# Initialize the monorepo with a new project
[doc("WIP: Initialize the monorepo with a new project.")]
[group("Setup")]
init:
    @echo "{{green}}⚙ Initializing new project...{{nc}}"
    @echo "{{green}}⚙ updating pyproject.toml...{{nc}}"
    @echo "{{green}}⚙ updating pre-commit hooks...{{nc}}"
    @echo "{{green}}✓ New project initialized.{{nc}}"


# Setup the development environment
[doc("Initialize the development environment.")]
[group("Setup")]
setup:
    @echo "{{green}}⚙ Installing dependencies...{{nc}}"
    uv sync
    @echo "{{green}}⚙ Installing pre-commit hooks...{{nc}}"
    {{run}} pre-commit install
    @if [ ! -f .env ]; then \
        cp .env.example .env; \
        echo "{{green}}⚙ Created .env from .env.example; update credentials as needed.{{nc}}"; \
    fi
    @echo "{{green}}✓ Environment ready.{{nc}}"


# WIP
[doc("WIP: Add a new workspace member template to the monorepo.")]
[group("Setup")]
add:
    @echo "{{green}}⚙ Adding new workspace member...{{nc}}"
    @echo "{{green}}⚙ Updating pyproject.toml...{{nc}}"
    @echo "{{green}}⚙ Updating pre-commit hooks...{{nc}}"
    @echo "{{green}}✓ New workspace member added.{{nc}}"
