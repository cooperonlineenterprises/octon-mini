#!/usr/bin/env python3
"""Three-way, fingerprint-bound live-project upgrade planning and application."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import stat
import subprocess
import sys
import tempfile
import types
from datetime import date
from pathlib import Path, PurePosixPath
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


SCAFFOLDER = load_module("pb_upgrade_scaffolder", SCRIPT_ROOT / "scaffold_project.py")
TRANSACTION = load_module(
    "pb_upgrade_transaction",
    SKILL_ROOT / "assets/templates/core/.agent/scripts/pb_transaction.py.tmpl",
)


class UpgradeError(ValueError):
    """A live upgrade is ambiguous, stale, or outside automatic policy."""


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise UpgradeError(f"cannot load {path}: {error}") from error


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")


def version_tuple(value: str) -> tuple[int, int, int]:
    if re.fullmatch(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)", value) is None:
        raise UpgradeError(f"invalid semantic version: {value!r}")
    return tuple(int(part) for part in value.split("."))  # type: ignore[return-value]


def proposal_digest(value: dict[str, Any]) -> str:
    unsigned = dict(value)
    supplied = unsigned.pop("canonical_proposal_digest", None)
    expected = hashlib.sha256(TRANSACTION.canonical_bytes(unsigned)).hexdigest()
    if supplied is not None and supplied != expected:
        raise UpgradeError("upgrade proposal digest is invalid")
    return expected


def candidate_state(candidate: Path, path: str) -> dict[str, Any] | None:
    source = candidate.joinpath(*PurePosixPath(path).parts)
    if not source.exists() or source.is_symlink() or not source.is_file():
        return None
    return {
        "mode": stat.S_IMODE(source.stat().st_mode),
        "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    }


def run_scaffold(target: Path, origin: dict[str, Any]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_ROOT / "scaffold_project.py"),
            "--target",
            str(target),
            "--project-name",
            origin["project_name"],
            "--project-slug",
            origin["project_slug"],
            "--profile",
            origin["profile"],
            "--layout",
            origin["layout"],
        ],
        cwd=SCRIPT_ROOT,
        capture_output=True,
        text=True,
        check=False,
        shell=False,
    )
    if result.returncode:
        raise UpgradeError("cannot generate candidate snapshot: " + (result.stderr or result.stdout)[:2000])


def evidence_record_paths(target: Path, refs: list[str]) -> list[str]:
    found: dict[str, list[str]] = {value: [] for value in refs}
    evidence_root = target / ".agent/evidence"
    if evidence_root.is_dir() and not evidence_root.is_symlink():
        for path in sorted(evidence_root.glob("EVD-*.md")):
            if path.is_symlink() or not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            lines = text.splitlines(keepends=True)
            if not lines or lines[0].strip() != "---":
                continue
            try:
                end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
                value = json.loads("".join(lines[1:end]))
            except (StopIteration, json.JSONDecodeError):
                continue
            record_id = value.get("id") if isinstance(value, dict) else None
            if record_id in found:
                found[record_id].append(path.relative_to(target).as_posix())
    index_path = target / "project-dossier/machine-readable/evidence-index.json"
    if index_path.is_file() and not index_path.is_symlink():
        value = load_json(index_path)
        for record in value.get("evidence", []) if isinstance(value, dict) else []:
            record_id = record.get("id") if isinstance(record, dict) else None
            if record_id in found:
                found[record_id].append(index_path.relative_to(target).as_posix())
    unresolved = [record_id for record_id, paths in found.items() if len(set(paths)) != 1]
    if unresolved:
        raise UpgradeError(
            "every migration evidence reference must resolve exactly once: " + ", ".join(unresolved)
        )
    return sorted({paths[0] for paths in found.values()})


def classification_rows(target: Path, candidate: Path, origin: dict[str, Any]) -> list[dict[str, Any]]:
    inventory = origin.get("installed_inventory")
    if not isinstance(inventory, dict) or inventory.get("schema_version") != "project-blueprint.installed-inventory.v2":
        raise UpgradeError(
            "the recorded old snapshot lacks installed-inventory v2; use the 3.1.0-to-4.0.0 reviewed migration before live automatic upgrade"
        )
    candidate_origin = load_json(candidate / ".project-blueprint-origin.json")
    candidate_inventory = candidate_origin["installed_inventory"]
    old = {item["path"]: item for item in inventory["paths"]}
    new = {item["path"]: item for item in candidate_inventory["paths"]}
    rows: list[dict[str, Any]] = []
    for number, path in enumerate(sorted(set(old) | set(new)), 1):
        old_item = old.get(path)
        new_item = new.get(path)
        policy_item = new_item or old_item
        assert policy_item is not None
        role = policy_item["role"]
        policy = policy_item["upgrade_policy"]
        current = TRANSACTION.path_state(target, path)
        candidate_value = (
            None
            if role in {"derived", "provenance"}
            else candidate_state(candidate, path)
        )
        automatic = False
        reason: str | None = None
        dispositions: list[str] = []
        if role == "derived":
            kind = "derived"
            automatic = True
        elif role == "provenance":
            kind = "provenance"
            automatic = True
        elif old_item is None:
            if current["type"] == "absent":
                kind = "additive"
                automatic = role == "blueprint_implementation_asset" and policy == "exact_pristine_or_additive"
                if not automatic:
                    reason = "new project-owned or governance-bearing path requires review"
                    dispositions = ["accept_candidate", "defer"]
            else:
                kind = "conflicting"
                reason = "candidate addition collides with current project content"
                dispositions = ["accept_candidate", "preserve_current", "defer"]
        elif new_item is None:
            kind = "removed_upstream"
            reason = "deletion is never automatic"
            dispositions = ["preserve_current", "delete", "defer"]
        else:
            pristine = (
                current["type"] == "file"
                and current["sha256"] == old_item.get("sha256")
                and current["mode"] == old_item.get("mode")
            )
            if pristine and candidate_value is not None and (
                candidate_value["sha256"] == current["sha256"]
                and candidate_value["mode"] == current["mode"]
            ):
                kind = "unchanged_from_pristine"
                automatic = True
            elif pristine and role == "blueprint_implementation_asset" and policy == "exact_pristine_or_additive":
                kind = "exact_pristine_update"
                automatic = True
            else:
                kind = "project_modified" if current["type"] == "file" else "conflicting"
                reason = (
                    "instructions, policy, configuration, project facts, stable IDs, or locally modified content require review"
                )
                dispositions = ["accept_candidate", "preserve_current", "defer"]
                if path == ".agent/project.json" and current["type"] == "file":
                    dispositions.insert(1, "merge_version_only")
                    if old_item.get("baseline_blueprint_version") == "3.1.0":
                        dispositions.insert(2, "migrate_legacy_project_contract")
        rows.append(
            {
                "id": f"UPG-{number:04d}",
                "path": path,
                "classification": kind,
                "role": role,
                "upgrade_policy": policy,
                "old_baseline": old_item,
                "current": current,
                "candidate": candidate_value,
                "automatic": automatic,
                "review_reason": reason,
                "allowed_dispositions": dispositions,
            }
        )
    return rows


def build_proposal(
    target: Path,
    origin: dict[str, Any],
    rows: list[dict[str, Any]],
    authority_source: str,
    evidence_refs: list[str],
    legacy_seed_digest: str | None = None,
) -> dict[str, Any]:
    value = {
        "schema_version": "project-blueprint.upgrade-proposal.v1",
        "artifact_kind": "upgrade_proposal",
        "permission_grant": False,
        "created_at": TRANSACTION.utc_timestamp(),
        "target": str(target),
        "from_blueprint_version": origin["blueprint_version"],
        "to_blueprint_version": SCAFFOLDER.blueprint_version(),
        "profile": origin["profile"],
        "layout": origin["layout"],
        "authority_source": authority_source,
        "evidence_refs": sorted(set(evidence_refs)),
        "legacy_seed_digest": legacy_seed_digest,
        "governing_instruction_fingerprint": TRANSACTION.instruction_fingerprint(target),
        "classifications": rows,
        "limitations": [
            "Classification is structural and does not establish target-project readiness.",
            "Project-owned, authority-bearing, modified, deleted, moved, permission, and symlink cases require explicit review.",
            "Derived outputs are regenerated and never treated as migration evidence.",
        ],
    }
    value["canonical_proposal_digest"] = proposal_digest(value)
    return value


def validate_stored_proposal(value: dict[str, Any], target: Path) -> None:
    if (
        value.get("schema_version") != "project-blueprint.upgrade-proposal.v1"
        or value.get("permission_grant") is not False
        or value.get("target") != str(target)
        or value.get("to_blueprint_version") != SCAFFOLDER.blueprint_version()
    ):
        raise UpgradeError("stored upgrade proposal target, version, or authority differs")
    proposal_digest(value)
    if value.get("governing_instruction_fingerprint") != TRANSACTION.instruction_fingerprint(target):
        raise UpgradeError("governing instructions changed after upgrade proposal")
    for row in value.get("classifications", []):
        if TRANSACTION.path_state(target, row["path"]) != row["current"]:
            raise UpgradeError(f"upgrade proposal is stale at {row['path']}")


def review_map(proposal: dict[str, Any], path: Path) -> dict[str, str]:
    review = load_json(path)
    if (
        review.get("schema_version") != "project-blueprint.upgrade-review.v1"
        or review.get("permission_grant") is not False
        or review.get("proposal_digest") != proposal["canonical_proposal_digest"]
    ):
        raise UpgradeError("upgrade review is not bound to the exact proposal digest")
    required = {row["id"]: row for row in proposal["classifications"] if not row["automatic"]}
    dispositions: dict[str, str] = {}
    for item in review.get("dispositions", []):
        if not isinstance(item, dict) or item.get("id") in dispositions:
            raise UpgradeError("upgrade review dispositions must be unique objects")
        row = required.get(item.get("id"))
        if row is None or item.get("disposition") not in row["allowed_dispositions"]:
            raise UpgradeError(f"invalid or unexpected upgrade disposition: {item}")
        if not str(item.get("rationale", "")).strip():
            raise UpgradeError("every upgrade disposition requires a rationale")
        dispositions[item["id"]] = item["disposition"]
    missing = sorted(set(required) - set(dispositions))
    if missing:
        raise UpgradeError("upgrade review must disposition every review item: " + ", ".join(missing))
    deferred = sorted(item for item, disposition in dispositions.items() if disposition == "defer")
    if deferred:
        raise UpgradeError("deferred upgrade conflicts cannot enter an apply plan: " + ", ".join(deferred))
    return dispositions


def next_migration_id(origin: dict[str, Any]) -> str:
    numbers = []
    for item in origin.get("migration_history", []):
        match = re.fullmatch(r"MIG-([0-9]{4})", str(item.get("id"))) if isinstance(item, dict) else None
        if match:
            numbers.append(int(match.group(1)))
    number = max(numbers, default=0) + 1
    if number > 9999:
        raise UpgradeError("migration ID space is exhausted")
    return f"MIG-{number:04d}"


def exact_plan(
    target: Path,
    proposal: dict[str, Any],
    candidate: Path,
    dispositions: dict[str, str],
    evidence_paths: list[str],
    baseline_origin: dict[str, Any] | None = None,
) -> dict[str, Any]:
    current_origin = baseline_origin or load_json(target / ".project-blueprint-origin.json")
    candidate_origin = load_json(candidate / ".project-blueprint-origin.json")
    old_inventory = {item["path"]: item for item in current_origin["installed_inventory"]["paths"]}
    final_contents: dict[str, tuple[bytes, int]] = {}
    operations: list[dict[str, Any]] = []
    preserved: set[str] = set()
    for row in proposal["classifications"]:
        path = row["path"]
        if row["classification"] in {"derived", "provenance", "unchanged_from_pristine"}:
            continue
        disposition = dispositions.get(row["id"])
        take_candidate = row["automatic"] or disposition == "accept_candidate"
        if take_candidate:
            source = candidate.joinpath(*PurePosixPath(path).parts)
            if not source.is_file() or source.is_symlink():
                raise UpgradeError(f"candidate source is absent or unsafe: {path}")
            content = source.read_bytes()
            mode = stat.S_IMODE(source.stat().st_mode)
            action = "create" if row["current"]["type"] == "absent" else "replace"
            operations.append(
                TRANSACTION.operation(action, path, content, "Apply an automatic-safe or explicitly reviewed candidate path.", mode=mode)
            )
            final_contents[path] = (content, mode)
        elif disposition == "merge_version_only":
            if path != ".agent/project.json":
                raise UpgradeError("merge_version_only is limited to .agent/project.json")
            current = load_json(target / path)
            candidate_value = load_json(candidate / path)
            if set(current) != set(candidate_value) or set(current.get("project", {})) != set(candidate_value.get("project", {})):
                raise UpgradeError("project contract shape changed; version-only merge is unsafe")
            current["schema_version"] = candidate_value["schema_version"]
            current["project"]["blueprint_version"] = candidate_value["project"]["blueprint_version"]
            content = json_bytes(current)
            mode = stat.S_IMODE((target / path).stat().st_mode)
            operations.append(
                TRANSACTION.operation("replace", path, content, "Apply only the explicitly reviewed mechanical Blueprint version fields.", mode=mode)
            )
            final_contents[path] = (content, mode)
            preserved.add(path)
        elif disposition == "migrate_legacy_project_contract":
            if path != ".agent/project.json" or proposal["from_blueprint_version"] != "3.1.0":
                raise UpgradeError("legacy project migration is limited to the reviewed 3.1.0 project contract")
            current = load_json(target / path)
            candidate_value = load_json(candidate / path)
            collaboration = current.get("collaboration_profile", {})
            if (
                current.get("schema_version") != "harness.project.v3"
                or collaboration.get("schema_version") != "harness.collaboration-profile.v1"
                or collaboration.get("assessment_status") != "not_assessed"
            ):
                raise UpgradeError("legacy project contract has assessed or unsupported collaboration state")
            migrated = {
                "schema_version": candidate_value["schema_version"],
                "project": dict(current["project"]),
                "collaboration_profile": candidate_value["collaboration_profile"],
                "paths": current["paths"],
                "commands": current["commands"],
                "project_checks": candidate_value["project_checks"],
                "packages": candidate_value["packages"],
                "mutable_work_status": current["mutable_work_status"],
            }
            migrated["project"]["blueprint_version"] = proposal["to_blueprint_version"]
            content = json_bytes(migrated)
            mode = stat.S_IMODE((target / path).stat().st_mode)
            operations.append(
                TRANSACTION.operation(
                    "replace",
                    path,
                    content,
                    "Migrate the explicitly reviewed unassessed 3.1 project contract without inferring collaboration, hooks, packages, authority, or readiness.",
                    mode=mode,
                )
            )
            final_contents[path] = (content, mode)
            preserved.add(path)
        elif disposition == "delete":
            operations.append(TRANSACTION.operation("delete", path, None, "Perform an explicitly reviewed upstream deletion."))
        else:
            preserved.add(path)

    candidate_inventory = candidate_origin["installed_inventory"]
    for item in candidate_inventory["paths"]:
        path = item["path"]
        if item["role"] in {"derived", "provenance"}:
            continue
        if path in final_contents and path not in preserved:
            content, mode = final_contents[path]
            item["sha256"] = hashlib.sha256(content).hexdigest()
            item["mode"] = mode
            item["baseline_blueprint_version"] = proposal["to_blueprint_version"]
        elif path in preserved:
            old = old_inventory.get(path)
            if old is not None:
                item.update(
                    baseline_blueprint_version=old["baseline_blueprint_version"],
                    sha256=old["sha256"],
                    mode=old["mode"],
                )

    guide = f"migrations/{proposal['from_blueprint_version']}-to-{proposal['to_blueprint_version']}.md"
    if not (SCAFFOLDER.blueprint_root() / guide).is_file():
        raise UpgradeError(f"migration guide is absent: {guide}")
    candidate_origin["initial_generation"] = current_origin["initial_generation"]
    candidate_origin["migration_history"] = [
        *current_origin.get("migration_history", []),
        {
            "schema_version": "project-blueprint.migration.v2",
            "id": next_migration_id(current_origin),
            "from_blueprint_version": proposal["from_blueprint_version"],
            "to_blueprint_version": proposal["to_blueprint_version"],
            "generator_version": SCAFFOLDER.GENERATOR_VERSION,
            "migrated_on": date.today().isoformat(),
            "from_profile": current_origin["profile"],
            "to_profile": candidate_origin["profile"],
            "from_layout": current_origin["layout"],
            "to_layout": candidate_origin["layout"],
            "migration_guide": guide,
            "authority_source": proposal["authority_source"],
            "evidence_refs": proposal["evidence_refs"],
            "limitations": [
                "Structural upgrade does not establish harness adoption or target-project readiness.",
                "Project-modified paths retain their prior pristine baseline for future three-way review.",
            ],
        },
    ]
    operations.append(
        TRANSACTION.operation(
            "replace",
            ".project-blueprint-origin.json",
            json_bytes(candidate_origin),
            "Record the independent upgraded snapshot, installed baselines, and migration provenance.",
        )
    )
    validators = load_json(candidate / ".agent/validators.json")
    derived = validators["commands"]["refresh"]["writes"]
    return TRANSACTION.build_plan(
        target,
        operation_name="upgrade.project",
        scope=f"Upgrade Project Blueprint {proposal['from_blueprint_version']} to {proposal['to_blueprint_version']}",
        operations=operations,
        evidence=[
            TRANSACTION.source_evidence("accepted_upgrade_proposal", proposal["canonical_proposal_digest"]),
            TRANSACTION.source_evidence("project_owned_upgrade_authority", proposal["authority_source"]),
            *[TRANSACTION.source_evidence("migration_evidence", value) for value in proposal["evidence_refs"]],
        ],
        evidence_paths=[".project-blueprint-origin.json", *evidence_paths],
        assumptions=[],
        confidence="deterministic",
        limitations=proposal["limitations"],
        analysis={
            "observations": [
                {
                    "id": "upgrade.three_way_classification",
                    "summary": "Recorded old baselines, current path states, and candidate bytes were classified path by path.",
                    "source_refs": [".project-blueprint-origin.json", proposal["canonical_proposal_digest"]],
                    "rule": "installed_inventory_three_way_v1",
                    "confidence": "deterministic",
                    "limitations": ["Renames are never inferred from content similarity."],
                }
            ],
            "inferences": [],
            "explicit_decisions": [
                {
                    "id": "upgrade.review_dispositions",
                    "summary": "Every non-automatic path has an exact proposal-bound disposition.",
                    "source_refs": [proposal["canonical_proposal_digest"], proposal["authority_source"]],
                    "rule": None,
                    "confidence": "deterministic",
                    "limitations": ["Plan acceptance applies only to this digest and these preimages."],
                }
            ],
            "authorization_gates": [],
        },
        derived_write_paths=derived,
        staged_validation_plan=[
            [sys.executable, "-B", ".agent/scripts/refresh.py", "--refresh"],
            [sys.executable, "-B", ".agent/scripts/validate.py", "--check"],
            [sys.executable, "-B", ".agent/tests/test_validate.py", "--tier", "release"],
        ],
        post_apply_validation_plan=[
            [sys.executable, "-B", ".agent/scripts/validate.py", "--check"]
        ],
    )


def write_artifact(path: Path, value: dict[str, Any]) -> None:
    TRANSACTION.write_new_json(path, value)
    digest = value.get("canonical_plan_digest") or value.get("canonical_proposal_digest")
    print(f"[PLAN] {path}")
    print(f"[DIGEST] {digest}")


def plan_command(args: argparse.Namespace) -> int:
    target = args.target.resolve()
    actual_origin = load_json(target / ".project-blueprint-origin.json")
    legacy_seed: dict[str, Any] | None = None
    if args.legacy_seed:
        legacy_seed = load_json(args.legacy_seed)
        unsigned = dict(legacy_seed)
        supplied_seed_digest = unsigned.pop("canonical_seed_digest", None)
        expected_seed_digest = hashlib.sha256(TRANSACTION.canonical_bytes(unsigned)).hexdigest()
        if (
            legacy_seed.get("schema_version")
            != "project-blueprint.migration-seed.3.1.0-to-4.0.0.v1"
            or legacy_seed.get("permission_grant") is not False
            or legacy_seed.get("target") != str(target)
            or supplied_seed_digest != expected_seed_digest
            or legacy_seed.get("source_origin_state")
            != TRANSACTION.path_state(target, ".project-blueprint-origin.json")
            or legacy_seed.get("source_project_state")
            != TRANSACTION.path_state(target, ".agent/project.json")
        ):
            raise UpgradeError("legacy migration seed is malformed, stale, or targets another project")
        origin = legacy_seed["origin_seed"]
    else:
        origin = actual_origin
    if origin.get("schema_version") != "project-blueprint.origin.v2":
        raise UpgradeError("live upgrade requires origin v2 provenance or an exact reviewed --legacy-seed")
    if not args.authority_source.startswith(("authority:", "external:")):
        raise UpgradeError("--authority-source must be a current project-owned authority reference")
    to_version = SCAFFOLDER.blueprint_version()
    if version_tuple(to_version) <= version_tuple(origin["blueprint_version"]):
        raise UpgradeError("candidate Blueprint version must be newer than the recorded snapshot")
    evidence_paths = evidence_record_paths(target, args.evidence_ref)
    if legacy_seed is not None and (
        legacy_seed.get("authority_source") != args.authority_source
        or sorted(legacy_seed.get("evidence_refs", [])) != sorted(set(args.evidence_ref))
    ):
        raise UpgradeError("authority or evidence differs from the reviewed legacy migration seed")
    with tempfile.TemporaryDirectory(prefix="project-blueprint-upgrade-") as temporary:
        candidate = Path(temporary) / "candidate"
        run_scaffold(candidate, origin)
        if args.proposal:
            proposal = load_json(args.proposal)
            validate_stored_proposal(proposal, target)
            if proposal["authority_source"] != args.authority_source or sorted(proposal["evidence_refs"]) != sorted(set(args.evidence_ref)):
                raise UpgradeError("authority or evidence differs from the stored proposal")
            expected_legacy_digest = legacy_seed.get("canonical_seed_digest") if legacy_seed else None
            if proposal.get("legacy_seed_digest") != expected_legacy_digest:
                raise UpgradeError("legacy migration seed differs from the stored proposal")
            rows = classification_rows(target, candidate, origin)
            stable_rows = [{key: value for key, value in row.items()} for row in rows]
            if stable_rows != proposal["classifications"]:
                raise UpgradeError("candidate or classification changed after proposal; re-plan")
            if not args.review:
                raise UpgradeError("--proposal requires its exact --review file")
            dispositions = review_map(proposal, args.review)
            value = exact_plan(
                target,
                proposal,
                candidate,
                dispositions,
                evidence_paths,
                baseline_origin=origin,
            )
            write_artifact(args.output, value)
            return 0
        rows = classification_rows(target, candidate, origin)
        proposal = build_proposal(
            target,
            origin,
            rows,
            args.authority_source,
            args.evidence_ref,
            legacy_seed_digest=(legacy_seed.get("canonical_seed_digest") if legacy_seed else None),
        )
        review_required = any(not row["automatic"] for row in rows)
        if review_required:
            write_artifact(args.output, proposal)
            print("[REVIEW REQUIRED] disposition every non-automatic UPG item in a proposal-bound review file")
            return 3
        value = exact_plan(
            target,
            proposal,
            candidate,
            {},
            evidence_paths,
            baseline_origin=origin,
        )
        write_artifact(args.output, value)
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan/apply a three-way Project Blueprint live upgrade")
    commands = parser.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("plan")
    plan.add_argument("--target", type=Path, required=True)
    plan.add_argument("--authority-source", required=True)
    plan.add_argument("--evidence-ref", action="append", required=True)
    plan.add_argument("--legacy-seed", type=Path)
    plan.add_argument("--proposal", type=Path)
    plan.add_argument("--review", type=Path)
    plan.add_argument("--output", type=Path, required=True)
    apply = commands.add_parser("apply")
    apply.add_argument("--target", type=Path, required=True)
    apply.add_argument("--plan", type=Path, required=True)
    apply.add_argument("--accept-digest", required=True)
    args = parser.parse_args()
    try:
        if args.command == "plan":
            return plan_command(args)
        target = args.target.resolve()
        value = TRANSACTION.load_plan(args.plan)
        if value.get("operation") != "upgrade.project":
            raise UpgradeError("plan is not a live-upgrade transaction")
        receipt, receipt_path = TRANSACTION.apply_plan(target, value, args.accept_digest)
        print(f"[APPLIED] {receipt['receipt_id']}")
        print(f"[RECEIPT] {receipt_path}")
        print("[STATUS] structural conformance passed; adoption and readiness were not inferred")
        return 0
    except (OSError, RuntimeError, ValueError, UpgradeError, TRANSACTION.TransactionError) as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
