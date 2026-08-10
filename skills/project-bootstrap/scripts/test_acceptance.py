#!/usr/bin/env python3
"""End-to-end and adversarial acceptance suite for Project Blueprint."""

from __future__ import annotations

import hashlib
import json
import os
import runpy
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath, PureWindowsPath


SKILL_ROOT = Path(__file__).resolve().parents[1]
SOURCE_CANDIDATE = SKILL_ROOT.parents[1]
BUNDLED_CANDIDATE = SKILL_ROOT / "assets/blueprint-source"
ROOT = (
    SOURCE_CANDIDATE
    if (SOURCE_CANDIDATE / "blueprint.json").is_file()
    else BUNDLED_CANDIDATE
)
SCAFFOLDER = SKILL_ROOT / "scripts/scaffold_project.py"
PLANNER = SKILL_ROOT / "scripts/plan_adoption.py"
INSTALLER = SKILL_ROOT / "scripts/install_skill.py"
MIGRATION_TEST = SKILL_ROOT / "scripts/test_migration_1_0_1_to_2_0_0.py"
PROFILES = ("minimal", "standard", "high-assurance")
PRODUCTION_EXTENSIONS = {
    "operations-observability",
    "security-supply-chain",
}
ACCEPTANCE_COVERAGE = {
    1: "project_demonstration_required",
    2: "automated_pass",
    3: "project_demonstration_required",
    4: "automated_pass",
    5: "automated_pass",
    6: "automated_pass",
    7: "automated_pass",
    8: "automated_pass",
    9: "automated_pass",
    10: "automated_pass",
    11: "project_demonstration_required",
    12: "automated_pass",
    13: "project_demonstration_required",
    14: "project_demonstration_required",
}


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def require(
    condition: bool,
    message: str,
    failures: list[str],
) -> None:
    if not condition:
        failures.append(message)


def generate(target: Path, profile: str, name: str) -> subprocess.CompletedProcess[str]:
    return run(
        [
            sys.executable,
            "-B",
            str(SCAFFOLDER),
            "--target",
            str(target),
            "--project-name",
            name,
            "--profile",
            profile,
        ],
        ROOT,
    )


def check_project(target: Path) -> subprocess.CompletedProcess[str]:
    return run(
        [
            sys.executable,
            "-I",
            "-B",
            ".agent/scripts/validate.py",
            "--check",
        ],
        target,
    )


def ready_frontier_project(target: Path) -> subprocess.CompletedProcess[str]:
    return run(
        [
            sys.executable,
            "-I",
            "-B",
            ".agent/scripts/validate.py",
            "--ready-frontier",
        ],
        target,
    )


def refresh(target: Path) -> subprocess.CompletedProcess[str]:
    return run(
        [
            sys.executable,
            "-I",
            "-B",
            ".agent/scripts/refresh.py",
            "--refresh",
        ],
        target,
    )


def write_task(
    target: Path,
    task_id: str,
    status: str,
    previous: str | None,
    dependencies: list[str],
    *,
    prepared: bool = False,
) -> None:
    value = {
        "schema_version": "harness.task.v2",
        "id": task_id,
        "status": status,
        "previous_status": previous,
        "title": "Acceptance mutation",
        "authority_basis": "authority:synthetic-test",
        "owner": "acceptance-suite",
        "created_at": "2030-01-02",
        "updated_at": "2030-01-02",
        "dependencies": dependencies,
        "plan_item_refs": [],
        "gate_refs": [],
        "blocking_refs": [],
        "scope": "Synthetic acceptance mutation only.",
        "acceptance_criteria": ["Synthetic acceptance criterion"] if prepared else [],
        "validation_plan": ["Synthetic validation plan"] if prepared else [],
        "implementation_result": None,
        "review_evidence": [],
        "blocked_by": [],
        "reopened_by": None,
        "acceptance_criteria_met": False,
        "closure_evidence": [],
        "external_effects": "none",
        "limitations": [],
    }
    path = target / ".agent/tasks" / f"{task_id}-mutation.md"
    path.write_text(
        "---\n" + json.dumps(value, indent=2) + "\n---\n\n# Mutation\n",
        encoding="utf-8",
    )


