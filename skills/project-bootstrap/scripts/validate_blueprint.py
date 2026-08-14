#!/usr/bin/env python3
"""Validate Project Blueprint source, contracts, templates, and profile builds."""

from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import tomllib
from datetime import date
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]


def blueprint_root() -> Path:
    candidates = (
        Path(__file__).resolve().parents[3],
        SKILL_ROOT / "assets" / "blueprint-source",
    )
    for candidate in candidates:
        if (
            (candidate / "VERSION").is_file()
            and (candidate / "dossier/artifact-types.json").is_file()
            and (candidate / "shared/schemas").is_dir()
        ):
            return candidate
    return candidates[0]


ROOT = blueprint_root()


def repository_path(value: str) -> Path:
    path = Path(value)
    skill_prefix = Path("skills/project-bootstrap")
    try:
        relative = path.relative_to(skill_prefix)
    except ValueError:
        return ROOT / path
    return SKILL_ROOT / relative
REQUIRED_PATHS = (
    ".github/workflows/validate.yml",
    ".gitignore",
    "AGENTS.md",
    "ARCHITECTURE_DECISIONS.md",
    "ARCHITECTURAL_PATTERN_INTEGRATION_REVIEW.md",
    "CHANGELOG.md",
    "GIT_WORKFLOW.md",
    "README.md",
    "RELEASE.md",
    "VERSION",
    "VELOCITY_ROADMAP.md",
    "VELOCITY_VALIDATION.md",
    "blueprint.json",
    "docs/COMPATIBILITY.md",
    "docs/DECISION_GOVERNANCE.md",
    "docs/GOLDEN_PATHS.md",
    "docs/examples/DECISION_GOVERNANCE_WORKED_EXAMPLE.md",
    "dossier/BLUEPRINT.md",
    "dossier/artifact-types.json",
    "dossier/references/REFERENCE_EVIDENCE.md",
    "harness/BLUEPRINT.md",
    "harness/references/REFERENCE_EVIDENCE.md",
    "migrations/0.2.0-to-1.0.0.md",
    "migrations/1.0.0-to-1.0.1.md",
    "migrations/1.0.1-to-2.0.0.md",
    "migrations/2.0.0-to-3.0.0.md",
    "migrations/3.0.0-to-3.1.0.md",
    "migrations/3.1.0-to-4.0.0.md",
    "patterns/README.md",
    "patterns/catalog.json",
    "patterns/schemas/pattern-catalog.schema.json",
    "patterns/schemas/pattern-record.schema.json",
    "patterns/records/PAT-0001-lifecycle-disposition.json",
    "patterns/records/PAT-0002-governed-change-and-effects.json",
    "patterns/records/PAT-0003-architecture-proof.json",
    "patterns/architecture-proof/README.md",
    "patterns/architecture-proof/schema.json",
    "patterns/architecture-proof/templates/spike.json",
    "patterns/architecture-proof/templates/reference-slice.json",
    "patterns/architecture-proof/templates/provider-qualification.json",
    "patterns/architecture-proof/templates/adversarial-fixture-pack.json",
    "patterns/architecture-proof/templates/readiness-evidence.json",
    "patterns/fixtures/context-pack/valid/active.json",
    "patterns/fixtures/architecture-proof/valid/unsupported-spike.json",
    "patterns/fixtures/architecture-proof/valid/inconclusive-provider.json",
    "pyproject.toml",
    "shared/GENERATION_CONTRACT.md",
    "shared/optional-schemas/context-pack-manifest.schema.json",
    "shared/reference-evidence.json",
    "shared/source-contracts/information-state-semantics.json",
    "shared/source-contracts/information-state-semantics.schema.json",
    "shared/source-contracts/commands.json",
    "shared/source-contracts/commands.schema.json",
    "shared/source-contracts/diagnostic-catalog.json",
    "shared/source-contracts/diagnostic-catalog.schema.json",
    "shared/source-contracts/hook-detector-protocol.json",
    "shared/source-contracts/hook-detector-protocol.schema.json",
    "shared/source-contracts/profile-manifest.json",
    "shared/source-contracts/profile-manifest.schema.json",
    "shared/schemas/artifact-catalog.schema.json",
    "shared/schemas/dossier-artifact-registry.schema.json",
    "shared/schemas/dossier-path-authority.schema.json",
    "shared/schemas/dossier-records.schema.json",
    "shared/schemas/harness-artifact-registry.schema.json",
    "shared/schemas/harness-assurance-records.schema.json",
    "shared/schemas/harness-capability-records.schema.json",
    "shared/schemas/harness-collaboration-profile.schema.json",
    "shared/schemas/harness-current-state.schema.json",
    "shared/schemas/harness-decision-governance.schema.json",
    "shared/schemas/harness-diagnostics.schema.json",
    "shared/schemas/harness-extension-registry.schema.json",
    "shared/schemas/harness-focus.schema.json",
    "shared/schemas/harness-git-workflows.schema.json",
    "shared/schemas/harness-hook-candidate.schema.json",
    "shared/schemas/harness-kernel.schema.json",
    "shared/schemas/harness-package-registry.schema.json",
    "shared/schemas/harness-project-check-evidence.schema.json",
    "shared/schemas/harness-record.schema.json",
    "shared/schemas/harness-scm.schema.json",
    "shared/schemas/harness-transaction.schema.json",
    "shared/schemas/harness-work-completion.schema.json",
    "shared/schemas/project-blueprint-migration-seed.schema.json",
    "shared/schemas/project-blueprint-origin.schema.json",
    "shared/schemas/project-blueprint-upgrade.schema.json",
    "shared/schemas/reference-evidence.schema.json",
    "skills/project-bootstrap/SKILL.md",
    "skills/project-bootstrap/agents/openai.yaml",
    "skills/project-bootstrap/references/dossier-model.md",
    "skills/project-bootstrap/references/generation-workflow.md",
    "skills/project-bootstrap/references/harness-model.md",
    "skills/project-bootstrap/references/profile-selection.md",
    "skills/project-bootstrap/scripts/install_skill.py",
    "skills/project-bootstrap/scripts/migrate_1_0_1_to_2_0_0.py",
    "skills/project-bootstrap/scripts/migrate_2_0_0_to_3_0_0.py",
    "skills/project-bootstrap/scripts/migrate_3_1_0_to_4_0_0.py",
    "skills/project-bootstrap/scripts/adopt_project.py",
    "skills/project-bootstrap/scripts/benchmark_validation.py",
    "skills/project-bootstrap/scripts/collaboration_project.py",
    "skills/project-bootstrap/scripts/detect_project.py",
    "skills/project-bootstrap/scripts/init_project.py",
    "skills/project-bootstrap/scripts/package_project.py",
    "skills/project-bootstrap/scripts/pb.py",
    "skills/project-bootstrap/scripts/plan_adoption.py",
    "skills/project-bootstrap/scripts/scaffold_project.py",
    "skills/project-bootstrap/scripts/test_acceptance.py",
    "skills/project-bootstrap/scripts/test_architectural_patterns.py",
    "skills/project-bootstrap/scripts/test_migration_1_0_1_to_2_0_0.py",
    "skills/project-bootstrap/scripts/test_migration_2_0_0_to_3_0_0.py",
    "skills/project-bootstrap/scripts/test_migration_3_1_0_to_4_0_0.py",
    "skills/project-bootstrap/scripts/test_velocity_workflows.py",
    "skills/project-bootstrap/scripts/test_work_completion.py",
    "skills/project-bootstrap/scripts/upgrade_project.py",
    "skills/project-bootstrap/scripts/validate_blueprint.py",
    "skills/project-bootstrap/scripts/validate_source_contracts.py",
    "skills/project-bootstrap/scripts/validate_skill_package.py",
    "skills/project-bootstrap/scripts/verify_reference_evidence.py",
    "skills/project-bootstrap/fixtures/decision-governance/README.md",
    "skills/project-bootstrap/fixtures/work-completion/README.md",
    "skills/project-bootstrap/fixtures/work-completion/valid-config.json",
    "skills/project-bootstrap/fixtures/work-completion/invalid-mutations.json",
    "skills/project-bootstrap/fixtures/decision-governance/valid/empty-register.json",
    "skills/project-bootstrap/fixtures/decision-governance/invalid/mutations.json",
    "skills/project-bootstrap/fixtures/migrations/1.0.1-to-2.0.0/README.md",
    "skills/project-bootstrap/fixtures/migrations/1.0.1-to-2.0.0/valid/v1-standard.json",
    "skills/project-bootstrap/fixtures/migrations/1.0.1-to-2.0.0/valid/expectations.json",
    "skills/project-bootstrap/fixtures/migrations/1.0.1-to-2.0.0/invalid/adopted-without-v2-evidence.json",
    "skills/project-bootstrap/fixtures/migrations/1.0.1-to-2.0.0/invalid/ambiguous-dependency.json",
    "skills/project-bootstrap/fixtures/migrations/1.0.1-to-2.0.0/invalid/configured-legacy-command.json",
    "skills/project-bootstrap/fixtures/migrations/1.0.1-to-2.0.0/invalid/hard-advisory-confusion.json",
    "skills/project-bootstrap/fixtures/migrations/1.0.1-to-2.0.0/invalid/legacy-blocked-direct-to-execution.json",
    "skills/project-bootstrap/fixtures/migrations/1.0.1-to-2.0.0/invalid/mixed-live-authority.json",
    "skills/project-bootstrap/fixtures/migrations/1.0.1-to-2.0.0/invalid/mixed-live-project-authority.json",
    "skills/project-bootstrap/fixtures/migrations/1.0.1-to-2.0.0/invalid/mixed-live-validator-authority.json",
    "skills/project-bootstrap/fixtures/migrations/1.0.1-to-2.0.0/invalid/mismatched-version-executable.json",
    "skills/project-bootstrap/fixtures/migrations/1.0.1-to-2.0.0/invalid/nonexternal-migration-authority.json",
    "skills/project-bootstrap/fixtures/migrations/1.0.1-to-2.0.0/invalid/nonreciprocal-plan-task-link.json",
    "skills/project-bootstrap/fixtures/migrations/1.0.1-to-2.0.0/invalid/task-cycle.json",
    "skills/project-bootstrap/fixtures/migrations/1.0.1-to-2.0.0/invalid/unsafe-explicit-command.json",
    "skills/project-bootstrap/fixtures/migrations/2.0.0-to-3.0.0/README.md",
    "skills/project-bootstrap/fixtures/migrations/2.0.0-to-3.0.0/valid/v2-minimal.json",
    "skills/project-bootstrap/fixtures/migrations/2.0.0-to-3.0.0/valid/expectations.json",
    "skills/project-bootstrap/fixtures/migrations/2.0.0-to-3.0.0/invalid/adopted-legacy-git-policy.json",
    "skills/project-bootstrap/fixtures/migrations/2.0.0-to-3.0.0/invalid/divergent-legacy-tools.json",
    "skills/project-bootstrap/fixtures/migrations/2.0.0-to-3.0.0/invalid/fabricated-collaboration-evidence.json",
    "skills/project-bootstrap/fixtures/migrations/2.0.0-to-3.0.0/invalid/fabricated-workflow-adoption.json",
    "skills/project-bootstrap/fixtures/migrations/2.0.0-to-3.0.0/invalid/mixed-live-project-version.json",
    "skills/project-bootstrap/fixtures/migrations/2.0.0-to-3.0.0/invalid/mixed-live-validator-version.json",
    "skills/project-bootstrap/fixtures/migrations/3.1.0-to-4.0.0/README.md",
    "skills/project-bootstrap/fixtures/migrations/2.0.0-to-3.0.0/invalid/nonexternal-migration-authority.json",
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


class DuplicateKeyError(ValueError):
    pass


SUPPORTED_SCHEMA_KEYWORDS = {
    "$defs",
    "$id",
    "$ref",
    "$schema",
    "additionalProperties",
    "allOf",
    "const",
    "description",
    "enum",
    "else",
    "format",
    "if",
    "items",
    "maxItems",
    "maximum",
    "minItems",
    "minLength",
    "minimum",
    "pattern",
    "properties",
    "required",
    "title",
    "then",
    "type",
    "uniqueItems",
}


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def reject_json_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number is prohibited: {value}")


def load_json(path: Path) -> Any:
    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=reject_json_constant,
    )


