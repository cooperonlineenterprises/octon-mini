#!/usr/bin/env python3
"""Guided, previewable plan/apply initialization for new Project Blueprint projects."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import types
from pathlib import Path
from typing import Any


SCRIPT_ROOT = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_ROOT.parent


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


SCAFFOLDER = load_module("pb_init_scaffolder", SCRIPT_ROOT / "scaffold_project.py")
DETECTOR = load_module("pb_init_detector", SCRIPT_ROOT / "detect_project.py")
COLLABORATION = load_module("pb_init_collaboration", SCRIPT_ROOT / "collaboration_project.py")
TRANSACTION = load_module(
    "pb_init_transaction",
    SKILL_ROOT / "assets/templates/core/.agent/scripts/pb_transaction.py.tmpl",
)


class InitError(ValueError):
    """Initialization cannot safely continue from the supplied explicit inputs."""


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def run(argv: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, check=False, shell=False)
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise InitError(f"command failed ({' '.join(argv[:3])}): {detail[:1000]}")
    return result


def ensure_target_container(target: Path) -> None:
    if not target.exists():
        if not target.parent.is_dir():
            raise InitError("target parent must already exist")
        target.mkdir()
    if target.is_symlink() or not target.is_dir():
        raise InitError("target must be a real directory")
    unexpected: list[str] = []
    for child in target.iterdir():
        if child.name == ".git":
            continue
        if child.name == ".agent" and child.is_dir() and not child.is_symlink():
            allowed = child / "transactions"
            if all(
                path == allowed or allowed in path.parents
                for path in child.rglob("*")
            ):
                continue
        unexpected.append(child.name)
    if unexpected:
        raise InitError(
            "guided init is only for a new project; existing content requires `pb adopt plan`: "
            + ", ".join(sorted(unexpected))
        )


def first_task_requested(args: argparse.Namespace) -> bool:
    names = (
        "first_task_title",
        "first_task_scope",
        "first_task_authority_basis",
        "first_task_owner",
        "first_task_operator",
        "first_task_acceptance",
        "first_task_validation",
        "first_task_next_action",
    )
    values = [getattr(args, name) for name in names]
    requested = any(value not in (None, []) for value in values)
    if requested and any(value in (None, []) for value in values):
        missing = [name.replace("_", "-") for name, value in zip(names, values, strict=True) if value in (None, [])]
        raise InitError("first-task creation requires all explicit semantic inputs; missing: " + ", ".join(missing))
    return requested


def create_candidate(args: argparse.Namespace, destination: Path) -> None:
    run(
        [
            sys.executable,
            str(SCRIPT_ROOT / "scaffold_project.py"),
            "--target",
            str(destination),
            "--project-name",
            args.project_name,
            "--profile",
            args.profile,
            "--layout",
            args.layout,
            *(["--project-slug", args.project_slug] if args.project_slug else []),
        ],
        SCRIPT_ROOT,
    )

    if args.writer_count is not None:
        collaboration_args = argparse.Namespace(
            writer_count=args.writer_count,
            source=args.collaboration_source,
            observed_at=args.collaboration_observed_at,
            expires_at=args.collaboration_expires_at,
            limitation=args.collaboration_limitation,
            solo_integration_preference=args.solo_integration_preference,
            independent_review_capacity=args.independent_review_capacity,
            concurrent_humans=args.concurrent_humans,
            concurrent_agents=args.concurrent_agents,
            external_contribution_mode=args.external_contribution_mode,
            adoption_decision_ref=None,
        )
        profile, _ = COLLABORATION.assessed_profile(collaboration_args)
        project_path = destination / ".agent/project.json"
        project = load_json(project_path)
        project["collaboration_profile"] = profile
        write_json(project_path, project)

    if first_task_requested(args):
        with tempfile.TemporaryDirectory(prefix="project-blueprint-first-task-") as temporary:
            plan_path = Path(temporary) / "first-task.json"
            command = [
                str(destination / "pb"),
                "work",
                "start",
                "--title",
                args.first_task_title,
                "--scope",
                args.first_task_scope,
                "--authority-basis",
                args.first_task_authority_basis,
                "--owner",
                args.first_task_owner,
                "--operator",
                args.first_task_operator,
                "--next-action",
                args.first_task_next_action,
                "--output",
                str(plan_path),
            ]
            for value in args.first_task_acceptance:
                command.extend(("--acceptance", value))
            for value in args.first_task_validation:
                command.extend(("--validation", value))
            run(command, destination)
            digest = load_json(plan_path)["canonical_plan_digest"]
            run(
                [
                    str(destination / "pb"),
                    "transaction",
                    "apply",
                    "--plan",
                    str(plan_path),
                    "--accept-digest",
                    digest,
                ],
                destination,
            )
        transaction_root = destination / ".agent/transactions"
        if transaction_root.exists():
            shutil.rmtree(transaction_root)

    run([sys.executable, "-B", ".agent/scripts/refresh.py", "--refresh"], destination)
    run([sys.executable, "-B", ".agent/scripts/validate.py", "--check"], destination)


def analysis_for(args: argparse.Namespace, detection: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    observations: list[dict[str, Any]] = []
    inferences: list[dict[str, Any]] = []
    for index, item in enumerate(detection.get("archetype_candidates", []), 1):
        refs = [f"repo:{value['path']}" for value in item.get("evidence", [])]
        observations.append(
            {
                "id": f"init.archetype_observation_{index}",
                "summary": f"Detector recipe {item['recipe_id']} observed archetype candidate {item['id']}.",
                "source_refs": refs,
                "rule": item.get("rule"),
                "confidence": item.get("confidence", "low"),
                "limitations": item.get("limitations", []),
            }
        )
    for index, item in enumerate(detection.get("hook_candidates", []), 1):
        inferences.append(
            {
                "id": f"init.hook_proposal_{index}",
                "summary": f"Reviewable hook candidate {item.get('hook')} uses argv {item.get('argv')}.",
                "source_refs": [f"repo:{value['path']}" for value in item.get("evidence", [])],
                "rule": item.get("recipe_id"),
                "confidence": item.get("confidence", "low"),
                "limitations": item.get("limitations", []),
            }
        )
    decisions = [
        {
            "id": "init.profile_and_layout",
            "summary": f"Explicit initialization input selects {args.profile} assurance with {args.layout} physical layout.",
            "source_refs": ["cli:--profile", "cli:--layout"],
            "rule": None,
            "confidence": "deterministic",
            "limitations": ["Profile selection does not establish project readiness."],
        }
    ]
    if args.writer_count is not None:
        decisions.append(
            {
                "id": "init.collaboration_facts",
                "summary": "Explicit, expiring aggregate collaboration facts seed a proposed workflow without adoption.",
                "source_refs": [args.collaboration_source],
                "rule": "progressive_collaboration_v2",
                "confidence": "high",
                "limitations": ["No collaborator identity or permission is recorded."],
            }
        )
    if first_task_requested(args):
        decisions.append(
            {
                "id": "init.first_task_semantics",
                "summary": "The first meaningful task uses only explicitly supplied purpose, scope, authority basis, acceptance, ownership, and validation semantics.",
                "source_refs": ["cli:first-task-inputs"],
                "rule": None,
                "confidence": "deterministic",
                "limitations": ["Task creation does not claim completion or authorize external effects."],
            }
        )
    return {
        "observations": observations,
        "inferences": inferences,
        "explicit_decisions": decisions,
        "authorization_gates": [],
    }


def build_plan(args: argparse.Namespace) -> dict[str, Any]:
    target = args.target.expanduser().resolve()
    ensure_target_container(target)
    detection = DETECTOR.detect(target)
    with tempfile.TemporaryDirectory(prefix="project-blueprint-init-") as temporary:
        candidate = Path(temporary) / "project"
        create_candidate(args, candidate)
        validators = load_json(candidate / ".agent/validators.json")
        derived_paths = validators.get("commands", {}).get("refresh", {}).get("writes", [])
        if not isinstance(derived_paths, list) or any(not isinstance(item, str) for item in derived_paths):
            raise InitError("candidate refresh write contract is malformed")
        derived_set = set(derived_paths)
        operations: list[dict[str, Any]] = []
        for path in sorted(candidate.rglob("*")):
            if path.is_symlink() or (not path.is_file()):
                continue
            relative = path.relative_to(candidate).as_posix()
            if relative.startswith(".agent/transactions/") or relative in derived_set:
                continue
            operations.append(
                TRANSACTION.operation(
                    "create",
                    relative,
                    path.read_bytes(),
                    "Create an exact file from the reviewed guided-initialization candidate.",
                    mode=stat.S_IMODE(path.stat().st_mode),
                )
            )
        profile_manifest = SCAFFOLDER.blueprint_root() / SCAFFOLDER.PROFILE_MANIFEST_RELATIVE
        return TRANSACTION.build_plan(
            target,
            operation_name="init.project",
            scope=f"Initialize {args.project_name} as a {args.profile} Project Blueprint snapshot",
            operations=operations,
            derived_write_paths=derived_paths,
            staged_validation_plan=[
                [sys.executable, "-B", ".agent/scripts/refresh.py", "--refresh"],
                [sys.executable, "-B", ".agent/scripts/validate.py", "--check"],
                [sys.executable, "-B", ".agent/tests/test_validate.py", "--tier", "release"],
            ],
            post_apply_validation_plan=[
                [sys.executable, "-B", ".agent/scripts/validate.py", "--check"]
            ],
            evidence=[
                TRANSACTION.source_evidence(
                    "authoritative_profile_manifest",
                    str(profile_manifest),
                    content=profile_manifest.read_bytes(),
                ),
                TRANSACTION.source_evidence(
                    "bounded_archetype_detection",
                    f"target-fingerprint:{detection['target_fingerprint']}",
                    limitations=detection["limitations"],
                ),
            ],
            assumptions=[],
            confidence="deterministic",
            limitations=[
                "Generation establishes structural conformance only.",
                "Harness adoption and target-project readiness remain explicit and separate.",
                "Hook candidates remain proposals and are not configured or executed.",
            ],
            analysis=analysis_for(args, detection),
        )


def add_common(parser: argparse.ArgumentParser, *, profile_required: bool) -> None:
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--project-slug")
    parser.add_argument("--profile", choices=("minimal", "standard", "high-assurance"), required=profile_required)
    parser.add_argument("--layout", choices=("compact", "separated"), default="compact")
    parser.add_argument("--writer-count", type=int)
    parser.add_argument("--collaboration-source")
    parser.add_argument("--collaboration-observed-at")
    parser.add_argument("--collaboration-expires-at")
    parser.add_argument("--collaboration-limitation", action="append", default=[])
    parser.add_argument("--solo-integration-preference", choices=("direct", "reviewable"))
    parser.add_argument("--independent-review-capacity", choices=("yes", "no"))
    parser.add_argument("--concurrent-humans", type=int)
    parser.add_argument("--concurrent-agents", type=int)
    parser.add_argument("--external-contribution-mode")
    parser.add_argument("--first-task-title")
    parser.add_argument("--first-task-scope")
    parser.add_argument("--first-task-authority-basis")
    parser.add_argument("--first-task-owner")
    parser.add_argument("--first-task-operator")
    parser.add_argument("--first-task-acceptance", action="append", default=[])
    parser.add_argument("--first-task-validation", action="append", default=[])
    parser.add_argument("--first-task-next-action")


def validate_collaboration_inputs(args: argparse.Namespace) -> None:
    if args.writer_count is None:
        related = (
            args.collaboration_source,
            args.collaboration_observed_at,
            args.collaboration_expires_at,
            args.solo_integration_preference,
            args.independent_review_capacity,
            args.concurrent_humans,
            args.concurrent_agents,
            args.external_contribution_mode,
        )
        if any(value is not None for value in related):
            raise InitError("collaboration inputs require --writer-count")
        return
    if not all((args.collaboration_source, args.collaboration_observed_at, args.collaboration_expires_at)):
        raise InitError("--writer-count requires source, observed-at, and expires-at evidence")


def main() -> int:
    parser = argparse.ArgumentParser(description="Guided Project Blueprint initialization")
    commands = parser.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("plan")
    add_common(plan, profile_required=True)
    plan.add_argument("--output", type=Path, required=True)
    apply = commands.add_parser("apply")
    apply.add_argument("--target", type=Path, required=True)
    apply.add_argument("--plan", type=Path, required=True)
    apply.add_argument("--accept-digest", required=True)
    interactive = commands.add_parser("interactive")
    add_common(interactive, profile_required=False)
    interactive.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "apply":
            target = args.target.expanduser().resolve()
            value = TRANSACTION.load_plan(args.plan)
            if value.get("operation") != "init.project":
                raise InitError("plan is not a guided-initialization transaction")
            receipt, receipt_path = TRANSACTION.apply_plan(target, value, args.accept_digest)
            print(f"[APPLIED] {receipt['receipt_id']}")
            print(f"[RECEIPT] {receipt_path}")
            print("[STATUS] structurally conforming; adoption and readiness remain unassessed")
            return 0
        if args.command == "interactive":
            if not sys.stdin.isatty():
                raise InitError("interactive init requires a terminal; use `init plan` with explicit --profile")
            if args.profile is None:
                print("[PROPOSAL] Minimal assurance (collaboration size is assessed separately).")
                if input("Select Minimal? [y/N] ").strip().lower() not in {"y", "yes"}:
                    raise InitError("profile was not explicitly confirmed")
                args.profile = "minimal"
            output = args.output or args.target / ".agent/transactions/plans/init.json"
        else:
            output = args.output
        validate_collaboration_inputs(args)
        value = build_plan(args)
        TRANSACTION.write_new_json(output, value)
        print(f"[PLAN] {output}")
        print(f"[DIGEST] {value['canonical_plan_digest']}")
        print(json.dumps(value["analysis"], indent=2, sort_keys=True))
        if args.command == "interactive":
            reviewed = input("Apply exactly this digest? [y/N] ").strip().lower()
            if reviewed not in {"y", "yes"}:
                print("[NOT APPLIED] plan remains reviewable")
                return 0
            receipt, receipt_path = TRANSACTION.apply_plan(
                args.target.expanduser().resolve(), value, value["canonical_plan_digest"]
            )
            print(f"[APPLIED] {receipt['receipt_id']}")
            print(f"[RECEIPT] {receipt_path}")
        return 0
    except (OSError, RuntimeError, ValueError, InitError, TRANSACTION.TransactionError) as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
