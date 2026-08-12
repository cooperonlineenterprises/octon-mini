#!/usr/bin/env python3
"""Transactionally generate a non-authorizing harness and dossier snapshot."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import secrets
import subprocess
import sys
import tempfile
from collections.abc import Iterable
from datetime import date
from pathlib import Path, PurePath, PurePosixPath


GENERATOR_VERSION = "3.1.0"
KERNEL_VERSION = "3.0.0"
PROFILE_LAYERS = {
    "minimal": ("core",),
    "standard": ("core", "standard"),
    "high-assurance": ("core", "standard", "high-assurance"),
}
PROFILE_RANK = {"minimal": 0, "standard": 1, "high-assurance": 2}
KNOWN_VARIABLES = {
    "PROJECT_NAME",
    "PROJECT_NAME_JSON",
    "PROJECT_SLUG",
    "CREATED_DATE",
    "BLUEPRINT_VERSION",
    "HARNESS_KERNEL_VERSION",
    "PROFILE",
    "HARNESS_REFRESH_COMMAND",
    "HARNESS_REFRESH_WRITES",
}
PLACEHOLDER_RE = re.compile(r"\{\{([A-Z_]+)\}\}")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DERIVED_PATHS = {
    Path("project-dossier/ARTIFACT_CATALOG.json"),
    Path("project-dossier/machine-readable/path-authority.json"),
    Path("project-dossier/MANIFEST.json"),
}
PROJECT_LOCAL_SOURCE_PATHS = {
    Path("project-dossier/machine-readable/artifact-registry.json"),
}
HIGH_DERIVED_PATHS = {
    Path("project-dossier/CHECKSUMS.sha256"),
    Path(".agent/generated/manifest.json"),
    Path(".agent/generated/validation-report.json"),
}
GENERATION_POLICY_RELATIVE = Path(
    "shared/source-contracts/generation-policy.json"
)
GENERATION_POLICY_KEYS = {
    "schema_version",
    "document_role",
    "permission_grant",
    "default_disposition",
    "inventory_hash_algorithm",
    "rules",
    "forbidden_outputs",
    "limitations",
}
GENERATION_RULE_KEYS = {
    "id",
    "source",
    "match",
    "suffix",
    "disposition",
    "profiles",
    "inventory_paths",
    "inventory_count",
    "inventory_paths_sha256",
    "output",
    "reason",
}
GENERATION_OUTPUT_KEYS = {"root", "strip_suffix"}
FORBIDDEN_OUTPUT_KEYS = {"path", "match", "reason"}


def canonical_posix_paths(paths: Iterable[PurePath]) -> list[str]:
    """Render and sort paths identically on every host platform."""
    return sorted(path.as_posix() for path in paths)


def configure_console_output() -> None:
    """Keep diagnostics writable when the host console has a legacy codec."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(errors="backslashreplace")


def require_runtime() -> None:
    if sys.version_info < (3, 11):
        raise ValueError(
            "Project Blueprint requires Python 3.11 or newer; "
            f"found {sys.version.split()[0]}."
        )


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def blueprint_root() -> Path:
    candidates = (
        Path(__file__).resolve().parents[3],
        skill_root() / "assets" / "blueprint-source",
    )
    for candidate in candidates:
        if (
            (candidate / "VERSION").is_file()
            and (candidate / "dossier/artifact-types.json").is_file()
            and (candidate / "shared/schemas").is_dir()
        ):
            return candidate
    raise ValueError(
        "Blueprint source bundle not found beside the skill or in its source checkout."
    )


def strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_nonfinite(value: str) -> object:
    raise ValueError(f"non-finite JSON number is prohibited: {value}")


def load_json(path: Path) -> object:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=strict_object,
            parse_constant=reject_nonfinite,
        )
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON {path}: {error}") from error


def blueprint_version() -> str:
    version_path = blueprint_root() / "VERSION"
    if not version_path.is_file():
        raise ValueError(f"Blueprint VERSION not found: {version_path}")
    version = version_path.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError(f"Invalid blueprint version: {version!r}")
    return version


def validate_project_name(value: str) -> str:
    name = value.strip()
    if not name:
        raise ValueError("--project-name must not be empty.")
    if len(name) > 200:
        raise ValueError("--project-name must be 200 characters or fewer.")
    if any(ord(character) < 32 or ord(character) == 127 for character in name):
        raise ValueError("--project-name must not contain control characters.")
    if "{{" in name or "}}" in name:
        raise ValueError("--project-name must not contain template delimiters.")
    return name


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    if not slug:
        suffix = hashlib.sha256(value.encode("utf-8")).hexdigest()[:8]
        slug = f"project-{suffix}"
    if not SLUG_RE.fullmatch(slug):
        raise ValueError("Project name cannot produce a portable project slug.")
    return slug