def lint_supported_schema(
    schema: Any,
    location: str,
    issues: list[str],
    *,
    root_schema: dict[str, Any] | None = None,
) -> None:
    if not isinstance(schema, dict):
        issues.append(f"{location}: schema node must be an object")
        return
    root_schema = root_schema or schema
    unexpected = sorted(set(schema) - SUPPORTED_SCHEMA_KEYWORDS)
    if unexpected:
        issues.append(
            f"{location}: unsupported schema keywords: {', '.join(unexpected)}"
        )
    schema_type = schema.get("type")
    allowed_types = {
        "array",
        "boolean",
        "integer",
        "null",
        "number",
        "object",
        "string",
    }
    declared_types = (
        schema_type if isinstance(schema_type, list) else [schema_type]
    )
    if schema_type is not None and (
        not declared_types
        or any(not isinstance(item, str) for item in declared_types)
        or len(declared_types) != len(set(declared_types))
        or any(item not in allowed_types for item in declared_types)
    ):
        issues.append(f"{location}.type: unsupported or duplicate JSON type")
    required = schema.get("required")
    if required is not None and (
        not isinstance(required, list)
        or any(not isinstance(item, str) for item in required)
        or len(required) != len(set(required))
    ):
        issues.append(f"{location}.required: expected unique string array")
    enum = schema.get("enum")
    if enum is not None and (not isinstance(enum, list) or not enum):
        issues.append(f"{location}.enum: expected nonempty array")
    for field in ("minItems", "maxItems", "minLength"):
        value = schema.get(field)
        if value is not None and (
            not isinstance(value, int) or isinstance(value, bool) or value < 0
        ):
            issues.append(f"{location}.{field}: expected nonnegative integer")
    minimum = schema.get("minimum")
    if minimum is not None and (
        not isinstance(minimum, (int, float))
        or isinstance(minimum, bool)
    ):
        issues.append(f"{location}.minimum: expected number")
    maximum = schema.get("maximum")
    if maximum is not None and (
        not isinstance(maximum, (int, float))
        or isinstance(maximum, bool)
    ):
        issues.append(f"{location}.maximum: expected number")
    if (
        isinstance(minimum, (int, float))
        and not isinstance(minimum, bool)
        and isinstance(maximum, (int, float))
        and not isinstance(maximum, bool)
        and minimum > maximum
    ):
        issues.append(f"{location}: minimum exceeds maximum")
    min_items = schema.get("minItems")
    max_items = schema.get("maxItems")
    if (
        isinstance(min_items, int)
        and not isinstance(min_items, bool)
        and isinstance(max_items, int)
        and not isinstance(max_items, bool)
        and min_items > max_items
    ):
        issues.append(f"{location}: minItems exceeds maxItems")
    if "uniqueItems" in schema and not isinstance(schema["uniqueItems"], bool):
        issues.append(f"{location}.uniqueItems: expected boolean")
    pattern = schema.get("pattern")
    if pattern is not None:
        if not isinstance(pattern, str):
            issues.append(f"{location}.pattern: expected string")
        else:
            try:
                re.compile(pattern)
            except re.error as error:
                issues.append(f"{location}.pattern: invalid regular expression: {error}")
    reference = schema.get("$ref")
    if reference is not None and (
        not isinstance(reference, str) or not reference.startswith("#/")
    ):
        issues.append(f"{location}.$ref: only local references are supported")
    elif isinstance(reference, str):
        current: Any = root_schema
        for raw_part in reference[2:].split("/"):
            part = raw_part.replace("~1", "/").replace("~0", "~")
            if not isinstance(current, dict) or part not in current:
                issues.append(f"{location}.$ref: unresolved reference {reference}")
                break
            current = current[part]
    schema_format = schema.get("format")
    if schema_format not in {None, "date", "date-time"}:
        issues.append(f"{location}.format: unsupported format {schema_format!r}")
    if "additionalProperties" in schema and not isinstance(
        schema["additionalProperties"], bool
    ):
        issues.append(f"{location}.additionalProperties: expected boolean")
    for field in ("properties", "$defs"):
        children = schema.get(field)
        if children is None:
            continue
        if not isinstance(children, dict):
            issues.append(f"{location}.{field}: expected object")
            continue
        for name, child in children.items():
            lint_supported_schema(
                child,
                f"{location}.{field}.{name}",
                issues,
                root_schema=root_schema,
            )
    items = schema.get("items")
    if items is not None:
        lint_supported_schema(
            items,
            f"{location}.items",
            issues,
            root_schema=root_schema,
        )
    all_of = schema.get("allOf")
    if all_of is not None:
        if not isinstance(all_of, list):
            issues.append(f"{location}.allOf: expected array")
        else:
            for index, child in enumerate(all_of):
                lint_supported_schema(
                    child,
                    f"{location}.allOf[{index}]",
                    issues,
                    root_schema=root_schema,
                )
    for field in ("if", "then", "else"):
        child = schema.get(field)
        if child is not None:
            lint_supported_schema(
                child,
                f"{location}.{field}",
                issues,
                root_schema=root_schema,
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
        "Category / classification:",
        "Purpose:",
        "Questions it must answer:",
        "Intended audience:",
        "Expected owner or maintainer:",
        "Required inputs:",
        "Outputs / downstream consumers:",
        "Recommended format:",
        "Source-of-truth expectations:",
        "Dependencies and related artifacts:",
        "Creation timing:",
        "Update triggers:",
        "Validation / quality checks:",
        "Omission or combination:",
        "Representative evidence:",
    ):
        if field not in dossier:
            issues.append(f"dossier artifact specifications missing field: {field}")
    if len(
        re.findall(
            r"^#### [A-Z][A-Z0-9]*-[0-9]{4} — ",
            dossier,
            re.MULTILINE,
        )
    ) < 25:
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


