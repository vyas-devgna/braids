#!/usr/bin/env python3
"""Embed diagrams/*.mmd into the docs that reference them, from one source.

GitHub renders mermaid natively, but markdown cannot include a file. Rather than
pasting each diagram and letting the copies drift, docs carry a marker:

    <!-- diagram:01-braids-system-architecture -->

and this script fills the fenced block beneath it. `--check` fails when an
embedded copy no longer matches its `.mmd`, so CI catches drift the same way it
catches a stale adapter README.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIAGRAMS = ROOT / "diagrams"
MARKER = re.compile(r"^<!-- diagram:([a-z0-9-]+) -->$", re.M)


def render(name: str) -> str:
    source = (DIAGRAMS / f"{name}.mmd").read_text(encoding="utf-8").strip()
    return f"<!-- diagram:{name} -->\n```mermaid\n{source}\n```"


def sync(path: Path, write: bool) -> list[str]:
    text = path.read_text(encoding="utf-8")
    updated = text
    problems: list[str] = []

    for match in MARKER.finditer(text):
        name = match.group(1)
        if not (DIAGRAMS / f"{name}.mmd").is_file():
            problems.append(f"{path.relative_to(ROOT)}: no diagram named {name}")
            continue
        block = render(name)
        # Replace the marker plus any fenced block immediately following it.
        pattern = re.compile(
            re.escape(match.group(0)) + r"(\n```mermaid\n.*?\n```)?",
            re.S,
        )
        updated = pattern.sub(lambda _: block, updated, count=1)

    if updated != text:
        if write:
            path.write_text(updated, encoding="utf-8")
        else:
            problems.append(f"{path.relative_to(ROOT)}: embedded diagram is stale")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Refresh embedded blocks in place.")
    args = parser.parse_args()

    problems: list[str] = []
    touched = 0
    for path in sorted(ROOT.rglob("*.md")):
        if any(part in {".git", "dist", "node_modules"} for part in path.parts):
            continue
        if MARKER.search(path.read_text(encoding="utf-8")):
            touched += 1
            problems.extend(sync(path, args.write))

    if problems:
        print("\n".join(f"ERROR: {p}" for p in problems), file=sys.stderr)
        return 1
    print(f"ok: {touched} documents carry embedded diagrams")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
