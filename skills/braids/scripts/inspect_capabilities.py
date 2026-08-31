#!/usr/bin/env python3
"""Emit a conservative HostCapabilities profile from directly observed local facts."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


def profile(host: str, host_version: str | None, surface: str) -> dict:
    readable = (Path.cwd() / ".").is_dir()
    return {
        "schema_version": "1.0",
        "host": host,
        "host_version": host_version,
        "surface": surface,
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "skill_loading": "unknown",
        "persistent_instruction": "unknown",
        "execution": {
            "read": "available" if readable else "unknown",
            "write": "unknown",
            "shell": "available",
            "browser": "unknown",
        },
        "network": "unknown",
        "code_intelligence": {
            "text_search": "available" if shutil.which("rg") else "unknown",
            "lsp": "unknown",
            "ast": "unknown",
            "static_analysis": "unknown",
            "compiler": "unknown",
            "tests": "unknown",
            "profiler": "unknown",
        },
        "delegation": "unknown",
        "isolation": "unknown",
        "permissions": "unknown",
        "mcp": "unknown",
        "hooks": {"availability": "unknown", "events": []},
        "enforcement": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="unknown")
    parser.add_argument("--host-version")
    parser.add_argument("--surface", choices=["local", "cloud", "mixed", "unknown"], default="unknown")
    args = parser.parse_args()
    print(json.dumps(profile(args.host, args.host_version, args.surface), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