def validate_config_and_schemas(issues: list[str], scaffolder: Any) -> None:
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
    if config.get("schema_version") != "project-blueprint.v3":
        issues.append("blueprint.json schema version must be project-blueprint.v3")
    try:
        manifest = scaffolder.load_generation_policy()
        profiles = tuple(scaffolder.profile_layers(manifest))
    except ValueError as error:
        issues.append(f"invalid authoritative profile manifest: {error}")
        return
    if config.get("reference_evidence_registry") != "shared/reference-evidence.json":
        issues.append("blueprint.json reference-evidence registry path mismatch")
    workflow_paths = {
        "workflow_interface": "skills/project-bootstrap/scripts/pb.py",
        "new_project_initializer": "skills/project-bootstrap/scripts/init_project.py",
        "established_project_adopter": "skills/project-bootstrap/scripts/adopt_project.py",
        "live_project_upgrader": "skills/project-bootstrap/scripts/upgrade_project.py",
        "advanced_new_project_generator": (
            "skills/project-bootstrap/scripts/scaffold_project.py"
        ),
        "advanced_existing_project_planner": (
            "skills/project-bootstrap/scripts/plan_adoption.py"
        ),
    }
    for key, expected_path in workflow_paths.items():
        if config.get(key) != expected_path:
            issues.append(f"blueprint.json {key} path mismatch")
        elif not repository_path(expected_path).is_file():
            issues.append(f"blueprint.json {key} path is absent")
    kernel = scaffolder.kernel_paths(manifest)
    if len(kernel) != 7 or any(path.parent != Path(".agent") for path in kernel):
        issues.append("profile manifest kernel files do not define the seven-file kernel")
    harness = config.get("modules", {}).get("harness", {})
    expected_trigger_contract = {
        "command_manifest": "shared/source-contracts/commands.json",
        "scm_trigger_file": ".agent/scm.json",
        "package_registry_file": ".agent/packages.json",
        "collaboration_workflow_package": "small-team-git-portfolio",
        "installed_collaboration_workflow_file": (
            ".agent/workflows/small-team-git.json"
        ),
        "collaboration_workflow_installed_by_default": False,
    }
    for key, value in expected_trigger_contract.items():
        if harness.get(key) != value:
            issues.append(f"blueprint.json harness {key} contract mismatch")
    if harness.get("supported_base_workflows") != [
        "solo_direct",
        "solo_hybrid",
        "pair_pr",
        "tiny_pr",
    ]:
        issues.append("blueprint.json small-team workflow vocabulary mismatch")
    if harness.get("maximum_supported_write_capable_humans") != 5:
        issues.append("blueprint.json maximum supported team size must be five")
    source_governance = config.get("source_governance", {})
    if source_governance != {
        "architecture_decisions": "ARCHITECTURE_DECISIONS.md",
        "decision_governance": "docs/DECISION_GOVERNANCE.md",
        "decision_governance_schema": "shared/schemas/harness-decision-governance.schema.json",
        "architectural_pattern_catalog": "patterns/catalog.json",
        "pattern_catalog_generated": False,
        "pattern_catalog_automatic_adoption": False,
        "profile_manifest": "shared/source-contracts/profile-manifest.json",
        "information_state_semantics": (
            "shared/source-contracts/information-state-semantics.json"
        ),
        "architecture_proof_schema": "patterns/architecture-proof/schema.json",
        "architecture_proof_generated": False,
    }:
        issues.append("blueprint.json source-governance contract differs")
    if "profiles" in config or "optional_contracts" in config:
        issues.append(
            "blueprint.json must not duplicate profile or optional-package inventory"
        )

    profile_schema_path = ROOT / "shared/source-contracts/profile-manifest.schema.json"
    try:
        profile_schema = load_json(profile_schema_path)
    except (ValueError, json.JSONDecodeError) as error:
        issues.append(f"invalid profile-manifest schema: {error}")
    else:
        lint_supported_schema(
            profile_schema,
            "profile-manifest.schema.json",
            issues,
        )

    if not profiles:
        issues.append("profile manifest resolved no profiles")

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
        lint_supported_schema(schema, path.name, issues)


