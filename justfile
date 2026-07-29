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

# --- VARIABLES ------------------------------------------
run  := "uv run"
bold := `tput bold 2>/dev/null || true`
nc   := `tput sgr0 2>/dev/null || true`
green := `tput setaf 2 2>/dev/null || true`
# Read from [tool.uv.workspace] members in the root pyproject.toml
# TODO: include tomlib reader scripts so excludes can be parsed too
_globs   := shell('awk "/^\[tool.uv.workspace\]/{f=1;next} /^\[/{f=0} f" pyproject.toml | grep -oE "\"[^\"]+\"" | tr -d "\"" | tr "\n" " "')
_members := shell('for p in $1; do ls -d $p/ 2>/dev/null; done | sed "s#/\$##" | tr "\n" " "', _globs)
_modules := shell('for d in $1; do basename "$d"; done | tr "\n" " "', _members)
_deployables := shell('for d in $1; do [ -f "$d/Dockerfile" ] && printf "%s " "$d"; done; true', _members)


# Read a field out of a member's pyproject.toml
[private]
_meta dir field:
    @grep -m1 '^{{field}}' {{dir}}/pyproject.toml | sed -E 's/^{{field}} *= *"//; s/".*//'

[doc("Default target: list all available targets.")]
[private]
default:
    @just --list

[doc("Show all available targets/members.")]
[group("Setup")]
show:
    @echo "{{bold}}{{green}}⚙ Workspace members:{{nc}}"
    @for m in {{_members}}; do \
        echo "{{bold}}{{green}}  - $m{{nc}}"; \
    done
    @echo "{{bold}}{{green}}⚙ Workspace deployables:{{nc}}"
    @for m in {{_deployables}}; do \
        echo "{{bold}}{{green}}  - $m{{nc}}"; \
    done

# Run all checks: fmt, test, typecheck, lint, deps-check, version-check
[doc("Run all qualitychecks")]
[group("Quality Checks")]
check: fmt lock-check typecheck lint deps-check spell-check test version-check
    @echo "{{bold}}{{green}}✓ All checks passed.{{nc}}"
