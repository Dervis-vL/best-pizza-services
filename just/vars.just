# Standard toolkit variables for just recipes
# PEP 723 scripts run in their own environment: `just` keeps working even when the workspace does not resolve.
_uv := require('uv')
_scripts    := quote(_uv) + ' run --script ' + quote(justfile_directory() / '.just/scripts')
_workspaces := _scripts / 'workspaces.py' + ' ' + quote(justfile_directory())
_members     := shell(_workspaces + ' members')
_modules     := shell(_workspaces + ' modules')
_deployables := shell(_workspaces + ' deployables')
run := quote(_uv) + ' run'
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
_trivy_flags := "--severity HIGH,CRITICAL --ignore-unfixed --scanners vuln --skip-version-check --exit-code 1"
_uv_audit := "uv audit --locked --preview-features audit"
_gitleaks_flags := "--redact --no-banner"
# Where per-member coverage data lands before it is combined
_cov_data := justfile_directory() / ".coverage-data"
# Define the name of the release scope env variable
_release_scope := "RELEASE"
