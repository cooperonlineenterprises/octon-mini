#!/usr/bin/env python3
"""End-to-end and adversarial acceptance suite for Project Blueprint."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCAFFOLDER = ROOT / "skills/project-bootstrap/scripts/scaffold_project.py"
PLANNER = ROOT / "skills/project-bootstrap/scripts/plan_adoption.py"
INSTALLER = ROOT / "skills/project-bootstrap/scripts/install_skill.py"
PROFILES = ("minimal", "standard", "high-assurance")


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


def write_task(target: Path, task_id: str, status: str, previous: str | None, dependencies: list[str]) -> None:
    value = {
        "schema_version": "harness.task.v1",
        "id": task_id,
        "status": status,
        "previous_status": previous,
        "title": "Acceptance mutation",
        "authority_basis": "authority:synthetic-test",
        "owner": "acceptance-suite",
        "dependencies": dependencies,
        "closure_evidence": [],
        "external_effects": "none",
        "limitations": [],
    }
    path = target / ".agent/tasks" / f"{task_id}-mutation.md"
    path.write_text(
        "---\n" + json.dumps(value, indent=2) + "\n---\n\n# Mutation\n",
        encoding="utf-8",
    )


def main() -> int:
    if sys.version_info < (3, 11):
        print("FAIL: Python 3.11+ is required")
        return 2
    failures: list[str] = []
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
            result = check_project(target)
            require(
                result.returncode == 0,
                f"{profile} isolated validation failed: {result.stderr or result.stdout}",
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

        broken_source = temp_root / "broken-blueprint-source"
        shutil.copytree(
            ROOT,
            broken_source,
            ignore=shutil.ignore_patterns(".git", ".DS_Store", "__pycache__", "*.pyc"),
        )
        policy_template = (
            broken_source
            / "skills/project-bootstrap/assets/templates/core/.agent/policy.json.tmpl"
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
                    broken_source
                    / "skills/project-bootstrap/scripts/scaffold_project.py"
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
            (high / "src").mkdir()
            (high / "src/domain-neutral-change.txt").write_text(
                "source change\n", encoding="utf-8"
            )
            result = check_project(high)
            require(
                result.returncode != 0 and "stale source fingerprint" in result.stderr,
                "arbitrary source change did not stale integrity",
                failures,
            )
            result = refresh(high)
            require(
                result.returncode == 0,
                f"refresh after source change failed: {result.stderr or result.stdout}",
                failures,
            )
            result = check_project(high)
            require(
                result.returncode == 0,
                f"post-refresh check failed: {result.stderr or result.stdout}",
                failures,
            )

            registry_path = high / ".agent/extensions/registry.json"
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
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
            registry["extensions"][0]["enabled"] = False
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
            invalid_registry["extensions"][0]["authority_effect"] = "expands_permission"
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
    print("PASS: Project Blueprint acceptance suite")
    print("- profiles: minimal, standard, high-assurance")
    print("- generation: transactional and format-safe")
    print("- adoption: read-only planning")
    print("- validator: adversarial authority, lifecycle, reference, secret, extension, and freshness checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