def markdown_anchors(text: str) -> set[str]:
    anchors: set[str] = set()
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*$", text, re.MULTILINE):
        normalized = heading.strip().casefold()
        normalized = re.sub(r"[^a-z0-9 _-]", "", normalized)
        normalized = re.sub(r"[\s_]+", "-", normalized).strip("-")
        anchors.add(normalized)
    return anchors


def validate_manifest_projections(issues: list[str], scaffolder: Any) -> None:
    try:
        manifest = scaffolder.load_generation_policy()
        profiles = scaffolder.profile_contracts(manifest)
    except ValueError as error:
        issues.append(f"cannot validate manifest projections: {error}")
        return

    for projection in manifest.get("documentation_projections", []):
        if not isinstance(projection, dict):
            continue
        source = projection.get("source")
        for raw_target in projection.get("targets", []):
            if not isinstance(raw_target, str):
                continue
            raw_path, separator, anchor = raw_target.partition("#")
            target = repository_path(raw_path)
            if not target.is_file():
                issues.append(
                    f"manifest documentation projection target is absent: {raw_target}"
                )
                continue
            text = target.read_text(encoding="utf-8")
            if separator and anchor not in markdown_anchors(text):
                issues.append(
                    f"manifest documentation projection anchor is absent: {raw_target}"
                )
            if source == "profiles":
                folded = text.casefold()
                for profile_id, profile in profiles.items():
                    label = str(profile.get("label", "")).casefold()
                    if profile_id.casefold() not in folded and label not in folded:
                        issues.append(
                            f"{raw_path}: profile projection omits {profile_id}"
                        )
            elif source == "acceptance_criteria":
                if raw_path == "harness/BLUEPRINT.md":
                    section = text.split("## 14. Acceptance criteria", 1)[-1].split(
                        "## 15. Evidence crosswalk", 1
                    )[0]
                    documented = {
                        int(match.group(1))
                        for match in re.finditer(
                            r"^(\d+)\. ", section, re.MULTILINE
                        )
                    }
                    expected = {
                        int(item["id"])
                        for item in manifest.get("acceptance_criteria", [])
                        if isinstance(item, dict) and isinstance(item.get("id"), int)
                    }
                    if documented != expected:
                        issues.append(
                            "harness acceptance criteria differ from the profile manifest"
                        )
                elif raw_path.endswith("test_acceptance.py") and (
                    'PROFILE_MANIFEST["acceptance_criteria"]' not in text
                ):
                    issues.append(
                        "acceptance suite does not derive coverage from the profile manifest"
                    )

    profile_fields = {"profile", "from_profile", "to_profile", "minimum_profile"}
    expected_profile_ids = set(profiles)

    def visit(value: Any, location: str) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                child_location = f"{location}.{key}"
                if (
                    key in profile_fields
                    and isinstance(child, dict)
                    and isinstance(child.get("enum"), list)
                    and set(child["enum"]) != expected_profile_ids
                ):
                    issues.append(
                        f"{child_location}: profile enum differs from the manifest"
                    )
                visit(child, child_location)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, f"{location}[{index}]")

    for path in sorted((ROOT / "shared/schemas").glob("*.schema.json")):
        try:
            visit(load_json(path), path.name)
        except (OSError, ValueError, json.JSONDecodeError):
            continue

    validator_template = (
        SKILL_ROOT / "assets/templates/core/.agent/scripts/validate.py.tmpl"
    ).read_text(encoding="utf-8")
    if (
        "{{PROFILE_OPERATIONAL_FILES_JSON}}" not in validator_template
        or "{{KERNEL_FILES_JSON}}" not in validator_template
        or "CORE_OPERATIONAL_FILES" in validator_template
    ):
        issues.append(
            "generated validator inventories are not projected from the manifest"
        )


