#!/usr/bin/env python3
"""Dependency-free structural validation for the portable Braids skill."""

from __future__ import annotations

import re
import sys
from pathlib import Path


LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    skill = root / "SKILL.md"
    if not skill.is_file():
        return ["missing SKILL.md"]

    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        return ["SKILL.md must contain YAML frontmatter"]
    frontmatter, body = text[4:].split("\n---\n", 1)
    fields = {}
    for line in frontmatter.splitlines():
        if line and not line.startswith(" ") and ":" in line:
            key, value = line.split(":", 1)
            raw = value.strip()
            # A plain YAML scalar may not contain ": ". Hosts parse this file with a
            # real YAML parser, so an unquoted description holding "Triggers on: x"
            # breaks skill discovery even though a naive line split reads it fine.
            if raw and raw[0] not in "\"'" and ": " in raw:
                errors.append(f"frontmatter {key} contains ': ' and must be quoted")
            fields[key] = raw.strip('"\'')

    name = fields.get("name", "")
    description = fields.get("description", "")
    if not NAME.fullmatch(name) or name != root.name:
        errors.append("frontmatter name must match the skill directory")
    if not 1 <= len(description) <= 1024:
        errors.append("description must contain 1-1024 characters")
    if len(text.splitlines()) >= 500:
        errors.append("SKILL.md must stay below 500 lines")
    if re.search(r"\b(?:TODO|FIXME)\b|\[TODO", text, re.IGNORECASE):
        errors.append("SKILL.md contains unfinished scaffold text")

    for target in LINK.findall(body):
        if "://" in target or target.startswith("#"):
            continue
        path = (root / target.split("#", 1)[0]).resolve()
        try:
            path.relative_to(root.resolve())
        except ValueError:
            errors.append(f"reference escapes skill root: {target}")
            continue
        if not path.is_file():
            errors.append(f"broken reference: {target}")
        if target.startswith("references/") and len(Path(target).parts) != 2:
            errors.append(f"reference must be one level deep: {target}")

    for path in root.rglob("*"):
        if path.is_symlink():
            try:
                path.resolve().relative_to(root.resolve())
            except ValueError:
                errors.append(f"symlink escapes skill root: {path.relative_to(root)}")
    return errors


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    errors = validate(root)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"ok: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