def markdown_escape(value: str) -> str:
    escaped = (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return re.sub(r"([\\`*_\{\}\[\]()#+.!|~-])", r"\\\1", escaped)


def policy_source_path(value: object, label: str) -> Path:
    if not isinstance(value, str) or ":" not in value or "\\" in value:
        raise ValueError(f"{label}: invalid logical source {value!r}")
    namespace, raw_path = value.split(":", 1)
    relative = PurePosixPath(raw_path)
    if (
        namespace not in {"skill", "blueprint"}
        or relative.is_absolute()
        or not relative.parts
        or any(part in {"", ".", ".."} for part in relative.parts)
    ):
        raise ValueError(f"{label}: unsafe logical source {value!r}")
    root = skill_root() if namespace == "skill" else blueprint_root()
    return root.joinpath(*relative.parts)


def generation_inventory_digest(paths: list[str]) -> str:
    payload = "".join(f"{path}\n" for path in sorted(paths)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def generation_inventory_path(value: object, label: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError(f"{label}: invalid relative path {value!r}")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or not path.parts
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        raise ValueError(f"{label}: unsafe relative path {value!r}")
    return path.as_posix()


def generation_rule_declared_paths(rule: dict[str, object]) -> list[str]:
    rule_id = str(rule.get("id"))
    raw_paths = rule.get("inventory_paths")
    if not isinstance(raw_paths, list):
        raise ValueError(
            f"generation rule {rule_id}: reviewed inventory paths are missing"
        )
    paths = [
        generation_inventory_path(item, f"generation rule {rule_id}")
        for item in raw_paths
    ]
    if not paths or len(paths) != len(set(paths)):
        raise ValueError(
            f"generation rule {rule_id}: reviewed inventory paths are empty or duplicate"
        )
    return paths


def generation_rule_source_root(rule: dict[str, object]) -> tuple[Path, Path]:
    rule_id = str(rule.get("id"))
    source = policy_source_path(rule.get("source"), f"generation rule {rule_id}")
    if rule.get("match") == "exact":
        return source.parent, source
    return source, source


def generation_rule_inventory(
    rule: dict[str, object],
) -> tuple[list[Path], list[str]]:
    rule_id = str(rule.get("id"))
    relative_paths = generation_rule_declared_paths(rule)
    source_root, exact_source = generation_rule_source_root(rule)
    if source_root.is_symlink():
        raise ValueError(
            f"generation rule {rule_id}: approved source root may not be a symlink"
        )
    if not source_root.is_dir():
        raise ValueError(f"generation rule {rule_id}: source root is missing")
    if rule.get("match") == "exact":
        expected = [exact_source.name]
        if relative_paths != expected:
            raise ValueError(
                f"generation rule {rule_id}: exact inventory must be {expected!r}"
            )
    boundary = source_root.resolve(strict=True)
    candidates = [
        source_root.joinpath(*PurePosixPath(path).parts)
        for path in relative_paths
    ]

    for candidate in candidates:
        if candidate.is_symlink():
            raise ValueError(
                f"generation rule {rule_id}: selected source may not be a symlink: "
                f"{candidate}"
            )
        if not candidate.exists():
            raise ValueError(
                f"generation rule {rule_id}: reviewed source is missing: {candidate}"
            )
        if not candidate.is_file():
            raise ValueError(
                f"generation rule {rule_id}: reviewed source is not a regular file: "
                f"{candidate}"
            )
        try:
            candidate.resolve(strict=True).relative_to(boundary)
        except ValueError as error:
            raise ValueError(
                f"generation rule {rule_id}: source escapes approved root: {candidate}"
            ) from error
    return candidates, relative_paths


def observed_generation_rule_paths(rule: dict[str, object]) -> list[str]:
    source_root, exact_source = generation_rule_source_root(rule)
    if source_root.is_symlink() or not source_root.is_dir():
        return []
    if rule.get("match") == "exact":
        return [exact_source.name] if exact_source.is_file() else []
    suffix = rule.get("suffix")
    return sorted(
        path.relative_to(source_root).as_posix()
        for path in source_root.rglob("*")
        if (path.is_file() or path.is_symlink())
        and (
            rule.get("match") == "recursive"
            or (
                rule.get("match") == "recursive_suffix"
                and isinstance(suffix, str)
                and path.name.endswith(suffix)
            )
        )
    )


def load_generation_policy() -> dict[str, object]:
    path = blueprint_root() / GENERATION_POLICY_RELATIVE
    value = load_json(path)
    if not isinstance(value, dict) or set(value) != GENERATION_POLICY_KEYS:
        raise ValueError("generation policy has an invalid top-level contract")
    if (
        value.get("schema_version") != "project-blueprint.generation-policy.v2"
        or value.get("document_role")
        != "authoritative_source_to_generated_snapshot_disposition"
        or value.get("permission_grant") is not False
        or value.get("default_disposition") != "source_only"
        or value.get("inventory_hash_algorithm")
        != "sha256_sorted_relative_posix_paths_newline_v1"
    ):
        raise ValueError("generation policy identity or non-authority contract differs")

    rules = value.get("rules")
    if not isinstance(rules, list) or not rules:
        raise ValueError("generation policy requires rules")
    seen_ids: set[str] = set()
    seen_sources: set[str] = set()
    valid_profiles = set(PROFILE_LAYERS)
    for index, raw in enumerate(rules):
        label = f"generation policy rule {index}"
        if not isinstance(raw, dict) or set(raw) != GENERATION_RULE_KEYS:
            raise ValueError(f"{label}: invalid rule contract")
        rule_id = raw.get("id")
        source_ref = raw.get("source")
        match = raw.get("match")
        suffix = raw.get("suffix")
        disposition = raw.get("disposition")
        profiles = raw.get("profiles")
        inventory_paths = raw.get("inventory_paths")
        count = raw.get("inventory_count")
        digest = raw.get("inventory_paths_sha256")
        output = raw.get("output")
        if (
            not isinstance(rule_id, str)
            or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", rule_id)
            or rule_id in seen_ids
        ):
            raise ValueError(f"{label}: invalid or duplicate rule ID")
        if not isinstance(source_ref, str) or source_ref in seen_sources:
            raise ValueError(f"{label}: invalid or duplicate logical source")
        policy_source_path(source_ref, label)
        seen_ids.add(rule_id)
        seen_sources.add(source_ref)
        if match not in {"exact", "recursive", "recursive_suffix"}:
            raise ValueError(f"{label}: invalid match mode")
        if (match == "recursive_suffix") != (
            isinstance(suffix, str) and suffix.startswith(".")
        ):
            raise ValueError(f"{label}: suffix and match mode are incoherent")
        if disposition not in {"source_only", "generated", "profile_optional"}:
            raise ValueError(f"{label}: invalid disposition")
        if (
            not isinstance(profiles, list)
            or len(profiles) != len(set(profiles))
            or any(profile not in valid_profiles for profile in profiles)
        ):
            raise ValueError(f"{label}: invalid profile set")
        if disposition == "source_only":
            if (
                profiles
                or inventory_paths is not None
                or count is not None
                or digest is not None
                or output is not None
            ):
                raise ValueError(f"{label}: source-only rule may not declare generation")
            continue
        if not profiles:
            raise ValueError(f"{label}: generated rule requires at least one profile")
        if disposition == "profile_optional" and match != "exact":
            raise ValueError(f"{label}: profile-optional source must be exact")
        if not isinstance(output, dict) or set(output) != GENERATION_OUTPUT_KEYS:
            raise ValueError(f"{label}: generated output contract is incomplete")
        output_root = output.get("root")
        strip_suffix = output.get("strip_suffix")
        portable_project_path(output_root, f"{label} output root")
        if strip_suffix is not None and (
            not isinstance(strip_suffix, str)
            or not strip_suffix.startswith(".")
            or strip_suffix != suffix
        ):
            raise ValueError(f"{label}: output suffix removal is incoherent")
        relative_paths = generation_rule_declared_paths(raw)
        if (
            not isinstance(count, int)
            or isinstance(count, bool)
            or count < 1
            or not isinstance(digest, str)
            or not re.fullmatch(r"[0-9a-f]{64}", digest)
        ):
            raise ValueError(f"{label}: generated inventory contract is incomplete")
        actual_digest = generation_inventory_digest(relative_paths)
        if len(relative_paths) != count or actual_digest != digest:
            raise ValueError(
                f"{label}: source inventory differs from the reviewed policy "
                f"(expected {count}/{digest}, found "
                f"{len(relative_paths)}/{actual_digest})"
            )

    forbidden = value.get("forbidden_outputs")
    if not isinstance(forbidden, list) or not forbidden:
        raise ValueError("generation policy requires forbidden output rules")
    seen_forbidden: set[tuple[str, str]] = set()
    for index, raw in enumerate(forbidden):
        label = f"forbidden output rule {index}"
        if not isinstance(raw, dict) or set(raw) != FORBIDDEN_OUTPUT_KEYS:
            raise ValueError(f"{label}: invalid rule contract")
        path_value = raw.get("path")
        match = raw.get("match")
        portable_project_path(path_value, label)
        key = (str(path_value), str(match))
        if match not in {"exact", "subtree"} or key in seen_forbidden:
            raise ValueError(f"{label}: invalid or duplicate match")
        seen_forbidden.add(key)
    limitations = value.get("limitations")
    if not isinstance(limitations, list) or not limitations or not all(
        isinstance(item, str) and item.strip() for item in limitations
    ):
        raise ValueError("generation policy limitations must be explicit")
    return value


def generation_rule_output_path(rule: dict[str, object], relative: str) -> Path:
    rule_id = str(rule.get("id"))
    output = rule.get("output")
    if not isinstance(output, dict):
        raise ValueError(f"generation rule {rule_id}: output contract is missing")
    root = portable_project_path(
        output.get("root"), f"generation rule {rule_id} output root"
    )
    source_relative = portable_project_path(
        relative, f"generation rule {rule_id} inventory path"
    )
    destination = root / source_relative
    strip_suffix = output.get("strip_suffix")
    if strip_suffix is not None:
        if not isinstance(strip_suffix, str) or not destination.name.endswith(
            strip_suffix
        ):
            raise ValueError(
                f"generation rule {rule_id}: source path lacks output suffix"
            )
        destination = Path(str(destination)[: -len(strip_suffix)])
    return portable_project_path(
        destination.as_posix(), f"generation rule {rule_id} output"
    )


def resolve_generation_inputs(
    profile: str, policy: dict[str, object]
) -> tuple[dict[Path, Path], dict[Path, Path]]:
    templates: dict[Path, Path] = {}
    copied_files: dict[Path, Path] = {}
    for raw in policy.get("rules", []):
        if (
            not isinstance(raw, dict)
            or raw.get("disposition") not in {"generated", "profile_optional"}
            or profile not in raw.get("profiles", [])
        ):
            continue
        sources, relative_paths = generation_rule_inventory(raw)
        output = raw.get("output")
        is_template = isinstance(output, dict) and output.get("strip_suffix") is not None
        bucket = templates if is_template else copied_files
        for source, relative in zip(sources, relative_paths, strict=True):
            destination = generation_rule_output_path(raw, relative)
            if destination in templates or destination in copied_files:
                raise ValueError(
                    f"generation rule {raw.get('id')}: duplicate output path "
                    f"{destination}"
                )
            reason = forbidden_output_reason(destination, policy)
            if reason:
                raise ValueError(
                    f"{destination}: forbidden generated output: {reason}"
                )
            bucket[destination] = source
    if not templates:
        raise ValueError(f"No reviewed templates resolved for profile {profile}")
    return templates, copied_files


def generation_policy_diagnostics(
    policy: dict[str, object], profiles: Iterable[str] | None = None
) -> dict[str, object]:
    selected_profiles = tuple(profiles) if profiles is not None else tuple(PROFILE_LAYERS)
    if (
        not selected_profiles
        or len(selected_profiles) != len(set(selected_profiles))
        or any(profile not in PROFILE_LAYERS for profile in selected_profiles)
    ):
        raise ValueError("generation diagnostics require valid unique profiles")
    status = {
        profile: {
            "capability": "project_generation",
            "mode": "normal",
            "finding_count": 0,
        }
        for profile in selected_profiles
    }
    findings: list[dict[str, object]] = []

    def add_finding(
        *,
        failure_class: str,
        severity: str,
        rule: dict[str, object],
        affected_profiles: list[str],
        paths: list[str],
        effect: str,
        recovery: str,
        candidate_policy_update: dict[str, object] | None = None,
    ) -> None:
        findings.append(
            {
                "failure_class": failure_class,
                "severity": severity,
                "rule_id": rule.get("id"),
                "affected_profiles": affected_profiles,
                "paths": paths,
                "effect": effect,
                "recovery": recovery,
                "candidate_policy_update": candidate_policy_update,
            }
        )
        for profile in affected_profiles:
            profile_status = status[profile]
            profile_status["finding_count"] = int(
                profile_status["finding_count"]
            ) + 1
            if severity == "error":
                profile_status["mode"] = "blocked"
            elif profile_status["mode"] == "normal":
                profile_status["mode"] = "degraded"

    for raw in policy.get("rules", []):
        if (
            not isinstance(raw, dict)
            or raw.get("disposition") not in {"generated", "profile_optional"}
        ):
            continue
        affected = [
            profile
            for profile in selected_profiles
            if profile in raw.get("profiles", [])
        ]
        if not affected:
            continue
        declared = set(generation_rule_declared_paths(raw))
        observed = set(observed_generation_rule_paths(raw))
        unreviewed = sorted(observed - declared)
        missing = sorted(declared - observed)
        safety_error: str | None = None
        try:
            generation_rule_inventory(raw)
        except ValueError as error:
            message = str(error)
            if any(
                marker in message
                for marker in (
                    "symlink",
                    "escapes approved root",
                    "not a regular file",
                    "unsafe",
                )
            ):
                safety_error = message
        if safety_error is not None:
            add_finding(
                failure_class="safety_invariant_degradation",
                severity="error",
                rule=raw,
                affected_profiles=affected,
                paths=[safety_error],
                effect="affected profile generation is blocked",
                recovery=(
                    "Restore confined regular files at the reviewed paths, then "
                    "rerun diagnostics."
                ),
            )
        elif missing:
            add_finding(
                failure_class="dependency_degradation",
                severity="error",
                rule=raw,
                affected_profiles=affected,
                paths=missing,
                effect="affected profile generation is blocked",
                recovery=(
                    "Restore the reviewed inputs or approve an explicit inventory "
                    "migration; do not substitute an unreviewed file."
                ),
            )
        if unreviewed:
            add_finding(
                failure_class="information_degradation",
                severity="warning",
                rule=raw,
                affected_profiles=affected,
                paths=unreviewed,
                effect="unreviewed paths are ignored and never generated",
                recovery=(
                    "Review the paths and either remove them, keep them source-only, "
                    "or explicitly update the versioned policy inventory."
                ),
                candidate_policy_update=(
                    {
                        "status": "review_required_not_approved",
                        "inventory_paths": sorted(declared | set(unreviewed)),
                        "inventory_count": len(declared | set(unreviewed)),
                        "inventory_paths_sha256": generation_inventory_digest(
                            sorted(declared | set(unreviewed))
                        ),
                    }
                    if not missing and safety_error is None
                    else None
                ),
            )

    for profile in selected_profiles:
        if status[profile]["mode"] == "blocked":
            continue
        try:
            resolve_generation_inputs(profile, policy)
        except ValueError as error:
            add_finding(
                failure_class="safety_invariant_degradation",
                severity="error",
                rule={"id": "profile-output-boundary"},
                affected_profiles=[profile],
                paths=[str(error)],
                effect="affected profile generation is blocked",
                recovery=(
                    "Restore the reviewed output mapping and rerun diagnostics; "
                    "no bypass or force mode is available."
                ),
            )

    overall_mode = "normal"
    if any(item["mode"] == "blocked" for item in status.values()):
        overall_mode = "blocked"
    elif any(item["mode"] == "degraded" for item in status.values()):
        overall_mode = "degraded"
    return {
        "schema_version": "project-blueprint.generation-policy-diagnostics.v1",
        "operation_mode": "recovering",
        "capability_status": overall_mode,
        "permission_grant": False,
        "profiles": status,
        "findings": findings,
        "limitations": [
            "Diagnostics are read-only and do not approve or modify an inventory.",
            "Inventory diagnostics do not render templates or prove their content valid.",
            "A normal structural result does not establish project readiness.",
        ],
    }


def generation_profile_mode(report: dict[str, object], profile: str) -> str:
    profiles = report.get("profiles")
    if not isinstance(profiles, dict):
        raise ValueError("generation diagnostics lack profile status")
    selected = profiles.get(profile)
    if not isinstance(selected, dict) or selected.get("mode") not in {
        "normal",
        "degraded",
        "blocked",
    }:
        raise ValueError(f"generation diagnostics lack valid status for {profile}")
    return str(selected["mode"])


def generation_profile_findings(
    report: dict[str, object], profile: str
) -> list[dict[str, object]]:
    return [
        finding
        for finding in report.get("findings", [])
        if isinstance(finding, dict)
        and profile in finding.get("affected_profiles", [])
    ]


def generation_rule_matches_source(source: Path, rule: dict[str, object]) -> bool:
    base = policy_source_path(rule.get("source"), f"generation rule {rule.get('id')}")
    match = rule.get("match")
    if match == "exact":
        return source == base
    try:
        source.relative_to(base)
    except ValueError:
        return False
    return match == "recursive" or (
        match == "recursive_suffix"
        and isinstance(rule.get("suffix"), str)
        and source.name.endswith(str(rule["suffix"]))
    )


def forbidden_output_reason(
    destination: Path, policy: dict[str, object]
) -> str | None:
    for raw in policy.get("forbidden_outputs", []):
        if not isinstance(raw, dict):
            continue
        boundary = portable_project_path(raw.get("path"), "forbidden output")
        match = raw.get("match")
        if destination == boundary or (
            match == "subtree" and boundary in destination.parents
        ):
            return str(raw.get("reason"))
    return None


def validate_generation_boundary(
    profile: str,
    templates: dict[Path, Path],
    schemas: dict[Path, Path],
    policy: dict[str, object],
) -> None:
    issues: list[str] = []
    duplicate_destinations = sorted(set(templates) & set(schemas))
    if duplicate_destinations:
        issues.append(
            "template/schema output collision: "
            + ", ".join(path.as_posix() for path in duplicate_destinations)
        )
    selected = {**templates, **schemas}
    authorized_templates, authorized_schemas = resolve_generation_inputs(
        profile, policy
    )
    authorized = {**authorized_templates, **authorized_schemas}

    selected_sources = set(selected.values())
    if len(selected_sources) != len(selected):
        issues.append("a reviewed source was selected for more than one output")
    for destination, source in selected.items():
        try:
            normalized_destination = portable_project_path(
                destination.as_posix(), "generated output"
            )
        except ValueError as error:
            issues.append(str(error))
            continue
        if normalized_destination != destination:
            issues.append(f"{destination}: generated output is not normalized")
            continue
        expected_source = authorized.get(destination)
        if expected_source is None:
            matches = [
                rule
                for rule in policy.get("rules", [])
                if isinstance(rule, dict)
                and generation_rule_matches_source(source, rule)
            ]
            source_only = next(
                (
                    rule
                    for rule in matches
                    if rule.get("disposition") == "source_only"
                ),
                None,
            )
            if source_only is not None:
                issues.append(
                    f"{destination}: source-only input is prohibited "
                    f"({source_only.get('id')})"
                )
            else:
                issues.append(
                    f"{destination}: output is absent from the reviewed "
                    f"{profile} inventory"
                )
        elif source != expected_source:
            issues.append(
                f"{destination}: selected source differs from the reviewed source"
            )
        reason = forbidden_output_reason(destination, policy)
        if reason:
            issues.append(f"{destination}: forbidden generated output: {reason}")

    authorized_sources = set(authorized.values())
    unexpected = sorted(selected_sources - authorized_sources)
    missing = sorted(authorized_sources - selected_sources)
    if unexpected:
        issues.append(
            "unreviewed generation inputs selected: "
            + ", ".join(path.as_posix() for path in unexpected)
        )
    if missing:
        issues.append(
            "reviewed generation inputs were not selected: "
            + ", ".join(path.as_posix() for path in missing)
        )
    if issues:
        raise ValueError("generation boundary rejected the inventory: " + "; ".join(issues))


def collect_templates(
    profile: str, policy: dict[str, object] | None = None
) -> dict[Path, Path]:
    selected_policy = policy if policy is not None else load_generation_policy()
    templates, _ = resolve_generation_inputs(profile, selected_policy)
    return templates


def render(template: Path, variables: dict[str, str]) -> str:
    content = template.read_text(encoding="utf-8")
    unknown = sorted(set(PLACEHOLDER_RE.findall(content)) - KNOWN_VARIABLES)
    if unknown:
        raise ValueError(f"Unknown variables in {template}: {', '.join(unknown)}")
    for key, value in variables.items():
        content = content.replace("{{" + key + "}}", value)
    unresolved = sorted(set(PLACEHOLDER_RE.findall(content)))
    if unresolved:
        raise ValueError(
            f"Unresolved variables in {template}: {', '.join(unresolved)}"
        )
    return content.rstrip() + "\n"


def validate_target(target: Path) -> None:
    if not target.is_absolute():
        raise ValueError("--target must be an absolute path.")
    resolved = target.resolve()
    if resolved in {Path("/"), Path.home().resolve(), blueprint_root().resolve()}:
        raise ValueError(f"Refusing unsafe generation target: {resolved}")
    if resolved.exists() and not resolved.is_dir():
        raise ValueError(f"Target is not a directory: {resolved}")
    if resolved.exists() and any(resolved.iterdir()):
        raise ValueError(
            "New-project generation requires a nonexistent or empty target. "
            "Use plan_adoption.py for an established project."
        )
    if not resolved.parent.is_dir():
        raise ValueError(
            f"Target parent must already exist for atomic generation: {resolved.parent}"
        )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


def generation_id() -> str:
    return secrets.token_hex(16)


def schema_outputs(
    profile: str, policy: dict[str, object] | None = None
) -> dict[Path, Path]:
    selected_policy = policy if policy is not None else load_generation_policy()
    _, outputs = resolve_generation_inputs(profile, selected_policy)
    return outputs


def portable_project_path(value: object, label: str) -> Path:
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError(f"{label}: invalid path {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError(f"{label}: unsafe path {value!r}")
    return Path(*path.parts)


def selected_artifact_registry(
    profile: str,
    created: str,
    project_slug: str,
    expected_paths: set[Path],
) -> dict[str, object]:
    source = load_json(blueprint_root() / "dossier" / "artifact-types.json")
    if (
        not isinstance(source, dict)
        or source.get("schema_version")
        != "project-blueprint.dossier-artifact-types.v2"
        or source.get("permission_grant") is not False
        or not isinstance(source.get("artifact_types"), list)
        or not isinstance(source.get("representations"), list)
    ):
        raise ValueError("dossier/artifact-types.json has an invalid top-level shape")

    types_by_id: dict[str, dict[str, object]] = {}
    selected_type_ids: set[str] = set()
    for index, raw in enumerate(source["artifact_types"]):
        if not isinstance(raw, dict):
            raise ValueError(f"artifact type {index} must be an object")
        artifact_type_id = raw.get("id")
        if (
            not isinstance(artifact_type_id, str)
            or not re.fullmatch(r"[A-Z]{3}-[0-9]{4}", artifact_type_id)
            or artifact_type_id in types_by_id
        ):
            raise ValueError(
                f"artifact type {index} has an invalid or duplicate ID"
            )
        type_profile = raw.get("profile")
        if type_profile not in PROFILE_RANK:
            raise ValueError(
                f"artifact type {artifact_type_id}: invalid profile"
            )
        types_by_id[artifact_type_id] = copy.deepcopy(raw)
        if PROFILE_RANK[str(type_profile)] <= PROFILE_RANK[profile]:
            selected_type_ids.add(artifact_type_id)

    selected_representations: list[dict[str, object]] = []
    seen_representation_ids: set[str] = set()
    seen_paths: set[str] = set()
    for index, raw in enumerate(source["representations"]):
        if not isinstance(raw, dict):
            raise ValueError(f"representation {index} must be an object")
        representation_profile = raw.get("profile")
        if representation_profile not in PROFILE_RANK:
            raise ValueError(
                f"representation {raw.get('id')}: invalid profile"
            )
        if PROFILE_RANK[str(representation_profile)] > PROFILE_RANK[profile]:
            continue
        representation_id = raw.get("id")
        artifact_type_ids = raw.get("artifact_type_ids")
        if (
            not isinstance(representation_id, str)
            or not re.fullmatch(r"REP-[0-9]{4}", representation_id)
            or representation_id in seen_representation_ids
        ):
            raise ValueError(
                f"representation {index} has an invalid or duplicate ID"
            )
        if (
            not isinstance(artifact_type_ids, list)
            or not artifact_type_ids
            or any(not isinstance(item, str) for item in artifact_type_ids)
            or len(artifact_type_ids) != len(set(artifact_type_ids))
            or any(item not in selected_type_ids for item in artifact_type_ids)
        ):
            raise ValueError(
                f"representation {representation_id} has invalid artifact_type_ids"
            )
        path = portable_project_path(
            raw.get("path"), f"representation {representation_id}"
        )
        if path.as_posix() in seen_paths:
            raise ValueError(f"duplicate representation path: {path.as_posix()}")
        if path not in expected_paths:
            raise ValueError(
                f"representation path absent from selected profile: {path.as_posix()}"
            )
        selected_representations.append(copy.deepcopy(raw))
        seen_representation_ids.add(representation_id)
        seen_paths.add(path.as_posix())

    expected_dossier = {
        path.as_posix()
        for path in expected_paths
        if path.as_posix().startswith("project-dossier/")
    }
    represented_dossier = {
        str(item["path"])
        for item in selected_representations
        if str(item["path"]).startswith("project-dossier/")
    }
    if expected_dossier != represented_dossier:
        missing = sorted(expected_dossier - represented_dossier)
        extra = sorted(represented_dossier - expected_dossier)
        details = []
        if missing:
            details.append("unrepresented expected paths: " + ", ".join(missing))
        if extra:
            details.append("unexpected represented paths: " + ", ".join(extra))
        raise ValueError("artifact registry coverage mismatch: " + "; ".join(details))

    selected_types = [
        types_by_id[str(raw["id"])]
        for raw in source["artifact_types"]
        if isinstance(raw, dict) and raw.get("id") in selected_type_ids
    ]
    return {
        "schema_version": "project-dossier.artifact-registry.v2",
        "document_role": "authoritative_project_local_artifact_metadata",
        "permission_grant": False,
        "dossier_version": blueprint_version(),
        "profile": profile,
        "project_slug": project_slug,
        "generated_on": created,
        "artifact_types": selected_types,
        "representations": selected_representations,
    }


def write_artifact_registry(
    stage: Path,
    profile: str,
    created: str,
    project_slug: str,
    expected_paths: set[Path],
) -> None:
    registry = selected_artifact_registry(
        profile, created, project_slug, expected_paths
    )
    write_json(
        stage / "project-dossier/machine-readable/artifact-registry.json",
        registry,
    )


def configure_high_assurance_extension(stage: Path) -> None:
    registry_path = stage / ".agent" / "extensions" / "registry.json"
    registry = load_json(registry_path)
    if not isinstance(registry, dict):
        raise ValueError("extension registry must be an object")
    extensions = registry.get("extensions")
    if not isinstance(extensions, list):
        raise ValueError("extension registry extensions must be an array")
    if any(
        isinstance(item, dict) and item.get("id") == "sample-restriction"
        for item in extensions
    ):
        raise ValueError("sample-restriction extension is already registered")
    extensions.append(
        {
            "id": "sample-restriction",
            "enabled": False,
            "version": "3.0.0",
            "path": ".agent/extensions/sample-restriction",
            "requires_core": "^3.0.0",
            "config": ".agent/extensions/sample-restriction/config.json",
            "validator": ".agent/extensions/sample-restriction/validate.py",
            "owner": "unassigned",
            "provenance": "generated_domain_neutral_reference_extension",
            "trust_class": "unassessed_project_local_code",
            "trust_decision_ref": None,
            "side_effects": "read_only",
            "network_access": "denied",
            "filesystem_writes": "prohibited",
            "authority_effect": "restrictions_only",
            "deprecated_at": None,
            "removal_version": None,
            "successor": None,
        }
    )
    registry["limitations"] = [
        "Reference extension only; project adoption must assess actual needs."
    ]
    write_json(registry_path, registry)


def write_origin(
    stage: Path,
    version: str,
    profile: str,
    created: str,
    project_name: str,
    slug: str,
    identifier: str,
    expected_paths: set[Path],
) -> None:
    write_json(
        stage / ".project-blueprint-origin.json",
        {
            "schema_version": "project-blueprint.origin.v1",
            "blueprint": "project-blueprint",
            "blueprint_version": version,
            "generator_version": GENERATOR_VERSION,
            "generation_id": identifier,
            "profile": profile,
            "generated_on": created,
            "project_name": project_name,
            "project_slug": slug,
            "harness_kernel_version": KERNEL_VERSION,
            "authority": (
                "Generation provenance only; does not grant permission or "
                "establish project facts, decisions, implementation, or readiness."
            ),
            "initial_generation": {
                "blueprint_version": version,
                "generator_version": GENERATOR_VERSION,
                "generation_id": identifier,
                "generated_on": created,
                "profile": profile,
            },
            "migration_history": [],
            "generated_paths": [
                path.as_posix() for path in sorted(expected_paths)
            ],
        },
    )


def staged_inventory_issues(stage: Path, expected_paths: set[Path]) -> list[str]:
    issues: list[str] = []
    actual_paths: set[Path] = set()
    actual_directories: set[Path] = set()
    expected_directories = {
        parent
        for path in expected_paths
        for parent in path.parents
        if parent != Path(".")
    }
    for path in sorted(stage.rglob("*")):
        relative = path.relative_to(stage)
        if path.is_symlink():
            issues.append(f"generated snapshot contains a symlink: {relative}")
        elif path.is_file():
            actual_paths.add(relative)
        elif path.is_dir():
            actual_directories.add(relative)
        else:
            issues.append(f"generated snapshot contains a special file: {relative}")
    missing = sorted(expected_paths - actual_paths)
    unexpected = sorted(actual_paths - expected_paths)
    unexpected_directories = sorted(actual_directories - expected_directories)
    issues.extend(f"missing generated file: {path}" for path in missing)
    issues.extend(f"unexpected generated file: {path}" for path in unexpected)
    issues.extend(
        f"unexpected generated directory: {path}"
        for path in unexpected_directories
    )
    return issues


def validate_generated(stage: Path, expected_paths: set[Path]) -> list[str]:
    issues = staged_inventory_issues(stage, expected_paths)
    for relative in sorted(expected_paths):
        path = stage / relative
        if not path.is_file():
            continue
        if path.suffix in {".md", ".json"}:
            text = path.read_text(encoding="utf-8")
            if PLACEHOLDER_RE.search(text):
                issues.append(f"unresolved template variable: {relative}")
        if (
            path.suffix == ".json"
            and not relative.as_posix().startswith(
                ".agent/tests/fixtures/invalid/"
            )
        ):
            try:
                load_json(path)
            except ValueError as error:
                issues.append(str(error))
    try:
        policy = load_json(stage / ".agent" / "policy.json")
        if not isinstance(policy, dict) or policy.get("permission_grant") is not False:
            issues.append(".agent/policy.json is not explicitly non-authorizing")
    except ValueError as error:
        issues.append(str(error))
    dossier = stage / "project-dossier" / "README.md"
    if dossier.is_file() and "Documentation only" not in dossier.read_text(
        encoding="utf-8"
    ):
        issues.append("project-dossier/README.md lacks documentation-only boundary")
    return issues


def run(command: list[str], cwd: Path) -> tuple[int, str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    return result.returncode, (result.stderr.strip() or result.stdout.strip())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate an independent project-specific harness and dossier into "
            "a nonexistent or empty target."
        )
    )
    parser.add_argument("--target", type=Path)
    parser.add_argument("--project-name")
    parser.add_argument("--project-slug")
    parser.add_argument(
        "--profile", choices=tuple(PROFILE_LAYERS)
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--diagnose-generation-policy",
        action="store_true",
        help=(
            "report reviewed, missing, and ignored generation inputs without "
            "writing; all profiles are checked unless --profile is supplied"
        ),
    )
    return parser.parse_args()


def main() -> int:
    configure_console_output()
    args = parse_args()
    try:
        require_runtime()
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    try:
        generation_policy = load_generation_policy()
    except ValueError as error:
        print(
            "ERROR: authority_degradation: generation policy cannot be "
            f"established: {error}",
            file=sys.stderr,
        )
        return 2
    try:
        if args.diagnose_generation_policy:
            diagnostic_profiles = (
                (args.profile,) if args.profile is not None else tuple(PROFILE_LAYERS)
            )
            report = generation_policy_diagnostics(
                generation_policy, diagnostic_profiles
            )
            print(json.dumps(report, indent=2, sort_keys=True))
            return 0 if report["capability_status"] == "normal" else 1
        if args.target is None or args.project_name is None:
            raise ValueError(
                "--target and --project-name are required unless "
                "--diagnose-generation-policy is used"
            )
        profile = args.profile or "standard"
        target = args.target.expanduser()
        diagnostics = generation_policy_diagnostics(
            generation_policy, (profile,)
        )
        mode = generation_profile_mode(diagnostics, profile)
        if mode == "blocked":
            details = "; ".join(
                f"{item.get('failure_class')}: "
                + ", ".join(str(path) for path in item.get("paths", []))
                for item in generation_profile_findings(diagnostics, profile)
                if item.get("severity") == "error"
            )
            raise ValueError(
                f"{profile} generation capability is blocked: {details}. "
                "Run --diagnose-generation-policy --profile "
                f"{profile} for read-only recovery guidance."
            )
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    try:
        validate_target(target)
        version = blueprint_version()
        name = validate_project_name(args.project_name)
        slug = args.project_slug or slugify(name)
        if not SLUG_RE.fullmatch(slug):
            raise ValueError(
                "--project-slug must use lowercase ASCII letters, digits, and hyphens."
            )
        try:
            templates, schemas = resolve_generation_inputs(
                profile, generation_policy
            )
            validate_generation_boundary(
                profile, templates, schemas, generation_policy
            )
        except ValueError as error:
            raise ValueError(
                f"safety_invariant_degradation: {error}"
            ) from error
        created = date.today().isoformat()
        identifier = generation_id()
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    expected = (
        set(templates)
        | set(schemas)
        | PROJECT_LOCAL_SOURCE_PATHS
        | DERIVED_PATHS
        | {Path(".project-blueprint-origin.json")}
    )
    if profile == "high-assurance":
        expected |= HIGH_DERIVED_PATHS

    print(f"Project: {name}")
    print(f"Slug: {slug}")
    print(f"Profile: {profile}")
    print(f"Generation capability: {mode}")
    for finding in generation_profile_findings(diagnostics, profile):
        if finding.get("severity") == "warning":
            print(
                "WARNING: "
                f"{finding.get('failure_class')} in {finding.get('rule_id')}: "
                f"{', '.join(str(path) for path in finding.get('paths', []))}; "
                f"{finding.get('effect')}."
            )
    print(f"Blueprint: {version}")
    print(f"Target: {target.resolve()}")
    print("Intended paths:")
    for relative in sorted(expected):
        print(f"  {relative.as_posix()}")
    if args.dry_run:
        print("Dry run complete; no files written.")
        return 0

    refresh_writes = set(DERIVED_PATHS)
    if profile == "high-assurance":
        refresh_writes.update(HIGH_DERIVED_PATHS)
    variables = {
        "PROJECT_NAME": markdown_escape(name),
        "PROJECT_NAME_JSON": json.dumps(name, ensure_ascii=False),
        "PROJECT_SLUG": slug,
        "CREATED_DATE": created,
        "BLUEPRINT_VERSION": version,
        "HARNESS_KERNEL_VERSION": KERNEL_VERSION,
        "PROFILE": profile,
        "HARNESS_REFRESH_COMMAND": (
            "python -B .agent/scripts/refresh.py --refresh"
        ),
        "HARNESS_REFRESH_WRITES": json.dumps(
            canonical_posix_paths(refresh_writes)
        ),
    }

    with tempfile.TemporaryDirectory(
        prefix=f".{target.name}.project-blueprint-", dir=target.parent
    ) as temporary:
        stage = Path(temporary) / "snapshot"
        stage.mkdir()
        try:
            for relative, template in templates.items():
                write_text(stage / relative, render(template, variables))
            for relative, source in schemas.items():
                write_text(stage / relative, source.read_text(encoding="utf-8"))
            if profile == "high-assurance":
                configure_high_assurance_extension(stage)
            write_artifact_registry(
                stage, profile, created, slug, expected
            )
            write_origin(
                stage,
                version,
                profile,
                created,
                name,
                slug,
                identifier,
                expected,
            )
            issues = validate_generated(
                stage, expected - DERIVED_PATHS - HIGH_DERIVED_PATHS
            )

            if not issues:
                code, details = run(
                    [
                        sys.executable,
                        "-B",
                        ".agent/scripts/refresh.py",
                        "--refresh",
                    ],
                    stage,
                )
                if code:
                    issues.append(f"initial derived refresh failed: {details}")
            if not issues:
                issues.extend(validate_generated(stage, expected))

            for command in (
                [
                    sys.executable,
                    "-B",
                    ".agent/scripts/validate.py",
                    "--check",
                ],
                [
                    sys.executable,
                    "-B",
                    "-m",
                    "unittest",
                    "discover",
                    "-s",
                    ".agent/tests",
                    "-p",
                    "test_*.py",
                ],
            ):
                if issues:
                    break
                code, details = run(command, stage)
                if code:
                    issues.append(
                        f"generated harness command failed: {' '.join(command)}: "
                        f"{details}"
                    )
            if not issues:
                issues.extend(validate_generated(stage, expected))
            if issues:
                print(
                    "ERROR: safety_invariant_degradation: staged "
                    "generated-project validation failed; "
                    "target was not changed:",
                    file=sys.stderr,
                )
                for issue in issues:
                    print(f"  {issue}", file=sys.stderr)
                return 4

            if target.exists():
                target.rmdir()
            os.replace(stage, target)
        except (OSError, ValueError) as error:
            print(
                "ERROR: safety_invariant_degradation: staged generation failed; "
                f"target was not changed: {error}",
                file=sys.stderr,
            )
            return 4

    print(f"Generated and validated {len(expected)} files transactionally.")
    print("Project-specific inspection and adoption remain required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
