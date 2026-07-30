# /// script
# requires-python = ">=3.14"
# ///
"""Print workspace paths from [tool.uv.workspace] in the root pyproject.toml."""

import pathlib
import sys
import tomllib

root = pathlib.Path(sys.argv[1])
kind = sys.argv[2]

ws = tomllib.loads((root / "pyproject.toml").read_text())["tool"]["uv"]["workspace"]
excluded = set(ws.get("exclude", []))

members = sorted(
    p
    for pattern in ws["members"]
    for p in root.glob(pattern)
    if p.is_dir() and str(p.relative_to(root)) not in excluded
)

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
