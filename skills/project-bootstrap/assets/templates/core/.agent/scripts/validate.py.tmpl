#!/usr/bin/env python3
"""Read-only validation for the domain-neutral project harness and dossier."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
KERNEL_VERSION = "1.0.0"
KERNEL_FILES = (
    ".agent/policy.json",
    ".agent/context.json",
    ".agent/schema.json",
    ".agent/lifecycle.json",
    ".agent/tools.json",
    ".agent/validators.json",
    ".agent/project.json",
)
DERIVED_EXCLUSIONS = {
    "project-dossier/MANIFEST.json",
    "project-dossier/CHECKSUMS.sha256",
}
PLACEHOLDER = re.compile(r"\{\{[A-Z_]+\}\}")
ID4 = re.compile(r"^[A-Z][A-Z0-9]*-[0-9]{4}$")
SECRET_ASSIGNMENT = re.compile(
    r"(?im)^\s*(?:api[_-]?key|access[_-]?token|auth[_-]?token|password|secret)"
    r"\s*[:=]\s*(?!null\b|none\b|false\b|\$\{|<|redacted\b)"
    r"[^\s#]{12,}\s*$"
)
AUTHORITY_EXPANSION = re.compile(
    r"""(?imx)
    (?:
      ["']?permission_grant["']?\s*:\s*true |
      ["']?may_expand["']?\s*:\s*true |
      ["']?child_may_weaken_ancestor["']?\s*:\s*true |
      ["']?(?:publication|deployment|communication|purchase)["']?
        \s*:\s*["']?allowed["']?
    )
    """
)
EXTERNAL_REFERENCE_PREFIXES = (
    "authority:",
    "external:",
    "project-blueprint:",
    "repo:",
    "url:",
)
REFERENCE_KEYS = {
    "dependencies",
    "depends_on",
    "supersedes",
    "successor",
    "task",
    "task_ref",
    "task_refs",
    "decision_ref",
    "decision_refs",
    "requirement_ref",
    "requirement_refs",
    "finding_ref",
    "finding_refs",
    "gate_ref",
    "gate_refs",
    "evidence_ref",
    "evidence_refs",
    "closure_evidence",
    "inspected_evidence",
    "source_refs",
}
DOSSIER_STORES = {
    "project-dossier/machine-readable/requirements.json": ("requirements", "requirement"),
    "project-dossier/machine-readable/findings.json": ("findings", "finding"),
    "project-dossier/machine-readable/plan.json": ("plan_items", "plan_item"),
    "project-dossier/machine-readable/raidq.json": ("items", "raidq_item"),
    "project-dossier/machine-readable/sources.json": ("sources", "source"),
    "project-dossier/machine-readable/evidence-index.json": ("evidence", "evidence"),
}
DOSSIER_STORE_VERSIONS = {
    "project-dossier/machine-readable/requirements.json": "project.dossier.requirements.v1",
    "project-dossier/machine-readable/findings.json": "project.dossier.findings.v1",
    "project-dossier/machine-readable/plan.json": "project.dossier.plan.v1",
    "project-dossier/machine-readable/raidq.json": "project.dossier.raidq.v1",
    "project-dossier/machine-readable/sources.json": "project.dossier.sources.v1",
    "project-dossier/machine-readable/evidence-index.json": "project.dossier.evidence-index.v1",
}


class DuplicateKeyError(ValueError):
    """Raised when strict JSON encounters a repeated object key."""


def relative(path: Path, root: Path = ROOT) -> str:
    return path.relative_to(root).as_posix()


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def loads_json(text: str) -> Any:
    return json.loads(text, object_pairs_hook=strict_object)


def load_json(path: Path) -> Any:
    return loads_json(path.read_text(encoding="utf-8"))


def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fingerprint_exclusions(root: Path) -> tuple[set[str], list[str]]:
    errors: list[str] = []
    exclusions: set[str] = set()
    project_path = root / ".agent" / "project.json"
    if not project_path.is_file():
        return exclusions, errors
    try:
        project = load_json(project_path)
    except (OSError, ValueError, json.JSONDecodeError):
        return exclusions, errors
    raw = project.get("paths", {}).get("fingerprint_exclusions", [])
    if not isinstance(raw, list):
        return exclusions, [".agent/project.json: fingerprint_exclusions must be an array"]
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            errors.append(
                f".agent/project.json: fingerprint_exclusions[{index}] must be an object"
            )
            continue
        path = item.get("path")
        reason = item.get("reason")
        if (
            not isinstance(path, str)
            or not path
            or path.startswith(("/", "../"))
            or path in {".", ".git"}
            or "*" in path
        ):
            errors.append(
                f".agent/project.json: unsafe fingerprint exclusion at index {index}"
            )
            continue
        if not isinstance(reason, str) or not reason.strip():
            errors.append(
                f".agent/project.json: exclusion {path!r} requires a reason"
            )
            continue
        exclusions.add(path.rstrip("/"))
    return exclusions, errors


def repository_files(
    root: Path = ROOT,
    *,
    source_only: bool = False,
) -> list[Path]:
    exclusions, _ = fingerprint_exclusions(root)
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        rel_path = path.relative_to(root)
        rel = rel_path.as_posix()
        if ".git" in rel_path.parts or "__pycache__" in rel_path.parts:
            continue
        if path.is_dir():
            continue
        if source_only and (
            rel.startswith(".agent/generated/")
            or rel in DERIVED_EXCLUSIONS
            or any(rel == item or rel.startswith(item + "/") for item in exclusions)
        ):
            continue
        files.append(path)
    return files


def source_fingerprint(root: Path = ROOT) -> str:
    digest = hashlib.sha256()
    for path in repository_files(root, source_only=True):
        if path.is_symlink():
            continue
        rel = relative(path, root)
        if path.name == ".DS_Store":
            continue
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
        digest.update(b"\0")
    return digest.hexdigest()


def schema_type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return False


def resolve_ref(root_schema: dict[str, Any], reference: str) -> dict[str, Any]:
    if not reference.startswith("#/"):
        raise ValueError(f"unsupported non-local schema reference: {reference}")
    current: Any = root_schema
    for part in reference[2:].split("/"):
        key = part.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, dict) or key not in current:
            raise ValueError(f"unresolved schema reference: {reference}")
        current = current[key]
    if not isinstance(current, dict):
        raise ValueError(f"schema reference does not resolve to an object: {reference}")
    return current


def validate_schema(
    value: Any,
    schema: dict[str, Any],
    path: str = "$",
    *,
    root_schema: dict[str, Any] | None = None,
) -> list[str]:
    root_schema = root_schema or schema
    if "$ref" in schema:
        try:
            resolved = resolve_ref(root_schema, schema["$ref"])
        except ValueError as error:
            return [f"{path}: {error}"]
        return validate_schema(value, resolved, path, root_schema=root_schema)

    errors: list[str] = []
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value is outside the allowed vocabulary")

    expected = schema.get("type")
    if expected is not None:
        types = expected if isinstance(expected, list) else [expected]
        if not any(schema_type_matches(value, item) for item in types):
            return [f"{path}: expected type {expected!r}"]

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: string is too short")
        pattern = schema.get("pattern")
        if pattern and not re.fullmatch(pattern, value):
            errors.append(f"{path}: string does not match required pattern")
        if schema.get("format") == "date":
            try:
                date.fromisoformat(value)
            except ValueError:
                errors.append(f"{path}: expected ISO date")

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: array has too few items")
        if schema.get("uniqueItems"):
            encoded = [json.dumps(item, sort_keys=True) for item in value]
            if len(encoded) != len(set(encoded)):
                errors.append(f"{path}: array items must be unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(
                    validate_schema(
                        item,
                        item_schema,
                        f"{path}[{index}]",
                        root_schema=root_schema,
                    )
                )

    if isinstance(value, dict):
        for required in schema.get("required", []):
            if required not in value:
                errors.append(f"{path}: missing required property {required!r}")
        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            for key, child in properties.items():
                if key in value and isinstance(child, dict):
                    errors.extend(
                        validate_schema(
                            value[key],
                            child,
                            f"{path}.{key}",
                            root_schema=root_schema,
                        )
                    )
            if schema.get("additionalProperties") is False:
                for key in value:
                    if key not in properties:
                        errors.append(f"{path}: unknown property {key!r}")
    return errors


def load_schema(root: Path, name: str) -> dict[str, Any]:
    value = load_json(root / ".agent" / "schemas" / name)
    if not isinstance(value, dict):
        raise ValueError(f"schema {name} must be an object")
    return value


def parse_json_header(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing JSON metadata header")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated JSON metadata header")
    value = loads_json(text[4:end])
    if not isinstance(value, dict):
        raise ValueError("metadata header must be a JSON object")
    return value


def check_runtime() -> list[str]:
    if sys.version_info < (3, 11):
        return [f"Python 3.11+ required; found {sys.version.split()[0]}"]
    return []


def check_files_and_json(root: Path) -> list[str]:
    errors: list[str] = []
    _, exclusion_errors = fingerprint_exclusions(root)
    errors.extend(exclusion_errors)
    for path in repository_files(root):
        rel = relative(path, root)
        if path.name == ".DS_Store":
            errors.append(f"{rel}: prohibited host metadata")
        if path.is_symlink():
            if path.name == "AGENTS.md":
                errors.append(f"{rel}: instruction files must not be symlinks")
            try:
                path.resolve(strict=True).relative_to(root.resolve())
            except (FileNotFoundError, ValueError):
                errors.append(f"{rel}: symlink escapes repository or is broken")
            continue
        if rel.startswith(".agent/tests/fixtures/invalid/"):
            continue
        if path.stat().st_size > 4 * 1024 * 1024:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if PLACEHOLDER.search(text):
            errors.append(f"{rel}: unresolved generation placeholder")
        if SECRET_ASSIGNMENT.search(text):
            errors.append(f"{rel}: possible embedded secret assignment (value redacted)")
        if path.name == "AGENTS.md" and AUTHORITY_EXPANSION.search(text):
            errors.append(f"{rel}: nested instruction may expand authority")
        if (
            rel.startswith((".agent/", ".agents/"))
            and not rel.startswith(
                (
                    ".agent/tests/",
                    ".agent/templates/",
                    ".agent/schemas/",
                    ".agent/generated/",
                )
            )
            and AUTHORITY_EXPANSION.search(text)
        ):
            errors.append(f"{rel}: harness component may expand authority")
        if path.suffix == ".json":
            try:
                value = loads_json(text)
            except DuplicateKeyError:
                errors.append(f"{rel}: duplicate JSON key")
                continue
            except json.JSONDecodeError as error:
                errors.append(f"{rel}: invalid JSON at line {error.lineno}")
                continue
            controlled = (
                rel.startswith((".agent/", ".agents/", "project-dossier/"))
                or rel == ".project-blueprint-origin.json"
            )
            is_schema = rel.startswith(".agent/schemas/")
            if (
                controlled
                and not is_schema
                and isinstance(value, dict)
                and "schema_version" not in value
            ):
                errors.append(f"{rel}: missing top-level schema_version")
        if path.suffix == ".jsonl":
            errors.extend(check_jsonl(path, root))
    return errors


def check_jsonl(path: Path, root: Path) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            value = loads_json(raw)
        except (ValueError, json.JSONDecodeError):
            errors.append(f"{relative(path, root)}:{number}: invalid strict JSON")
            continue
        event_id = value.get("id") if isinstance(value, dict) else None
        if (
            not isinstance(value, dict)
            or value.get("schema_version") != "harness.event.v1"
            or not isinstance(event_id, str)
            or not re.fullmatch(r"EVT-[0-9]{4}", event_id)
        ):
            errors.append(f"{relative(path, root)}:{number}: invalid event record")
        elif event_id in seen:
            errors.append(f"{relative(path, root)}:{number}: duplicate event ID")
        else:
            seen.add(event_id)
    return errors


def check_kernel(root: Path) -> list[str]:
    errors: list[str] = []
    values: dict[str, dict[str, Any]] = {}
    for relative_path in KERNEL_FILES:
        path = root / relative_path
        if not path.is_file():
            errors.append(f"missing required kernel file: {relative_path}")
            continue
        try:
            value = load_json(path)
        except (ValueError, json.JSONDecodeError) as error:
            errors.append(f"{relative_path}: {error}")
            continue
        if not isinstance(value, dict):
            errors.append(f"{relative_path}: expected object")
            continue
        values[relative_path] = value

    policy = values.get(".agent/policy.json", {})
    if not (
        policy.get("permission_grant") is False
        and policy.get("default") == "deny"
        and policy.get("declarative_only") is True
        and policy.get("external", {}).get("publication")
        == "requires_explicit_current_authorization"
        and policy.get("external", {}).get("deployment")
        == "requires_explicit_current_authorization"
        and policy.get("repository", {}).get("dossier_instruction_channel") is False
        and "lower_level_files_cannot_expand_authority"
        in policy.get("invariants", [])
    ):
        errors.append(".agent/policy.json: critical non-authorizing invariants missing")

    context = values.get(".agent/context.json", {})
    if not (
        context.get("permission_grant") is False
        and "applicable_AGENTS_md_root_to_leaf" in context.get("precedence", [])
        and context.get("path_scope", {}).get("child_may_weaken_ancestor") is False
        and context.get("conflicts", {}).get("ambiguous_high_impact_action")
        == "stop_and_request_authority"
    ):
        errors.append(".agent/context.json: precedence or path-scope contract invalid")

    schema = values.get(".agent/schema.json", {})
    lifecycle = values.get(".agent/lifecycle.json", {})
    if schema.get("kernel_version") != KERNEL_VERSION:
        errors.append(".agent/schema.json: unsupported kernel version")
    task_statuses = set(schema.get("statuses", {}).get("task", []))
    task_transitions = lifecycle.get("task", {}).get("transitions", {})
    if task_statuses != set(task_transitions):
        errors.append(".agent/lifecycle.json: task status/transition graph mismatch")
    decision_statuses = set(schema.get("statuses", {}).get("decision", []))
    decision_transitions = lifecycle.get("decision", {}).get("transitions", {})
    if decision_statuses != set(decision_transitions):
        errors.append(".agent/lifecycle.json: decision status/transition graph mismatch")
    artifact_statuses = set(schema.get("statuses", {}).get("artifact", []))
    artifact_transitions = lifecycle.get("artifact", {}).get("transitions", {})
    if artifact_statuses != set(artifact_transitions):
        errors.append(".agent/lifecycle.json: artifact status/transition graph mismatch")
    return errors


def check_origin(root: Path) -> list[str]:
    path = root / ".project-blueprint-origin.json"
    try:
        origin = load_json(path)
        schema = load_schema(root, "project-blueprint-origin.schema.json")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [f".project-blueprint-origin.json: {error}"]
    return [
        f".project-blueprint-origin.json: {item}"
        for item in validate_schema(origin, schema)
    ]


def record_files(root: Path) -> list[tuple[Path, str]]:
    result: list[tuple[Path, str]] = []
    specifications = (
        (".agent/tasks", "TASK-*.md", "task"),
        (".agent/decisions", "DEC-*.md", "decision"),
        (".agent/evidence", "EVD-*.md", "evidence"),
        (".agent/reviews", "REV-*.md", "review"),
        (".agent/checkpoints", "CHK-*.md", "checkpoint"),
    )
    for directory, pattern, kind in specifications:
        base = root / directory
        if base.is_dir():
            result.extend((path, kind) for path in sorted(base.glob(pattern)))
    return result


def collect_records(
    root: Path,
) -> tuple[dict[str, tuple[dict[str, Any], str]], list[str]]:
    records: dict[str, tuple[dict[str, Any], str]] = {}
    errors: list[str] = []
    try:
        record_schema = load_schema(root, "harness-record.schema.json")
        dossier_schema = load_schema(root, "dossier-records.schema.json")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return records, [f"schema loading failed: {error}"]

    for path, kind in record_files(root):
        rel = relative(path, root)
        try:
            record = parse_json_header(path)
        except (ValueError, json.JSONDecodeError) as error:
            errors.append(f"{rel}: {error}")
            continue
        errors.extend(
            f"{rel}: {item}"
            for item in validate_schema(record, record_schema)
        )
        record_id = record.get("id")
        expected_prefix = {
            "task": "TASK",
            "decision": "DEC",
            "evidence": "EVD",
            "review": "REV",
            "checkpoint": "CHK",
        }[kind]
        if (
            not isinstance(record_id, str)
            or not re.fullmatch(rf"{expected_prefix}-[0-9]{{4}}", record_id)
        ):
            errors.append(f"{rel}: invalid {kind} ID")
            continue
        if not path.name.startswith(record_id):
            errors.append(f"{rel}: filename/ID mismatch")
        if record_id in records:
            errors.append(f"{rel}: duplicate global record ID {record_id}")
        else:
            records[record_id] = (record, rel)

    for store_path, (array_name, definition) in DOSSIER_STORES.items():
        path = root / store_path
        if not path.is_file():
            continue
        try:
            store = load_json(path)
        except (ValueError, json.JSONDecodeError) as error:
            errors.append(f"{store_path}: {error}")
            continue
        if (
            not isinstance(store, dict)
            or store.get("schema_version") != DOSSIER_STORE_VERSIONS[store_path]
            or store.get("permission_grant") is not False
        ):
            errors.append(
                f"{store_path}: invalid schema version or authorization boundary"
            )
        entries = store.get(array_name) if isinstance(store, dict) else None
        if not isinstance(entries, list):
            errors.append(f"{store_path}: {array_name} must be an array")
            continue
        item_schema = {"$ref": f"#/$defs/{definition}"}
        for index, record in enumerate(entries):
            item_path = f"{store_path}:{array_name}[{index}]"
            errors.extend(
                f"{item_path}: {item}"
                for item in validate_schema(
                    record, item_schema, root_schema=dossier_schema
                )
            )
            record_id = record.get("id") if isinstance(record, dict) else None
            if isinstance(record_id, str):
                if record_id in records:
                    errors.append(f"{item_path}: duplicate global record ID {record_id}")
                else:
                    records[record_id] = (record, item_path)

    gates_path = root / "project-dossier" / "validation" / "QUALITY_GATES.json"
    if gates_path.is_file():
        try:
            gates_value = load_json(gates_path)
            if (
                not isinstance(gates_value, dict)
                or gates_value.get("schema_version")
                != "project.dossier.quality-gates.v1"
                or gates_value.get("permission_grant") is not False
            ):
                raise ValueError("invalid schema version or authorization boundary")
            gates = gates_value.get("gates", [])
            if not isinstance(gates, list):
                raise ValueError("gates must be an array")
            for index, gate in enumerate(gates):
                gate_id = gate.get("id") if isinstance(gate, dict) else None
                location = f"project-dossier/validation/QUALITY_GATES.json:gates[{index}]"
                if not isinstance(gate_id, str) or not re.fullmatch(
                    r"GATE-[0-9]{4}", gate_id
                ):
                    errors.append(f"{location}: invalid gate ID")
                elif gate_id in records:
                    errors.append(f"{location}: duplicate global record ID {gate_id}")
                else:
                    records[gate_id] = (gate, location)
        except (ValueError, json.JSONDecodeError) as error:
            errors.append(f"project-dossier/validation/QUALITY_GATES.json: {error}")
    return records, errors


def iter_references(value: Any, key: str | None = None):
    if isinstance(value, dict):
        for child_key, child in value.items():
            yield from iter_references(child, child_key)
    elif isinstance(value, list):
        if key in REFERENCE_KEYS:
            for child in value:
                if isinstance(child, str):
                    yield key, child
        else:
            for child in value:
                yield from iter_references(child, key)
    elif isinstance(value, str) and key in REFERENCE_KEYS:
        yield key, value


def check_references_and_lifecycle(
    root: Path,
    records: dict[str, tuple[dict[str, Any], str]],
) -> list[str]:
    errors: list[str] = []
    lifecycle = load_json(root / ".agent" / "lifecycle.json")
    for record_id, (record, location) in records.items():
        for key, reference in iter_references(record):
            if reference.startswith(EXTERNAL_REFERENCE_PREFIXES):
                continue
            if not ID4.fullmatch(reference):
                errors.append(f"{location}: {key} contains invalid reference")
            elif reference not in records:
                errors.append(f"{location}: unresolved reference {reference}")

        kind = (
            "task"
            if record_id.startswith("TASK-")
            else "decision"
            if record_id.startswith("DEC-")
            else "artifact"
            if record_id.startswith("ART-")
            else None
        )
        if kind is None:
            continue
        status = record.get("status")
        previous = record.get("previous_status")
        graph = lifecycle.get(kind, {}).get("transitions", {})
        initial = lifecycle.get(kind, {}).get("initial")
        if status not in graph:
            errors.append(f"{location}: unknown {kind} status")
        elif previous is None:
            if status != initial:
                errors.append(
                    f"{location}: noninitial status requires previous_status"
                )
        elif previous not in graph or status not in graph.get(previous, []):
            errors.append(
                f"{location}: illegal {kind} transition {previous!r} -> {status!r}"
            )
        if kind == "task" and status == "completed":
            if not record.get("closure_evidence"):
                errors.append(f"{location}: completed task lacks closure evidence")
            if record.get("external_effects") in {None, "not_assessed"}:
                errors.append(f"{location}: completed task external effects unassessed")
            if "limitations" not in record:
                errors.append(f"{location}: completed task lacks limitations field")
        if kind == "decision" and status == "superseded" and not record.get(
            "successor"
        ):
            errors.append(f"{location}: superseded decision requires successor")
    return errors


def check_plan_and_traceability(
    records: dict[str, tuple[dict[str, Any], str]]
) -> list[str]:
    errors: list[str] = []
    plans = {
        record_id: record
        for record_id, (record, _) in records.items()
        if record_id.startswith("PLAN-")
    }
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            errors.append(f"plan dependency cycle includes {node}")
            return
        if node in visited:
            return
        visiting.add(node)
        for dependency in plans[node].get("depends_on", []):
            if dependency in plans:
                visit(dependency)
        visiting.remove(node)
        visited.add(node)

    for plan_id in plans:
        visit(plan_id)

    linked_requirements: set[str] = set()
    for record_id, (record, location) in records.items():
        for key in ("requirement_refs",):
            values = record.get(key, [])
            if isinstance(values, list):
                linked_requirements.update(
                    item for item in values if isinstance(item, str)
                )
        if record_id.startswith("FIND-") and record.get("status") not in {
            "not_assessed",
            "not_applicable",
        } and not record.get("inspected_evidence"):
            errors.append(f"{location}: assessed finding lacks inspected evidence")
        if record_id.startswith("PLAN-") and record.get("status") == "completed":
            evidence = record.get("evidence_refs")
            if not isinstance(evidence, list) or not evidence:
                errors.append(f"{location}: completed plan item lacks evidence_refs")
    for record_id, (record, location) in records.items():
        if record_id.startswith("REQ-") and record.get("status") == "active":
            for field in ("owner_role", "basis", "validation"):
                if not record.get(field):
                    errors.append(f"{location}: active requirement lacks {field}")
            if record_id not in linked_requirements:
                errors.append(
                    f"{location}: active requirement has no finding, plan, or evidence link"
                )
    return errors


def check_dossier_catalog(root: Path) -> list[str]:
    errors: list[str] = []
    catalog_path = root / "project-dossier" / "ARTIFACT_CATALOG.json"
    authority_path = (
        root / "project-dossier" / "machine-readable" / "path-authority.json"
    )
    try:
        catalog = load_json(catalog_path)
        catalog_schema = load_schema(root, "artifact-catalog.schema.json")
        errors.extend(
            f"project-dossier/ARTIFACT_CATALOG.json: {item}"
            for item in validate_schema(catalog, catalog_schema)
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [f"project-dossier/ARTIFACT_CATALOG.json: {error}"]
    artifacts = catalog.get("artifacts", []) if isinstance(catalog, dict) else []
    catalog_paths: set[str] = set()
    catalog_ids: set[str] = set()
    for item in artifacts:
        if not isinstance(item, dict):
            continue
        artifact_id = item.get("id")
        path = item.get("path")
        if artifact_id in catalog_ids:
            errors.append(f"artifact catalog: duplicate ID {artifact_id}")
        if path in catalog_paths:
            errors.append(f"artifact catalog: duplicate path {path}")
        catalog_ids.add(artifact_id)
        catalog_paths.add(path)
        if isinstance(path, str) and not (root / path).is_file():
            errors.append(f"artifact catalog: missing path {path}")
    try:
        authority = load_json(authority_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return errors + [f"machine-readable/path-authority.json: {error}"]
    if (
        not isinstance(authority, dict)
        or authority.get("schema_version")
        != "project.dossier.path-authority.v1"
        or authority.get("permission_grant") is not False
        or authority.get("document_role") != "generated_from_artifact_catalog"
    ):
        errors.append("machine-readable/path-authority.json: invalid contract")
    entries = authority.get("paths", []) if isinstance(authority, dict) else []
    authority_paths = {
        item.get("path")
        for item in entries
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    }
    actual_paths = {
        relative(path, root)
        for path in (root / "project-dossier").rglob("*")
        if path.is_file()
    }
    if authority_paths != actual_paths:
        missing = sorted(actual_paths - authority_paths)
        extra = sorted(authority_paths - actual_paths)
        if missing:
            errors.append(
                "path authority missing dossier files: " + ", ".join(missing)
            )
        if extra:
            errors.append(
                "path authority contains absent files: " + ", ".join(extra)
            )
    for item in entries:
        if not isinstance(item, dict):
            errors.append("path authority entry must be an object")
            continue
        path = item.get("path")
        artifact_id = item.get("artifact_id")
        matching = next(
            (
                artifact
                for artifact in artifacts
                if isinstance(artifact, dict) and artifact.get("path") == path
            ),
            None,
        )
        if matching is None or matching.get("id") != artifact_id:
            errors.append(f"path authority/catalog mismatch for {path}")
    return errors


def version_satisfies_core(requirement: str) -> bool:
    match = re.fullmatch(r"\^([0-9]+)\.([0-9]+)\.([0-9]+)", requirement)
    core = re.fullmatch(r"([0-9]+)\.([0-9]+)\.([0-9]+)", KERNEL_VERSION)
    return bool(match and core and match.group(1) == core.group(1))


def confined(root: Path, declared_root: Path, candidate: Path) -> bool:
    try:
        (root / candidate).resolve(strict=True).relative_to(
            (root / declared_root).resolve(strict=True)
        )
        return True
    except (FileNotFoundError, ValueError):
        return False


def check_extensions(root: Path) -> list[str]:
    registry_path = root / ".agent" / "extensions" / "registry.json"
    if not registry_path.exists():
        return []
    errors: list[str] = []
    try:
        registry = load_json(registry_path)
        schema = load_schema(root, "harness-extension-registry.schema.json")
        errors.extend(
            f".agent/extensions/registry.json: {item}"
            for item in validate_schema(registry, schema)
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [f".agent/extensions/registry.json: {error}"]
    if errors:
        return errors
    for extension in registry.get("extensions", []):
        extension_id = extension["id"]
        declared_root = Path(extension["path"])
        config = Path(extension["config"])
        validator = Path(extension["validator"])
        if declared_root.name != extension_id:
            errors.append(f"extension {extension_id}: path/ID mismatch")
        if not confined(root, declared_root, config):
            errors.append(f"extension {extension_id}: config escapes extension path")
        if not confined(root, declared_root, validator):
            errors.append(f"extension {extension_id}: validator escapes extension path")
        if not version_satisfies_core(extension["requires_core"]):
            errors.append(f"extension {extension_id}: incompatible core version")
        if not extension["enabled"] or errors:
            continue
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    extension["validator"],
                    "--config",
                    extension["config"],
                ],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
                timeout=30,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )
        except subprocess.TimeoutExpired:
            errors.append(f"extension {extension_id}: validator timed out")
            continue
        try:
            response = loads_json(result.stdout)
        except (ValueError, json.JSONDecodeError):
            errors.append(f"extension {extension_id}: validator returned invalid JSON")
            continue
        if (
            not isinstance(response, dict)
            or response.get("schema_version") != "harness.extension-findings.v1"
            or response.get("extension_id") != extension_id
            or not isinstance(response.get("findings"), list)
        ):
            errors.append(f"extension {extension_id}: invalid validator response")
            continue
        if result.returncode not in {0, 1}:
            errors.append(f"extension {extension_id}: validator execution failed")
        if any(
            isinstance(item, dict) and item.get("severity") == "error"
            for item in response["findings"]
        ):
            errors.append(f"extension {extension_id}: validator reported errors")
    return errors


def expected_manifest_files(root: Path) -> dict[str, str]:
    return {
        relative(path, root): hash_file(path)
        for path in repository_files(root, source_only=True)
        if not path.is_symlink() and path.name != ".DS_Store"
    }


def parse_checksums(path: Path) -> tuple[dict[str, str], list[str]]:
    values: dict[str, str] = {}
    errors: list[str] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        match = re.fullmatch(r"([a-f0-9]{64})  ([^\n]+)", line)
        if not match:
            errors.append(f"project-dossier/CHECKSUMS.sha256:{number}: invalid line")
            continue
        digest, target = match.groups()
        if target in values:
            errors.append(f"project-dossier/CHECKSUMS.sha256:{number}: duplicate path")
        values[target] = digest
    return values, errors


def check_integrity(root: Path, include_generated: bool = True) -> list[str]:
    errors: list[str] = []
    manifest_path = root / "project-dossier" / "MANIFEST.json"
    try:
        manifest = load_json(manifest_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [f"project-dossier/MANIFEST.json: {error}"]
    expected_fingerprint = source_fingerprint(root)
    if manifest.get("source_fingerprint") != expected_fingerprint:
        errors.append("project-dossier/MANIFEST.json: stale source fingerprint")
    listed = {
        item.get("path"): item.get("sha256")
        for item in manifest.get("files", [])
        if isinstance(item, dict)
    }
    expected = expected_manifest_files(root)
    if listed != expected:
        errors.append("project-dossier/MANIFEST.json: file inventory or hashes are stale")

    checksum_path = root / "project-dossier" / "CHECKSUMS.sha256"
    if checksum_path.exists():
        checksums, checksum_errors = parse_checksums(checksum_path)
        errors.extend(checksum_errors)
        expected_checksums = {
            relative(path, root): hash_file(path)
            for path in sorted((root / "project-dossier").rglob("*"))
            if path.is_file() and path != checksum_path
        }
        if checksums != expected_checksums:
            errors.append("project-dossier/CHECKSUMS.sha256: stale or incomplete")

    if not include_generated:
        return errors
    generated = root / ".agent" / "generated"
    manifest_generated = generated / "manifest.json"
    report_path = generated / "validation-report.json"
    temporary = sorted(generated.glob("*.tmp")) if generated.is_dir() else []
    if temporary:
        errors.append(".agent/generated: interrupted refresh artifacts present")
    if not manifest_generated.exists() and not report_path.exists():
        return errors
    if not manifest_generated.is_file() or not report_path.is_file():
        errors.append(".agent/generated: manifest and validation report must coexist")
        return errors
    try:
        generated_manifest = load_json(manifest_generated)
        report = load_json(report_path)
    except (ValueError, json.JSONDecodeError) as error:
        errors.append(f".agent/generated: {error}")
        return errors
    generation_ids = {
        manifest.get("generation_id"),
        generated_manifest.get("generation_id"),
        report.get("generation_id"),
    }
    if len(generation_ids) != 1 or None in generation_ids:
        errors.append("generated integrity files have mismatched generation IDs")
    for name, value in (
        (".agent/generated/manifest.json", generated_manifest),
        (".agent/generated/validation-report.json", report),
    ):
        if value.get("source_fingerprint") != expected_fingerprint:
            errors.append(f"{name}: stale source fingerprint")
        if value.get("authority") != "generated_non_authoritative_point_in_time":
            errors.append(f"{name}: invalid authority label")
    if report.get("result") != "PASS":
        errors.append(".agent/generated/validation-report.json: result is not PASS")
    return errors


def git_scope(root: Path) -> dict[str, Any]:
    result = {
        "available": False,
        "tracked_modified": "not_assessed",
        "untracked": "not_assessed",
        "ignored": "not_assessed",
    }
    probe = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if probe.returncode:
        return result
    result["available"] = True
    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "--ignored"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    tracked = untracked = ignored = 0
    if status.returncode == 0:
        for line in status.stdout.splitlines():
            if line.startswith("!!"):
                ignored += 1
            elif line.startswith("??"):
                untracked += 1
            else:
                tracked += 1
        result.update(
            tracked_modified=tracked,
            untracked=untracked,
            ignored=ignored,
        )
    return result


def check(root: Path = ROOT, include_generated: bool = True) -> list[str]:
    errors: list[str] = []
    errors.extend(check_runtime())
    errors.extend(check_files_and_json(root))
    errors.extend(check_kernel(root))
    errors.extend(check_origin(root))
    records, record_errors = collect_records(root)
    errors.extend(record_errors)
    if not record_errors:
        errors.extend(check_references_and_lifecycle(root, records))
        errors.extend(check_plan_and_traceability(records))
    errors.extend(check_dossier_catalog(root))
    errors.extend(check_extensions(root))
    if include_generated:
        errors.extend(check_integrity(root, include_generated=True))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only structural validation of the project foundation."
    )
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    errors = check()
    for error in errors:
        print(f"[FAIL] {error}", file=sys.stderr)
    if errors:
        return 1
    print("[PASS] harness and dossier structural contracts")
    print("[INFO] project adoption, implementation, and readiness remain unassessed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