def validate_artifact_types(issues: list[str], scaffolder: Any) -> None:
    try:
        manifest = scaffolder.load_generation_policy()
        profiles = tuple(scaffolder.profile_layers(manifest))
    except ValueError as error:
        issues.append(f"cannot validate artifact profiles: {error}")
        return
    try:
        source = load_json(ROOT / "dossier/artifact-types.json")
    except (ValueError, json.JSONDecodeError) as error:
        issues.append(f"invalid dossier/artifact-types.json: {error}")
        return
    if (
        not isinstance(source, dict)
        or source.get("schema_version")
        != "project-blueprint.dossier-artifact-types.v2"
        or source.get("permission_grant") is not False
        or not isinstance(source.get("artifact_types"), list)
        or not isinstance(source.get("representations"), list)
    ):
        issues.append("dossier/artifact-types.json has an invalid v2 envelope")
        return
    artifact_types = source["artifact_types"]
    representations = source["representations"]
    ids: set[str] = set()
    paths: set[str] = set()
    for index, artifact in enumerate(artifact_types):
        if not isinstance(artifact, dict):
            issues.append(f"artifact type {index} is not an object")
            continue
        artifact_id = artifact.get("id")
        if not isinstance(artifact_id, str) or not re.fullmatch(
            r"[A-Z][A-Z0-9]*-[0-9]{4}", artifact_id
        ):
            issues.append(f"artifact type {index} has invalid four-digit ID")
        elif artifact_id in ids:
            issues.append(f"duplicate artifact type ID: {artifact_id}")
        ids.add(artifact_id)
        for required in (
            "recommended_name",
            "category",
            "classification",
            "purpose",
            "questions",
            "intended_audiences",
            "owner_role",
            "required_inputs",
            "downstream_consumers",
            "recommended_formats",
            "source_of_truth_expectations",
            "dependencies",
            "creation_timing",
            "review_cadence",
            "update_triggers",
            "validation_checks",
            "triggers",
            "omission_or_combination",
            "representative_evidence",
        ):
            if required not in artifact:
                issues.append(f"artifact {artifact_id}: missing {required}")
    if len(artifact_types) < 25:
        issues.append("artifact taxonomy is unexpectedly incomplete")

    representation_ids: set[str] = set()
    for index, representation in enumerate(representations):
        if not isinstance(representation, dict):
            issues.append(f"representation {index} is not an object")
            continue
        representation_id = representation.get("id")
        path = representation.get("path")
        type_refs = representation.get("artifact_type_ids")
        if (
            not isinstance(representation_id, str)
            or not re.fullmatch(r"REP-[0-9]{4}", representation_id)
            or representation_id in representation_ids
        ):
            issues.append(f"representation {index} has invalid or duplicate ID")
        representation_ids.add(str(representation_id))
        if (
            not isinstance(path, str)
            or not path.startswith((".agent/decisions/", "project-dossier/"))
            or path in paths
        ):
            issues.append(f"representation {representation_id}: invalid/duplicate path")
        paths.add(str(path))
        if (
            not isinstance(type_refs, list)
            or not type_refs
            or len(type_refs) != len(set(type_refs))
            or any(item not in ids for item in type_refs)
        ):
            issues.append(
                f"representation {representation_id}: invalid artifact_type_ids"
            )
        if representation.get("profile") not in profiles:
            issues.append(f"representation {representation_id}: invalid profile")
        status = representation.get("applicability", {}).get("status")
        if len(type_refs or []) > 1 and status != "combined":
            issues.append(
                f"representation {representation_id}: combined mapping lacks status"
            )
        if len(type_refs or []) == 1 and status == "combined":
            issues.append(
                f"representation {representation_id}: singleton marked combined"
            )

    for profile in profiles:
        try:
            expected_paths = (
                set(scaffolder.collect_templates(profile))
                | set(scaffolder.schema_outputs(profile))
                | set(scaffolder.project_local_source_paths(profile, manifest))
                | set(scaffolder.derived_output_paths(profile, manifest))
                | {scaffolder.origin_path(manifest)}
            )
            selected = scaffolder.selected_artifact_registry(
                profile,
                date.today().isoformat(),
                "source-validation",
                expected_paths,
            )
        except ValueError as error:
            issues.append(f"{profile} artifact selection failed: {error}")
            continue
        if not selected.get("artifact_types") or not selected.get("representations"):
            issues.append(f"{profile} artifact selection is empty")


