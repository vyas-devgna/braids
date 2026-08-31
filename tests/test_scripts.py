import importlib.util
import tempfile
import unittest
from pathlib import Path


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
        # Progressive disclosure is the product requirement, not an aspiration:
        # dormant cost must stay a small fraction of the activated cost.
        self.assertLess(report["stages"]["dormant"] * 5, report["stages"]["activated_no_reference"])

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


if __name__ == "__main__":
    unittest.main()
