# Container engine
container := env_var_or_default("CONTAINER_ENGINE", "docker")
# Container registry
_registry_owner  := `git remote get-url origin | sed 's/.*github\.com[:/]\([^/]*\)\/.*/\1/' | tr '[:upper:]' '[:lower:]'`
_registry := "ghcr.io/" + _registry_owner
_trivy_flags := "--severity HIGH,CRITICAL --ignore-unfixed --scanners vuln --skip-version-check --exit-code 1"
_uv_audit := "uv audit --locked --preview-features audit"
