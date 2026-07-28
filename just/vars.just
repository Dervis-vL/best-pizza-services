# Glob patterns, read from [tool.uv.workspace] members in the root pyproject.toml
_globs   := shell('awk "/^\[tool.uv.workspace\]/{f=1;next} /^\[/{f=0} f" pyproject.toml | grep -oE "\"[^\"]+\"" | tr -d "\"" | tr "\n" " "')
_members := shell('for p in $1; do ls -d $p/ 2>/dev/null; done | sed "s#/\$##" | tr "\n" " "', _globs)
_modules := shell('for d in $1; do basename "$d"; done | tr "\n" " "', _members)
_deployables := shell('for d in $1; do [ -f "$d/Dockerfile" ] && printf "%s " "$d"; done; true', _members)

# Container engine
container := env_var_or_default("CONTAINER_ENGINE", "podman")

# Container registry
_github_user  := `git remote get-url origin | sed 's/.*github\.com[:/]\([^/]*\)\/.*/\1/' | tr '[:upper:]' '[:lower:]'`
_registry_ghcr := "ghcr.io/" + _github_user
