#!/usr/bin/env python3
"""Validate Braids eval corpora, fixtures, and optional observed run results."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASE_FILES = tuple(sorted((ROOT / "evals").glob("*/cases.jsonl")))
PROJECT = json.loads((ROOT / "braids.json").read_text(encoding="utf-8"))
CURRENT_CORE = PROJECT["methodology_version"]
CURRENT_PACKAGE = PROJECT["package_version"]
REQUIREMENTS = {f"R-{number:03d}" for number in range(1, 31)} | {"NFR-10"}
CASE_REQUIRED = {
    "id", "category", "partition", "requirement_ids", "module_owners", "fixture", "fixture_hash",
    "prompt", "expected_trigger", "expected_depth", "expected_properties", "forbidden_properties",
    "hidden_checks", "cost_budget_class",
}


def load_jsonl(path: Path) -> list[dict]:
    records = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path.relative_to(ROOT)}:{number}: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path.relative_to(ROOT)}:{number}: expected object")
        records.append(value)
    return records


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
            continue
        digest.update(str(path.relative_to(root)).encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def check_cases(cases: list[dict]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    covered: set[str] = set()
    for case in cases:
        case_id = str(case.get("id", "<missing>"))
        missing = CASE_REQUIRED - set(case)
        if missing:
            errors.append(f"{case_id}: missing {sorted(missing)}")
        if case_id in seen:
            errors.append(f"duplicate case id: {case_id}")
        seen.add(case_id)
        covered.update(case.get("requirement_ids", []))
        if not case.get("expected_properties"):
            errors.append(f"{case_id}: expected_properties cannot be empty")
        if case.get("expected_depth") == "D0" and case.get("cost_budget_class") != "tiny":
            errors.append(f"{case_id}: D0 must use the tiny budget class")
        fixture = case.get("fixture")
        expected_hash = case.get("fixture_hash")
        if fixture is None:
            if expected_hash is not None:
                errors.append(f"{case_id}: fixture_hash requires a fixture")
            continue
        path = (ROOT / fixture).resolve()
        try:
            path.relative_to(ROOT)
        except ValueError:
            errors.append(f"{case_id}: fixture escapes repository")
            continue
        if not path.is_dir():
            errors.append(f"{case_id}: missing fixture {fixture}")
        elif tree_hash(path) != expected_hash:
            errors.append(f"{case_id}: fixture hash is stale")

    missing_requirements = REQUIREMENTS - covered
    if missing_requirements:
        errors.append(f"requirements without eval coverage: {sorted(missing_requirements)}")

    # A case missing `id` or `expected_trigger` is already reported above. Filter it
    # out rather than raising here, so a malformed corpus yields the full error list
    # instead of a traceback from the gate that guards releases.
    triggers = [
        case for case in cases
        if str(case.get("id", "")).startswith("TR-") and "expected_trigger" in case and "partition" in case
    ]
    positives = [case for case in triggers if case["expected_trigger"] == "yes"]
    negatives = [case for case in triggers if case["expected_trigger"] == "no"]
    if len(positives) < 30 or len(negatives) < 30:
        errors.append(f"trigger corpus needs >=30 positive and negative cases, got {len(positives)}/{len(negatives)}")
    for partition in ("train", "validation", "holdout"):
        selected = [case for case in triggers if case.get("partition") == partition]
        if not any(case["expected_trigger"] == "yes" for case in selected) or not any(case["expected_trigger"] == "no" for case in selected):
            errors.append(f"trigger partition {partition} is not balanced")
    return errors


def full_schema_check(cases: list[dict], results: list[dict]) -> list[str]:
    errors: list[str] = []
    installed = shutil_which("check-jsonschema")
    if installed:
        prefix = [installed]
    elif shutil_which("uvx"):
        prefix = ["uvx", "--from", "check-jsonschema==0.38.0", "check-jsonschema"]
    else:
        return ["--full-schema requires check-jsonschema 0.38.0 or uvx"]
    with tempfile.TemporaryDirectory(prefix="braids-schema-") as directory:
        temp = Path(directory)
        case_paths = []
        for index, case in enumerate(cases):
            path = temp / f"case-{index}.json"
            path.write_text(json.dumps(case), encoding="utf-8")
            case_paths.append(str(path))
        command = [*prefix, "--schemafile", str(ROOT / "schemas/evaluation-case.schema.json"), *case_paths]
        completed = subprocess.run(command, text=True, capture_output=True)
        if completed.returncode:
            errors.append(completed.stdout + completed.stderr)
        if results:
            result_paths = []
            for index, result in enumerate(results):
                path = temp / f"result-{index}.json"
                path.write_text(json.dumps(result), encoding="utf-8")
                result_paths.append(str(path))
            command = [*prefix, "--schemafile", str(ROOT / "schemas/eval-run.schema.json"), *result_paths]
            completed = subprocess.run(command, text=True, capture_output=True)
            if completed.returncode:
                errors.append(completed.stdout + completed.stderr)
    return errors


def shutil_which(name: str) -> str | None:
    from shutil import which
    return which(name)


def run_fixture_tests() -> list[str]:
    errors = []
    for fixture in sorted((ROOT / "fixtures").iterdir()):
        if not fixture.is_dir() or fixture.name in {"contracts", "dependency-selection"}:
            continue
        if not any(fixture.rglob("test_*.py")):
            continue
        completed = subprocess.run([sys.executable, "-m", "unittest", "discover", "-q"], cwd=fixture, text=True, capture_output=True)
        if completed.returncode:
            errors.append(f"{fixture.relative_to(ROOT)}:\n{completed.stdout}{completed.stderr}")
    return errors


def grade_results(cases: list[dict], results: list[dict], release: bool) -> list[str]:
    errors: list[str] = []
    by_id = {case["id"]: case for case in cases}
    runs: dict[str, list[dict]] = defaultdict(list)
    identities: set[tuple] = set()
    for result in results:
        case_id = result.get("case_id")
        if case_id not in by_id:
            errors.append(f"result references unknown case {case_id}")
            continue
        runs[case_id].append(result)
        case = by_id[case_id]
        if result.get("fixture_hash") != case.get("fixture_hash"):
            errors.append(f"{case_id}: result fixture hash differs from the case")
        identity = (case_id, result.get("host"), result.get("started_at"))
        if identity in identities:
            errors.append(f"{case_id}: duplicate run record for {result.get('host')} at {result.get('started_at')}")
        identities.add(identity)
        if result.get("result") != "pass":
            errors.append(f"{case_id}: run is {result.get('result', 'missing')}")
            continue
        if case_id.startswith("TR-"):
            expected_trigger = case["expected_trigger"]
            if expected_trigger in {"yes", "no"} and result.get("triggered") is not (expected_trigger == "yes"):
                errors.append(f"{case_id}: trigger result differs from expectation")
            continue
        observed = set(result.get("observed_properties", []))
        expected = set(case["expected_properties"])
        forbidden = set(case["forbidden_properties"])
        if not expected <= observed:
            errors.append(f"{case_id}: missing observed properties {sorted(expected - observed)}")
        if forbidden & observed:
            errors.append(f"{case_id}: observed forbidden properties {sorted(forbidden & observed)}")
        if case["expected_depth"] not in {"variable", "not-applicable"} and result.get("observed_depth") != case["expected_depth"]:
            errors.append(f"{case_id}: expected {case['expected_depth']}, got {result.get('observed_depth')}")
        expected_trigger = case["expected_trigger"]
        if expected_trigger in {"yes", "no"} and result.get("triggered") is not (expected_trigger == "yes"):
            errors.append(f"{case_id}: trigger result differs from expectation")

    trigger_cases = [case for case in cases if case["id"].startswith("TR-")]
    complete_cohorts: set[tuple] = set()
    if release:
        release_runs: dict[str, list[dict]] = defaultdict(list)
        for case in trigger_cases:
            for run in runs[case["id"]]:
                if run.get("core_version") != CURRENT_CORE:
                    errors.append(
                        f"{case['id']}: release run uses core {run.get('core_version')}, expected {CURRENT_CORE}"
                    )
                    continue
                if run.get("adapter_version") != CURRENT_PACKAGE:
                    errors.append(
                        f"{case['id']}: release run uses adapter {run.get('adapter_version')}, expected {CURRENT_PACKAGE}"
                    )
                    continue
                if run.get("result") == "pass":
                    release_runs[case["id"]].append(run)

        cohorts = {
            (run.get("host"), run.get("host_version"), run.get("model"), run.get("model_version"))
            for case_runs in release_runs.values() for run in case_runs
        }
        complete_cohorts = {
            cohort for cohort in cohorts
            if all(sum(
                (run.get("host"), run.get("host_version"), run.get("model"), run.get("model_version")) == cohort
                for run in release_runs[case["id"]]
            ) >= 5 for case in trigger_cases)
        }
        if not complete_cohorts:
            errors.append("release trigger cases require five current-version runs in one comparable cohort")

    observed_triggers = [
        result for case in trigger_cases for result in runs[case["id"]]
        if result.get("result") == "pass"
    ]
    groups = {"all runs": observed_triggers}
    if release:
        groups = {
            "/".join(str(part) for part in cohort): [
                run for run in observed_triggers
                if run.get("core_version") == CURRENT_CORE
                and run.get("adapter_version") == CURRENT_PACKAGE
                and (run.get("host"), run.get("host_version"), run.get("model"), run.get("model_version")) == cohort
            ]
            for cohort in complete_cohorts
        }
    for label, selected in groups.items():
        positives = [result for result in selected if by_id[result["case_id"]]["expected_trigger"] == "yes"]
        negatives = [result for result in selected if by_id[result["case_id"]]["expected_trigger"] == "no"]
        suffix = f" for {label}" if release else ""
        if positives and sum(result["triggered"] is True for result in positives) / len(positives) < 0.90:
            errors.append(f"positive trigger rate is below 0.90{suffix}")
        if negatives and sum(result["triggered"] is True for result in negatives) / len(negatives) > 0.10:
            errors.append(f"near-miss false-trigger rate exceeds 0.10{suffix}")
    return errors


def summarize(cases: list[dict], results: list[dict]) -> str:
    """Report what the runs actually showed, per host, without asserting a threshold."""
    by_id = {case["id"]: case for case in cases}
    hosts: dict[str, list[dict]] = defaultdict(list)
    for result in results:
        if result.get("case_id") in by_id:
            hosts[result.get("host", "unknown")].append(result)

    lines = []
    for host, runs in sorted(hosts.items()):
        successful = [run for run in runs if run.get("result") == "pass"]
        blocked = len(runs) - len(successful)
        graded = [run for run in successful if by_id[run["case_id"]]["expected_trigger"] in {"yes", "no"}]
        positives = [r for r in graded if by_id[r["case_id"]]["expected_trigger"] == "yes"]
        negatives = [r for r in graded if by_id[r["case_id"]]["expected_trigger"] == "no"]
        decision_runs = [r for r in successful if not r["case_id"].startswith("TR-")]
        depth_cases = [
            r for r in decision_runs
            if by_id[r["case_id"]]["expected_depth"] not in {"variable", "not-applicable"}
        ]
        depth_hits = [r for r in depth_cases if r.get("observed_depth") == by_id[r["case_id"]]["expected_depth"]]
        expected_total = sum(len(by_id[r["case_id"]]["expected_properties"]) for r in decision_runs)
        expected_seen = sum(
            len(set(by_id[r["case_id"]]["expected_properties"]) & set(r.get("observed_properties", [])))
            for r in decision_runs
        )
        violations = [r for r in runs if r.get("violations")]

        def rate(hit: int, total: int) -> str:
            return f"{hit}/{total} ({hit / total:.0%})" if total else "n/a"

        lines.append(f"{host}: {len(runs)} runs")
        if blocked:
            lines.append(f"  blocked/error runs          {blocked}")
        lines.append(f"  activated when expected     {rate(sum(r['triggered'] is True for r in positives), len(positives))}")
        lines.append(f"  stayed dormant when expected {rate(sum(r['triggered'] is not True for r in negatives), len(negatives))}")
        lines.append(f"  depth matched                {rate(len(depth_hits), len(depth_cases))}")
        lines.append(f"  expected properties shown    {rate(expected_seen, expected_total)}")
        lines.append(f"  runs with a forbidden property {len(violations)}"
                     + (f" ({', '.join(sorted(r['case_id'] for r in violations))})" if violations else ""))
        tokens = [r["telemetry"].get("input_tokens") for r in runs if r["telemetry"].get("input_tokens")]
        if tokens:
            lines.append(f"  median input tokens         {sorted(tokens)[len(tokens) // 2]}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full-schema", action="store_true", help="Use pinned isolated check-jsonschema validation (may fetch the dev tool).")
    parser.add_argument("--fixture-tests", action="store_true", help="Run visible baseline fixture tests.")
    parser.add_argument("--results", type=Path, help="Grade observed host/model run JSONL.")
    parser.add_argument("--release", action="store_true", help="Apply release-run count thresholds.")
    parser.add_argument("--summary", action="store_true", help="Print observed per-host rates alongside grading.")
    args = parser.parse_args()

    try:
        cases = [case for path in CASE_FILES for case in load_jsonl(path)]
        results = load_jsonl(args.results) if args.results else []
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    errors = check_cases(cases)
    if args.fixture_tests:
        errors.extend(run_fixture_tests())
    if args.full_schema:
        errors.extend(full_schema_check(cases, results))
    if results:
        errors.extend(grade_results(cases, results, args.release))
    elif args.release:
        errors.append("--release requires --results")

    if args.summary and results:
        print(summarize(cases, results))

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"ok: {len(cases)} eval cases; deterministic corpus checks only" + ("; observed results graded" if results else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
