#!/usr/bin/env python3
"""Positive, negative, mutation, stale-session, read-only, and resume tests."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import types
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock


SCRIPT_ROOT = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_ROOT.parent


def octon_mini_source_root() -> Path:
    candidates = (
        SKILL_ROOT.parents[1],
        SKILL_ROOT / "assets/octon-mini-source",
    )
    for candidate in candidates:
        if (candidate / "octon-mini.json").is_file():
            return candidate
    return candidates[0]


OCTON_MINI_ROOT = octon_mini_source_root()
SETUP_SOURCE = SCRIPT_ROOT / "setup_session.py"
OCTON_SOURCE = SCRIPT_ROOT / "octon.py"
COMMAND_MANIFEST = OCTON_MINI_ROOT / "shared/source-contracts/commands.json"
INIT_FIXTURE = SKILL_ROOT / "fixtures/guided-setup/valid/initialization-answers.json"
ADOPT_FIXTURE = SKILL_ROOT / "fixtures/guided-setup/valid/adoption-answers.json"
UPGRADE_FIXTURE = SKILL_ROOT / "fixtures/guided-setup/valid/upgrade-answers.json"
MUTATIONS = SKILL_ROOT / "fixtures/guided-setup/invalid/mutations.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        module = types.ModuleType(name)
        module.__file__ = str(path)
        exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), module.__dict__)
        return module
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file() and not path.is_symlink()
    }


def command(argv: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
        shell=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "GIT_OPTIONAL_LOCKS": "0"},
    )


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def evidence(*, source: str = "user:fixture", expiring: bool = False) -> dict[str, object]:
    now = datetime.now(timezone.utc)
    return {
        "source": source,
        "observed_at": now.isoformat().replace("+00:00", "Z"),
        "expires_at": (now + timedelta(days=7)).isoformat().replace("+00:00", "Z") if expiring else None,
        "confidence": "high",
        "limitations": ["Synthetic test evidence; grants no authority."],
    }


def answer_batch(
    setup: object,
    session: dict[str, object],
    rows: list[tuple[str, str, object, bool]],
    *,
    supplied_by: str = "agent",
) -> dict[str, object]:
    return {
        "schema_version": setup.ANSWER_SCHEMA,
        "permission_grant": False,
        "session_digest": session["canonical_session_digest"],
        "answers": [
            {
                "question_id": identifier,
                "state": state,
                "value": value,
                "supplied_by": supplied_by,
                "evidence": evidence(expiring=expiring),
            }
            for identifier, state, value, expiring in rows
        ],
        "limitations": ["Synthetic answer batch; not implementation or readiness evidence."],
    }


def with_digest(path: Path, digest: str) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    value["session_digest"] = digest
    return value


def normalized_plan(value: object) -> object:
    if isinstance(value, list):
        return [normalized_plan(item) for item in value]
    if isinstance(value, dict):
        ignored = {
            "created_at",
            "observed_at",
            "planned_receipt_id",
            "canonical_plan_digest",
        }
        return {key: normalized_plan(item) for key, item in value.items() if key not in ignored}
    return value


class GuidedSetupTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.setup = load_module("guided_setup_fixture", SETUP_SOURCE)
        self.catalog = self.setup.load_catalog()

    def new_target(self, area: Path, mode: str) -> Path:
        target = area / "target"
        target.mkdir()
        if mode == "adoption":
            (target / "README.md").write_text("# Established project\n", encoding="utf-8")
        elif mode == "upgrade":
            write_json(
                target / ".octon-mini-origin.json",
                {
                    "schema_version": "octon-mini.project.origin.v1",
                    "product": "octon-mini",
                    "octon_mini_version": "4.0.0",
                },
            )
        return target

    def ready_initialization(self, target: Path) -> dict[str, object]:
        session = self.setup.create_session("initialization", target)
        payload = with_digest(INIT_FIXTURE, session["canonical_session_digest"])
        return self.setup.apply_answer_batch(session, payload, self.catalog)

    def test_catalog_is_single_closed_dependency_ordered_authority(self) -> None:
        catalog = self.setup.validate_catalog(copy.deepcopy(self.catalog))
        ids = [item["id"] for item in catalog["questions"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(
            next(item for item in catalog["questions"] if item["id"] == "setup.work-finish-mode")["answer"]["valid_values"],
            ["disabled", "on_demand", "on_demand_plus_plan_only_event"],
        )
        self.assertFalse(catalog["permission_grant"])
        self.assertNotIn("automatic_apply", json.dumps(catalog))

    def test_mode_detection_and_question_generation_are_target_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            area = Path(temporary)
            for mode in self.setup.MODES:
                target = self.new_target(area / mode, mode) if (area / mode).mkdir(parents=True) is None else None
                assert target is not None
                marker = target / "generated-projection.txt"
                if mode != "initialization":
                    marker.write_text("must not refresh\n", encoding="utf-8")
                before = snapshot(target)
                session = self.setup.create_session(mode, target)
                batch = self.setup.question_batch(session, self.catalog, 3)
                self.assertEqual(snapshot(target), before)
                self.assertEqual(session["mode"], mode)
                self.assertFalse(batch["permission_grant"])
                self.assertLessEqual(len(batch["questions"]), 3)
            ambiguous = area / "ambiguous" / "target"
            (ambiguous / ".agent").mkdir(parents=True)
            with self.assertRaisesRegex(self.setup.SetupError, "ambiguous"):
                self.setup.create_session("adoption", ambiguous)

    def test_explicit_session_output_is_outside_target_and_atomic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            area = Path(temporary)
            target = self.new_target(area, "initialization")
            session = self.setup.create_session("initialization", target)
            with self.assertRaisesRegex(self.setup.SetupError, "outside the target"):
                self.setup.ensure_output_outside_target(target / "session.json", target)
            output = area / "session.json"
            self.setup.write_new_json(output, session)
            self.assertTrue(output.is_file())
            with self.assertRaisesRegex(self.setup.SetupError, "refusing to overwrite"):
                self.setup.write_new_json(output, session)
            interrupted = area / "interrupted.json"
            with mock.patch.object(os, "link", side_effect=OSError("interrupted")):
                with self.assertRaises(OSError):
                    self.setup.write_new_json(interrupted, session)
            self.assertFalse(interrupted.exists())
            self.assertFalse(list(area.glob(".interrupted.json.tmp-*")))

    def test_answer_file_and_tty_use_same_catalog_and_plan_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.new_target(Path(temporary), "initialization")
            initial = self.setup.create_session("initialization", target)
            agent_payload = answer_batch(
                self.setup,
                initial,
                [
                    ("setup.project-name", "answered", "TTY Equivalent", False),
                    ("setup.assurance-profile", "answered", "standard", False),
                    ("setup.write-capable-humans", "unknown", None, False),
                ],
            )
            agent_session = self.setup.apply_answer_batch(initial, agent_payload, self.catalog)
            fake_stdin = mock.Mock()
            fake_stdin.isatty.return_value = True
            with redirect_stdout(io.StringIO()), mock.patch.object(
                sys, "stdin", fake_stdin
            ), mock.patch(
                "builtins.input", side_effect=["TTY Equivalent", "standard", "unknown"]
            ):
                tty_payload = self.setup.tty_answer_batch(initial, self.catalog, 3)
            tty_session = self.setup.apply_answer_batch(initial, tty_payload, self.catalog)
            for identifier in ("setup.project-name", "setup.assurance-profile", "setup.write-capable-humans"):
                self.assertEqual(
                    self.setup.session_question_state(agent_session)[identifier]["value"],
                    self.setup.session_question_state(tty_session)[identifier]["value"],
                )
            agent_session = self.setup.apply_answer_batch(
                agent_session,
                answer_batch(
                    self.setup,
                    agent_session,
                    [
                        ("setup.layout", "answered", "compact", False),
                        ("setup.work-finish-mode", "answered", "disabled", False),
                    ],
                    supplied_by="agent",
                ),
                self.catalog,
            )
            tty_session = self.setup.apply_answer_batch(
                tty_session,
                answer_batch(
                    self.setup,
                    tty_session,
                    [
                        ("setup.layout", "answered", "compact", False),
                        ("setup.work-finish-mode", "answered", "disabled", False),
                    ],
                    supplied_by="tty",
                ),
                self.catalog,
            )
            self.assertEqual(agent_session["session_status"], "ready_for_plan")
            self.assertEqual(tty_session["session_status"], "ready_for_plan")
            semantic_plans: list[dict[str, object]] = []
            for channel, session in (("agent", agent_session), ("tty", tty_session)):
                session_path = Path(temporary) / f"{channel}-session.json"
                plan_path = Path(temporary) / f"{channel}-plan.json"
                self.setup.write_new_json(session_path, session)
                result = command(
                    [
                        sys.executable,
                        "-B",
                        str(OCTON_SOURCE),
                        "init",
                        "plan",
                        "--target",
                        str(target),
                        "--setup-session",
                        str(session_path),
                        "--output",
                        str(plan_path),
                    ],
                    OCTON_MINI_ROOT,
                )
                self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
                plan = json.loads(plan_path.read_text(encoding="utf-8"))
                semantic_plans.append(
                    {
                        key: plan[key]
                        for key in (
                            "operation",
                            "scope",
                            "operations",
                            "targets",
                            "validation",
                        )
                    }
                )
            self.assertEqual(semantic_plans[0], semantic_plans[1])

    def test_resume_preserves_unknown_deferred_and_invalidates_facts_after_reinspection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.new_target(Path(temporary), "initialization")
            initial = self.setup.create_session("initialization", target)
            first = self.setup.apply_answer_batch(
                initial,
                answer_batch(
                    self.setup,
                    initial,
                    [
                        ("setup.project-name", "answered", "Resume Example", False),
                        ("setup.assurance-profile", "answered", "minimal", False),
                        ("setup.write-capable-humans", "unknown", None, False),
                        ("setup.work-finish-mode", "deferred", None, False),
                    ],
                ),
                self.catalog,
            )
            second = self.setup.apply_answer_batch(
                first,
                answer_batch(self.setup, first, [("setup.layout", "answered", "compact", False)]),
                self.catalog,
            )
            self.assertEqual(second["session_status"], "ready_for_plan")
            (target / ".agent").mkdir()
            (target / ".agent/transactions").mkdir()
            (target / ".agent/transactions/ignored.json").write_text("{}\n", encoding="utf-8")
            self.assertEqual(self.setup.current_state_mismatches(second), [])
            reinspection = self.setup.reinspect_session(second)
            states = self.setup.session_question_state(reinspection)
            self.assertEqual(states["setup.write-capable-humans"]["state"], "unknown")
            self.assertEqual(states["setup.work-finish-mode"]["state"], "deferred")
            self.assertEqual(reinspection["work_completion_assessment"]["status"], "deferred")
            self.assertNotIn("setup.project-name", states)
            self.assertNotIn("setup.assurance-profile", states)

    def test_target_instruction_catalog_and_revision_staleness_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            area = Path(temporary)
            target = self.new_target(area, "adoption")
            (target / "AGENTS.md").write_text("# Initial rules\n", encoding="utf-8")
            session = self.setup.create_session("adoption", target)
            path = area / "session.json"
            self.setup.write_new_json(path, session)
            (target / "README.md").write_text("# Changed\n", encoding="utf-8")
            with self.assertRaisesRegex(self.setup.SetupError, "target content fingerprint"):
                self.setup.load_session(path)
            (target / "README.md").write_text("# Established project\n", encoding="utf-8")
            (target / "AGENTS.md").write_text("# Changed rules\n", encoding="utf-8")
            with self.assertRaisesRegex(self.setup.SetupError, "governing instruction fingerprint"):
                self.setup.load_session(path)
            changed_catalog = copy.deepcopy(session)
            changed_catalog["question_catalog"]["sha256"] = "f" * 64
            changed_catalog["canonical_session_digest"] = self.setup.record_digest(changed_catalog, "canonical_session_digest")
            changed_path = area / "catalog-changed.json"
            self.setup.write_new_json(changed_path, changed_catalog)
            with self.assertRaisesRegex(self.setup.SetupError, "catalog definitions changed"):
                self.setup.load_session(changed_path, require_current=False)

    def test_recommendations_selections_authority_and_runtime_permission_remain_separate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            area = Path(temporary)
            target = self.new_target(area, "adoption")
            session = self.setup.create_session("adoption", target)
            value = self.setup.apply_answer_batch(
                session,
                with_digest(ADOPT_FIXTURE, session["canonical_session_digest"]),
                self.catalog,
            )
            recommended = {item["question_id"] for item in value["recommendations"]}
            selected = {item["question_id"] for item in value["user_selections"]}
            accepted = {item["question_id"] for item in value["accepted_authority_references"]}
            self.assertIn("setup.project-name", recommended)
            self.assertIn("setup.project-name", selected)
            self.assertNotIn("setup.project-name", accepted)
            self.assertIn("setup.adoption-authority", accepted)
            self.assertTrue(
                all(
                    item["setup_validation"]
                    == "reference_syntax_valid_project_resolution_required"
                    for item in value["accepted_authority_references"]
                )
            )
            self.assertFalse(value["permission_grant"])
            self.assertFalse(value["work_completion_assessment"]["external_action_authorization"])

    def test_team_size_is_independent_of_assurance_and_automation_count(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.new_target(Path(temporary), "initialization")
            session = self.setup.create_session("initialization", target)
            value = self.setup.apply_answer_batch(
                session,
                answer_batch(
                    self.setup,
                    session,
                    [
                        ("setup.project-name", "answered", "Independent Axes", False),
                        ("setup.assurance-profile", "answered", "high-assurance", False),
                        ("setup.write-capable-humans", "answered", 1, True),
                        ("setup.work-finish-mode", "answered", "disabled", False),
                    ],
                ),
                self.catalog,
            )
            value = self.setup.apply_answer_batch(
                value,
                answer_batch(
                    self.setup,
                    value,
                    [
                        ("setup.layout", "answered", "separated", False),
                        ("setup.collaboration-concurrency", "answered", {"human_writers": 1, "agents_or_automation": 25}, True),
                    ],
                ),
                self.catalog,
            )
            self.assertEqual(value["selected_profile"], "high-assurance")
            self.assertEqual(self.setup.answer_value(value, "setup.write-capable-humans"), 1)
            self.assertEqual(self.setup.answer_value(value, "setup.collaboration-concurrency")["agents_or_automation"], 25)

            oversized_target = Path(temporary) / "oversized"
            oversized_target.mkdir()
            oversized = self.setup.create_session("initialization", oversized_target)
            oversized = self.setup.apply_answer_batch(
                oversized,
                answer_batch(
                    self.setup,
                    oversized,
                    [
                        ("setup.write-capable-humans", "answered", 6, True),
                        ("setup.scm-selection", "answered", "git", False),
                    ],
                ),
                self.catalog,
            )
            with self.assertRaisesRegex(self.setup.SetupError, "no supported workflow"):
                self.setup.apply_answer_batch(
                    oversized,
                    answer_batch(
                        self.setup,
                        oversized,
                        [("setup.workflow-selection", "answered", "tiny_pr", True)],
                    ),
                    self.catalog,
                )

    def test_unknown_collaboration_selects_no_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.new_target(Path(temporary), "initialization")
            session = self.setup.create_session("initialization", target)
            value = self.setup.apply_answer_batch(
                session,
                answer_batch(self.setup, session, [("setup.write-capable-humans", "unknown", None, False)]),
                self.catalog,
            )
            self.assertIsNone(self.setup.answer_value(value, "setup.workflow-selection"))
            self.assertNotIn("setup.workflow-selection", {item["question_id"] for item in value["recommendations"]})

    def test_work_completion_selection_stays_pending_without_prerequisites(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.new_target(Path(temporary), "initialization")
            session = self.setup.create_session("initialization", target)
            value = self.setup.apply_answer_batch(
                session,
                answer_batch(
                    self.setup,
                    session,
                    [("setup.work-finish-mode", "answered", "on_demand_plus_plan_only_event", False)],
                ),
                self.catalog,
            )
            assessment = value["work_completion_assessment"]
            self.assertEqual(assessment["status"], "pending_prerequisites")
            self.assertTrue(assessment["missing_prerequisites"])
            self.assertFalse(assessment["external_action_authorization"])
            self.assertTrue(all(item["blocks_enablement"] for item in assessment["closure_sequence"]))
            closure = value["minimum_closure_sequence"]
            self.assertTrue(closure)
            self.assertEqual([item["order"] for item in closure], list(range(1, len(closure) + 1)))
            self.assertTrue(any(item["can_run_in_parallel"] for item in closure))

    def test_optional_package_assessments_create_explicit_parallel_closure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.new_target(Path(temporary), "initialization")
            session = self.setup.create_session("initialization", target)
            session = self.setup.apply_answer_batch(
                session,
                answer_batch(
                    self.setup,
                    session,
                    [
                        (
                            "setup.optional-package-assessments",
                            "answered",
                            {
                                "operations_observability": {
                                    "status": "applicable",
                                    "rationale": "Runtime evidence requires an explicit package plan.",
                                    "evidence_refs": ["evidence:risk-review"],
                                },
                                "security_supply_chain": {
                                    "status": "unknown",
                                    "rationale": "Specialist evidence is not yet available.",
                                    "evidence_refs": [],
                                },
                                "context_packages": {
                                    "status": "not_applicable",
                                    "rationale": "Current reviewed scope has no context-package trigger.",
                                    "evidence_refs": ["evidence:scope-review"],
                                },
                            },
                            True,
                        )
                    ],
                ),
                self.catalog,
            )
            rows = [
                item
                for item in session["minimum_closure_sequence"]
                if item["question_id"] == "setup.optional-package-assessments"
            ]
            self.assertEqual([item["kind"] for item in rows], ["package", "evidence"])
            self.assertTrue(all(item["can_run_in_parallel"] for item in rows))
            self.assertTrue(all(not item["blocks_plan"] for item in rows))
            self.assertNotIn("context packages", " ".join(item["description"] for item in rows))
            invalid_session = self.setup.create_session("initialization", target)
            with self.assertRaisesRegex(self.setup.SetupError, "supported trigger families"):
                self.setup.apply_answer_batch(
                    invalid_session,
                    answer_batch(
                        self.setup,
                        invalid_session,
                        [
                            (
                                "setup.optional-package-assessments",
                                "answered",
                                {
                                    "unsupported": {
                                        "status": "applicable",
                                        "rationale": "Invalid test value.",
                                        "evidence_refs": [],
                                    }
                                },
                                True,
                            )
                        ],
                    ),
                    self.catalog,
                )

    def test_work_completion_becomes_only_eligible_after_every_prerequisite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.new_target(Path(temporary), "upgrade")
            (target / ".agent").mkdir()
            write_json(
                target / ".agent/packages.json",
                {"packages": [{"id": "small-team-git-portfolio"}]},
            )
            before = snapshot(target)
            session = self.setup.create_session("upgrade", target)
            hook = {
                "status": "configured",
                "owner": "project-owner-role",
                "argv": ["python", "-B", ".agent/scripts/validate.py", "--check"],
                "version_argv": ["python", "--version"],
                "timeout_seconds": 120,
                "evidence_freshness_days": 30,
                "repository_write_paths": [],
                "external_effects": [],
                "limitations": ["Structural validation only."],
                "rationale": "Existing project-owned read-only closure check.",
            }
            rows = [
                ("setup.upgrade-authority", "answered", "authority:upgrade-owner", False),
                ("setup.upgrade-evidence", "answered", ["evidence:installed-inventory"], False),
                ("setup.work-finish-mode", "answered", "on_demand", False),
                ("setup.write-capable-humans", "answered", 1, True),
                ("setup.scm-selection", "answered", "git", False),
                (
                    "setup.repository-contract",
                    "answered",
                    {"identity": "example/repository", "remote": "origin", "default_branch": "main"},
                    True,
                ),
                ("setup.workflow-selection", "answered", "solo_direct", True),
                ("setup.workflow-authority", "answered", "authority:DEC-0001", False),
                (
                    "setup.provider-assessment",
                    "answered",
                    {"adapter": "none", "hosted_repository": None, "configuration_is_authority": False},
                    True,
                ),
                (
                    "setup.integration-and-checks",
                    "answered",
                    {
                        "integration_method": "not_applicable",
                        "required_hosted_checks": {"status": "configured", "names": []},
                        "eligible_peer_reviewers": [],
                        "solo_hybrid_pull_request": "not_applicable",
                        "remote_cleanup": "disabled",
                        "local_cleanup": "disabled",
                    },
                    True,
                ),
                ("setup.hook-test", "not_applicable", None, False),
                ("setup.hook-lint", "not_applicable", None, False),
                ("setup.hook-build", "not_applicable", None, False),
                ("setup.hook-closure", "answered", hook, True),
                (
                    "setup.work-finish-local-controls",
                    "answered",
                    {
                        "validation_hooks": ["project_closure"],
                        "git_hooks": "require_none",
                        "core_fsmonitor": "inactive",
                        "assurance_control_refs": [],
                        "completion_hook": "disabled",
                    },
                    True,
                ),
            ]
            session = self.setup.apply_answer_batch(
                session,
                answer_batch(self.setup, session, rows),
                self.catalog,
            )
            assessment = session["work_completion_assessment"]
            self.assertEqual(assessment["status"], "eligible_for_separate_configuration")
            self.assertEqual(assessment["missing_prerequisites"], [])
            self.assertEqual(assessment["closure_sequence"], [])
            self.assertFalse(assessment["external_action_authorization"])
            self.assertEqual(session["minimum_closure_sequence"], [])
            self.assertEqual(snapshot(target), before)

    def test_existing_flags_have_stable_question_mappings(self) -> None:
        expected = {
            "initialization": {"project_name", "profile", "layout", "writer_count", "first_task_title"},
            "adoption": {"project_name", "profile", "authority_source", "proposal", "review"},
            "upgrade": {"authority_source", "evidence_ref", "legacy_seed", "proposal", "review"},
        }
        for mode, names in expected.items():
            mapping = self.setup.mapped_flag_ids(mode)
            self.assertTrue(names <= set(mapping))
            self.assertTrue(all(identifier.startswith("setup.") for identifier in mapping.values()))

    def test_setup_driven_init_plan_is_read_only_digest_bound_and_repeatable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            area = Path(temporary)
            target = self.new_target(area, "initialization")
            session = self.ready_initialization(target)
            session_path = area / "session.json"
            self.setup.write_new_json(session_path, session)
            before = snapshot(target)
            plans = []
            for index in (1, 2):
                plan_path = area / f"plan-{index}.json"
                result = command(
                    [
                        sys.executable,
                        "-B",
                        str(OCTON_SOURCE),
                        "init",
                        "plan",
                        "--target",
                        str(target),
                        "--setup-session",
                        str(session_path),
                        "--output",
                        str(plan_path),
                    ],
                    OCTON_MINI_ROOT,
                )
                self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
                plans.append(json.loads(plan_path.read_text(encoding="utf-8")))
            self.assertEqual(snapshot(target), before)
            self.assertEqual(normalized_plan(plans[0]), normalized_plan(plans[1]))
            evidence_rows = [item for item in plans[0]["source_evidence"] if item["kind"] == self.setup.SETUP_EVIDENCE_KIND]
            self.assertEqual(len(evidence_rows), 1)
            self.setup.verify_plan_binding(target, plans[0])
            recorded_session = area / "session-with-plan.json"
            result = command(
                [
                    sys.executable,
                    "-B",
                    str(OCTON_SOURCE),
                    "init",
                    "setup",
                    "--target",
                    str(target),
                    "--session",
                    str(session_path),
                    "--record-plan",
                    str(area / "plan-1.json"),
                    "--output",
                    str(recorded_session),
                ],
                OCTON_MINI_ROOT,
            )
            self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
            recorded = self.setup.load_session(recorded_session)
            self.assertEqual(
                recorded["generated_plan_references"][0]["canonical_plan_digest"],
                plans[0]["canonical_plan_digest"],
            )
            self.assertEqual(snapshot(target), before)
            (target / "unexpected.txt").write_text("change\n", encoding="utf-8")
            with self.assertRaisesRegex(self.setup.SetupError, "stale"):
                self.setup.verify_plan_binding(target, plans[0])

    def test_nonexistent_initialization_target_is_created_only_by_apply(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            area = Path(temporary)
            target = area / "new-project"
            session = self.ready_initialization(target)
            session_path = area / "session.json"
            plan_path = area / "plan.json"
            self.setup.write_new_json(session_path, session)
            result = command(
                [
                    sys.executable,
                    "-B",
                    str(OCTON_SOURCE),
                    "init",
                    "plan",
                    "--target",
                    str(target),
                    "--setup-session",
                    str(session_path),
                    "--output",
                    str(plan_path),
                ],
                OCTON_MINI_ROOT,
            )
            self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
            self.assertFalse(target.exists())
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            result = command(
                [
                    sys.executable,
                    "-B",
                    str(OCTON_SOURCE),
                    "init",
                    "apply",
                    "--target",
                    str(target),
                    "--plan",
                    str(plan_path),
                    "--accept-digest",
                    plan["canonical_plan_digest"],
                ],
                OCTON_MINI_ROOT,
            )
            self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
            self.assertTrue(target.is_dir())
            self.assertTrue((target / ".octon-mini-origin.json").is_file())
            self.assertIn("structurally conforming", result.stdout)

    def test_direct_explicit_init_plan_without_setup_session_is_supported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            area = Path(temporary)
            target = self.new_target(area, "initialization")
            plan = area / "explicit-inputs.json"
            result = command(
                [
                    sys.executable,
                    "-B",
                    str(OCTON_SOURCE),
                    "init",
                    "plan",
                    "--target",
                    str(target),
                    "--project-name",
                    "Explicit Inputs",
                    "--profile",
                    "minimal",
                    "--output",
                    str(plan),
                ],
                OCTON_MINI_ROOT,
            )
            self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
            value = json.loads(plan.read_text(encoding="utf-8"))
            self.assertFalse(any(item["kind"] == self.setup.SETUP_EVIDENCE_KIND for item in value["source_evidence"]))

    def test_source_dispatcher_delegates_directly_without_root_launcher_recursion(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            scripts = project / ".agent/scripts"
            scripts.mkdir(parents=True)
            write_json(
                project / ".agent/commands.json",
                json.loads(COMMAND_MANIFEST.read_text(encoding="utf-8")),
            )
            (scripts / "octon.py").write_text(
                "import json, sys\n"
                "print(json.dumps({'argv': sys.argv[1:], 'dispatch_count': 1}))\n",
                encoding="utf-8",
            )
            result = command(
                [sys.executable, "-B", str(OCTON_SOURCE), "check", "--json"],
                project,
            )
            self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
            self.assertEqual(
                json.loads(result.stdout),
                {"argv": ["check", "--json"], "dispatch_count": 1},
            )
            self.assertFalse((project / "octon").exists())

    def test_adoption_and_upgrade_setup_preserve_project_owned_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            area = Path(temporary)
            for mode in ("adoption", "upgrade"):
                mode_area = area / mode
                mode_area.mkdir()
                target = self.new_target(mode_area, mode)
                owned = target / "PROJECT-OWNED.md"
                owned.write_text("do not overwrite\n", encoding="utf-8")
                before = snapshot(target)
                session = self.setup.create_session(mode, target)
                fixture = ADOPT_FIXTURE if mode == "adoption" else UPGRADE_FIXTURE
                self.setup.apply_answer_batch(
                    session,
                    with_digest(fixture, session["canonical_session_digest"]),
                    self.catalog,
                )
                self.assertEqual(snapshot(target), before)

    def test_every_mutation_rejects_with_expected_diagnostic(self) -> None:
        inventory = json.loads(MUTATIONS.read_text(encoding="utf-8"))["mutations"]
        observed: dict[str, str] = {}
        with tempfile.TemporaryDirectory() as temporary:
            area = Path(temporary)
            for index, mutation in enumerate(inventory):
                case = area / str(index)
                case.mkdir()
                target = self.new_target(case, "initialization")
                session = self.setup.create_session("initialization", target)
                identifier = mutation["id"]
                try:
                    if identifier in {"catalog-duplicate-id", "catalog-cycle"}:
                        catalog = copy.deepcopy(self.catalog)
                        if identifier == "catalog-duplicate-id":
                            catalog["questions"].append(copy.deepcopy(catalog["questions"][0]))
                        else:
                            catalog["questions"][0]["dependencies"] = [catalog["questions"][-1]["id"]]
                        self.setup.validate_catalog(catalog)
                    elif identifier == "changed-catalog-digest":
                        changed = copy.deepcopy(session)
                        changed["question_catalog"]["sha256"] = "f" * 64
                        changed["canonical_session_digest"] = self.setup.record_digest(changed, "canonical_session_digest")
                        self.setup.validate_session_shape(changed, self.catalog)
                    elif identifier in {"changed-target", "changed-instructions"}:
                        path = target / ("AGENTS.md" if identifier == "changed-instructions" else "changed.txt")
                        path.write_text("changed\n", encoding="utf-8")
                        mismatches = self.setup.current_state_mismatches(session)
                        if not mismatches:
                            raise AssertionError("mutation did not create a mismatch")
                        raise self.setup.SetupError(", ".join(mismatches))
                    else:
                        rows: list[tuple[str, str, object, bool]]
                        if identifier == "duplicate-question-id":
                            rows = [("setup.project-name", "answered", "A", False), ("setup.project-name", "answered", "B", False)]
                        elif identifier == "missing-question-id":
                            payload = answer_batch(
                                self.setup,
                                session,
                                [("setup.project-name", "answered", "A", False)],
                            )
                            del payload["answers"][0]["question_id"]
                            self.setup.apply_answer_batch(session, payload, self.catalog)
                            continue
                        elif identifier == "unknown-question-id":
                            rows = [("setup.unallocated", "answered", "A", False)]
                        elif identifier == "stale-session-digest":
                            payload = answer_batch(self.setup, session, [("setup.project-name", "answered", "A", False)])
                            payload["session_digest"] = "f" * 64
                            self.setup.apply_answer_batch(session, payload, self.catalog)
                            continue
                        elif identifier == "invalid-enum":
                            rows = [("setup.assurance-profile", "answered", "enterprise", False)]
                        elif identifier == "invalid-answer-type":
                            rows = [("setup.assurance-profile", "answered", 3, False)]
                        elif identifier == "premature-dependency":
                            rows = [("setup.layout", "answered", "compact", False)]
                        elif identifier == "selection-laundered-as-authority":
                            target = self.new_target(case / "adopt", "adoption") if (case / "adopt").mkdir() is None else target
                            session = self.setup.create_session("adoption", target)
                            rows = [("setup.adoption-authority", "answered", "owner said yes", False)]
                        elif identifier == "runtime-authorization":
                            rows = [("setup.runtime-authorization", "answered", {"push": True}, False)]
                        elif identifier == "secret-material":
                            rows = [("setup.project-name", "answered", "ghp_12345678901234567890", False)]
                        elif identifier == "missing-freshness-expiry":
                            rows = [("setup.write-capable-humans", "answered", 1, False)]
                        elif identifier == "automatic-apply-choice":
                            rows = [("setup.work-finish-mode", "answered", "automatic_apply", False)]
                        else:
                            raise AssertionError(f"unimplemented mutation: {identifier}")
                        self.setup.apply_answer_batch(session, answer_batch(self.setup, session, rows), self.catalog)
                except (self.setup.SetupError, AssertionError) as error:
                    observed[identifier] = str(error)
            self.assertEqual(set(observed), {item["id"] for item in inventory})
            for mutation in inventory:
                self.assertIn(mutation["expected_diagnostic"], observed[mutation["id"]])


if __name__ == "__main__":
    unittest.main(verbosity=2)
