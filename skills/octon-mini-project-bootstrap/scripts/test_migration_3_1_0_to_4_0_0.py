#!/usr/bin/env python3
"""Cross-brand integration, refusal, rollback, and recovery tests for 3.1→4.0."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_ROOT = Path(__file__).resolve().parent
SCAFFOLDER = SCRIPT_ROOT / "scaffold_project.py"
MIGRATOR = SCRIPT_ROOT / "migrate_3_1_0_to_4_0_0.py"
UPGRADER = SCRIPT_ROOT / "upgrade_project.py"
LEGACY_ORIGIN = ".project-blueprint-origin.json"
CURRENT_ORIGIN = ".octon-mini-origin.json"

LEGACY_PATH_MAP = {
    "octon": "pb",
    ".agent/scripts/octon.py": ".agent/scripts/pb.py",
    ".agent/scripts/octon_doctor.py": ".agent/scripts/pb_doctor.py",
    ".agent/scripts/octon_work_completion.py": ".agent/scripts/pb_finish.py",
    ".agent/scripts/octon_transaction.py": ".agent/scripts/pb_transaction.py",
    ".agent/schemas/octon-mini-bootstrap-migration-seed.schema.json": ".agent/schemas/project-blueprint-migration-seed.schema.json",
    ".agent/schemas/octon-mini-bootstrap-setup-answers.schema.json": ".agent/schemas/project-blueprint-setup-answers.schema.json",
    ".agent/schemas/octon-mini-bootstrap-setup-session.schema.json": ".agent/schemas/project-blueprint-setup-session.schema.json",
    ".agent/schemas/octon-mini-bootstrap-upgrade.schema.json": ".agent/schemas/project-blueprint-upgrade.schema.json",
    ".agent/schemas/octon-mini-project-origin.schema.json": ".agent/schemas/project-blueprint-origin.schema.json",
    CURRENT_ORIGIN: LEGACY_ORIGIN,
}

V1_COLLABORATION = {
    "schema_version": "harness.collaboration-profile.v1",
    "permission_grant": False,
    "assessment_status": "not_assessed",
    "confidence": "unknown",
    "declared_write_capable_humans": None,
    "observed_repository_access": {
        "write_capable_humans": None,
        "read_only_humans": None,
        "bots_or_automation": None,
    },
    "active_contributors": {
        "human_count": None,
        "bots_or_automation_count": None,
        "window_days": None,
    },
    "independent_review_capacity": None,
    "expected_concurrent_repository_writers": {
        "humans": None,
        "agents_or_automation": None,
    },
    "external_contribution_mode": "unknown",
    "solo_integration_preference": "unknown",
    "evidence": [],
    "assessed_at": None,
    "reassess_after": None,
    "conflicting_signals": [],
    "limitations": ["generated_unassessed_baseline"],
    "team_band": "unknown",
    "workflow_selection": {
        "status": "not_assessed",
        "base_workflow": None,
        "modifiers": [],
        "review_mode": "not_assessed",
        "integration_method": None,
        "adoption_decision_ref": None,
    },
}


def run(argv: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv, cwd=cwd, capture_output=True, text=True, check=False, shell=False
    )


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_state(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): digest(path)
        for path in root.rglob("*")
        if path.is_file() and not path.is_symlink()
    }


class Migration310To400Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(
            prefix="octon-mini-cross-brand-migration-310-400-"
        )
        self.root = Path(self.temporary.name) / "project"
        result = run(
            [
                sys.executable,
                "-B",
                str(SCAFFOLDER),
                "--target",
                str(self.root),
                "--project-name",
                "Legacy Seed Fixture",
                "--profile",
                "minimal",
                "--layout",
                "separated",
            ],
            SCRIPT_ROOT,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self._create_task_and_evidence_with_current_runtime()
        self._downgrade_to_inert_legacy_fixture()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _create_task_and_evidence_with_current_runtime(self) -> None:
        plan = self.root / ".agent/transactions/plans/work.json"
        result = run(
            [
                str(self.root / "octon"),
                "work",
                "start",
                "--title",
                "Migrate the legacy snapshot",
                "--scope",
                "Exercise the reviewed migration boundary",
                "--authority-basis",
                "authority:migration-fixture-owner",
                "--owner",
                "fixture-owner",
                "--operator",
                "fixture-operator",
                "--acceptance",
                "The structural migration passes its release tier",
                "--validation",
                "Run the generated release suite",
                "--next-action",
                "Review legacy inventory",
                "--output",
                str(plan),
            ],
            self.root,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        plan_value = load(plan)
        result = run(
            [
                str(self.root / "octon"),
                "transaction",
                "apply",
                "--plan",
                str(plan),
                "--accept-digest",
                plan_value["canonical_plan_digest"],
            ],
            self.root,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        evidence = {
            "schema_version": "harness.evidence.v1",
            "id": "EVD-0001",
            "title": "Reviewed legacy migration fixture",
            "task": "TASK-0001",
            "recorded_at": "2026-08-12",
            "authority_source": "authority:migration-fixture-owner",
            "owner": "fixture-owner",
            "scope": "Project Blueprint 3.1.0 to Octon Mini 4.0.0 structural migration",
            "method": "Deterministic local integration fixture",
            "environment": "temporary repository",
            "subject_revision_or_fingerprint": "synthetic-project-blueprint-3.1.0-baseline",
            "result": "pass",
            "fresh_until": "2027-08-12",
            "supersedes": None,
            "limitations": ["Synthetic evidence proves only the migration fixture"],
        }
        evidence_path = self.root / ".agent/evidence/EVD-0001-migration.md"
        evidence_path.parent.mkdir()
        evidence_path.write_text(
            "---\n"
            + json.dumps(evidence, indent=2, sort_keys=True)
            + "\n---\n\n# Migration evidence\n",
            encoding="utf-8",
        )

    def _downgrade_to_inert_legacy_fixture(self) -> None:
        current_origin_path = self.root / CURRENT_ORIGIN
        current_origin = load(current_origin_path)
        generated_paths = [
            LEGACY_PATH_MAP.get(path, path) for path in current_origin["generated_paths"]
        ]
        for current, legacy in LEGACY_PATH_MAP.items():
            source = self.root / current
            destination = self.root / legacy
            if source.exists():
                destination.parent.mkdir(parents=True, exist_ok=True)
                source.rename(destination)

        project_path = self.root / ".agent/project.json"
        project = load(project_path)
        project["schema_version"] = "harness.project.v3"
        project["project"].pop("octon_mini_version", None)
        project["project"]["blueprint_version"] = "3.1.0"
        project["collaboration_profile"] = V1_COLLABORATION
        project["project_checks"] = {
            "evidence_schema": ".agent/schemas/harness-project-check-evidence.schema.json",
            "evidence_store": ".agent/project-checks/evidence.json",
            "writer_argv": [
                "python",
                "-B",
                ".agent/scripts/run_project_checks.py",
                "--write-evidence",
            ],
            "adoption_verification_argv": [
                "python",
                "-B",
                ".agent/scripts/run_project_checks.py",
                "--write-evidence",
                "--verify-adoption",
            ],
            "execution": "explicit_writer_only",
            "shell_interpretation": False,
        }
        project["extensions"] = {
            "registry": ".agent/extensions/registry.json",
            "registry_required_in_profile": "standard_or_higher",
        }
        project.pop("packages", None)
        write(project_path, project)

        initial = current_origin["initial_generation"]
        legacy_origin = {
            "schema_version": "project-blueprint.origin.v1",
            "blueprint": "project-blueprint",
            "blueprint_version": "3.1.0",
            "generator_version": "3.1.0",
            "generation_id": current_origin["generation_id"],
            "profile": current_origin["profile"],
            "generated_on": current_origin["generated_on"],
            "project_name": current_origin["project_name"],
            "project_slug": current_origin["project_slug"],
            "harness_kernel_version": "3.0.0",
            "authority": current_origin["authority"],
            "initial_generation": {
                "blueprint_version": "3.1.0",
                "generator_version": "3.1.0",
                "generation_id": initial["generation_id"],
                "generated_on": initial["generated_on"],
                "profile": initial["profile"],
            },
            "migration_history": [],
            "generated_paths": generated_paths,
        }
        write(self.root / LEGACY_ORIGIN, legacy_origin)
        self.assertFalse(current_origin_path.exists())
        self.assertTrue((self.root / "pb").is_file())
        self.assertFalse((self.root / "octon").exists())

    def _review_and_seed(self) -> tuple[Path, Path]:
        artifacts = Path(self.temporary.name) / "artifacts"
        artifacts.mkdir(exist_ok=True)
        inspection_path = artifacts / "inspection.json"
        before = file_state(self.root)
        result = run(
            [
                sys.executable,
                "-B",
                str(MIGRATOR),
                "inspect",
                "--target",
                str(self.root),
                "--output",
                str(inspection_path),
            ],
            SCRIPT_ROOT,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertEqual(before, file_state(self.root))
        inspection = load(inspection_path)
        self.assertEqual(
            inspection["schema_version"],
            "octon-mini.bootstrap.cross-brand-migration-inspection.v1",
        )
        reviewed_paths = []
        for item in inspection["paths"]:
            role = item["expected_role"]
            if role in {"derived", "provenance"}:
                confirmation = role
                mode = None
                sha256 = None
            else:
                confirmation = "exact_pristine"
                mode = item["current"]["mode"]
                sha256 = item["current"]["sha256"]
            reviewed_paths.append(
                {
                    "path": item["path"],
                    "role": role,
                    "upgrade_policy": item["expected_upgrade_policy"],
                    "baseline_product": "project-blueprint",
                    "baseline_version": "3.1.0",
                    "baseline_confirmation": confirmation,
                    "mode": mode,
                    "sha256": sha256,
                    "rationale": "Explicit deterministic fixture review of the old pristine baseline.",
                }
            )
        review = {
            "schema_version": "octon-mini.bootstrap.cross-brand-migration-review.v1",
            "permission_grant": False,
            "source_product": "project-blueprint",
            "source_version": "3.1.0",
            "target_product": "octon-mini",
            "target_version": "4.0.0",
            "reviewed_at": "2026-08-12T20:00:00Z",
            "origin_sha256": inspection["origin_sha256"],
            "project_sha256": inspection["project_sha256"],
            "layout": "separated",
            "authority_source": "authority:migration-fixture-owner",
            "evidence_refs": ["EVD-0001"],
            "paths": reviewed_paths,
            "limitations": ["Synthetic fixture review only"],
        }
        review_path = artifacts / "review.json"
        write(review_path, review)
        seed_path = artifacts / "seed.json"
        result = run(
            [
                sys.executable,
                "-B",
                str(MIGRATOR),
                "seed",
                "--target",
                str(self.root),
                "--review",
                str(review_path),
                "--output",
                str(seed_path),
            ],
            SCRIPT_ROOT,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        second = artifacts / "seed-second.json"
        result = run(
            [
                sys.executable,
                "-B",
                str(MIGRATOR),
                "seed",
                "--target",
                str(self.root),
                "--review",
                str(review_path),
                "--output",
                str(second),
            ],
            SCRIPT_ROOT,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertEqual(seed_path.read_bytes(), second.read_bytes())
        return review_path, seed_path

    def test_reviewed_cross_brand_upgrade_rollback_and_refusals(self) -> None:
        _, seed_path = self._review_and_seed()
        seed = load(seed_path)
        self.assertFalse(seed["permission_grant"])
        self.assertEqual(seed["source_product"], "project-blueprint")
        self.assertEqual(seed["target_product"], "octon-mini")
        self.assertEqual(
            seed["legacy_baseline"]["installed_inventory"]["profile_manifest_status"],
            "legacy_unavailable_reviewed",
        )

        project_path = self.root / ".agent/project.json"
        original_project = project_path.read_bytes()
        project_path.write_bytes(original_project + b"\n")
        stale = run(
            [
                sys.executable,
                "-B",
                str(MIGRATOR),
                "check",
                "--target",
                str(self.root),
                "--seed",
                str(seed_path),
            ],
            SCRIPT_ROOT,
        )
        self.assertNotEqual(stale.returncode, 0)
        project_path.write_bytes(original_project)
        current = run(
            [
                sys.executable,
                "-B",
                str(MIGRATOR),
                "check",
                "--target",
                str(self.root),
                "--seed",
                str(seed_path),
            ],
            SCRIPT_ROOT,
        )
        self.assertEqual(current.returncode, 0, current.stderr or current.stdout)

        legacy_preimages = {
            path: (self.root / path).read_bytes()
            for path in [LEGACY_ORIGIN, "pb", *sorted(set(LEGACY_PATH_MAP.values()) - {LEGACY_ORIGIN, "pb"})]
            if (self.root / path).is_file()
        }
        proposals = self.root / ".agent/transactions/proposals"
        reviews = self.root / ".agent/transactions/reviews"
        plans = self.root / ".agent/transactions/plans"
        proposals.mkdir(parents=True, exist_ok=True)
        reviews.mkdir(parents=True, exist_ok=True)
        proposal_path = proposals / "upgrade.json"
        result = run(
            [
                sys.executable,
                "-B",
                str(UPGRADER),
                "plan",
                "--target",
                str(self.root),
                "--authority-source",
                "authority:migration-fixture-owner",
                "--evidence-ref",
                "EVD-0001",
                "--project-blueprint-seed",
                str(seed_path),
                "--output",
                str(proposal_path),
            ],
            SCRIPT_ROOT,
        )
        self.assertEqual(result.returncode, 3, result.stderr or result.stdout)
        proposal = load(proposal_path)
        self.assertEqual(
            proposal["schema_version"], "octon-mini.bootstrap.upgrade-proposal.v1"
        )
        dispositions = []
        for row in proposal["classifications"]:
            if row["automatic"]:
                continue
            if row["path"] == ".agent/project.json":
                disposition = "migrate_legacy_project_contract"
            elif row["classification"] == "removed_upstream":
                disposition = "delete"
            elif (
                row["classification"] in {"additive", "conflicting"}
                and "accept_candidate" in row["allowed_dispositions"]
            ):
                disposition = "accept_candidate"
            else:
                disposition = "preserve_current"
            dispositions.append(
                {
                    "id": row["id"],
                    "disposition": disposition,
                    "rationale": "Explicit cross-brand migration integration fixture disposition.",
                }
            )
        upgrade_review = {
            "schema_version": "octon-mini.bootstrap.upgrade-review.v1",
            "permission_grant": False,
            "proposal_digest": proposal["canonical_proposal_digest"],
            "dispositions": dispositions,
            "limitations": ["Synthetic migration integration fixture"],
        }
        upgrade_review_path = reviews / "upgrade.json"
        write(upgrade_review_path, upgrade_review)
        transaction_path = plans / "upgrade.json"
        result = run(
            [
                sys.executable,
                "-B",
                str(UPGRADER),
                "plan",
                "--target",
                str(self.root),
                "--authority-source",
                "authority:migration-fixture-owner",
                "--evidence-ref",
                "EVD-0001",
                "--project-blueprint-seed",
                str(seed_path),
                "--proposal",
                str(proposal_path),
                "--review",
                str(upgrade_review_path),
                "--output",
                str(transaction_path),
            ],
            SCRIPT_ROOT,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        transaction = load(transaction_path)
        result = run(
            [
                sys.executable,
                "-B",
                str(UPGRADER),
                "apply",
                "--target",
                str(self.root),
                "--plan",
                str(transaction_path),
                "--accept-digest",
                transaction["canonical_plan_digest"],
            ],
            SCRIPT_ROOT,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

        final_origin = load(self.root / CURRENT_ORIGIN)
        final_project = load(self.root / ".agent/project.json")
        self.assertEqual(final_origin["schema_version"], "octon-mini.project.origin.v1")
        self.assertEqual(final_origin["product"], "octon-mini")
        self.assertEqual(final_origin["octon_mini_version"], "4.0.0")
        self.assertEqual(final_project["schema_version"], "harness.project.v5")
        self.assertEqual(final_project["project"]["octon_mini_version"], "4.0.0")
        self.assertEqual(
            final_project["collaboration_profile"]["assessment_status"],
            "not_assessed",
        )
        self.assertFalse((self.root / LEGACY_ORIGIN).exists())
        for legacy_path in LEGACY_PATH_MAP.values():
            self.assertFalse((self.root / legacy_path).exists(), legacy_path)
        self.assertTrue((self.root / "octon").is_file())
        self.assertTrue((self.root / ".agent/scripts/octon.py").is_file())
        check = run([str(self.root / "octon"), "check"], self.root)
        self.assertEqual(check.returncode, 0, check.stderr or check.stdout)

        after_apply = file_state(self.root)
        second_application = run(
            [
                sys.executable,
                "-B",
                str(MIGRATOR),
                "check",
                "--target",
                str(self.root),
                "--seed",
                str(seed_path),
            ],
            SCRIPT_ROOT,
        )
        self.assertNotEqual(second_application.returncode, 0)
        self.assertIn("already migrated", second_application.stderr)
        self.assertEqual(after_apply, file_state(self.root))

        receipt_path = Path(
            next(
                line.split(" ", 1)[1]
                for line in result.stdout.splitlines()
                if line.startswith("[RECEIPT]")
            )
        )
        rollback_copy = Path(self.temporary.name) / "rollback-copy"
        shutil.copytree(self.root, rollback_copy)
        rollback_receipt = (
            rollback_copy / receipt_path.resolve().relative_to(self.root.resolve())
        )
        rollback = run(
            [
                str(rollback_copy / "octon"),
                "transaction",
                "rollback",
                "--receipt",
                str(rollback_receipt),
            ],
            rollback_copy,
        )
        self.assertEqual(rollback.returncode, 0, rollback.stderr or rollback.stdout)
        self.assertEqual(
            load(rollback_copy / LEGACY_ORIGIN)["schema_version"],
            "project-blueprint.origin.v1",
        )
        self.assertEqual(
            load(rollback_copy / ".agent/project.json")["schema_version"],
            "harness.project.v3",
        )
        for path, content in legacy_preimages.items():
            self.assertEqual((rollback_copy / path).read_bytes(), content, path)
        self.assertFalse((rollback_copy / CURRENT_ORIGIN).exists())
        self.assertFalse((rollback_copy / "octon").exists())
        self.assertTrue((rollback_copy / "pb").is_file())

        project = load(self.root / ".agent/project.json")
        project["project"]["name"] = "Changed after upgrade"
        write(self.root / ".agent/project.json", project)
        refused = run(
            [
                str(self.root / "octon"),
                "transaction",
                "rollback",
                "--receipt",
                str(receipt_path),
            ],
            self.root,
        )
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("post-apply path changed", refused.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
