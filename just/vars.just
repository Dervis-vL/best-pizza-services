# Standard toolkit variables for just recipes
# PEP 723 scripts run in their own environment: `just` keeps working even when the workspace does not resolve.
_uv := require('uv')
_just := quote(just_executable())
_scripts    := quote(_uv) + ' run --script ' + quote(justfile_directory() / 'just/scripts')
_workspaces := _scripts / 'workspaces.py' + ' ' + quote(justfile_directory())
_members     := shell(_workspaces + ' members')
_modules     := shell(_workspaces + ' modules')
_deployables := shell(_workspaces + ' deployables')
uv := quote(_uv)
run := uv + ' run'
green := style('bold') + style('green')
yellow := style('yellow')
blue := style('blue')
red := style('red')
nc   := NORMAL
# Container engine
container := env_var_or_default("CONTAINER_ENGINE", "docker")
# Container registry
_registry_owner  := `git remote get-url origin | sed 's/.*github\.com[:/]\([^/]*\)\/.*/\1/' | tr '[:upper:]' '[:lower:]'`
_registry := "ghcr.io/" + _registry_owner
# uv audit is in preview
_uv_audit := "uv audit --locked --preview-features audit"
