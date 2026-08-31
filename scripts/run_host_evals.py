#!/usr/bin/env python3
"""Run Braids eval cases against a real host and emit gradeable run records.

Produces JSONL conforming to `schemas/eval-run.schema.json`, which
`scripts/run_evals.py --results` then grades against the case corpus.

Two signals are measured differently and must not be confused:

- `triggered`, `telemetry` and `references_loaded` are read directly out of the
  host's own event stream. They are observations, not opinions.
- `observed_depth` and `observed_properties` come from a separate judge model
  that is shown the transcript and the case's declared property vocabulary. That
  is a model judgement and is labelled as one wherever it is reported.

Fixtures are copied to a temporary directory before every run, so a case can
never mutate the hash-pinned originals.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KERNEL = ROOT / "skills/braids"
JUDGE_MODEL = "claude-haiku-4-5-20251001"
HOST_MODELS = {"claude-code": "sonnet", "codex": "gpt-5.6-sol"}
ISOLATED: dict[str, str] = {}

# Appended to every prompt, identically on every host, so the judge has a
# consistent surface to read. It asks for a summary; it does not tell the model
# how to engineer, which depth to pick, or which properties to claim.
ENVELOPE = (
    "\n\n---\n"
    "When you have finished, end your reply with a fenced ```json block containing exactly:\n"
    '{"depth": "<D0|D1|D2|D3|D4>", "summary": "<two sentences on what you decided and why>", '
    '"claims": [{"claim": "...", "evidence": "..."}]}\n'
    "Report the depth you actually worked at. If you made no change, say so in the summary."
)

JUDGE_PROMPT = """You are grading one run of an engineering-agent evaluation. Answer only from the transcript.

TASK GIVEN TO THE AGENT:
{prompt}

AGENT TRANSCRIPT:
{response}

Decide which of these properties the transcript demonstrates. A property holds only if the transcript shows it, not if the agent merely could have done it.

CANDIDATE PROPERTIES (the agent should show these):
{expected}

FORBIDDEN PROPERTIES (the agent should NOT show these):
{forbidden}

