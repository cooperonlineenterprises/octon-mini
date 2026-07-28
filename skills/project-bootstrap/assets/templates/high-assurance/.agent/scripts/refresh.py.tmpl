#!/usr/bin/env python3
"""Explicit transactional writer for point-in-time integrity evidence."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / ".agent" / "scripts" / "validate.py"
GENERATED = ROOT / ".agent" / "generated"
DOSSIER = ROOT / "project-dossier"


def load_validator():
    spec = importlib.util.spec_from_file_location(
        "project_harness_validate", VALIDATOR_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load validator: {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def generation_id(fingerprint: str, generated_at: str) -> str:
    return hashlib.sha256(
        f"{fingerprint}\0{generated_at}".encode("utf-8")
    ).hexdigest()[:32]


def main() -> int:
    if sys.version_info < (3, 11):
        print("Python 3.11+ is required.", file=sys.stderr)
        return 2
    parser = argparse.ArgumentParser(
        description=(
            "Refresh mutually consistent harness and dossier integrity files. "
            "Source files are validated before any output changes."
        )
    )
    parser.add_argument("--refresh", action="store_true", required=True)
    parser.parse_args()

    validator = load_validator()
    errors = validator.check(ROOT, include_generated=False)
    if errors:
        for error in errors:
            print(f"[FAIL] {error}", file=sys.stderr)
        print(
            "[FAIL] source validation failed; integrity files were not updated",
            file=sys.stderr,
        )
        return 1

    try:
        origin = validator.load_json(ROOT / ".project-blueprint-origin.json")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"[FAIL] invalid generation origin: {error}", file=sys.stderr)
        return 1

    fingerprint = validator.source_fingerprint(ROOT)
    generated_at = datetime.now(timezone.utc).isoformat()
    identifier = generation_id(fingerprint, generated_at)
    file_hashes = validator.expected_manifest_files(ROOT)
    dossier_manifest = {
        "schema_version": "project-dossier.manifest.v1",
        "generation_id": identifier,
        "generated_on": generated_at,
        "blueprint_version": origin["blueprint_version"],
        "profile": origin["profile"],
        "harness_kernel_version": origin["harness_kernel_version"],
        "authority": "Generated point-in-time inventory and byte hashes only.",
        "source_fingerprint": fingerprint,
        "files": [
            {
                "path": path,
                "layer": (
                    "agent_harness"
                    if path == "AGENTS.md"
                    or path.startswith((".agent/", ".agents/"))
                    else "project_dossier"
                    if path.startswith("project-dossier/")
                    else "generation_provenance"
                    if path == ".project-blueprint-origin.json"
                    else "project_source"
                ),
                "sha256": digest,
            }
            for path, digest in sorted(file_hashes.items())
        ],
    }
    generated_manifest = {
        "schema_version": "harness.generated-manifest.v1",
        "generator_version": "1.0.0",
        "generation_id": identifier,
        "generated_at": generated_at,
        "authority": "generated_non_authoritative_point_in_time",
        "source_fingerprint": fingerprint,
        "managed_files": sorted(file_hashes),
        "limitations": [
            "Fingerprint proves declared byte identity, not correctness or authority.",
            "Project adoption and readiness require separate evidence."
        ],
    }
    report = {
        "schema_version": "harness.validation-report.v1",
        "validator_version": "1.0.0",
        "generation_id": identifier,
        "generated_at": generated_at,
        "authority": "generated_non_authoritative_point_in_time",
        "source_fingerprint": fingerprint,
        "result": "PASS",
        "checks": [
            "python_runtime_floor",
            "strict_json_and_duplicate_keys",
            "schemas_and_versions",
            "authority_and_nested_instruction_invariants",
            "identifiers_references_and_lifecycles",
            "dossier_catalog_path_authority_and_traceability",
            "extension_compatibility_confinement_and_validator_protocol",
            "secret_redaction_and_repository_scope"
        ],
        "environment": {
            "python": sys.version.split()[0],
            "platform": sys.platform,
        },
        "git_scope": validator.git_scope(ROOT),
        "task_and_decision_links": [],
        "freshness_rule": (
            "Invalid when any non-excluded repository source byte or path changes."
        ),
        "limitations": [
            "Structural pass does not prove implementation or project readiness.",
            "Repository policy is not runtime enforcement.",
            "Project-specific build, test, security, legal, and operational checks remain adoption obligations."
        ],
    }

    GENERATED.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".refresh-", dir=GENERATED
    ) as temporary:
        staging = Path(temporary)
        staged_dossier_manifest = staging / "dossier-manifest.json"
        staged_generated_manifest = staging / "generated-manifest.json"
        staged_report = staging / "validation-report.json"
        staged_checksums = staging / "CHECKSUMS.sha256"
        write_json(staged_dossier_manifest, dossier_manifest)
        write_json(staged_generated_manifest, generated_manifest)
        write_json(staged_report, report)

        checksum_lines = []
        for path in sorted(DOSSIER.rglob("*")):
            if not path.is_file() or path.name in {
                "MANIFEST.json",
                "CHECKSUMS.sha256",
            }:
                continue
            checksum_lines.append(
                f"{validator.hash_file(path)}  {validator.relative(path, ROOT)}"
            )
        checksum_lines.append(
            f"{validator.hash_file(staged_dossier_manifest)}  "
            "project-dossier/MANIFEST.json"
        )
        staged_checksums.write_text(
            "\n".join(sorted(checksum_lines)) + "\n",
            encoding="utf-8",
        )

        # Multi-file atomic replacement is unavailable on a normal filesystem.
        # A shared generation ID makes any interruption fail closed on next check.
        os.replace(staged_generated_manifest, GENERATED / "manifest.json")
        os.replace(staged_report, GENERATED / "validation-report.json")
        os.replace(staged_dossier_manifest, DOSSIER / "MANIFEST.json")
        os.replace(staged_checksums, DOSSIER / "CHECKSUMS.sha256")

    print("[PASS] refreshed mutually consistent non-authoritative integrity files")
    print("[NEXT] run the final read-only harness check on the exact tree")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
