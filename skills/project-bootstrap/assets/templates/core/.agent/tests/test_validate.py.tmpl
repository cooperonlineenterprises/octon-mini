from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / ".agent/scripts/validate.py"
SPEC = importlib.util.spec_from_file_location(
    "project_harness_validate", VALIDATOR_PATH
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load validator: {VALIDATOR_PATH}")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def snapshot(base: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(base.rglob("*")):
        if path.is_file():
            result[path.relative_to(base).as_posix()] = hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
    return result


def clone() -> tuple[tempfile.TemporaryDirectory[str], Path]:
    temporary = tempfile.TemporaryDirectory(prefix="harness-mutation-")
    test_root = Path(temporary.name) / "project"
    shutil.copytree(ROOT, test_root, symlinks=True)
    return temporary, test_root


def write_task(path: Path, value: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n"
        + json.dumps(value, indent=2, sort_keys=True)
        + "\n---\n\n# Mutation fixture\n",
        encoding="utf-8",
    )


class HarnessValidatorTests(unittest.TestCase):
    def test_generated_foundation_is_valid(self) -> None:
        self.assertEqual(VALIDATOR.check(ROOT), [])

    def test_strict_json_accepts_valid_fixture(self) -> None:
        fixture = ROOT / ".agent/tests/fixtures/valid/kernel.json"
        value = VALIDATOR.load_json(fixture)
        self.assertIs(value["permission_grant"], False)

    def test_duplicate_json_key_is_rejected(self) -> None:
        fixture = ROOT / ".agent/tests/fixtures/invalid/duplicate-key.json"
        with self.assertRaises(VALIDATOR.DuplicateKeyError):
            VALIDATOR.load_json(fixture)

    def test_json_safe_project_identity_is_parseable(self) -> None:
        project = VALIDATOR.load_json(ROOT / ".agent/project.json")
        self.assertIsInstance(project["project"]["name"], str)
        self.assertTrue(project["project"]["name"])

    def test_nested_instruction_authority_expansion_is_rejected(self) -> None:
        temporary, test_root = clone()
        try:
            nested = test_root / "src" / "AGENTS.md"
            nested.parent.mkdir()
            nested.write_text(
                '# Invalid\n\n"permission_grant": true\n',
                encoding="utf-8",
            )
            findings = VALIDATOR.check_files_and_json(test_root)
            self.assertTrue(
                any("nested instruction may expand authority" in item for item in findings)
            )
        finally:
            temporary.cleanup()

    def test_illegal_lifecycle_transition_is_rejected(self) -> None:
        temporary, test_root = clone()
        try:
            write_task(
                test_root / ".agent/tasks/TASK-9001-mutation.md",
                {
                    "schema_version": "harness.task.v1",
                    "id": "TASK-9001",
                    "status": "proposed",
                    "previous_status": "completed",
                    "title": "Illegal transition",
                    "authority_basis": "authority:test",
                    "owner": "test",
                    "dependencies": [],
                    "closure_evidence": [],
                    "external_effects": "none",
                    "limitations": [],
                },
            )
            records, errors = VALIDATOR.collect_records(test_root)
            self.assertEqual(errors, [])
            findings = VALIDATOR.check_references_and_lifecycle(test_root, records)
            self.assertTrue(any("illegal task transition" in item for item in findings))
        finally:
            temporary.cleanup()

    def test_broken_record_reference_is_rejected(self) -> None:
        temporary, test_root = clone()
        try:
            write_task(
                test_root / ".agent/tasks/TASK-9002-mutation.md",
                {
                    "schema_version": "harness.task.v1",
                    "id": "TASK-9002",
                    "status": "proposed",
                    "previous_status": None,
                    "title": "Broken reference",
                    "authority_basis": "authority:test",
                    "owner": "test",
                    "dependencies": ["TASK-9999"],
                    "closure_evidence": [],
                    "external_effects": "none",
                    "limitations": [],
                },
            )
            records, errors = VALIDATOR.collect_records(test_root)
            self.assertEqual(errors, [])
            findings = VALIDATOR.check_references_and_lifecycle(test_root, records)
            self.assertTrue(any("unresolved reference TASK-9999" in item for item in findings))
        finally:
            temporary.cleanup()

    def test_synthetic_secret_is_detected_and_redacted(self) -> None:
        temporary, test_root = clone()
        synthetic_value = "synthetic_test_value_123456789"
        try:
            path = test_root / "src" / "synthetic-secret.txt"
            path.parent.mkdir()
            path.write_text(f"api_key: {synthetic_value}\n", encoding="utf-8")
            findings = VALIDATOR.check_files_and_json(test_root)
            matching = [item for item in findings if "secret assignment" in item]
            self.assertTrue(matching)
            self.assertNotIn(synthetic_value, "\n".join(matching))
        finally:
            temporary.cleanup()

    def test_any_source_change_invalidates_integrity(self) -> None:
        temporary, test_root = clone()
        try:
            source = test_root / "src" / "new-domain-file.txt"
            source.parent.mkdir()
            source.write_text("changed\n", encoding="utf-8")
            findings = VALIDATOR.check_integrity(test_root)
            self.assertTrue(any("stale source fingerprint" in item for item in findings))
        finally:
            temporary.cleanup()

    def test_checksum_scope_is_current_when_enabled(self) -> None:
        checksum = ROOT / "project-dossier/CHECKSUMS.sha256"
        if not checksum.exists():
            self.skipTest("checksums are high-assurance only")
        self.assertEqual(VALIDATOR.check_integrity(ROOT), [])

    def test_interrupted_refresh_generation_mismatch_is_rejected(self) -> None:
        report_path = ROOT / ".agent/generated/validation-report.json"
        if not report_path.exists():
            self.skipTest("generated integrity is high-assurance only")
        temporary, test_root = clone()
        try:
            mutated = VALIDATOR.load_json(
                test_root / ".agent/generated/validation-report.json"
            )
            mutated["generation_id"] = "0" * 32
            (test_root / ".agent/generated/validation-report.json").write_text(
                json.dumps(mutated, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            findings = VALIDATOR.check_integrity(test_root)
            self.assertTrue(any("mismatched generation IDs" in item for item in findings))
        finally:
            temporary.cleanup()

    def test_extension_authority_expansion_is_rejected(self) -> None:
        registry_path = ROOT / ".agent/extensions/registry.json"
        if not registry_path.exists():
            self.skipTest("extensions are standard profile or higher")
        temporary, test_root = clone()
        try:
            registry = VALIDATOR.load_json(
                test_root / ".agent/extensions/registry.json"
            )
            if not registry["extensions"]:
                self.skipTest("active reference extension is high-assurance only")
            registry["extensions"][0]["authority_effect"] = "expands_permission"
            (test_root / ".agent/extensions/registry.json").write_text(
                json.dumps(registry, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            findings = VALIDATOR.check_extensions(test_root)
            self.assertTrue(any("allowed vocabulary" in item or "equal" in item for item in findings))
        finally:
            temporary.cleanup()

    def test_extension_can_be_disabled_without_kernel_change(self) -> None:
        registry_path = ROOT / ".agent/extensions/registry.json"
        if not registry_path.exists():
            self.skipTest("extensions are standard profile or higher")
        temporary, test_root = clone()
        try:
            registry = VALIDATOR.load_json(
                test_root / ".agent/extensions/registry.json"
            )
            if not registry["extensions"]:
                self.skipTest("active reference extension is high-assurance only")
            kernel_before = {
                path: (test_root / path).read_bytes()
                for path in VALIDATOR.KERNEL_FILES
            }
            registry["extensions"][0]["enabled"] = False
            (test_root / ".agent/extensions/registry.json").write_text(
                json.dumps(registry, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            self.assertEqual(VALIDATOR.check_extensions(test_root), [])
            kernel_after = {
                path: (test_root / path).read_bytes()
                for path in VALIDATOR.KERNEL_FILES
            }
            self.assertEqual(kernel_before, kernel_after)
        finally:
            temporary.cleanup()

    def test_read_only_check_does_not_write(self) -> None:
        before = snapshot(ROOT)
        VALIDATOR.check(ROOT)
        after = snapshot(ROOT)
        self.assertEqual(before, after)

    def test_clean_isolated_runtime(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-I",
                "-B",
                ".agent/scripts/validate.py",
                "--check",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)


if __name__ == "__main__":
    unittest.main()
