#!/usr/bin/env python3
"""Measure the static context budget of the Braids kernel against docs/24 ceilings.

This measures only what is deterministic: how much text each disclosure stage can
possibly cost. Per-run metrics in docs/24 (tool calls, rework ratio, research
marginal value) need graded host runs and are not produced here.

Token counts are a chars/4 ESTIMATE, not a tokenizer result. The estimator is
calibrated against the one host-authoritative measurement available:
`claude plugin details braids` on Claude Code 2.1.248 reported ~280 always-on and
~2.8k on-invoke tokens.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KERNEL = ROOT / "skills/braids"
CHARS_PER_TOKEN = 4

# docs/24: ecosystem guidance, restated here as the gate Braids holds itself to.
CEILINGS = {
    "metadata_tokens": 250,
    "kernel_body_tokens": 5000,
    "kernel_body_lines": 500,
    "reference_tokens": 1500,
}
# Host-measured, not estimated. Recorded so drift is visible when the kernel changes.
OBSERVED = {
    # `claude plugin details braids`, methodology 3.0.0 with the widened description.
    "claude-code@2.1.248": {"always_on_tokens": 280, "on_invoke_tokens": 2800},
}


def estimate(text: str) -> int:
    return round(len(text) / CHARS_PER_TOKEN)


def split_skill() -> tuple[str, str]:
    text = (KERNEL / "SKILL.md").read_text(encoding="utf-8")
    frontmatter, body = text[4:].split("\n---\n", 1)
    return frontmatter, body


def measure() -> dict:
    frontmatter, body = split_skill()
    references = {
        path.name: estimate(path.read_text(encoding="utf-8"))
        for path in sorted((KERNEL / "references").glob("*.md"))
    }
    metadata = estimate(frontmatter)
    kernel = estimate(body)
    return {
        "estimator": f"chars/{CHARS_PER_TOKEN}",
        "metadata_tokens": metadata,
        "kernel_body_tokens": kernel,
        "kernel_body_lines": len(body.splitlines()),
        "references": references,
        "stages": {
            "dormant": metadata,
            "activated_no_reference": metadata + kernel,
            "activated_one_reference": metadata + kernel + max(references.values()),
            "activated_all_references": metadata + kernel + sum(references.values()),
        },
        "observed_host_measurements": OBSERVED,
    }


def check(report: dict) -> list[str]:
    errors = []
    for key in ("metadata_tokens", "kernel_body_tokens", "kernel_body_lines"):
        if report[key] > CEILINGS[key]:
            errors.append(f"{key} is {report[key]}, above the docs/24 ceiling of {CEILINGS[key]}")
    for name, tokens in report["references"].items():
        if tokens > CEILINGS["reference_tokens"]:
            errors.append(f"reference {name} is {tokens} tokens, above the {CEILINGS['reference_tokens']} ceiling")
    # Progressive disclosure only pays off if a routed reference costs less than the kernel.
    if report["references"] and max(report["references"].values()) >= report["kernel_body_tokens"]:
        errors.append("a single reference is as large as the kernel; routing buys nothing")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit the raw measurement.")
    args = parser.parse_args()

    report = measure()
    errors = check(report)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        stages = report["stages"]
        print(f"estimator: {report['estimator']} (estimate, not a tokenizer)")
        print(f"dormant metadata          {stages['dormant']:>6} tok")
        print(f"activated, no reference   {stages['activated_no_reference']:>6} tok  ({report['kernel_body_lines']} lines)")
        print(f"activated, one reference  {stages['activated_one_reference']:>6} tok  (worst single route)")
        print(f"activated, all references {stages['activated_all_references']:>6} tok  (never a normal path)")
        for name, tokens in report["references"].items():
            print(f"  reference {name:<28} {tokens:>5} tok")
        for host, values in OBSERVED.items():
            print(f"host-measured {host}: {values['always_on_tokens']} always-on, {values['on_invoke_tokens']} on-invoke")

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
