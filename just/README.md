# `just/` — task runner

All repo tasks live here. The root `justfile` sets the shell, defines shared display
variables, and imports every module in this directory.

```
justfile          shell settings, colours, `check` aggregate, imports
just/vars.just    derived workspace variables + configurable knobs
just/setup.just   environment setup, validation, member scaffolding
just/check.just   fmt, typecheck, lint, deps-check, spell-check, lock-check
just/test.just    pytest with per-member coverage
just/build.just   container images, compose, alembic
just/security.just security scanning
just/version.just per-project change detection, changelog checks, version bumps
just/git.just     branch cleanup
```

Run `just` for the grouped recipe list, `just --groups` for group names alone, and
`just --variables` to see every variable.

## Nothing is hardcoded per member

`justfile` derives the workspace layout from the root `pyproject.toml`, so adding a
member requires **no edits here**:

| Variable | Contents | Derived from |
| --- | --- | --- |
| `_globs` | `apps/* packages/* services/*` | `[tool.uv.workspace] members` |
| `_members` | member directories | expanding `_globs` |
| `_modules` | member module names | basename of each member directory |

Recipes consume these instead of listing projects. `typecheck` and `test` build their
flags with just's `prepend()`; `deps-check` and the versioning recipes loop over
`_members`.

This relies on one convention: **a member's directory name must equal its Python module
name**, and its distribution name must be the same with hyphens
(`services/pizza_data_collector` → module `pizza_data_collector` → dist
`pizza-data-collector`). The `uv_build` backend requires this too, so it is not an extra
constraint — just one worth knowing when it breaks.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `CONTAINER_ENGINE` | `docker` | Engine used by the build and compose recipes |

Override per invocation or export it:

```bash
CONTAINER_ENGINE=docker just build
```

Recipes taking an env file default to `.env`:

```bash
just compose                    # uses .env
just compose dev/env/.env       # uses another dotenv
just alembic-upgrade .env.local
```

## Adding a workspace member

Membership itself is automatic — `[tool.uv.workspace] members` uses globs, so a new
directory under `apps/`, `packages/`, or `services/` with a `pyproject.toml` is picked
up by uv and by every recipe here.

What the member must contain for the recipes to work:

- `pyproject.toml` with `[project]` name/version/requires-python and
  `build-backend = "uv_build"`
- `src/<module>/__init__.py` and `src/<module>/py.typed`
- `README.md` declared as `readme`, and copied by the Dockerfiles
- `CHANGELOG.md` containing an `[Unreleased]` section
- `release_scope.env` with `SCOPE=patch|minor|major`
- `[tool.bumpversion]` with `tag_name = "<dist-name>/v{new_version}"`
- a `Dockerfile`, only if it should produce a deployable image

Run `uv lock` afterwards, or `lock-check` will fail.