def write_accepted_decision(target: Path, decision_id: str) -> None:
    template = (target / ".agent/templates/decision.md").read_text(encoding="utf-8")
    header_end = template.find("\n---\n", 4)
    value = json.loads(template[4:header_end])
    value.update(
        id=decision_id,
        status="accepted",
        previous_status="proposed",
        title="Trust packaged sample restriction extension",
        authority_source="authority:synthetic-acceptance",
        owner="acceptance-suite",
        scope="sample-restriction extension at the generated revision",
    )
    path = target / ".agent/decisions" / f"{decision_id}-extension-trust.md"
    path.write_text(
        "---\n" + json.dumps(value, indent=2, sort_keys=True)
        + "\n---\n\n# Synthetic acceptance decision\n",
        encoding="utf-8",
    )


def write_passing_evidence(
    target: Path,
    evidence_id: str,
    task_id: str,
) -> None:
    value = {
        "schema_version": "harness.evidence.v1",
        "id": evidence_id,
        "title": "Synthetic extension contract evidence",
        "task": task_id,
        "recorded_at": "2030-01-02",
        "authority_source": "authority:synthetic-acceptance",
        "owner": "acceptance-suite",
        "scope": "Generated extension integration test only.",
        "method": "Repository-contained deterministic fixture validation.",
        "environment": "Temporary acceptance project.",
        "subject_revision_or_fingerprint": "synthetic-extension-fixture-v1",
        "result": "pass",
        "fresh_until": "2099-12-31",
        "supersedes": None,
        "limitations": [
            "Synthetic evidence does not establish an external production control."
        ],
    }
    path = target / ".agent/evidence" / f"{evidence_id}-extension-fixture.md"
    path.write_text(
        "---\n" + json.dumps(value, indent=2, sort_keys=True)
        + "\n---\n\n# Synthetic extension evidence\n",
        encoding="utf-8",
    )


