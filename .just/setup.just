# Setup the development environment
[doc("Initialize the development environment.")]
[group("Setup")]
setup:
    @echo "{{green}}⚙ Installing dependencies...{{nc}}"
    uv sync
    @echo "{{green}}⚙ Installing pre-commit hooks...{{nc}}"
    {{run}} prek install
    @if [ ! -f .env ]; then \
        cp .env.example .env; \
        echo "{{green}}⚙ Created .env from .env.example; update credentials as needed.{{nc}}"; \
    fi
    @echo "{{green}}✓ Environment ready.{{nc}}"


[doc("Scaffold a new member from templates/member, e.g. `just new-member services/pizza_stats --depends pizza-shared`")]
[group("Setup")]
[script]
new-member target *args:
    #!/usr/bin/env bash

    echo -e "{{ green }}📦 Scaffolding {{target}}{{ nc }}"
    # positional-arguments keeps quoted values intact, e.g. --description "Aggregations over the rankings"
    {{ _scripts }}/new_member.py "{{ justfile_directory() }}" "$1" "${@:2}"
    echo -e "{{ green }}📦 Syncing the workspace (the glob in [tool.uv.workspace] already includes it){{ nc }}"
    uv sync
    echo -e "{{ green }}✓ {{target}} is a workspace member. Run: just test-member {{target}}{{ nc }}"
