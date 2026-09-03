#!/usr/bin/env python3
"""Measure the static context budget of the Braids kernel against docs/24 ceilings.

This measures only what is deterministic: how much text each disclosure stage can
possibly cost. Per-run metrics in docs/24 (tool calls, rework ratio, research
marginal value) need graded host runs and are not produced here.

Token counts are a chars/4 ESTIMATE, not a tokenizer result. The estimator is
calibrated against the one current host projection available:
`claude plugin details braids` on Claude Code 2.1.248 reported ~870 always-on
across the seven skills and ~3.9k when the 3.1.0 core skill fires.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
KERNEL = SKILLS / "braids"
CHARS_PER_TOKEN = 4

# docs/24: ecosystem guidance, restated here as the gate Braids holds itself to.
CEILINGS = {
    # docs/24 states the guidance per *discovered skill*, so the per-skill figure is
    # the real gate; the total is bounded separately because the user pays the sum
    # on every turn whether or not any skill fires.
    "per_skill_metadata_tokens": 250,
    # The kernel's description is the activation classifier for the whole set, so it
    # carries behavioural clauses the six satellites do not need. Measured runs put
    # activation on high-severity decision cases at 3/8 with the shorter description;
    # the clauses that fix that do not fit in 250. The binding constraint is the total
    # paid every turn, which stays well under `metadata_tokens`. See
    # docs/decisions/0004-kernel-description-allowance.md.
    "kernel_metadata_tokens": 280,
    "metadata_tokens": 1000,
    "kernel_body_tokens": 5000,
    "kernel_body_lines": 500,
    "reference_tokens": 1500,
}
# Host-projected, not measured runtime usage. Recorded so drift is visible.
OBSERVED = {
    # `claude --plugin-dir . plugin details braids`, 2026-09-03, methodology 3.1.0.
    # Per-component always-on: braids 330, review 160, audit 80, depth 80, risk 80,
    # claims 70, help 60. On-invoke: braids 3.9k, depth 1.2k, help 960, audit 800,
    # review 790, claims 750, risk 700.
    "claude-code@2.1.248/methodology-3.1.0": {
        "always_on_tokens": 870, "on_invoke_tokens": 3900,
    },
}


def estimate(text: str) -> int:
    return round(len(text) / CHARS_PER_TOKEN)


def split_skill(skill: Path = KERNEL) -> tuple[str, str]:
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    frontmatter, body = text[4:].split("\n---\n", 1)
    return frontmatter, body


def shipped_skills() -> list[Path]:
    return sorted(p for p in SKILLS.iterdir() if (p / "SKILL.md").is_file())


def measure() -> dict:
    frontmatter, body = split_skill()
    references = {
        path.name: estimate(path.read_text(encoding="utf-8"))
        for path in sorted((KERNEL / "references").glob("*.md"))
    }
    # Every shipped skill advertises its metadata on every turn, so dormant cost
    # is the sum across the whole set, not the kernel's share of it.
    per_skill = {skill.name: estimate(split_skill(skill)[0]) for skill in shipped_skills()}
    metadata = sum(per_skill.values())
    kernel = estimate(body)
    return {
        "estimator": f"chars/{CHARS_PER_TOKEN}",
        "skills": per_skill,
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
    for name, tokens in report["skills"].items():
        key = "kernel_metadata_tokens" if name == "braids" else "per_skill_metadata_tokens"
        if tokens > CEILINGS[key]:
            errors.append(f"skill {name} advertises {tokens} metadata tokens, "
                          f"above the {CEILINGS[key]} ceiling")
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
        print(f"dormant metadata          {stages['dormant']:>6} tok  ({len(report['skills'])} skills, paid every turn)")
        for name, tokens in report["skills"].items():
            print(f"  skill {name:<28} {tokens:>5} tok")
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
