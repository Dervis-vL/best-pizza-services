set shell := ["bash", "-euo", "pipefail", "-c"]
# set minimum-version := '1.57.0'

# --- IMPORTS --------------------------------------------
import 'just/vars.just'
import 'just/setup.just'
import 'just/check.just'
import 'just/test.just'
import 'just/build.just'
import 'just/security.just'
import 'just/version.just'
import 'just/git.just'
import 'just/database.just'

# --- VARIABLES ------------------------------------------
run  := "uv run"
bold := `tput bold 2>/dev/null || true`
nc   := `tput sgr0 2>/dev/null || true`
green := `tput setaf 2 2>/dev/null || true`

# Read from [tool.uv.workspace] members in the root pyproject.toml
_workspaces := 'python3 ' + quote(justfile_directory() / 'just/scripts/workspaces.py') \
    + ' ' + quote(justfile_directory())
_members     := shell(_workspaces + ' members')
_modules     := shell(_workspaces + ' modules')
_deployables := shell(_workspaces + ' deployables')

# --- TARGETS -------------------------------------

[doc("Default target: list all available targets.")]
[private]
default:
    @just --list

# Read a field out of a member's pyproject.toml
[private]
_meta dir field:
    @grep -m1 '^{{field}}' {{dir}}/pyproject.toml | sed -E 's/^{{field}} *= *"//; s/".*//'

[doc("Show all available targets/members.")]
[group("Setup")]
show:
    @echo "{{bold}}{{green}}⚙ Workspace members:{{nc}}"
    @for m in {{_members}}; do \
        echo "{{bold}}{{green}}  - $m{{nc}}"; \
    done
    @echo "{{bold}}{{green}}⚙ Workspace modules:{{nc}}"
    @for m in {{_modules}}; do \
        echo "{{bold}}{{green}}  - $m{{nc}}"; \
    done
    @echo "{{bold}}{{green}}⚙ Workspace deployables:{{nc}}"
    @for m in {{_deployables}}; do \
        echo "{{bold}}{{green}}  - $m{{nc}}"; \
    done

# Run all checks
[doc("Run all quality checks")]
[group("Quality Checks")]
check: fmt check-lock check-type lint check-deps check-spelling test check-version
    @echo "{{bold}}{{green}}✓ All checks passed.{{nc}}"
