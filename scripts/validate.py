#!/usr/bin/env python3
"""Validate Braids source invariants without runtime dependencies."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_FIELDS = {"$schema", "name", "version", "description", "author", "homepage", "repository", "license", "keywords", "extensions"}
PLUGIN_NAME = re.compile(r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]{0,62}[a-z0-9])?$")
LOCAL_REF = re.compile(r'"\$ref"\s*:\s*"([^"#][^"#]*)')
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico"}
EXCLUDED_DIRS = {".git", ".ci-venv", ".venv", "venv", "dist", "__pycache__"}
LIFECYCLE_FILES = {"hooks.json", "mcp.json", "mcp_config.json", ".mcp.json", ".lsp.json", "settings.json"}
UNSAFE_SCRIPT = re.compile(r"\bimport\s+(?:urllib|http\.client|socket|requests|ftplib|smtplib)\b|(?<![.\w])(?:eval|exec)\s*\(")
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{32,}\b"),
)


def load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return None


def validate() -> list[str]:
    errors: list[str] = []
    metadata = load_json(ROOT / "braids.json", errors)
    plugin = load_json(ROOT / "plugin.json", errors)

    if isinstance(metadata, dict) and isinstance(plugin, dict):
        unknown = set(plugin) - PLUGIN_FIELDS
        if unknown:
            errors.append(f"plugin.json has non-portable fields: {sorted(unknown)}")
        if plugin.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
            errors.append("plugin.json targets the wrong Agent Plugins schema")
        if not isinstance(plugin.get("name"), str) or not PLUGIN_NAME.fullmatch(plugin["name"]):
            errors.append("plugin.json has an invalid name")
        if plugin.get("version") != metadata.get("package_version"):
            errors.append("plugin and package versions differ")
        if metadata.get("license") is None and "license" in plugin:
            errors.append("plugin.json must not claim an unresolved license")
        if metadata.get("guard_mode_default") is not False or metadata.get("production_telemetry") is not False:
            errors.append("unresolved Guard Mode/telemetry defaults must remain off")

        if plugin.get("license") != metadata.get("license"):
            errors.append("plugin and package licenses differ")

    validator = ROOT / "skills/braids/scripts/validate_braids.py"
    result = subprocess.run([sys.executable, str(validator), str(ROOT / "skills/braids")], text=True, capture_output=True)
    if result.returncode:
        errors.extend(line for line in result.stderr.splitlines() if line)

    adapters = subprocess.run([sys.executable, str(ROOT / "scripts/build_adapters.py")], text=True, capture_output=True)
    if adapters.returncode:
        errors.extend(line for line in adapters.stderr.splitlines() if line.startswith("ERROR: "))

    for path in sorted((ROOT / "schemas").glob("*.json")):
        schema = load_json(path, errors)
        if not isinstance(schema, dict) or schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"{path.relative_to(ROOT)} is not a Draft 2020-12 schema")
            continue
        text = path.read_text(encoding="utf-8")
        for target in LOCAL_REF.findall(text):
            target_path = path.parent / target
            if not target_path.is_file():
                errors.append(f"{path.relative_to(ROOT)} has unresolved $ref {target}")

    for path in ROOT.rglob("*"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.is_symlink():
            try:
                path.resolve().relative_to(ROOT)
            except ValueError:
                errors.append(f"symlink escapes package: {path.relative_to(ROOT)}")
            continue
        if not path.is_file() or path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".zip", ".gz"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"unexpected binary file: {path.relative_to(ROOT)}")
            continue
        if path.parts[0] in {"skills", "adapters", "scripts", "evals", "fixtures", ".github"}:
            if re.search(r"\[TODO|\bFIXME\b", text, re.IGNORECASE):
                errors.append(f"unfinished implementation marker: {path.relative_to(ROOT)}")
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            errors.append(f"possible secret material: {path.relative_to(ROOT)}")

    if not (ROOT / "skills/braids/SKILL.md").is_file() or (ROOT / "mcp.json").exists():
        errors.append("portable package must contain the Braids skill and no mandatory MCP config")

    for path in ROOT.rglob("*"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        relative = path.relative_to(ROOT)
        if relative.parts[0] == "assets":
            continue
        # An adapter may stage one asset for a host manifest that documents a logo field.
        if relative.parts[:2] == ("adapters", relative.parts[1]) and relative.parts[2:3] == ("files",):
            continue
        if relative.parts[0] == "dist":
            continue
        errors.append(f"brand asset outside assets/: {relative}")

    for path in (ROOT / "adapters").rglob("SKILL.md"):
        errors.append(f"adapter duplicates the kernel: {path.relative_to(ROOT)}")

    # docs/decisions/0003: no adapter installs anything the host executes or trusts on its own.
    for path in (ROOT / "adapters").rglob("*"):
        if path.is_file() and path.name in LIFECYCLE_FILES:
            errors.append(f"adapter ships an unexercised enforcement surface: {path.relative_to(ROOT)}")

    # The kernel's helpers are deterministic local tools; they must not reach the network or eval input.
    for path in sorted((ROOT / "skills/braids/scripts").glob("*.py")):
        source = path.read_text(encoding="utf-8")
        if UNSAFE_SCRIPT.search(source):
            errors.append(f"kernel script gained network or dynamic execution: {path.relative_to(ROOT)}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print("ok: source invariants")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
