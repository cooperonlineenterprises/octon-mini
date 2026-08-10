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


GENERATOR_VERSION = "2.0.0"
KERNEL_VERSION = "2.0.0"
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


def canonical_posix_paths(paths: Iterable[PurePath]) -> list[str]:
    """Render and sort paths identically on every host platform."""
    return sorted(path.as_posix() for path in paths)


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


def output_path(template: Path, layer_root: Path) -> Path:
    relative = template.relative_to(layer_root)
    if relative.suffix != ".tmpl":
        raise ValueError(f"Template lacks .tmpl suffix: {template}")
    return relative.with_suffix("")


def collect_templates(profile: str) -> dict[Path, Path]:
    templates_root = skill_root() / "assets" / "templates"
    resolved: dict[Path, Path] = {}
    for layer in PROFILE_LAYERS[profile]:
        layer_root = templates_root / layer
        if not layer_root.is_dir():
            raise ValueError(f"Missing template layer: {layer_root}")
        for template in sorted(layer_root.rglob("*.tmpl")):
            destination = output_path(template, layer_root)
            if destination in resolved:
                raise ValueError(
                    f"Duplicate output path {destination}: "
                    f"{resolved[destination]} and {template}"
                )
            resolved[destination] = template
    if not resolved:
        raise ValueError(f"No templates resolved for profile {profile}")
    return resolved


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


def schema_outputs() -> dict[Path, Path]:
    schema_root = blueprint_root() / "shared" / "schemas"
    return {
        Path(".agent/schemas") / path.name: path
        for path in sorted(schema_root.glob("*.schema.json"))
    }


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
            "version": "2.0.0",
            "path": ".agent/extensions/sample-restriction",
            "requires_core": "^2.0.0",
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


def validate_generated(stage: Path, expected_paths: set[Path]) -> list[str]:
    issues: list[str] = []
    for relative in sorted(expected_paths):
        path = stage / relative
        if not path.is_file():
            issues.append(f"missing generated file: {relative}")
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
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--project-slug")
    parser.add_argument(
        "--profile", choices=tuple(PROFILE_LAYERS), default="standard"
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target = args.target.expanduser()
    try:
        require_runtime()
        validate_target(target)
        version = blueprint_version()
        name = validate_project_name(args.project_name)
        slug = args.project_slug or slugify(name)
        if not SLUG_RE.fullmatch(slug):
            raise ValueError(
                "--project-slug must use lowercase ASCII letters, digits, and hyphens."
            )
        templates = collect_templates(args.profile)
        schemas = schema_outputs()
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
    if args.profile == "high-assurance":
        expected |= HIGH_DERIVED_PATHS

    print(f"Project: {name}")
    print(f"Slug: {slug}")
    print(f"Profile: {args.profile}")
    print(f"Blueprint: {version}")
    print(f"Target: {target.resolve()}")
    print("Intended paths:")
    for relative in sorted(expected):
        print(f"  {relative.as_posix()}")
    if args.dry_run:
        print("Dry run complete; no files written.")
        return 0

    refresh_writes = set(DERIVED_PATHS)
    if args.profile == "high-assurance":
        refresh_writes.update(HIGH_DERIVED_PATHS)
    variables = {
        "PROJECT_NAME": markdown_escape(name),
        "PROJECT_NAME_JSON": json.dumps(name, ensure_ascii=False),
        "PROJECT_SLUG": slug,
        "CREATED_DATE": created,
        "BLUEPRINT_VERSION": version,
        "HARNESS_KERNEL_VERSION": KERNEL_VERSION,
        "PROFILE": args.profile,
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
            if args.profile == "high-assurance":
                configure_high_assurance_extension(stage)
            write_artifact_registry(
                stage, args.profile, created, slug, expected
            )
            write_origin(
                stage,
                version,
                args.profile,
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
            if issues:
                print(
                    "ERROR: staged generated-project validation failed; "
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
                f"ERROR: staged generation failed; target was not changed: {error}",
                file=sys.stderr,
            )
            return 4

    print(f"Generated and validated {len(expected)} files transactionally.")
    print("Project-specific inspection and adoption remain required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
