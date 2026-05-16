set shell := ["bash", "-euo", "pipefail", "-c"]

# --- IMPORTS --------------------------------------------
import 'just/check.just'
import 'just/test.just'

# --- VARIABLES ------------------------------------------
run  := "uv run"
bold := `tput bold 2>/dev/null || true`
nc   := `tput sgr0 2>/dev/null || true`
green := `tput setaf 2 2>/dev/null || true`

default:
    @just --list


# Run all checks: fmt, test, typecheck, lint, deps-check
check: fmt typecheck lint deps-check test
    @echo "{{bold}}{{green}}✓ All checks passed.{{nc}}"