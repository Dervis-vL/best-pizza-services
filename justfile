set shell := ["bash", "-euo", "pipefail", "-c"]

# --- IMPORTS --------------------------------------------
import '.just/check.just'

# --- VARIABLES ------------------------------------------
run  := "uv run"
bold := `tput bold 2>/dev/null || true`
nc   := `tput sgr0 2>/dev/null || true`
green := `tput setaf 2 2>/dev/null || true`

default:
    @just --list

lint: fmt typecheck
    @echo "{{bold}}{{green}}✓ All lint checks passed.{{nc}}"