Reply with only a fenced ```json block:
{{"depth": "<D0|D1|D2|D3|D4|unknown>", "present": ["<exact strings from either list above>"], "reasoning": "<one sentence>"}}

Put a string in "present" only if it appears verbatim in one of the two lists above and the transcript demonstrates it."""


def isolate() -> dict[str, str]:
    """Give each host a throwaway config home holding only credentials.

    Without this the run measures whichever skills and marketplaces happen to be
    installed on the developer's machine — 56 skills here, of which Braids is
    one. Isolation reduces that to the host's built-ins plus Braids, so the
    numbers describe Braids rather than this laptop.
    """
    if ISOLATED:
        return ISOLATED
    home = Path(tempfile.mkdtemp(prefix="braids-eval-home-"))
    (home / ".claude").mkdir()
    credentials = Path.home() / ".claude/.credentials.json"
    if credentials.exists():
        (home / ".claude/.credentials.json").symlink_to(credentials)
    account = json.loads((Path.home() / ".claude.json").read_text(encoding="utf-8"))
    (home / ".claude.json").write_text(json.dumps(
        {key: account[key] for key in ("oauthAccount", "userID", "hasCompletedOnboarding") if key in account}
    ), encoding="utf-8")

    codex_home = home / ".codex"
    codex_home.mkdir()
    auth = Path.home() / ".codex/auth.json"
    if auth.exists():
        (codex_home / "auth.json").symlink_to(auth)

    ISOLATED.update({"HOME": str(home), "CODEX_HOME": str(codex_home)})
    return ISOLATED


def environment() -> dict[str, str]:
    import os
    return {**os.environ, **isolate()}


def parse_json_block(text: str) -> dict | None:
    """Pull the last fenced json object out of a model reply."""
    depth = 0
    for index in range(len(text) - 1, -1, -1):
        if text[index] == "}":
            depth += 1
            if depth == 1:
                end = index + 1
        elif text[index] == "{":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[index:end])
                except json.JSONDecodeError:
                    depth = 0
    return None


def run_claude(prompt: str, cwd: Path, plugin: Path | None, timeout: int) -> tuple[str, list[dict], dict]:
    command = [
        "claude", "-p", prompt,
        "--model", HOST_MODELS["claude-code"],
        "--output-format", "stream-json", "--verbose",
        "--permission-mode", "plan", "--strict-mcp-config",
    ]
    if plugin:
        command += ["--plugin-dir", str(plugin)]
    completed = subprocess.run(
        command, cwd=cwd, text=True, capture_output=True, timeout=timeout,
        stdin=subprocess.DEVNULL, env=environment(),
    )
    events = []
    for line in completed.stdout.splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    tools, response, meta, model = [], "", {}, None
    for event in events:
        if event.get("type") == "system" and event.get("subtype") == "init":
            model = event.get("model")
        if event.get("type") == "assistant":
            for block in event["message"].get("content", []):
                if block.get("type") == "tool_use":
                    tools.append({"name": block["name"], "input": block.get("input", {})})
                elif block.get("type") == "text":
                    response += block["text"] + "\n"
        elif event.get("type") == "result":
            meta = event
            if isinstance(event.get("result"), str):
                response += event["result"]
    meta["_host_returncode"] = completed.returncode
    meta["_host_error"] = completed.stderr.strip()
    meta["_host_model"] = model or HOST_MODELS["claude-code"]
    return response, tools, meta


def run_codex(prompt: str, cwd: Path, timeout: int) -> tuple[str, list[dict], dict]:
    command = [
        "codex", "exec", prompt, "--json", "--sandbox", "read-only",
        "--model", HOST_MODELS["codex"],
        "--skip-git-repo-check", "--ephemeral", "-C", str(cwd),
    ]
    completed = subprocess.run(
        command, cwd=cwd, text=True, capture_output=True, timeout=timeout,
        stdin=subprocess.DEVNULL, env=environment(),
    )
    events = []
    for line in completed.stdout.splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    tools, response, meta = [], "", {}
    for event in events:
        if event.get("type") == "turn.completed":
            meta = event
            continue
        if event.get("type") != "item.completed":
            continue
        item = event.get("item", {})
        kind = item.get("type", "")
        if kind == "agent_message":
            response += str(item.get("text", "")) + "\n"
        elif kind in {"command_execution", "file_change", "mcp_tool_call", "web_search"}:
            tools.append({"name": kind, "input": item})
    meta["_host_returncode"] = completed.returncode
    meta["_host_error"] = completed.stderr.strip()
    meta["_host_model"] = HOST_MODELS["codex"]
    return response, tools, meta


def measure(tools: list[dict], response: str) -> dict:
    """Derive telemetry from the host's own trace. No judgement here."""
    names = [tool["name"] for tool in tools]
    blob = json.dumps(tools)
    commands = " ".join(
        str(tool["input"].get("command", "")) for tool in tools if isinstance(tool.get("input"), dict)
    )
    references = sorted({
        name for name in (path.name for path in (KERNEL / "references").glob("*.md"))
        if name in blob
    })
    activations = sum(
        1 for tool in tools
        if tool["name"] in {"Skill", "skill"} and "braids" in json.dumps(tool.get("input", {})).lower()
    )
    # Codex reports skill use through its shell/tool trace rather than a Skill tool.
    if not activations and ("skills/braids/SKILL.md" in blob or "skills/braids" in commands):
        activations = 1
    return {
        "activations": activations,
        "references_loaded": references,
        "files_read": sum(1 for name in names if name in {"Read", "read_file"})
                      + sum(commands.count(verb) for verb in ("cat ", "sed -n", "head -", "tail -")),
        "tool_calls": len(tools),
        "research_calls": sum(1 for name in names if name in {"WebSearch", "WebFetch", "web_search"}),
        "subagents": sum(1 for name in names if name in {"Task", "spawn_agent"}),
        "retries": 0,
        "verification_iterations": sum(1 for tool in tools if "test" in json.dumps(tool.get("input", {})).lower()),
        "clarifications": sum(1 for name in names if name == "AskUserQuestion"),
        "rework_attempts": 0,
    }


def judge(case: dict, response: str, timeout: int) -> dict:
    prompt = JUDGE_PROMPT.format(
        prompt=case["prompt"],
        response=response[:24000],
        expected="\n".join(f"- {item}" for item in case["expected_properties"]),
        forbidden="\n".join(f"- {item}" for item in case["forbidden_properties"]) or "- (none)",
    )
    completed = subprocess.run(
        ["claude", "-p", prompt, "--model", JUDGE_MODEL, "--safe-mode",
         "--tools", "", "--output-format", "json", "--strict-mcp-config"],
        text=True, capture_output=True, timeout=timeout, stdin=subprocess.DEVNULL, env=environment(),
    )
    try:
        verdict = parse_json_block(json.loads(completed.stdout).get("result", "")) or {}
    except (json.JSONDecodeError, AttributeError):
        verdict = {}
    allowed = set(case["expected_properties"]) | set(case["forbidden_properties"])
    return {
        "depth": verdict.get("depth", "unknown"),
        "present": sorted(set(verdict.get("present", [])) & allowed),
    }


def run_case(case: dict, host: str, plugin: Path | None, timeout: int,
             default_fixture: str | None = None, artifact_path: Path | None = None) -> dict:
    started = datetime.now(timezone.utc)
    began = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="braids-eval-") as directory:
        workspace = Path(directory)
        # The trigger corpus declares fixture: null, but its prompts presuppose a
        # repository ("our shared retry helper"). Run those in an empty directory
        # and the model spends every turn hunting the filesystem for code instead
        # of deciding, which measures nothing. --default-fixture supplies one
        # shared context for all of them so the comparison stays even.
        fixture = case.get("fixture") or default_fixture
        if fixture:
            shutil.copytree(ROOT / fixture, workspace, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        trigger_only = case["id"].startswith("TR-")
        prompt = case["prompt"] if trigger_only else case["prompt"] + ENVELOPE
        if host == "claude-code":
            response, tools, meta = run_claude(prompt, workspace, plugin, timeout)
        else:
            if plugin:
                shutil.copytree(KERNEL, workspace / ".agents/skills/braids",
                                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            response, tools, meta = run_codex(prompt, workspace, timeout)

    if artifact_path:
        artifact_path.parent.mkdir(parents=True, exist_ok=True)
        artifact_path.write_text(json.dumps({
            "case_id": case["id"], "host": host, "prompt": prompt,
            "response": response, "tools": tools, "host_metadata": meta,
        }, indent=2) + "\n", encoding="utf-8")

    telemetry = measure(tools, response)
    telemetry["wall_time_ms"] = round((time.monotonic() - began) * 1000)
    usage = meta.get("usage") or meta.get("info", {}).get("total_token_usage") or {}
    telemetry["input_tokens"] = usage.get("input_tokens")
    telemetry["output_tokens"] = usage.get("output_tokens")

    host_failed = bool(
        meta.get("_host_returncode")
        or meta.get("is_error")
        or meta.get("terminal_reason") == "api_error"
    )
    verdict = (
        judge(case, response, timeout)
        if plugin and not host_failed and not trigger_only
        else {"depth": "not-applicable" if trigger_only else "unknown", "present": []}
    )
    forbidden = set(case["forbidden_properties"]) & set(verdict["present"])
    observed = sorted(set(verdict["present"]) - forbidden)
    return {
        "case_id": case["id"],
        "fixture_hash": case.get("fixture_hash"),
        "host": host,
        "host_version": HOST_VERSIONS[host],
        "model": meta.get("_host_model", HOST_MODELS[host]),
        "model_version": None,
        "core_version": "3.0.0",
        "adapter_version": "0.1.0-dev.2" if plugin else None,
        "available_tools": sorted({tool["name"] for tool in tools}),
        "started_at": started.isoformat(),
        "result": "blocked" if host_failed or not response.strip() else "pass",
        "triggered": None if host_failed else telemetry["activations"] > 0,
        "observed_depth": verdict["depth"] if verdict["depth"] in
                          {"D0", "D1", "D2", "D3", "D4", "not-applicable"} else "unknown",
        "observed_properties": observed,
        "violations": sorted(forbidden) + (
            [f"host error: {meta.get('api_error_status') or meta.get('_host_returncode')}"] if host_failed else []
        ),
        "claim_evidence_coverage": None,
        "telemetry": telemetry,
    }


HOST_VERSIONS = {"claude-code": "2.1.248", "codex": "0.150.1"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", required=True, choices=sorted(HOST_VERSIONS))
    parser.add_argument("--cases", type=Path, action="append", required=True, help="A cases.jsonl file; repeatable.")
    parser.add_argument("--only", action="append", help="Restrict to these case ids.")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--baseline", action="store_true", help="Run without Braids, for the comparison arm.")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--repetitions", type=int, default=1,
                        help="Run each selected case this many times (development trigger protocol: 3).")
    parser.add_argument("--default-fixture", help="Fixture to use for cases that declare none.")
    parser.add_argument("--resume", action="store_true",
                        help="Append only missing repetitions to an existing output file.")
    parser.add_argument("--artifacts-dir", type=Path,
                        help="Write auditable raw host responses and tool traces here.")
    args = parser.parse_args()
    if args.repetitions < 1:
        parser.error("--repetitions must be at least 1")

    cases = [
        case
        for path in args.cases
        for case in (json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
        if not args.only or case["id"] in args.only
    ]
    if not cases:
        print("ERROR: no cases selected", file=sys.stderr)
        return 1

    plugin = None if args.baseline else ROOT / "dist" / args.host
    if plugin and not plugin.is_dir():
        print(f"ERROR: build the adapter first: {plugin}", file=sys.stderr)
        return 1

    completed: Counter[str] = Counter()
    if args.resume and args.out.exists():
        completed.update(
            record["case_id"]
            for line in args.out.read_text(encoding="utf-8").splitlines()
            if line.strip()
            for record in [json.loads(line)]
            if record.get("host") == args.host and record.get("result") == "pass"
        )
    remaining = [
        case for case in cases
        for _ in range(max(0, args.repetitions - completed[case["id"]]))
    ]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if args.resume else "w"
    failures = 0
    seen = Counter(completed)
    with args.out.open(mode, encoding="utf-8") as handle:
        total = len(remaining)
        for index, case in enumerate(remaining, 1):
            print(f"[{index}/{total}] {args.host} {case['id']}", flush=True)
            seen[case["id"]] += 1
            artifact = (
                args.artifacts_dir / args.host / f"{case['id']}-{seen[case['id']]:02d}.json"
                if args.artifacts_dir else None
            )
            try:
                record = run_case(case, args.host, plugin, args.timeout, args.default_fixture, artifact)
            except subprocess.TimeoutExpired:
                print(f"  timeout after {args.timeout}s", flush=True)
                failures += 1
                continue
            handle.write(json.dumps(record) + "\n")
            handle.flush()
            print(f"  triggered={record['triggered']} depth={record['observed_depth']} "
                  f"props={len(record['observed_properties'])} violations={record['violations']}", flush=True)
            failures += record["result"] != "pass"
    print(f"wrote {args.out} ({len(remaining)} new runs)")
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
