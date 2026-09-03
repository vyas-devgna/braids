#!/usr/bin/env python3
"""Emit a HostCapabilities profile from directly observed local facts.

Braids' first rule about a host is never to infer a capability from a product
name. This script is how that rule is kept: it reports only what it can observe
from this process — environment, PATH, and files in the working tree — and
records the observation next to every value it reports. Anything it cannot
observe stays `unknown`, which is a useful answer, not a missing one.

It is deliberately hermetic: no network, no subprocesses, no writes outside a
single probe file it removes. Running it twice on an unchanged tree gives the
same answer apart from the timestamp.

    python3 inspect_capabilities.py            # JSON profile on stdout
    python3 inspect_capabilities.py --summary  # short human/model-readable form

The `verification` block is the part that changes decisions most: it names the
commands this project actually offers for the claims Braids has to evidence.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


# Environment markers that identify a host. Presence is observed; the mapping
# from marker to host name is documented behaviour, not a capability claim.
HOST_MARKERS = (
    ("claude-code", ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT")),
    ("codex", ("CODEX_HOME", "CODEX_SANDBOX", "CODEX_PROXY_CERT")),
    ("cursor", ("CURSOR_TRACE_ID", "CURSOR_AGENT")),
    ("windsurf", ("WINDSURF_SESSION_ID", "WINDSURF_USER_ID")),
    ("cline", ("CLINE_SESSION_ID", "CLINE_TASK_ID")),
    ("opencode", ("OPENCODE_SESSION", "OPENCODE_DISABLE_EXTERNAL_SKILLS")),
    ("copilot", ("COPILOT_AGENT_ID", "GITHUB_COPILOT_SESSION")),
    ("antigravity", ("ANTIGRAVITY_SESSION", "ANTIGRAVITY_WORKSPACE")),
)

CI_MARKERS = ("GITHUB_ACTIONS", "GITLAB_CI", "CIRCLECI", "BUILDKITE", "JENKINS_URL", "CODESPACES", "CI")

# Tool name -> the capability it evidences. First hit on PATH wins.
SEARCH_TOOLS = ("rg", "ag", "ack", "grep")
AST_TOOLS = ("ast-grep", "sg", "semgrep", "comby")
ANALYSIS_TOOLS = ("ruff", "mypy", "pyright", "eslint", "shellcheck", "golangci-lint", "clippy-driver", "cppcheck")
COMPILER_TOOLS = ("tsc", "gcc", "clang", "cargo", "go", "javac", "dotnet", "swiftc", "rustc")
PROFILER_TOOLS = ("perf", "py-spy", "valgrind", "pprof", "dtrace")
LSP_TOOLS = ("pyright-langserver", "gopls", "rust-analyzer", "typescript-language-server", "clangd", "jdtls")

# Project file -> (verification kind, command that would produce the evidence).
# Only reported when the file actually exists in the working tree.
VERIFICATION_SIGNALS = (
    ("pyproject.toml", "tests", "pytest"),
    ("pytest.ini", "tests", "pytest"),
    ("tox.ini", "tests", "tox"),
    ("Cargo.toml", "tests", "cargo test"),
    ("Cargo.toml", "build", "cargo build"),
    ("go.mod", "tests", "go test ./..."),
    ("go.mod", "build", "go build ./..."),
    ("Makefile", "build", "make"),
    ("CMakeLists.txt", "build", "cmake --build"),
    ("pom.xml", "tests", "mvn test"),
    ("build.gradle", "tests", "gradle test"),
    ("Gemfile", "tests", "bundle exec rspec"),
)

INSTRUCTION_FILES = (
    ("CLAUDE.md", "project"),
    ("AGENTS.md", "project"),
    (".cursorrules", "project"),
    (".cursor/rules", "project"),
    (".github/copilot-instructions.md", "project"),
    (".windsurfrules", "project"),
    (".clinerules", "project"),
)


def first_on_path(names: tuple[str, ...]) -> str | None:
    for name in names:
        if shutil.which(name):
            return name
    return None


def detect_host(env: dict[str, str]) -> tuple[str, str]:
    for host, markers in HOST_MARKERS:
        hit = [marker for marker in markers if env.get(marker)]
        if hit:
            return host, f"environment sets {', '.join(sorted(hit))}"
    return "unknown", "no known host marker in the environment"


def detect_surface(env: dict[str, str]) -> tuple[str, str]:
    ci = [marker for marker in CI_MARKERS if env.get(marker)]
    if ci:
        return "cloud", f"CI environment: {', '.join(sorted(ci))}"
    if Path("/.dockerenv").exists() or Path("/run/.containerenv").exists():
        return "unknown", "container marker present; a container may be local or cloud-hosted"
    return "local", "no CI or container marker observed"


def detect_isolation(env: dict[str, str], cwd: Path) -> tuple[str, str]:
    sandbox = env.get("CODEX_SANDBOX") or env.get("SECCOMP_SANDBOX")
    if sandbox:
        return "sandbox", f"host reports sandbox mode {sandbox!r}"
    if Path("/.dockerenv").exists() or Path("/run/.containerenv").exists():
        return "sandbox", "running inside a container"
    git = cwd / ".git"
    if git.is_file():
        # A linked worktree stores a `gitdir:` pointer file rather than a directory.
        return "worktree", ".git is a file, so this is a linked git worktree"
    return "unknown", "no isolation marker observed; absence is not proof of none"


def detect_network(env: dict[str, str]) -> tuple[str, str]:
    # Probing the network is forbidden in a kernel script, so this reports only
    # what the host states about itself.
    if env.get("CODEX_SANDBOX_NETWORK_DISABLED") == "1":
        return "none", "host sets CODEX_SANDBOX_NETWORK_DISABLED=1"
    proxies = [name for name in ("HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY", "http_proxy", "https_proxy", "no_proxy")
               if env.get(name)]
    detail = f"; proxy variables present: {', '.join(sorted(proxies))}" if proxies else ""
    return "unknown", f"not probed; a kernel script must not open the network{detail}"


def detect_write(cwd: Path) -> tuple[str, str]:
    probe: Path | None = None
    try:
        descriptor, raw_path = tempfile.mkstemp(prefix=".braids-write-probe-", dir=cwd)
        os.close(descriptor)
        probe = Path(raw_path)
    except OSError as exc:
        return "unavailable", f"cannot create a file in the working tree ({exc.strerror or exc})"
    try:
        probe.unlink()
    except OSError as exc:
        return "available", f"created a unique probe file but could not remove it ({exc.strerror or exc})"
    return "available", "created and removed a probe file in the working tree"


def detect_read(cwd: Path) -> tuple[str, str]:
    try:
        next(iter(cwd.iterdir()), None)
    except OSError as exc:
        return "unavailable", f"cannot list the working tree ({exc.strerror or exc})"
    return "available", "listed the working tree"


def detect_instructions(cwd: Path) -> tuple[str, str]:
    found = []
    for directory in (cwd, *cwd.parents):
        for name, _ in INSTRUCTION_FILES:
            path = directory / name
            if path.exists():
                found.append(str(path.relative_to(cwd)) if path.is_relative_to(cwd) else str(path))
    if not found:
        return "unknown", "no project instruction file found in the working tree or its parents"
    return "project", f"project instruction files present: {', '.join(sorted(set(found)))}"


def detect_hooks(cwd: Path) -> tuple[dict, str]:
    """Hooks are the only deterministic enforcement surface, so read them exactly."""
    for relative in (".claude/settings.json", ".claude/settings.local.json"):
        path = cwd / relative
        if not path.is_file():
            continue
        try:
            settings = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {"availability": "unknown", "events": []}, f"{relative} is present but unreadable"
        hooks = settings.get("hooks")
        if isinstance(hooks, dict) and hooks:
            events = sorted(str(event) for event in hooks)
            return ({"availability": "available", "events": events},
                    f"{relative} configures hooks for {', '.join(events)}")
        return {"availability": "unavailable", "events": []}, f"{relative} configures no hooks"
    return {"availability": "unknown", "events": []}, "no host settings file found in the working tree"


def detect_mcp(cwd: Path) -> tuple[str, str]:
    for relative in (".mcp.json", ".cursor/mcp.json", ".vscode/mcp.json"):
        if (cwd / relative).is_file():
            return "available", f"{relative} is present in the working tree"
    return "unknown", "no MCP configuration found in the working tree"


def detect_verification(cwd: Path) -> tuple[dict[str, list[str]], str]:
    """Name the commands this project offers for the claims Braids must evidence."""
    found: dict[str, list[str]] = {}
    for filename, kind, command in VERIFICATION_SIGNALS:
        if (cwd / filename).exists():
            found.setdefault(kind, [])
            if command not in found[kind]:
                found[kind].append(command)

    package = cwd / "package.json"
    if package.is_file():
        try:
            scripts = json.loads(package.read_text(encoding="utf-8")).get("scripts", {})
        except (OSError, json.JSONDecodeError):
            scripts = {}
        for name in ("test", "build", "lint", "typecheck"):
            if isinstance(scripts, dict) and name in scripts:
                kind = "tests" if name == "test" else ("build" if name == "build" else "static_analysis")
                found.setdefault(kind, [])
                found[kind].append(f"npm run {name}")

    if any(cwd.glob("test_*.py")) or (cwd / "tests").is_dir():
        found.setdefault("tests", [])
        if not found["tests"]:
            found["tests"].append("python3 -m unittest discover")

    if not found:
        return {}, "no build, test or lint entry point found in the working tree"
    summary = "; ".join(f"{kind}: {', '.join(commands)}" for kind, commands in sorted(found.items()))
    return found, summary


def profile(host: str | None, host_version: str | None, surface: str | None) -> dict:
    env = dict(os.environ)
    cwd = Path.cwd()
    observations: dict[str, str] = {}

    def record(field: str, pair: tuple):
        value, evidence = pair
        observations[field] = evidence
        return value

    detected_host, host_evidence = detect_host(env)
    resolved_host = host or detected_host
    observations["host"] = host_evidence if host is None else f"supplied by the caller as {host!r}"

    detected_surface, surface_evidence = detect_surface(env)
    resolved_surface = surface or detected_surface
    observations["surface"] = surface_evidence if surface is None else f"supplied by the caller as {surface!r}"

    search = first_on_path(SEARCH_TOOLS)
    ast = first_on_path(AST_TOOLS)
    analysis = first_on_path(ANALYSIS_TOOLS)
    compiler = first_on_path(COMPILER_TOOLS)
    profiler = first_on_path(PROFILER_TOOLS)
    lsp = first_on_path(LSP_TOOLS)
    shell = first_on_path(("sh", "bash", "zsh"))

    verification, verification_evidence = detect_verification(cwd)
    observations["verification"] = verification_evidence

    for field, tool, names in (
        ("code_intelligence.text_search", search, SEARCH_TOOLS),
        ("code_intelligence.ast", ast, AST_TOOLS),
        ("code_intelligence.static_analysis", analysis, ANALYSIS_TOOLS),
        ("code_intelligence.compiler", compiler, COMPILER_TOOLS),
        ("code_intelligence.profiler", profiler, PROFILER_TOOLS),
        ("code_intelligence.lsp", lsp, LSP_TOOLS),
    ):
        observations[field] = (
            f"{tool} is on PATH" if tool
            else f"none of {', '.join(names)} is on PATH"
        )
    observations["code_intelligence.tests"] = (
        f"project declares a test entry point ({', '.join(verification['tests'])})"
        if verification.get("tests") else "no test entry point found in the working tree"
    )
    observations["execution.shell"] = (
        f"{shell} is on PATH; whether the agent may call it is a host policy this process cannot see"
        if shell else "no shell binary found on PATH"
    )
    observations["execution.browser"] = "not observable from this process"
    observations["delegation"] = "not observable from this process; ask the host"
    observations["permissions"] = "not observable from this process; ask the host"
    observations["skill_loading"] = "not observable from this process; ask the host"
    observations["host_version"] = (
        f"supplied by the caller as {host_version!r}" if host_version
        else "not observable from this process; read it from the host"
    )

    hooks, hooks_evidence = detect_hooks(cwd)
    observations["hooks"] = hooks_evidence

    return {
        "schema_version": "1.0",
        "host": resolved_host,
        "host_version": host_version,
        "surface": resolved_surface,
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "skill_loading": "unknown",
        "persistent_instruction": record("persistent_instruction", detect_instructions(cwd)),
        "execution": {
            "read": record("execution.read", detect_read(cwd)),
            "write": record("execution.write", detect_write(cwd)),
            "shell": "available" if shell else "unknown",
            "browser": "unknown",
        },
        "network": record("network", detect_network(env)),
        "code_intelligence": {
            "text_search": "available" if search else "unknown",
            "lsp": "available" if lsp else "unknown",
            "ast": "available" if ast else "unknown",
            "static_analysis": "available" if analysis else "unknown",
            "compiler": "available" if compiler else "unknown",
            "tests": "available" if verification.get("tests") else "unknown",
            "profiler": "available" if profiler else "unknown",
        },
        "delegation": "unknown",
        "isolation": record("isolation", detect_isolation(env, cwd)),
        "permissions": "unknown",
        "mcp": record("mcp", detect_mcp(cwd)),
        "hooks": hooks,
        # Enforcement stays empty by construction. A capability is not an
        # enforcement guarantee, and nothing this script can see proves one.
        "enforcement": [],
        "observations": observations,
    }


def summarize(profile: dict) -> str:
    observations = profile.get("observations", {})
    lines = [
        f"host        {profile['host']}  ({observations.get('host', '')})",
        f"surface     {profile['surface']}  ({observations.get('surface', '')})",
        f"isolation   {profile['isolation']}  ({observations.get('isolation', '')})",
        f"network     {profile['network']}  ({observations.get('network', '')})",
        f"write       {profile['execution']['write']}  ({observations.get('execution.write', '')})",
        f"instructions {profile['persistent_instruction']}  ({observations.get('persistent_instruction', '')})",
        f"hooks       {profile['hooks']['availability']}  ({observations.get('hooks', '')})",
        f"verify      {observations.get('verification', '')}",
    ]
    unknown = sorted(
        key for key, value in profile["code_intelligence"].items() if value == "unknown"
    )
    if unknown:
        lines.append(f"unknown     code intelligence: {', '.join(unknown)}")
    lines.append("")
    lines.append("Values above are observations or explicit caller overrides. Every `unknown` is genuinely unknown, not absent.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--host", help="Override the detected host name.")
    parser.add_argument("--host-version", help="Host version, which this process cannot observe.")
    parser.add_argument("--surface", choices=["local", "cloud", "mixed", "unknown"],
                        help="Override the detected execution surface.")
    parser.add_argument("--summary", action="store_true", help="Print a short readable form instead of JSON.")
    args = parser.parse_args()

    value = profile(args.host, args.host_version, args.surface)
    if args.summary:
        print(summarize(value))
    else:
        print(json.dumps(value, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
