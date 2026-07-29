# CONFIG
# Container engine
container := env_var_or_default("CONTAINER_ENGINE", "docker")
# Container registry
_registry_owner  := `git remote get-url origin | sed 's/.*github\.com[:/]\([^/]*\)\/.*/\1/' | tr '[:upper:]' '[:lower:]'`
_registry := "ghcr.io/" + _registry_owner
