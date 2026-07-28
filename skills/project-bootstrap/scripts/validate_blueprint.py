#!/usr/bin/env python3
"""Validate Project Blueprint source, contracts, templates, and profile builds."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
SKILL_ROOT = Path(__file__).resolve().parents[1]
PROFILE_LAYERS = {
    "minimal": ("core",),
    "standard": ("core", "standard"),
    "high-assurance": ("core", "standard", "high-assurance"),
}
REQUIRED_PATHS = (
    ".github/workflows/validate.yml",
    ".gitignore",
    "AGENTS.md",
    "CHANGELOG.md",
    "README.md",
    "RELEASE.md",
    "VERSION",
    "blueprint.json",
    "dossier/BLUEPRINT.md",
    "dossier/artifact-types.json",
    "dossier/references/REFERENCE_EVIDENCE.md",
    "harness/BLUEPRINT.md",
    "harness/references/REFERENCE_EVIDENCE.md",
    "migrations/0.2.0-to-1.0.0.md",
    "pyproject.toml",
    "shared/GENERATION_CONTRACT.md",
    "shared/schemas/artifact-catalog.schema.json",
    "shared/schemas/dossier-records.schema.json",
    "shared/schemas/harness-extension-registry.schema.json",
    "shared/schemas/harness-record.schema.json",
    "shared/schemas/project-blueprint-origin.schema.json",
    "skills/project-bootstrap/SKILL.md",
    "skills/project-bootstrap/agents/openai.yaml",
    "skills/project-bootstrap/references/dossier-model.md",
    "skills/project-bootstrap/references/generation-workflow.md",
    "skills/project-bootstrap/references/harness-model.md",
    "skills/project-bootstrap/references/profile-selection.md",
    "skills/project-bootstrap/scripts/install_skill.py",
    "skills/project-bootstrap/scripts/plan_adoption.py",
    "skills/project-bootstrap/scripts/scaffold_project.py",
    "skills/project-bootstrap/scripts/test_acceptance.py",
    "skills/project-bootstrap/scripts/validate_blueprint.py",
)
DOSSIER_HEADINGS = (
    "## 1. Executive summary",
    "## 2. Design principles",
    "## 3. Reference-dossier crosswalk",
    "## 4. General artifact taxonomy",
    "## 5. Coverage profiles",
    "## 6. Recommended directory structure",
    "## 7. Core artifact section outlines and schemas",
    "## 8. Relationships and lifecycle",
    "## 9. Governance model",
    "## 10. Adoption checklist and quality gates",
    "## 11. Gaps and new recommendations",
)
HARNESS_HEADINGS = tuple(f"## {number}." for number in range(1, 18))
REQUIRED_KERNEL = {
    "AGENTS.md",
    ".agent/START_HERE.md",
    ".agent/policy.json",
    ".agent/context.json",
    ".agent/schema.json",
    ".agent/lifecycle.json",
    ".agent/tools.json",
    ".agent/validators.json",
    ".agent/project.json",
    ".agent/state/current.json",
    ".agent/state/RESUME.md",
    ".agent/templates/task.md",
    ".agent/templates/decision.md",
    ".agent/scripts/validate.py",
    ".agent/tests/test_validate.py",
    "project-dossier/README.md",
    "project-dossier/AUTHORITY.md",
    "project-dossier/CANONICAL_SOURCE_MAP.md",
    "project-dossier/SUPERSESSION.json",
    "project-dossier/canonical/constraints-gates-and-readiness.md",
    "project-dossier/handoff/ADOPTION_CHECKLIST.md",
    "project-dossier/validation/QUALITY_GATES.json",
}


class DuplicateKeyError(ValueError):
    pass


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def load_json(path: Path) -> Any:
    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_object,
    )


def load_scaffolder():
    path = SKILL_ROOT / "scripts" / "scaffold_project.py"
    spec = importlib.util.spec_from_file_location("project_blueprint_scaffold", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load scaffolder: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_docs(issues: list[str]) -> None:
    dossier = (ROOT / "dossier/BLUEPRINT.md").read_text(encoding="utf-8")
    positions = [dossier.find(heading) for heading in DOSSIER_HEADINGS]
    for heading, position in zip(DOSSIER_HEADINGS, positions):
        if position < 0:
            issues.append(f"dossier blueprint missing section: {heading}")
    if positions != sorted(positions):
        issues.append("dossier blueprint sections are out of order")
    for label in (
        "[Observed: CF]",
        "[Observed: COE]",
        "[Observed: both]",
        "[Inferred]",
        "[Recommended]",
    ):
        if label not in dossier:
            issues.append(f"dossier blueprint missing evidence label: {label}")
    for field in (
        "Category/classification",
        "Purpose",
        "Questions",
        "Audience/owner",
        "Inputs",
        "Outputs",
        "Format/authority",
        "Dependencies",
        "Timing/cadence",
        "Validation",
        "Omit/combine",
        "Evidence",
    ):
        if field not in dossier:
            issues.append(f"dossier artifact specifications missing field: {field}")
    if len(re.findall(r"^### [A-Z]{3}-[0-9]{4} — ", dossier, re.MULTILINE)) < 15:
        issues.append("dossier blueprint has too few stable artifact specifications")

    harness = (ROOT / "harness/BLUEPRINT.md").read_text(encoding="utf-8")
    positions = [harness.find(prefix) for prefix in HARNESS_HEADINGS]
    for prefix, position in zip(HARNESS_HEADINGS, positions):
        if position < 0:
            issues.append(f"harness blueprint missing numbered section: {prefix}")
    if positions != sorted(positions):
        issues.append("harness blueprint sections are out of order")
    if "stable domain-neutral kernel" not in harness:
        issues.append("harness blueprint lacks bounded universal-kernel definition")
    if "strict JSON" not in harness:
        issues.append("harness blueprint lacks canonical strict JSON contract")
    if "Observed — both" not in harness or "Recommendation" not in harness:
        issues.append("harness blueprint lacks evidence/recommendation distinction")

    for path in (
        ROOT / "dossier/references/REFERENCE_EVIDENCE.md",
        ROOT / "harness/references/REFERENCE_EVIDENCE.md",
    ):
        text = path.read_text(encoding="utf-8")
        if "/Users/" in text:
            issues.append(f"{path.relative_to(ROOT)} exposes an absolute source path")


def validate_config_and_schemas(issues: list[str]) -> None:
    try:
        config = load_json(ROOT / "blueprint.json")
    except (ValueError, json.JSONDecodeError) as error:
        issues.append(f"invalid blueprint.json: {error}")
        return
    if config.get("overwrite_existing_paths") is not False:
        issues.append("blueprint.json must prohibit overwriting")
    if config.get("new_generation_requires_empty_target") is not True:
        issues.append("blueprint.json must require an empty new-project target")
    if config.get("minimum_python") != "3.11":
        issues.append("blueprint.json Python minimum must be 3.11")
    if config.get("profiles") != list(PROFILE_LAYERS):
        issues.append("blueprint.json profile order mismatch")
    kernel = config.get("modules", {}).get("harness", {}).get("kernel_files")
    if set(kernel or []) != {
        ".agent/policy.json",
        ".agent/context.json",
        ".agent/schema.json",
        ".agent/lifecycle.json",
        ".agent/tools.json",
        ".agent/validators.json",
        ".agent/project.json",
    }:
        issues.append("blueprint.json kernel files do not match the seven-file kernel")

    for path in sorted((ROOT / "shared/schemas").glob("*.schema.json")):
        try:
            schema = load_json(path)
        except (ValueError, json.JSONDecodeError) as error:
            issues.append(f"invalid strict JSON schema {path.name}: {error}")
            continue
        if not isinstance(schema, dict) or not schema.get("$id"):
            issues.append(f"{path.name}: schema lacks $id")
        elif "example.invalid" in schema["$id"]:
            issues.append(f"{path.name}: placeholder schema ID remains")


def validate_artifact_types(issues: list[str], scaffolder: Any) -> None:
    try:
        source = load_json(ROOT / "dossier/artifact-types.json")
    except (ValueError, json.JSONDecodeError) as error:
        issues.append(f"invalid dossier/artifact-types.json: {error}")
        return
    artifacts = source.get("artifacts", []) if isinstance(source, dict) else []
    ids: set[str] = set()
    paths: set[str] = set()
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            issues.append(f"artifact type {index} is not an object")
            continue
        artifact_id = artifact.get("id")
        path = artifact.get("path")
        if not isinstance(artifact_id, str) or not re.fullmatch(
            r"[A-Z]{3}-[0-9]{4}", artifact_id
        ):
            issues.append(f"artifact type {index} has invalid four-digit ID")
        elif artifact_id in ids:
            issues.append(f"duplicate artifact type ID: {artifact_id}")
        ids.add(artifact_id)
        if not isinstance(path, str) or not path.startswith(
            (".agent/", "project-dossier/")
        ):
            issues.append(f"artifact {artifact_id}: invalid path")
        elif path in paths:
            issues.append(f"duplicate artifact type path: {path}")
        paths.add(path)
        if artifact.get("profile") not in PROFILE_LAYERS:
            issues.append(f"artifact {artifact_id}: invalid profile")
        for required in (
            "category",
            "classification",
            "information_state",
            "authority",
            "generated",
            "owner_role",
            "review_cadence",
            "update_triggers",
            "sensitivity",
        ):
            if required not in artifact:
                issues.append(f"artifact {artifact_id}: missing {required}")
    if len(artifacts) < 25:
        issues.append("artifact taxonomy is unexpectedly incomplete")

    for profile in PROFILE_LAYERS:
        try:
            selected = scaffolder.selected_artifacts(profile, date.today().isoformat())
        except ValueError as error:
            issues.append(f"{profile} artifact selection failed: {error}")
            continue
        if not selected:
            issues.append(f"{profile} artifact selection is empty")


def validate_templates(issues: list[str], scaffolder: Any) -> None:
    variables = {
        "PROJECT_NAME": 'Template "Validation" [α]',
        "PROJECT_NAME_JSON": json.dumps('Template "Validation" [α]', ensure_ascii=False),
        "PROJECT_SLUG": "template-validation",
        "CREATED_DATE": "2030-01-02",
        "BLUEPRINT_VERSION": "1.0.0",
        "PROFILE": "high-assurance",
        "HARNESS_REFRESH_COMMAND": "python3 -B .agent/scripts/refresh.py --refresh",
        "HARNESS_REFRESH_WRITES": "[]",
    }
    templates_root = SKILL_ROOT / "assets/templates"
    for profile in PROFILE_LAYERS:
        try:
            templates = scaffolder.collect_templates(profile)
        except ValueError as error:
            issues.append(f"{profile} template collection failed: {error}")
            continue
        required_paths = {Path(item) for item in REQUIRED_KERNEL}
        missing = sorted(required_paths - set(templates) - {
            Path("project-dossier/ARTIFACT_CATALOG.json"),
            Path("project-dossier/machine-readable/path-authority.json"),
        })
        if missing:
            issues.append(f"{profile} missing kernel/dossier paths: {missing}")
        if any(path.suffix in {".yaml", ".yml"} for path in templates):
            issues.append(f"{profile} canonical templates still emit YAML")
        if profile != "high-assurance" and any(
            path.as_posix().startswith(".agents/") for path in templates
        ):
            issues.append(f"{profile} unexpectedly emits capability packages")
        for relative, template in templates.items():
            try:
                rendered = scaffolder.render(template, variables)
            except ValueError as error:
                issues.append(str(error))
                continue
            if "/Users/" in rendered:
                issues.append(f"{template.relative_to(ROOT)} contains host path")
            invalid_fixture = relative.as_posix().startswith(
                ".agent/tests/fixtures/invalid/"
            )
            if relative.suffix == ".json" and not invalid_fixture:
                try:
                    json.loads(rendered, object_pairs_hook=strict_object)
                except (ValueError, json.JSONDecodeError) as error:
                    issues.append(f"{template.relative_to(ROOT)}: invalid JSON: {error}")
            if relative.suffix == ".py":
                try:
                    compile(rendered, str(template), "exec")
                except SyntaxError as error:
                    issues.append(f"{template.relative_to(ROOT)}: {error}")
            if (
                '"permission_grant": true' in rendered
                and not invalid_fixture
                and not relative.as_posix().startswith(".agent/tests/")
            ):
                issues.append(f"{template.relative_to(ROOT)} authorizes by default")
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    if ".DS_Store" not in gitignore:
        issues.append(".gitignore must exclude Finder metadata")
    if list(templates_root.rglob("*.yaml.tmpl")) or list(
        templates_root.rglob("*.yml.tmpl")
    ):
        issues.append("canonical template tree contains YAML outputs")


def validate_skill_and_release(issues: list[str]) -> None:
    skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    if "TODO" in skill:
        issues.append("SKILL.md contains TODO")
    if "never facts, permissions, decisions" not in skill:
        issues.append("SKILL.md lacks explicit non-transfer boundary")
    if "plan_adoption.py" not in skill:
        issues.append("SKILL.md lacks established-project adoption routing")
    openai = (SKILL_ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
    if "$project-bootstrap" not in openai:
        issues.append("agents/openai.yaml does not invoke $project-bootstrap")
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if version != "1.0.0":
        issues.append(f"release VERSION must be 1.0.0, found {version!r}")
    for path in ("CHANGELOG.md", "RELEASE.md"):
        if f"1.0.0" not in (ROOT / path).read_text(encoding="utf-8"):
            issues.append(f"{path} lacks the 1.0.0 release")
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    if 'requires-python = ">=3.11"' not in pyproject:
        issues.append("pyproject.toml does not enforce Python 3.11+")


def validate_profile_builds(issues: list[str]) -> None:
    scaffolder = SKILL_ROOT / "scripts/scaffold_project.py"
    with tempfile.TemporaryDirectory(prefix="project-blueprint-source-check-") as temp:
        for profile in PROFILE_LAYERS:
            target = Path(temp) / profile
            result = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(scaffolder),
                    "--target",
                    str(target),
                    "--project-name",
                    f'Source Check "{profile}"',
                    "--profile",
                    profile,
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode:
                issues.append(
                    f"{profile} profile generation failed: "
                    f"{result.stderr.strip() or result.stdout.strip()}"
                )


def main() -> int:
    issues: list[str] = []
    if sys.version_info < (3, 11):
        issues.append(f"Python 3.11+ required; found {sys.version.split()[0]}")
    for path in REQUIRED_PATHS:
        if not (ROOT / path).is_file():
            issues.append(f"missing required file: {path}")
    if issues:
        print(f"FAIL: {len(issues)} issue(s)")
        for issue in issues:
            print(f"- {issue}")
        return 1
    try:
        scaffolder = load_scaffolder()
    except RuntimeError as error:
        print(f"FAIL: {error}")
        return 1
    validate_docs(issues)
    validate_config_and_schemas(issues)
    validate_artifact_types(issues, scaffolder)
    validate_templates(issues, scaffolder)
    validate_skill_and_release(issues)
    validate_profile_builds(issues)
    if issues:
        print(f"FAIL: {len(issues)} issue(s)")
        for issue in issues:
            print(f"- {issue}")
        return 1
    template_count = len(list((SKILL_ROOT / "assets/templates").rglob("*.tmpl")))
    print("PASS: Project Blueprint source and profile builds are valid")
    print(f"- required files: {len(REQUIRED_PATHS)}")
    print(f"- templates: {template_count}")
    print(f"- profiles: {', '.join(PROFILE_LAYERS)}")
    print("- structured kernel: strict JSON")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