def validate_templates(issues: list[str], scaffolder: Any) -> None:
    try:
        manifest = scaffolder.load_generation_policy()
        profiles = tuple(scaffolder.profile_layers(manifest))
        ranks = scaffolder.profile_ranks(manifest)
        highest_profile = max(ranks, key=ranks.__getitem__)
    except ValueError as error:
        issues.append(f"cannot validate templates without profile manifest: {error}")
        return
    variables = {
        "PROJECT_NAME": 'Template "Validation" [α]',
        "PROJECT_NAME_JSON": json.dumps('Template "Validation" [α]', ensure_ascii=False),
        "PROJECT_SLUG": "template-validation",
        "CREATED_DATE": "2030-01-02",
        "BLUEPRINT_VERSION": (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        "HARNESS_KERNEL_VERSION": scaffolder.KERNEL_VERSION,
        "PROFILE": highest_profile,
        "HARNESS_REFRESH_COMMAND": "python -B .agent/scripts/refresh.py --refresh",
        "HARNESS_REFRESH_WRITES": "[]",
        "PROFILE_OPERATIONAL_FILES_JSON": "[]",
        "DERIVED_OPERATIONAL_FILES_JSON": "[]",
        "KERNEL_FILES_JSON": "[]",
        "GIT_PORTFOLIO_SHA256": str(
            scaffolder.package_contract(manifest, "small-team-git-portfolio")["sha256"]
        ),
    }
    templates_root = SKILL_ROOT / "assets/templates"
    extension_registry_template = (
        templates_root / "standard/.agent/extensions/registry.json.tmpl"
    )
    if (
        '"core_version": "{{HARNESS_KERNEL_VERSION}}"'
        not in extension_registry_template.read_text(encoding="utf-8")
    ):
        issues.append(
            "extension registry must use the harness-kernel version axis, "
            "not the blueprint release version"
        )
    for profile in profiles:
        try:
            templates = scaffolder.collect_templates(profile)
            variables["PROFILE"] = profile
            variables["PROFILE_OPERATIONAL_FILES_JSON"] = json.dumps(
                scaffolder.canonical_posix_paths(
                    scaffolder.operational_project_paths(profile, manifest)
                ),
                separators=(",", ":"),
            )
            variables["DERIVED_OPERATIONAL_FILES_JSON"] = json.dumps(
                scaffolder.canonical_posix_paths(
                    scaffolder.derived_output_paths(profile, manifest)
                    & scaffolder.operational_project_paths(profile, manifest)
                ),
                separators=(",", ":"),
            )
            variables["KERNEL_FILES_JSON"] = json.dumps(
                scaffolder.canonical_posix_paths(scaffolder.kernel_paths(manifest)),
                separators=(",", ":"),
            )
        except ValueError as error:
            issues.append(f"{profile} template collection failed: {error}")
            continue
        missing = sorted(set(scaffolder.kernel_paths(manifest)) - set(templates))
        if missing:
            issues.append(f"{profile} missing manifest-declared kernel paths: {missing}")
        if any(path.suffix in {".yaml", ".yml"} for path in templates):
            issues.append(f"{profile} canonical templates still emit YAML")
        if profile != highest_profile and any(
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
                    json.loads(
                        rendered,
                        object_pairs_hook=strict_object,
                        parse_constant=reject_json_constant,
                    )
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
    non_transfer_terms = (
        "Transfer structure and validators",
        "facts",
        "identities",
        "permissions",
        "accepted decisions",
        "evidence",
        "readiness",
    )
    if not all(term in skill for term in non_transfer_terms):
        issues.append("SKILL.md lacks explicit non-transfer boundary")
    if "pb adopt plan|apply" not in skill or "bounded semantic" not in skill:
        issues.append("SKILL.md lacks established-project adoption routing")
    openai = (SKILL_ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
    if "$project-bootstrap" not in openai:
        issues.append("agents/openai.yaml does not invoke $project-bootstrap")
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if version != "4.0.0":
        issues.append(f"development VERSION must be 4.0.0, found {version!r}")
    for path in ("CHANGELOG.md", "RELEASE.md"):
        if version not in (ROOT / path).read_text(encoding="utf-8"):
            issues.append(f"{path} lacks the {version} release")
    try:
        with (ROOT / "pyproject.toml").open("rb") as source:
            pyproject = tomllib.load(source)
    except (OSError, tomllib.TOMLDecodeError) as error:
        issues.append(f"pyproject.toml is invalid: {error}")
        pyproject = {}
    project_metadata = pyproject.get("project", {})
    if not isinstance(project_metadata, dict):
        issues.append("pyproject.toml project metadata must be a table")
        project_metadata = {}
    if project_metadata.get("requires-python") != ">=3.11":
        issues.append("pyproject.toml does not enforce Python 3.11+")
    if project_metadata.get("version") != version:
        issues.append("pyproject.toml version differs from VERSION")
    if project_metadata.get("name") != "project-blueprint":
        issues.append("pyproject.toml project name differs from release identity")
    blueprint_metadata = pyproject.get("tool", {}).get("project-blueprint", {})
    if not isinstance(blueprint_metadata, dict) or (
        blueprint_metadata.get("runtime-dependencies") != []
        or blueprint_metadata.get("canonical-structured-format") != "strict-json"
    ):
        issues.append("pyproject.toml blueprint runtime contract is invalid")
    config = load_json(ROOT / "blueprint.json")
    kernel_version = config.get("modules", {}).get("harness", {}).get(
        "kernel_version"
    )
    if kernel_version != "4.0.0":
        issues.append("blueprint.json harness kernel must be 4.0.0")
    scaffolder = load_scaffolder()
    if scaffolder.GENERATOR_VERSION != version:
        issues.append("scaffolder generator version differs from VERSION")
    if scaffolder.KERNEL_VERSION != kernel_version:
        issues.append("scaffolder kernel version differs from blueprint.json")
    schema_template = (
        SKILL_ROOT / "assets/templates/core/.agent/schema.json.tmpl"
    ).read_text(encoding="utf-8")
    validator_template = (
        SKILL_ROOT / "assets/templates/core/.agent/scripts/validate.py.tmpl"
    ).read_text(encoding="utf-8")
    if f'"kernel_version": "{kernel_version}"' not in schema_template:
        issues.append("generated schema kernel version differs from blueprint.json")
    if f'KERNEL_VERSION = "{kernel_version}"' not in validator_template:
        issues.append("generated validator kernel version differs from blueprint.json")

    commands = (
        (
            [sys.executable, "-B", "scripts/validate_skill_package.py"],
            SKILL_ROOT,
            "skill package validator",
        ),
        (
            [
                sys.executable,
                "-B",
                str(SKILL_ROOT / "scripts/verify_reference_evidence.py"),
            ],
            ROOT,
            "reference evidence validator",
        ),
    )
    for command, cwd, label in commands:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode:
            issues.append(
                f"{label} failed: {result.stderr.strip() or result.stdout.strip()}"
            )


def validate_ci_contract(issues: list[str]) -> None:
    workflow_path = ROOT / ".github/workflows/validate.yml"
    try:
        workflow = workflow_path.read_text(encoding="utf-8")
    except OSError as error:
        issues.append(f"cannot read CI workflow: {error}")
        return
    push_block = re.search(
        r"(?ms)^  push:\n(?P<body>.*?)(?=^  [A-Za-z_][^:\n]*:|\Z)",
        workflow,
    )
    if (
        push_block is None
        or push_block.group("body") != "    branches:\n      - main\n"
    ):
        issues.append("CI workflow push validation must target only main")
    if re.search(r"(?m)^  pull_request:\s*$", workflow) is None:
        issues.append("CI workflow must retain pull-request validation")
    expected_concurrency = (
        "concurrency:\n"
        "  group: ${{ github.workflow }}-${{ "
        "github.event.pull_request.number || github.ref }}\n"
        "  cancel-in-progress: ${{ github.event_name == 'pull_request' || "
        "github.ref == 'refs/heads/main' }}"
    )
    if expected_concurrency not in workflow:
        issues.append(
            "CI workflow concurrency must cancel superseded pull-request and "
            "main smoke runs without cancelling manual release matrices"
        )
    required_snippets = {
        "read-only contents permission": "permissions:\n  contents: read",
        "manual full-matrix trigger": "workflow_dispatch:",
        "stable pull-request gate": (
            "pull-request-gate:\n    name: required\n"
            "    if: github.event_name == 'pull_request'"
        ),
        "minimum-runtime pull-request gate": 'python-version: "3.11"',
        "main smoke gate": (
            "main-smoke:\n    name: main-smoke\n"
            "    if: github.event_name == 'push' && "
            "github.ref == 'refs/heads/main'"
        ),
        "current-runtime main smoke": 'python-version: "3.14"',
        "manual-only full matrix": (
            "full-matrix:\n    name: full / ${{ matrix.os }} / Python "
            "${{ matrix.python }}\n"
            "    if: github.event_name == 'workflow_dispatch'"
        ),
        "three-OS release matrix": (
            "os: [ubuntu-latest, macos-latest, windows-latest]"
        ),
        "Python 3.11-3.14 release matrix": (
            'python: ["3.11", "3.12", "3.13", "3.14"]'
        ),
        "routine cancellation": (
            "cancel-in-progress: ${{ github.event_name == 'pull_request' || "
            "github.ref == 'refs/heads/main' }}"
        ),
        "routine timeout": "timeout-minutes: 20",
        "main timeout": "timeout-minutes: 15",
        "release timeout": "timeout-minutes: 30",
        "pinned checkout action": (
            "actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803"
        ),
        "pinned setup-python action": (
            "actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1"
        ),
        "skill metadata validation": (
            "python -B skills/project-bootstrap/scripts/"
            "validate_skill_package.py"
        ),
        "reference evidence validation": (
            "python -B skills/project-bootstrap/scripts/"
            "verify_reference_evidence.py"
        ),
        "blueprint source validation": (
            "python -B skills/project-bootstrap/scripts/validate_blueprint.py"
        ),
        "acceptance suite": (
            "python -B skills/project-bootstrap/scripts/test_acceptance.py"
        ),
    }
    for label, snippet in required_snippets.items():
        if snippet not in workflow:
            issues.append(f"CI workflow lacks {label}")
    acceptance_command = (
        "python -B skills/project-bootstrap/scripts/test_acceptance.py"
    )
    if workflow.count(acceptance_command) != 2:
        issues.append(
            "CI workflow must run acceptance exactly in the pull-request gate "
            "and manually dispatched full matrix"
        )


def validate_executable_contracts(issues: list[str]) -> None:
    commands = (
        (
            [
                sys.executable,
                "-B",
                str(SKILL_ROOT / "scripts/validate_source_contracts.py"),
            ],
            ROOT,
            "source-only architectural contract validation",
        ),
        (
            [
                sys.executable,
                "-B",
                str(SKILL_ROOT / "scripts/test_architectural_patterns.py"),
            ],
            ROOT,
            "architectural pattern adversarial fixtures",
        ),
        (
            [
                sys.executable,
                "-B",
                str(SKILL_ROOT / "scripts/test_migration_1_0_1_to_2_0_0.py"),
            ],
            ROOT,
            "1.0.1 to 2.0.0 migration fixtures",
        ),
        (
            [
                sys.executable,
                "-B",
                str(SKILL_ROOT / "scripts/test_migration_2_0_0_to_3_0_0.py"),
            ],
            ROOT,
            "2.0.0 to 3.0.0 migration fixtures",
        ),
        (
            [
                sys.executable,
                "-B",
                str(SKILL_ROOT / "scripts/test_migration_3_1_0_to_4_0_0.py"),
            ],
            ROOT,
            "3.1.0 to 4.0.0 migration and live-upgrade fixtures",
        ),
        (
            [
                sys.executable,
                "-B",
                str(SKILL_ROOT / "scripts/test_velocity_workflows.py"),
            ],
            ROOT,
            "4.0.0 guided, adoption, collaboration, lifecycle, and recovery workflows",
        ),
        (
            [
                sys.executable,
                "-B",
                str(
                    SKILL_ROOT
                    / "assets/packages/operations-observability/templates/.agent/extensions/"
                    "operations-observability/tests/test_validate.py.tmpl"
                ),
            ],
            ROOT,
            "operations and observability extension fixtures",
        ),
        (
            [
                sys.executable,
                "-B",
                str(
                    SKILL_ROOT
                    / "assets/packages/security-supply-chain/templates/.agent/extensions/"
                    "security-supply-chain/tests/test_validate.py.tmpl"
                ),
            ],
            ROOT,
            "security and supply-chain extension fixtures",
        ),
    )
    for command, cwd, label in commands:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        if result.returncode:
            issues.append(
                f"{label} failed: {result.stderr.strip() or result.stdout.strip()}"
            )


def validate_profile_builds(issues: list[str], scaffolder: Any) -> None:
    try:
        manifest = scaffolder.load_generation_policy()
        profiles = tuple(scaffolder.profile_layers(manifest))
    except ValueError as error:
        issues.append(f"cannot build profiles without profile manifest: {error}")
        return
    scaffolder_script = SKILL_ROOT / "scripts/scaffold_project.py"
    with tempfile.TemporaryDirectory(prefix="project-blueprint-source-check-") as temp:
        for profile in profiles:
            for layout in ("compact", "separated"):
                target = Path(temp) / f"{profile}-{layout}"
                result = subprocess.run(
                    [
                        sys.executable,
                        "-B",
                        str(scaffolder_script),
                        "--target",
                        str(target),
                        "--project-name",
                        f'Source Check "{profile}" ({layout})',
                        "--profile",
                        profile,
                        "--layout",
                        layout,
                    ],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode:
                    issues.append(
                        f"{profile}/{layout} profile generation failed: "
                        f"{result.stderr.strip() or result.stdout.strip()}"
                    )


def main() -> int:
    issues: list[str] = []
    if sys.version_info < (3, 11):
        issues.append(f"Python 3.11+ required; found {sys.version.split()[0]}")
    for path in REQUIRED_PATHS:
        if not repository_path(path).is_file():
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
    validate_config_and_schemas(issues, scaffolder)
    validate_manifest_projections(issues, scaffolder)
    validate_artifact_types(issues, scaffolder)
    validate_templates(issues, scaffolder)
    validate_skill_and_release(issues)
    validate_ci_contract(issues)
    validate_executable_contracts(issues)
    validate_profile_builds(issues, scaffolder)
    if issues:
        print(f"FAIL: {len(issues)} issue(s)")
        for issue in issues:
            print(f"- {issue}")
        return 1
    template_count = len(list((SKILL_ROOT / "assets/templates").rglob("*.tmpl")))
    print("PASS: Project Blueprint source and profile builds are valid")
    print(f"- required files: {len(REQUIRED_PATHS)}")
    print(f"- templates: {template_count}")
    manifest = scaffolder.load_generation_policy()
    print(f"- profiles: {', '.join(scaffolder.profile_layers(manifest))}")
    print("- structured kernel: strict JSON")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
