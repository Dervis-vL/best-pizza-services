# --- SETTINGS -------------------------------------------
set shell              := ["bash", "-euo", "pipefail", "-c"]
set windows-shell      := ["bash", "-euo", "pipefail", "-c"]
set script-interpreter := ["bash", "-euo", "pipefail"]

set minimum-version := '1.58.0'
set positional-arguments
set default-list
set lazy

# --- IMPORTS --------------------------------------------
import '.just/vars.just'
import '.just/build.just'
import '.just/check.just'
import '.just/database.just'
import '.just/git.just'
import '.just/security.just'
import '.just/setup.just'
import '.just/test.just'
import '.just/version.just'

# --- TARGETS -------------------------------------
# Read a field out of a member's pyproject.toml
[private]
_meta dir field:
    @grep -m1 '^{{field}}' {{dir}}/pyproject.toml | sed -E 's/^{{field}} *= *"//; s/".*//'


[doc("Show all available targets/members.")]
[group("Setup")]
show:
    @echo "{{yellow}}⚙ Workspace members:{{nc}}"
    @for m in {{_members}}; do \
        echo "{{green}}  - $m{{nc}}"; \
    done
    @echo "{{yellow}}⚙ Workspace modules:{{nc}}"
    @for m in {{_modules}}; do \
        echo "{{green}}  - $m{{nc}}"; \
    done
    @echo "{{yellow}}⚙ Workspace deployables:{{nc}}"
    @for m in {{_deployables}}; do \
        echo "{{green}}  - $m{{nc}}"; \
    done


[doc("Build and push all images to registry, also tagging latest")]
[group("Build & Deploy")]
publish: build push-to-registry
    @echo "{{yellow}}✓ All images built and pushed to registry.{{nc}}"
