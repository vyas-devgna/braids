import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


skill_validator = load("skill_validator", ROOT / "skills/braids/scripts/validate_braids.py")
capabilities = load("capabilities", ROOT / "skills/braids/scripts/inspect_capabilities.py")
eval_runner = load("eval_runner", ROOT / "scripts/run_evals.py")
adapters = load("adapters", ROOT / "scripts/build_adapters.py")
budget = load("budget", ROOT / "scripts/measure_budget.py")
host_runner = load("host_runner", ROOT / "scripts/run_host_evals.py")


class ScriptTests(unittest.TestCase):
    def test_current_skill_is_valid(self):
        self.assertEqual(skill_validator.validate(ROOT / "skills/braids"), [])

    def test_skill_validator_rejects_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "bad-skill"
            root.mkdir()
            (root / "SKILL.md").write_text(
                "---\nname: bad-skill\ndescription: Validate a bad fixture.\n---\n\n[escape](../secret.md)\n",
                encoding="utf-8",
            )
            self.assertIn("reference escapes skill root: ../secret.md", skill_validator.validate(root))

    def test_capability_probe_does_not_invent_enforcement(self):
        value = capabilities.profile("test", "1", "local")
        self.assertEqual(value["hooks"]["availability"], "unknown")
        self.assertEqual(value["enforcement"], [])
        self.assertEqual(value["execution"]["write"], "unknown")

    def test_adapters_are_consistent_with_canonical_metadata(self):
        values = adapters.canonical_values()
        for directory in sorted(p for p in adapters.ADAPTERS.iterdir() if p.is_dir()):
            with self.subTest(adapter=directory.name):
                self.assertEqual(adapters.check_adapter(directory, values), [])

    def test_adapter_cannot_claim_a_status_its_evidence_does_not_support(self):
        import json

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "fake-host"
            root.mkdir()
            (root / "capabilities.json").write_text(
                json.dumps(capabilities.profile("fake-host", None, "local")), encoding="utf-8"
            )
            adapter = {
                "schema_version": "1.0", "id": "fake-host", "adapter_version": "0.1.0",
                "methodology_version": adapters.canonical_values()["methodology_version"],
                "status": "supported", "tested_host_versions": [], "surfaces": ["local"],
                "capabilities_file": "./capabilities.json", "guard_mode_default": False,
                "install": ["copy the skill"], "disable": ["delete the skill"],
                "uninstall": ["delete the skill"],
                "conformance": [f"{check}: not-exercised — never run" for check in adapters.CONFORMANCE_CHECKS],
                "source_revalidated_at": None, "limitations": [],
                "package": {"skill_target": "skills/braids", "manifests": []},
            }
            (root / "adapter.json").write_text(json.dumps(adapter), encoding="utf-8")
            errors = adapters.check_adapter(root, adapters.canonical_values())
        self.assertTrue(any("requires discovery to pass" in error for error in errors), errors)
        self.assertTrue(any("requires a primary-source revalidation date" in error for error in errors), errors)

    def test_context_budget_stays_within_the_documented_ceilings(self):
        report = budget.measure()
        self.assertEqual(budget.check(report), [])
        # Progressive disclosure is the product requirement, not an aspiration.
        # Braids now ships several skills, so dormant cost is the sum every user
        # pays on every turn whether or not any of them fires. The invariant that
        # matters: having Braids installed must cost well under using it once.
        # This fails if roughly five more skills are added without trimming.
        self.assertLess(report["stages"]["dormant"] * 3, report["stages"]["activated_no_reference"])
        # And no single skill may dominate the standing cost.
        for name, tokens in report["skills"].items():
            with self.subTest(skill=name):
                self.assertLessEqual(tokens, budget.CEILINGS["per_skill_metadata_tokens"])

    def test_kernel_keeps_its_safety_invariants(self):
        """These sentences are the kernel's security posture; losing one is a silent regression."""
        text = (ROOT / "skills/braids/SKILL.md").read_text(encoding="utf-8")
        for phrase in (
            "untrusted evidence",           # repository/web/tool text never outranks the user or host
            "Do not place secrets",         # no secrets or private source in external queries
            "decision authority and implementation authority separately",
            "Never infer a capability or enforcement guarantee from a product name",
            "request authorization before writing",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_eval_corpus_is_complete(self):
        cases = [case for path in eval_runner.CASE_FILES for case in eval_runner.load_jsonl(path)]
        self.assertEqual(eval_runner.check_cases(cases), [])

    def test_host_error_is_blocked_not_passed(self):
        case = eval_runner.load_jsonl(ROOT / "evals/kernel/cases.jsonl")[0]
        failed = ("rate limited", [], {
            "_host_returncode": 1,
            "_host_error": "limit",
            "is_error": True,
            "api_error_status": 429,
            "usage": {"input_tokens": 0, "output_tokens": 0},
        })
        with patch.object(host_runner, "run_claude", return_value=failed), \
             patch.object(host_runner, "judge") as judge:
            result = host_runner.run_case(case, "claude-code", ROOT, 1)
        self.assertEqual(result["result"], "blocked")
        self.assertIsNone(result["triggered"])
        self.assertEqual(result["violations"], ["host error: 429"])
        judge.assert_not_called()

    def test_listing_skill_files_is_not_an_activation(self):
        tools = [{"name": "command_execution", "input": {
            "command": "rg --files -uu",
            "aggregated_output": ".agents/skills/braids/SKILL.md\n",
        }}]
        self.assertEqual(host_runner.measure(tools, "")["activations"], 0)

    def test_reading_the_skill_is_an_activation(self):
        tools = [{"name": "command_execution", "input": {
            "command": "/usr/bin/bash -lc \"sed -n '1,220p' .agents/skills/braids/SKILL.md\"",
        }}]
        self.assertEqual(host_runner.measure(tools, "")["activations"], 1)

    def test_trigger_grading_does_not_require_decision_judgement(self):
        case = next(
            case for case in eval_runner.load_jsonl(ROOT / "evals/trigger/cases.jsonl")
            if case["expected_trigger"] == "yes"
        )
        result = {"case_id": case["id"], "host": "test", "result": "pass", "triggered": True,
                  "observed_depth": "not-applicable", "observed_properties": [], "violations": [],
                  "telemetry": {"input_tokens": None}}
        self.assertEqual(eval_runner.grade_results([case], [result], False), [])

    def test_blocked_trigger_run_fails_without_distorting_rates(self):
        case = next(
            case for case in eval_runner.load_jsonl(ROOT / "evals/trigger/cases.jsonl")
            if case["expected_trigger"] == "yes"
        )
        result = {"case_id": case["id"], "host": "test", "result": "blocked", "triggered": None,
                  "observed_depth": "not-applicable", "observed_properties": [], "violations": [],
                  "telemetry": {"input_tokens": None}}
        self.assertEqual(eval_runner.grade_results([case], [result], False),
                         [f"{case['id']}: run is blocked"])

    def test_skill_validator_rejects_unquotable_frontmatter(self):
        """An unquoted scalar holding ": " is invalid YAML and breaks host discovery."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "braids"
            root.mkdir()
            (root / "SKILL.md").write_text(
                "---\nname: braids\ndescription: Right-size work. Triggers on: security, retry\n---\n\n# Braids\n",
                encoding="utf-8",
            )
            self.assertIn("frontmatter description contains ': ' and must be quoted",
                          skill_validator.validate(root))

    def test_trigger_summary_does_not_report_fake_decision_scores(self):
        case = next(
            case for case in eval_runner.load_jsonl(ROOT / "evals/trigger/cases.jsonl")
            if case["expected_trigger"] == "yes"
        )
        result = {"case_id": case["id"], "host": "test", "result": "pass", "triggered": True,
                  "observed_depth": "not-applicable", "observed_properties": [], "violations": [],
                  "telemetry": {"input_tokens": None}}
        summary = eval_runner.summarize([case], [result])
        self.assertIn("depth matched                n/a", summary)
        self.assertIn("expected properties shown    n/a", summary)


if __name__ == "__main__":
    unittest.main()
