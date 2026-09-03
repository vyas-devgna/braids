import importlib.util
import shutil
import subprocess
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
        """A capability is never an enforcement guarantee, whatever the probe sees."""
        with tempfile.TemporaryDirectory() as directory:
            with patch("pathlib.Path.cwd", return_value=Path(directory)):
                value = capabilities.profile("test", "1", "local")
        self.assertEqual(value["enforcement"], [])
        self.assertEqual(value["hooks"]["availability"], "unknown")
        self.assertEqual(value["hooks"]["events"], [])
        for field in ("delegation", "permissions", "skill_loading"):
            self.assertEqual(value[field], "unknown", f"{field} is not observable from the probe process")

    def test_every_reported_capability_carries_an_observation(self):
        """A value with no observation behind it is an assertion, which is what Braids forbids."""
        with tempfile.TemporaryDirectory() as directory:
            with patch("pathlib.Path.cwd", return_value=Path(directory)):
                value = capabilities.profile(None, None, None)
        observations = value["observations"]
        for field in ("host", "surface", "isolation", "network", "hooks", "persistent_instruction", "mcp"):
            self.assertIn(field, observations)
            self.assertTrue(observations[field].strip(), f"{field} reported with an empty observation")
        for group in ("execution", "code_intelligence"):
            for key, reported in value[group].items():
                if reported != "unknown":
                    self.assertIn(f"{group}.{key}", observations)

    def test_probe_detects_the_host_from_the_environment_not_a_product_name(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch("pathlib.Path.cwd", return_value=Path(directory)):
                with patch.dict("os.environ", {"CODEX_SANDBOX": "seatbelt"}, clear=True):
                    value = capabilities.profile(None, None, None)
        self.assertEqual(value["host"], "codex")
        self.assertEqual(value["isolation"], "sandbox")
        self.assertIn("CODEX_SANDBOX", value["observations"]["host"])

    def test_probe_reports_unknown_host_rather_than_guessing(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch("pathlib.Path.cwd", return_value=Path(directory)):
                with patch.dict("os.environ", {}, clear=True):
                    value = capabilities.profile(None, None, None)
        self.assertEqual(value["host"], "unknown")
        self.assertEqual(value["network"], "unknown")

    def test_probe_names_the_verification_commands_the_project_offers(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "go.mod").write_text("module x\n", encoding="utf-8")
            with patch("pathlib.Path.cwd", return_value=root):
                value = capabilities.profile(None, None, None)
        self.assertEqual(value["code_intelligence"]["tests"], "available")
        self.assertIn("go test ./...", value["observations"]["verification"])

    def test_probe_reads_configured_hooks_exactly(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".claude").mkdir()
            (root / ".claude/settings.json").write_text(
                '{"hooks": {"PreToolUse": [], "Stop": []}}', encoding="utf-8")
            with patch("pathlib.Path.cwd", return_value=root):
                value = capabilities.profile(None, None, None)
        self.assertEqual(value["hooks"]["availability"], "available")
        self.assertEqual(value["hooks"]["events"], ["PreToolUse", "Stop"])
        # Configured hooks still prove nothing about enforcement coverage.
        self.assertEqual(value["enforcement"], [])

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


class InstallerTests(unittest.TestCase):
    """The installer writes into a directory the user also owns.

    Every case here is a way to destroy work that is not ours to destroy.
    """

    node = shutil.which("node")

    def run_installer(self, workspace, *args):
        return subprocess.run(
            [self.node, str(ROOT / "scripts/install.mjs"), "agents", *args],
            cwd=workspace, text=True, capture_output=True, timeout=120,
        )

    def setUp(self):
        if not self.node:
            self.skipTest("node is not installed")
        self.workspace = Path(tempfile.mkdtemp(prefix="braids-install-test-"))
        self.skills = self.workspace / ".agents/skills"
        self.addCleanup(shutil.rmtree, self.workspace, ignore_errors=True)

    def write_foreign_skill(self, name):
        target = self.skills / name
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: \"A skill the user wrote themselves.\"\n---\n\nirreplaceable\n",
            encoding="utf-8",
        )
        return target / "SKILL.md"

    def test_install_then_uninstall_round_trips(self):
        self.assertEqual(self.run_installer(self.workspace).returncode, 0)
        self.assertTrue((self.skills / "braids/SKILL.md").is_file())
        self.assertEqual(self.run_installer(self.workspace, "--uninstall").returncode, 0)
        self.assertFalse((self.skills / "braids").exists())
        self.assertFalse((self.skills / ".braids-install.json").exists())

    def test_uninstall_never_deletes_a_skill_it_did_not_install(self):
        theirs = self.write_foreign_skill("braids-review")
        self.run_installer(self.workspace, "--uninstall")
        self.assertTrue(theirs.is_file(), "uninstall destroyed a user-authored skill")
        self.assertIn("irreplaceable", theirs.read_text(encoding="utf-8"))

    def test_uninstall_keeps_a_copy_the_user_edited(self):
        self.run_installer(self.workspace)
        edited = self.skills / "braids/SKILL.md"
        edited.write_text(edited.read_text(encoding="utf-8") + "\nlocal edit\n", encoding="utf-8")
        self.run_installer(self.workspace, "--uninstall")
        self.assertTrue(edited.is_file(), "uninstall destroyed local edits")
        self.assertIn("local edit", edited.read_text(encoding="utf-8"))

    def test_install_refuses_to_overwrite_a_foreign_skill_but_installs_the_rest(self):
        theirs = self.write_foreign_skill("braids-review")
        result = self.run_installer(self.workspace)
        self.assertIn("irreplaceable", theirs.read_text(encoding="utf-8"))
        self.assertIn("refusing", result.stderr)
        self.assertTrue((self.skills / "braids/SKILL.md").is_file(), "unrelated skills should still install")

    def test_force_overrides_the_refusal(self):
        theirs = self.write_foreign_skill("braids-review")
        self.assertEqual(self.run_installer(self.workspace, "--force").returncode, 0)
        self.assertNotIn("irreplaceable", theirs.read_text(encoding="utf-8"))

    def test_dry_run_writes_nothing(self):
        result = self.run_installer(self.workspace, "--dry-run")
        self.assertEqual(result.returncode, 0)
        self.assertIn("would install", result.stdout)
        self.assertFalse(self.skills.exists())

    def test_mistyped_flag_is_rejected_rather_than_installing(self):
        result = self.run_installer(self.workspace, "--uninstal")
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.skills.exists(), "a typo must not fall through to an install")

    def test_unknown_host_does_not_resolve_through_object_prototype(self):
        result = subprocess.run(
            [self.node, str(ROOT / "scripts/install.mjs"), "constructor"],
            cwd=self.workspace, text=True, capture_output=True, timeout=120,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("unknown host", result.stderr)

    def test_reinstall_over_our_own_clean_copy_is_allowed(self):
        self.run_installer(self.workspace)
        result = self.run_installer(self.workspace)
        self.assertEqual(result.returncode, 0)
        self.assertNotIn("refusing", result.stderr)


if __name__ == "__main__":
    unittest.main()