def main() -> int:
    if sys.version_info < (3, 11):
        print("FAIL: Python 3.11+ is required")
        return 2
    failures: list[str] = []
    scaffolder_namespace = runpy.run_path(str(SCAFFOLDER))
    canonical_posix_paths = scaffolder_namespace["canonical_posix_paths"]
    refresh_path_values = (
        "project-dossier/ARTIFACT_CATALOG.json",
        "project-dossier/MANIFEST.json",
        "project-dossier/machine-readable/path-authority.json",
    )
    expected_refresh_paths = sorted(refresh_path_values)
    windows_native_order = [
        path.as_posix()
        for path in sorted(PureWindowsPath(value) for value in refresh_path_values)
    ]
    require(
        windows_native_order != expected_refresh_paths,
        "cross-platform ordering fixture does not expose Windows path ordering",
        failures,
    )
    require(
        canonical_posix_paths(
            PurePosixPath(value) for value in refresh_path_values
        )
        == expected_refresh_paths
        and canonical_posix_paths(
            PureWindowsPath(value) for value in refresh_path_values
        )
        == expected_refresh_paths,
        "scaffolder path rendering is not deterministic across host platforms",
        failures,
    )
    migration_result = run(
        [sys.executable, "-B", str(MIGRATION_TEST)],
        ROOT,
    )
    require(
        migration_result.returncode == 0,
        "executable 1.0.1 to 2.0.0 migration fixtures failed: "
        f"{migration_result.stderr or migration_result.stdout}",
        failures,
    )
    with tempfile.TemporaryDirectory(prefix="project-blueprint-acceptance-") as temp:
        temp_root = Path(temp)
        projects: dict[str, Path] = {}
        names = {
            "minimal": 'A "Quoted" Project: [α]',
            "standard": "Standard Cross-Domain Initiative",
            "high-assurance": "High Assurance Hybrid Initiative",
        }
        for profile in PROFILES:
            target = temp_root / profile
            result = generate(target, profile, names[profile])
            require(
                result.returncode == 0,
                f"{profile} generation failed: {result.stderr or result.stdout}",
                failures,
            )
            if result.returncode:
                continue
            projects[profile] = target
            project_json = json.loads(
                (target / ".agent/project.json").read_text(encoding="utf-8")
            )
            require(
                project_json["project"]["name"] == names[profile],
                f"{profile} project name was not JSON-safe",
                failures,
            )
            require(
                project_json["project"]["adoption_status"] == "not_assessed"
                and project_json["project"]["adoption_decision_ref"] is None
                and all(
                    command["status"] == "not_assessed"
                    for command in project_json["commands"].values()
                ),
                f"{profile} generation fabricated project adoption or command assessment",
                failures,
            )
            extension_registry_path = target / ".agent/extensions/registry.json"
            if profile == "minimal":
                require(
                    not extension_registry_path.exists()
                    and not (target / ".agent/extensions/operations-observability").exists()
                    and not (target / ".agent/extensions/security-supply-chain").exists(),
                    "minimal inherited production-control extensions",
                    failures,
                )
            else:
                extension_registry = json.loads(
                    extension_registry_path.read_text(encoding="utf-8")
                )
                extension_by_id = {
                    item["id"]: item for item in extension_registry["extensions"]
                }
                require(
                    PRODUCTION_EXTENSIONS <= set(extension_by_id),
                    f"{profile} lacks production-control extension entry points",
                    failures,
                )
                require(
                    all(
                        extension_by_id[extension_id]["enabled"] is False
                        and extension_by_id[extension_id]["trust_class"]
                        == "unassessed_project_local_code"
                        and extension_by_id[extension_id]["trust_decision_ref"] is None
                        for extension_id in PRODUCTION_EXTENSIONS
                    ),
                    f"{profile} auto-enabled or trusted a production extension",
                    failures,
                )
                for extension_id in sorted(PRODUCTION_EXTENSIONS):
                    extension_config = json.loads(
                        (
                            target
                            / ".agent/extensions"
                            / extension_id
                            / "config.json"
                        ).read_text(encoding="utf-8")
                    )
                    require(
                        extension_config["adoption"]["status"] == "not_assessed"
                        and extension_config["adoption"]["decision_ref"] is None
                        and extension_config["permission_grant"] is False,
                        f"{profile} fabricated {extension_id} adoption or authority",
                        failures,
                    )
            result = check_project(target)
            require(
                result.returncode == 0,
                f"{profile} isolated validation failed: {result.stderr or result.stdout}",
                failures,
            )

        if "standard" in projects:
            for extension_id in sorted(PRODUCTION_EXTENSIONS):
                result = run(
                    [
                        sys.executable,
                        "-B",
                        str(
                            projects["standard"]
                            / ".agent/extensions"
                            / extension_id
                            / "tests/test_validate.py"
                        ),
                    ],
                    projects["standard"],
                )
                require(
                    result.returncode == 0,
                    f"{extension_id} package tests failed: "
                    f"{result.stderr or result.stdout}",
                    failures,
                )

        for profile, target in projects.items():
            source_change = target / f"acceptance-refresh-{profile}.txt"
            source_change.write_text(
                "legitimate project-maintained source change\n",
                encoding="utf-8",
            )
            result = check_project(target)
            require(
                result.returncode != 0
                and "stale source fingerprint" in result.stderr,
                f"{profile} source change did not stale integrity",
                failures,
            )
            result = refresh(target)
            require(
                result.returncode == 0,
                f"{profile} refresh failed: {result.stderr or result.stdout}",
                failures,
            )
            result = check_project(target)
            require(
                result.returncode == 0,
                f"{profile} post-refresh check failed: "
                f"{result.stderr or result.stdout}",
                failures,
            )

        nonempty = temp_root / "nonempty"
        nonempty.mkdir()
        sentinel = nonempty / "sentinel.txt"
        sentinel.write_text("preserve\n", encoding="utf-8")
        before = snapshot(nonempty)
        result = generate(nonempty, "standard", "Must Refuse")
        require(result.returncode != 0, "nonempty target was accepted", failures)
        require(snapshot(nonempty) == before, "nonempty target changed on refusal", failures)

        invalid_name_target = temp_root / "invalid-name"
        result = generate(invalid_name_target, "minimal", "line one\nline two")
        require(result.returncode != 0, "control-character name was accepted", failures)
        require(not invalid_name_target.exists(), "invalid-name target was created", failures)

        broken_skill = temp_root / "broken-project-bootstrap"
        shutil.copytree(
            SKILL_ROOT,
            broken_skill,
            ignore=shutil.ignore_patterns(".git", ".DS_Store", "__pycache__", "*.pyc"),
        )
        broken_source = broken_skill / "assets/blueprint-source"
        if not broken_source.is_dir():
            shutil.copytree(
                ROOT,
                broken_source,
                ignore=shutil.ignore_patterns(
                    ".git", ".DS_Store", "__pycache__", "*.pyc"
                ),
            )
        policy_template = (
            broken_skill
            / "assets/templates/core/.agent/policy.json.tmpl"
        )
        policy_text = policy_template.read_text(encoding="utf-8")
        policy_template.write_text(
            policy_text.replace(
                '"permission_grant": false,',
                '"permission_grant": false,\n  "permission_grant": true,',
                1,
            ),
            encoding="utf-8",
        )
        failed_target = temp_root / "failed-transaction-target"
        result = run(
            [
                sys.executable,
                "-B",
                str(
                    broken_skill
                    / "scripts/scaffold_project.py"
                ),
                "--target",
                str(failed_target),
                "--project-name",
                "Failed Transaction",
                "--profile",
                "minimal",
            ],
            broken_source,
        )
        require(result.returncode != 0, "invalid staged snapshot was installed", failures)
        require(
            not failed_target.exists(),
            "failed staged validation changed the target",
            failures,
        )

        adoption_target = temp_root / "existing"
        adoption_target.mkdir()
        (adoption_target / "AGENTS.md").write_text("# Existing\n", encoding="utf-8")
        (adoption_target / "src").mkdir()
        (adoption_target / "src/domain.txt").write_text("existing\n", encoding="utf-8")
        before = snapshot(adoption_target)
        result = run(
            [
                sys.executable,
                "-B",
                str(PLANNER),
                "--target",
                str(adoption_target),
                "--profile",
                "standard",
                "--format",
                "json",
            ],
            ROOT,
        )
        require(result.returncode == 0, "adoption planner failed", failures)
        require(snapshot(adoption_target) == before, "adoption planner wrote target", failures)
        if result.returncode == 0:
            plan = json.loads(result.stdout)
            require(
                "AGENTS.md" in plan["collisions"],
                "adoption planner missed root instruction collision",
                failures,
            )
            require(
                "AGENTS.md"
                in plan["functional_equivalent_candidates"][
                    "repository_instructions"
                ],
                "adoption planner missed repository-instruction candidate",
                failures,
            )
            require(
                "before accepting"
                in plan["functional_equivalence_limit"].casefold(),
                "adoption plan treated path/name candidates as accepted equivalents",
                failures,
            )

        skill_parent = temp_root / "personal-codex/skills"
        skill_parent.mkdir(parents=True)
        installed_skill = skill_parent / "project-bootstrap"
        result = run(
            [
                sys.executable,
                "-B",
                str(INSTALLER),
                "--destination",
                str(installed_skill),
            ],
            ROOT,
        )
        require(
            result.returncode == 0,
            f"self-contained skill installation failed: {result.stderr or result.stdout}",
            failures,
        )
        require(
            (
                installed_skill
                / "assets/blueprint-source/dossier/artifact-types.json"
            ).is_file(),
            "installed skill lacks bundled dossier taxonomy",
            failures,
        )
        if installed_skill.is_dir():
            before = snapshot(installed_skill)
            result = run(
                [
                    sys.executable,
                    "-B",
                    str(INSTALLER),
                    "--destination",
                    str(installed_skill),
                ],
                ROOT,
            )
            require(result.returncode != 0, "skill installer overwrote a collision", failures)
            require(
                snapshot(installed_skill) == before,
                "skill collision refusal changed installed files",
                failures,
            )

        if "standard" in projects:
            standard = projects["standard"]
            artifact_path = standard / "project-dossier/acceptance-lifecycle.md"
            artifact_path.write_text(
                "# Acceptance lifecycle artifact\n",
                encoding="utf-8",
            )
            artifact_registry_path = (
                standard
                / "project-dossier/machine-readable/artifact-registry.json"
            )
            artifact_registry = json.loads(
                artifact_registry_path.read_text(encoding="utf-8")
            )
            artifact_registry["artifact_types"].append(
                {
                    "id": "TST-9000",
                    "recommended_name": "Acceptance lifecycle artifact",
                    "category": "acceptance_test",
                    "classification": "optional",
                    "purpose": (
                        "Exercise project-local dossier artifact maintenance."
                    ),
                    "questions": [
                        "Can a registered artifact be added, renamed, and omitted?"
                    ],
                    "intended_audiences": ["maintainers"],
                    "owner_role": "acceptance_suite",
                    "required_inputs": ["authority:synthetic-test"],
                    "downstream_consumers": ["lifecycle acceptance"],
                    "recommended_formats": ["Markdown"],
                    "source_of_truth_expectations": (
                        "The registered Markdown file owns only its synthetic scope."
                    ),
                    "dependencies": [],
                    "creation_timing": "During lifecycle acceptance testing.",
                    "update_triggers": ["acceptance mutation"],
                    "review_cadence": "on_change",
                    "validation_checks": ["registered physical path exists"],
                    "triggers": ["explicit synthetic acceptance"],
                    "omission_or_combination": (
                        "May be omitted only after a not-applicable assessment."
                    ),
                    "representative_evidence": ["authority:synthetic-test"],
                    "profile": "standard",
                    "applicability": {
                        "status": "applicable",
                        "rationale": "Explicit synthetic lifecycle acceptance.",
                        "assessed_on": "2030-01-02",
                        "assessed_by": "acceptance_suite",
                    },
                }
            )
            artifact_registry["representations"].append(
                {
                    "id": "REP-9000",
                    "artifact_type_ids": ["TST-9000"],
                    "path": "project-dossier/acceptance-lifecycle.md",
                    "profile": "standard",
                    "representation_role": "acceptance_test",
                    "information_state": "current_state",
                    "authority": "bounded_synthetic_test_source",
                    "source_direction": "authoritative_edit_source",
                    "generated": False,
                    "owner_role": "acceptance_suite",
                    "review_cadence": "on_change",
                    "update_triggers": ["acceptance mutation"],
                    "sensitivity": "internal",
                    "applicability": {
                        "status": "applicable",
                        "rationale": "Physical acceptance artifact is present.",
                        "assessed_on": "2030-01-02",
                    },
                    "review": {
                        "status": "not_reviewed",
                        "last_reviewed_on": None,
                        "basis": "Synthetic acceptance only.",
                    },
                    "superseded_by": None,
                    "legacy_v1_id": None,
                }
            )
            write_json(artifact_registry_path, artifact_registry)
            result = refresh(standard)
            require(
                result.returncode == 0,
                f"registered artifact add failed: {result.stderr or result.stdout}",
                failures,
            )
            result = check_project(standard)
            require(
                result.returncode == 0,
                f"registered artifact add did not validate: "
                f"{result.stderr or result.stdout}",
                failures,
            )

            renamed_artifact_path = (
                standard / "project-dossier/acceptance-lifecycle-renamed.md"
            )
            artifact_path.rename(renamed_artifact_path)
            artifact_registry = json.loads(
                artifact_registry_path.read_text(encoding="utf-8")
            )
            next(
                item
                for item in artifact_registry["representations"]
                if item["id"] == "REP-9000"
            )["path"] = "project-dossier/acceptance-lifecycle-renamed.md"
            write_json(artifact_registry_path, artifact_registry)
            result = refresh(standard)
            require(
                result.returncode == 0,
                f"registered artifact rename failed: "
                f"{result.stderr or result.stdout}",
                failures,
            )
            result = check_project(standard)
            require(
                result.returncode == 0,
                f"registered artifact rename did not validate: "
                f"{result.stderr or result.stdout}",
                failures,
            )

            renamed_artifact_path.unlink()
            artifact_registry = json.loads(
                artifact_registry_path.read_text(encoding="utf-8")
            )
            artifact_registry["representations"] = [
                item
                for item in artifact_registry["representations"]
                if item["id"] != "REP-9000"
            ]
            retained_type = next(
                item
                for item in artifact_registry["artifact_types"]
                if item["id"] == "TST-9000"
            )
            retained_type["applicability"] = {
                "status": "not_applicable",
                "rationale": "Synthetic lifecycle representation was removed.",
                "assessed_on": "2030-01-02",
                "assessed_by": "acceptance_suite",
            }
            write_json(artifact_registry_path, artifact_registry)
            result = refresh(standard)
            require(
                result.returncode == 0,
                f"registered artifact omission failed: "
                f"{result.stderr or result.stdout}",
                failures,
            )
            result = check_project(standard)
            require(
                result.returncode == 0,
                f"registered artifact omission did not validate: "
                f"{result.stderr or result.stdout}",
                failures,
            )
            catalog = json.loads(
                (standard / "project-dossier/ARTIFACT_CATALOG.json").read_text(
                    encoding="utf-8"
                )
            )
            require(
                any(
                    item["id"] == "TST-9000"
                    and item["applicability"]["status"] == "not_applicable"
                    for item in catalog["artifact_types"]
                )
                and all(
                    item["id"] != "REP-9000"
                    for item in catalog["representations"]
                ),
                "artifact omission erased its not-applicable assessment",
                failures,
            )

            unregistered_path = (
                standard / "project-dossier/unregistered-acceptance.md"
            )
            unregistered_path.write_text(
                "# Unregistered acceptance mutation\n",
                encoding="utf-8",
            )
            before_failed_refresh = snapshot(standard)
            result = refresh(standard)
            require(
                result.returncode != 0
                and "artifact registry missing project-maintained dossier files"
                in result.stderr,
                "refresh invented metadata for an unregistered dossier file",
                failures,
            )
            require(
                snapshot(standard) == before_failed_refresh,
                "failed unregistered-file refresh changed project files",
                failures,
            )
            unregistered_path.unlink()
            result = check_project(standard)
            require(
                result.returncode == 0,
                "unregistered-file refusal did not preserve prior valid state",
                failures,
            )

            illegal = temp_root / "illegal-transition"
            shutil.copytree(standard, illegal)
            write_task(illegal, "TASK-9001", "proposed", "completed", [])
            result = check_project(illegal)
            require(
                result.returncode != 0 and "illegal task transition" in result.stderr,
                "illegal lifecycle transition passed",
                failures,
            )

            broken = temp_root / "broken-reference"
            shutil.copytree(standard, broken)
            write_task(broken, "TASK-9002", "proposed", None, ["TASK-9999"])
            result = check_project(broken)
            require(
                result.returncode != 0 and "unresolved reference TASK-9999" in result.stderr,
                "broken record reference passed",
                failures,
            )

            dependency_cycle = temp_root / "task-dependency-cycle"
            shutil.copytree(standard, dependency_cycle)
            write_task(
                dependency_cycle,
                "TASK-9020",
                "proposed",
                None,
                ["TASK-9021"],
            )
            write_task(
                dependency_cycle,
                "TASK-9021",
                "proposed",
                None,
                ["TASK-9020"],
            )
            result = check_project(dependency_cycle)
            require(
                result.returncode != 0
                and "task dependency cycle" in result.stderr,
                "task dependency cycle passed",
                failures,
            )

            incomplete_dependency = temp_root / "incomplete-task-dependency"
            shutil.copytree(standard, incomplete_dependency)
            write_task(
                incomplete_dependency,
                "TASK-9022",
                "ready",
                "proposed",
                [],
                prepared=True,
            )
            write_task(
                incomplete_dependency,
                "TASK-9023",
                "in_progress",
                "ready",
                ["TASK-9022"],
                prepared=True,
            )
            result = check_project(incomplete_dependency)
            require(
                result.returncode != 0
                and "dependency:TASK-9022" in result.stderr
                and "unsatisfied readiness" in result.stderr,
                "execution against incomplete dependency passed",
                failures,
            )

            frontier_target = temp_root / "ready-frontier"
            shutil.copytree(standard, frontier_target)
            write_task(
                frontier_target,
                "TASK-9024",
                "proposed",
                None,
                [],
                prepared=True,
            )
            write_task(
                frontier_target,
                "TASK-9025",
                "proposed",
                None,
                ["TASK-9024"],
                prepared=True,
            )
            before_frontier = snapshot(frontier_target)
            result = ready_frontier_project(frontier_target)
            require(
                result.returncode == 0,
                f"ready frontier failed: {result.stderr or result.stdout}",
                failures,
            )
            require(
                snapshot(frontier_target) == before_frontier,
                "ready frontier command wrote project files",
                failures,
            )
            if result.returncode == 0:
                frontier = json.loads(result.stdout)
                require(
                    frontier.get("tasks") == ["TASK-9024"],
                    "ready frontier included waiting work or omitted eligible work",
                    failures,
                )
                require(
                    frontier.get("permission_grant") is False
                    and frontier.get("priority_ordered") is False
                    and frontier.get("timeline_fields_determine_readiness") is False,
                    "ready frontier implied authority, priority, or timeline readiness",
                    failures,
                )

            dossier_broken = temp_root / "broken-dossier-reference"
            shutil.copytree(standard, dossier_broken)
            findings_path = (
                dossier_broken
                / "project-dossier/machine-readable/findings.json"
            )
            findings = json.loads(findings_path.read_text(encoding="utf-8"))
            findings["findings"] = [
                {
                    "id": "FIND-9001",
                    "title": "Broken requirement reference",
                    "requirement_refs": ["REQ-9999"],
                    "status": "not_assessed",
                    "assessed_on": "2030-01-02",
                    "subject_version": "synthetic",
                    "inspected_evidence": [],
                    "rationale": "Synthetic acceptance mutation.",
                    "owner_role": "acceptance_suite",
                    "remediation_plan_refs": [],
                    "limitations": [],
                }
            ]
            findings_path.write_text(
                json.dumps(findings, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            result = check_project(dossier_broken)
            require(
                result.returncode != 0
                and "unresolved reference REQ-9999" in result.stderr,
                "broken dossier reference passed",
                failures,
            )

            nested = temp_root / "nested-authority"
            shutil.copytree(standard, nested)
            (nested / "src").mkdir()
            (nested / "src/AGENTS.md").write_text(
                '# Invalid\n\n"permission_grant": true\n',
                encoding="utf-8",
            )
            result = check_project(nested)
            require(
                result.returncode != 0
                and "nested instruction may expand authority" in result.stderr,
                "nested authority expansion passed",
                failures,
            )

            secret = temp_root / "secret-redaction"
            shutil.copytree(standard, secret)
            (secret / "src").mkdir()
            secret_value = "synthetic_acceptance_secret_123456"
            (secret / "src/secret.txt").write_text(
                f"api_key: {secret_value}\n",
                encoding="utf-8",
            )
            result = check_project(secret)
            require(
                result.returncode != 0 and "secret assignment" in result.stderr,
                "synthetic secret passed",
                failures,
            )
            require(
                secret_value not in result.stderr + result.stdout,
                "synthetic secret value was echoed",
                failures,
            )

        if "high-assurance" in projects:
            high = projects["high-assurance"]
            registry_path = high / ".agent/extensions/registry.json"
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            sample_extension = next(
                item
                for item in registry["extensions"]
                if item["id"] == "sample-restriction"
            )
            kernel_before = {
                path: hashlib.sha256((high / path).read_bytes()).hexdigest()
                for path in (
                    ".agent/policy.json",
                    ".agent/context.json",
                    ".agent/schema.json",
                    ".agent/lifecycle.json",
                    ".agent/tools.json",
                    ".agent/validators.json",
                    ".agent/project.json",
                )
            }
            write_accepted_decision(high, "DEC-9090")
            sample_extension["enabled"] = True
            sample_extension["owner"] = "acceptance-suite"
            sample_extension["provenance"] = "authority:synthetic-acceptance"
            sample_extension["trust_class"] = "trusted_project_local_code"
            sample_extension["trust_decision_ref"] = "DEC-9090"
            write_json(registry_path, registry)
            result = refresh(high)
            require(
                result.returncode == 0,
                f"trusted sample extension failed: {result.stderr or result.stdout}",
                failures,
            )
            result = check_project(high)
            require(
                result.returncode == 0,
                "trusted sample extension did not validate",
                failures,
            )
            sample_extension["enabled"] = False
            sample_extension["trust_class"] = "unassessed_project_local_code"
            sample_extension["trust_decision_ref"] = None
            registry_path.write_text(
                json.dumps(registry, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            result = refresh(high)
            require(result.returncode == 0, "disabled extension blocked refresh", failures)
            result = check_project(high)
            require(result.returncode == 0, "disabled extension invalidated kernel", failures)
            kernel_after = {
                path: hashlib.sha256((high / path).read_bytes()).hexdigest()
                for path in kernel_before
            }
            require(
                kernel_before == kernel_after,
                "disabling extension required a kernel edit",
                failures,
            )

            invalid_extension = temp_root / "invalid-extension"
            shutil.copytree(high, invalid_extension)
            invalid_registry_path = invalid_extension / ".agent/extensions/registry.json"
            invalid_registry = json.loads(
                invalid_registry_path.read_text(encoding="utf-8")
            )
            next(
                item
                for item in invalid_registry["extensions"]
                if item["id"] == "sample-restriction"
            )["authority_effect"] = "expands_permission"
            invalid_registry_path.write_text(
                json.dumps(invalid_registry, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            result = check_project(invalid_extension)
            require(
                result.returncode != 0
                and ".agent/extensions/registry.json" in result.stderr,
                "authority-expanding extension passed",
                failures,
            )

            production_fixture_ids = {
                "operations-observability": "9001",
                "security-supply-chain": "9101",
            }
            production_extension_base = projects.get("standard", high)
            for extension_id, numeric_id in production_fixture_ids.items():
                production_target = temp_root / f"enabled-{extension_id}"
                shutil.copytree(production_extension_base, production_target)
                extension_root = (
                    production_target / ".agent/extensions" / extension_id
                )
                scenario = json.loads(
                    (
                        extension_root / "tests/fixtures/valid.json"
                    ).read_text(encoding="utf-8")
                )
                write_json(extension_root / "config.json", scenario["config"])
                write_json(extension_root / "records.json", scenario["records"])
                decision_id = f"DEC-{numeric_id}"
                task_id = f"TASK-{numeric_id}"
                evidence_id = f"EVD-{numeric_id}"
                write_accepted_decision(production_target, decision_id)
                write_task(
                    production_target,
                    task_id,
                    "proposed",
                    None,
                    [],
                )
                write_passing_evidence(
                    production_target,
                    evidence_id,
                    task_id,
                )
                production_registry_path = (
                    production_target / ".agent/extensions/registry.json"
                )
                production_registry = json.loads(
                    production_registry_path.read_text(encoding="utf-8")
                )
                production_extension = next(
                    item
                    for item in production_registry["extensions"]
                    if item["id"] == extension_id
                )
                production_extension["enabled"] = True
                production_extension["owner"] = "acceptance-suite"
                production_extension["provenance"] = (
                    "authority:synthetic-acceptance"
                )
                production_extension["trust_class"] = (
                    "trusted_project_local_code"
                )
                production_extension["trust_decision_ref"] = decision_id
                write_json(production_registry_path, production_registry)
                production_kernel_before = {
                    path: hashlib.sha256(
                        (production_target / path).read_bytes()
                    ).hexdigest()
                    for path in kernel_before
                }
                result = refresh(production_target)
                require(
                    result.returncode == 0,
                    f"adopted {extension_id} failed: "
                    f"{result.stderr or result.stdout}",
                    failures,
                )
                result = check_project(production_target)
                require(
                    result.returncode == 0,
                    f"adopted {extension_id} did not validate: "
                    f"{result.stderr or result.stdout}",
                    failures,
                )
                production_extension["enabled"] = False
                write_json(production_registry_path, production_registry)
                result = refresh(production_target)
                require(
                    result.returncode == 0,
                    f"disabled {extension_id} blocked refresh: "
                    f"{result.stderr or result.stdout}",
                    failures,
                )
                result = check_project(production_target)
                require(
                    result.returncode == 0,
                    f"disabled {extension_id} invalidated the kernel",
                    failures,
                )
                production_kernel_after = {
                    path: hashlib.sha256(
                        (production_target / path).read_bytes()
                    ).hexdigest()
                    for path in production_kernel_before
                }
                require(
                    production_kernel_before == production_kernel_after,
                    f"disabling {extension_id} required a kernel edit",
                    failures,
                )

            interrupted = temp_root / "interrupted-refresh"
            shutil.copytree(high, interrupted)
            report_path = interrupted / ".agent/generated/validation-report.json"
            report = json.loads(report_path.read_text(encoding="utf-8"))
            report["generation_id"] = "0" * 32
            report_path.write_text(
                json.dumps(report, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            result = check_project(interrupted)
            require(
                result.returncode != 0 and "mismatched generation IDs" in result.stderr,
                "partial refresh generation mismatch passed",
                failures,
            )

    if failures:
        print(f"FAIL: {len(failures)} acceptance failure(s)")
        for failure in failures:
            print(f"- {failure}")
        return 1
    if set(ACCEPTANCE_COVERAGE) != set(range(1, 15)):
        print("FAIL: acceptance coverage map is incomplete")
        return 1
    print("PASS: Project Blueprint acceptance suite")
    print("- profiles: minimal, standard, high-assurance")
    print("- generation: transactional and format-safe")
    print(
        "- maintenance: all-profile refresh plus registered "
        "add, rename, omission, and refusal paths"
    )
    print(
        "- migration: executable idempotence, exact rollback evidence, and "
        "fail-closed ambiguity coverage"
    )
    print(
        "- adoption: read-only planning/checks plus separately explicit, "
        "fingerprint-bound project-check evidence"
    )
    print(
        "- validator: adversarial authority, dependency readiness/frontier, "
        "lifecycle, reference, secret, extension, and freshness checks"
    )
    print(
        "- production controls: disabled/unassessed defaults, strict fixture "
        "suites, and deliberate Standard enable/disable paths"
    )
    print(
        "ACCEPTANCE_COVERAGE_JSON="
        + json.dumps(
            {
                "schema_version": "project-blueprint.acceptance-coverage.v1",
                "criteria": {
                    str(number): status
                    for number, status in sorted(ACCEPTANCE_COVERAGE.items())
                },
                "scope": "blueprint release automation",
                "failures": [],
                "skipped_checks": [
                    "target-project human demonstrations remain project-owned"
                ],
                "limitations": [
                    "structural automation does not prove project readiness",
                    "runtime policy text is not an external sandbox",
                ],
                "dirty_state": "not_assessed_by_acceptance_suite",
                "external_effects": "none",
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    for number, status in sorted(ACCEPTANCE_COVERAGE.items()):
        print(f"criterion_{number:02d}={status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
