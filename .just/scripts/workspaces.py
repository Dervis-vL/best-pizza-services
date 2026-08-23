# /// script
# requires-python = ">=3.14"
# ///
"""Print monorepo workspace paths from [tool.uv.workspace] in the root pyproject.toml."""

import pathlib
import sys
import tomllib

root = pathlib.Path(sys.argv[1])
project_path = root / "pyproject.toml"
kind = sys.argv[2]


# read the root level project toml
try:
    ws = tomllib.loads((project_path).read_text())["tool"]["uv"]["workspace"]
except tomllib.TOMLDecodeError as exc:
    msg = f"{project_path} is not valid TOML: {exc}"
    raise SystemExit(msg) from exc
except KeyError as exc:
    msg = f"{project_path} has no [tool.uv.workspace] table (missing {exc})"
    raise SystemExit(msg) from exc

excluded = set(ws.get("exclude", []))

members = sorted(
    p
    for pattern in ws["members"]
    for p in root.glob(pattern)
    if p.is_dir() and str(p.relative_to(root)) not in excluded
)

# Match environment type argument for the return
match kind:
    case "members":
        out = [str(p.relative_to(root)) for p in members]
    case "modules":
        out = [p.name for p in members]
    case "deployables":
        out = [str(p.relative_to(root)) for p in members if (p / "Dockerfile").exists()]
    case _:
        sys.exit(f"unknown kind: {kind}")

print(" ".join(out))  # noqa: T201
