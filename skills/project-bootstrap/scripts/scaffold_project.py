#!/usr/bin/env python3
"""Transactionally generate a non-authorizing harness and dossier snapshot."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path


GENERATOR_VERSION = "1.0.0"
KERNEL_VERSION = "1.0.0"
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
HIGH_DERIVED_PATHS = {
    Path("project-dossier/CHECKSUMS.sha256"),
    Path(".agent/generated/manifest.json"),
    Path(".agent/generated/validation-report.json"),
}
SOURCE_EXCLUSIONS = {
    "project-dossier/MANIFEST.json",
    "project-dossier/CHECKSUMS.sha256",
}


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


def load_json(path: Path) -> object:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=strict_object,
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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(root).as_posix()
        if (
            ".git" in path.relative_to(root).parts
            or "__pycache__" in path.parts
            or path.name in {".DS_Store"}
            or relative.startswith(".agent/generated/")
            or relative in SOURCE_EXCLUSIONS
        ):
            continue
        files.append(path)
    return files


def source_fingerprint(root: Path) -> str:
    digest = hashlib.sha256()
    for path in source_files(root):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
        digest.update(b"\0")
    return digest.hexdigest()


def generation_id(
    version: str,
    profile: str,
    created: str,
    project_name: str,
    slug: str,
) -> str:
    material = "\0".join((version, profile, created, project_name, slug))
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:32]


def schema_outputs() -> dict[Path, Path]:
    schema_root = blueprint_root() / "shared" / "schemas"
    return {
        Path(".agent/schemas") / path.name: path
        for path in sorted(schema_root.glob("*.schema.json"))
    }


def selected_artifacts(profile: str, created: str) -> list[dict[str, object]]:
    source = load_json(blueprint_root() / "dossier" / "artifact-types.json")
    if not isinstance(source, dict) or not isinstance(source.get("artifacts"), list):
        raise ValueError("dossier/artifact-types.json has an invalid top-level shape")
    selected: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    for raw in source["artifacts"]:
        if not isinstance(raw, dict):
            raise ValueError("artifact type entry must be an object")
        artifact_profile = raw.get("profile")
        if artifact_profile not in PROFILE_RANK:
            raise ValueError(f"artifact {raw.get('id')}: invalid profile")
        if PROFILE_RANK[str(artifact_profile)] > PROFILE_RANK[profile]:
            continue
        artifact_id = raw.get("id")
        path = raw.get("path")
        if not isinstance(artifact_id, str) or not re.fullmatch(
            r"[A-Z]{3}-[0-9]{4}", artifact_id
        ):
            raise ValueError(f"invalid artifact ID: {artifact_id!r}")
        if not isinstance(path, str) or not path:
            raise ValueError(f"artifact {artifact_id}: invalid path")
        if artifact_id in seen_ids or path in seen_paths:
            raise ValueError(f"duplicate artifact ID or path: {artifact_id} / {path}")
        seen_ids.add(artifact_id)
        seen_paths.add(path)
        selected.append(
            {
                key: raw[key]
                for key in (
                    "id",
                    "path",
                    "category",
                    "classification",
                    "information_state",
                    "authority",
                    "generated",
                    "owner_role",
                    "review_cadence",
                    "update_triggers",
                    "sensitivity",
                )
            }
            | {
                "source_refs": [
                    f"project-blueprint:dossier/artifact-types.json#{artifact_id}"
                ],
                "last_reviewed": created,
                "superseded_by": None,
            }
        )
    return selected


def generate_catalog(
    stage: Path,
    profile: str,
    created: str,
    expected_paths: set[Path],
) -> list[dict[str, object]]:
    artifacts = selected_artifacts(profile, created)
    missing = [
        str(item["path"])
        for item in artifacts
        if Path(str(item["path"])) not in expected_paths
    ]
    if missing:
        raise ValueError(
            "artifact catalog paths absent from selected profile: " + ", ".join(missing)
        )
    catalog = {
        "schema_version": "project-dossier.artifact-catalog.v1",
        "dossier_version": "1.0.0",
        "authority": "Artifact metadata and source ownership only; not permission.",
        "artifacts": artifacts,
    }
    write_json(stage / "project-dossier" / "ARTIFACT_CATALOG.json", catalog)
    return artifacts


def generate_path_authority(
    stage: Path,
    artifacts: list[dict[str, object]],
    expected_paths: set[Path],
    project_slug: str,
) -> None:
    by_path = {str(item["path"]): item for item in artifacts}
    dossier_paths = sorted(
        path.as_posix()
        for path in expected_paths
        if path.as_posix().startswith("project-dossier/")
    )
    entries: list[dict[str, object]] = []
    for path in dossier_paths:
        artifact = by_path.get(path)
        if artifact is None:
            raise ValueError(f"no artifact catalog owner for dossier path: {path}")
        entries.append(
            {
                "path": path,
                "artifact_id": artifact["id"],
                "information_state": artifact["information_state"],
                "authority": artifact["authority"],
                "generated": artifact["generated"],
            }
        )
    value = {
        "schema_version": "project.dossier.path-authority.v1",
        "document_role": "generated_from_artifact_catalog",
        "permission_grant": False,
        "project_slug": project_slug,
        "paths": entries,
    }
    write_json(
        stage / "project-dossier" / "machine-readable" / "path-authority.json",
        value,
    )


def configure_high_assurance_extension(stage: Path) -> None:
    registry_path = stage / ".agent" / "extensions" / "registry.json"
    registry = load_json(registry_path)
    if not isinstance(registry, dict):
        raise ValueError("extension registry must be an object")
    registry["extensions"] = [
        {
            "id": "sample-restriction",
            "enabled": True,
            "version": "1.0.0",
            "path": ".agent/extensions/sample-restriction",
            "requires_core": "^1.0.0",
            "config": ".agent/extensions/sample-restriction/config.json",
            "validator": ".agent/extensions/sample-restriction/validate.py",
            "owner": "unassigned",
            "provenance": "generated_domain_neutral_reference_extension",
            "side_effects": "read_only",
            "authority_effect": "restrictions_only",
            "deprecated_at": None,
            "successor": None,
        }
    ]
    registry["limitations"] = [
        "Reference extension only; project adoption must assess actual needs."
    ]
    write_json(registry_path, registry)


def classify(path: Path) -> str:
    text = path.as_posix()
    if text == "AGENTS.md" or text.startswith((".agent/", ".agents/")):
        return "agent_harness"
    if text.startswith("project-dossier/"):
        return "project_dossier"
    if text == ".project-blueprint-origin.json":
        return "generation_provenance"
    return "generated_control"


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
            "generated_paths": [
                path.as_posix() for path in sorted(expected_paths)
            ],
        },
    )


def write_dossier_integrity(
    stage: Path,
    version: str,
    profile: str,
    created: str,
    identifier: str,
) -> None:
    fingerprint = source_fingerprint(stage)
    files = [
        {
            "path": path.relative_to(stage).as_posix(),
            "layer": classify(path.relative_to(stage)),
            "sha256": sha256(path),
        }
        for path in source_files(stage)
    ]
    write_json(
        stage / "project-dossier" / "MANIFEST.json",
        {
            "schema_version": "project-dossier.manifest.v1",
            "generation_id": identifier,
            "generated_on": created,
            "blueprint_version": version,
            "profile": profile,
            "harness_kernel_version": KERNEL_VERSION,
            "authority": "Generated point-in-time inventory and byte hashes only.",
            "source_fingerprint": fingerprint,
            "files": files,
        },
    )
    checksum_path = stage / "project-dossier" / "CHECKSUMS.sha256"
    if checksum_path.parent.exists() and profile == "high-assurance":
        lines = []
        for path in sorted((stage / "project-dossier").rglob("*")):
            if not path.is_file() or path == checksum_path:
                continue
            relative = path.relative_to(stage).as_posix()
            lines.append(f"{sha256(path)}  {relative}")
        write_text(checksum_path, "\n".join(lines) + "\n")


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
        identifier = generation_id(version, args.profile, created, name, slug)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    expected = set(templates) | set(schemas) | DERIVED_PATHS | {
        Path(".project-blueprint-origin.json")
    }
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

    variables = {
        "PROJECT_NAME": markdown_escape(name),
        "PROJECT_NAME_JSON": json.dumps(name, ensure_ascii=False),
        "PROJECT_SLUG": slug,
        "CREATED_DATE": created,
        "BLUEPRINT_VERSION": version,
        "PROFILE": args.profile,
        "HARNESS_REFRESH_COMMAND": (
            "python3 -B .agent/scripts/refresh.py --refresh"
            if args.profile == "high-assurance"
            else "not_available_in_this_profile"
        ),
        "HARNESS_REFRESH_WRITES": (
            '[".agent/generated/manifest.json", '
            '".agent/generated/validation-report.json", '
            '"project-dossier/MANIFEST.json", '
            '"project-dossier/CHECKSUMS.sha256"]'
            if args.profile == "high-assurance"
            else "[]"
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
            artifacts = generate_catalog(stage, args.profile, created, expected)
            generate_path_authority(stage, artifacts, expected, slug)
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
            write_dossier_integrity(
                stage, version, args.profile, created, identifier
            )
            issues = validate_generated(stage, expected - {
                Path(".agent/generated/manifest.json"),
                Path(".agent/generated/validation-report.json"),
            })

            if args.profile == "high-assurance" and not issues:
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
                    issues.append(f"high-assurance refresh failed: {details}")

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
