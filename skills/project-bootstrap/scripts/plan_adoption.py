#!/usr/bin/env python3
"""Produce a read-only adoption plan for an established project."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


def load_scaffolder():
    path = Path(__file__).with_name("scaffold_project.py")
    spec = importlib.util.spec_from_file_location("project_blueprint_scaffold", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load generator contracts: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def classify_existing(target: Path) -> dict[str, Any]:
    indicators = {
        "root_instructions": (target / "AGENTS.md").is_file(),
        "agent_harness": (target / ".agent").is_dir(),
        "capability_packages": (target / ".agents").is_dir(),
        "project_dossier": (target / "project-dossier").is_dir(),
        "blueprint_origin": (target / ".project-blueprint-origin.json").is_file(),
        "git_repository": (target / ".git").exists(),
    }
    technology_markers = [
        name
        for name in (
            "package.json",
            "pyproject.toml",
            "Cargo.toml",
            "go.mod",
            "Gemfile",
            "pom.xml",
            "build.gradle",
            "Makefile",
            "Dockerfile",
        )
        if (target / name).exists()
    ]
    return {
        "indicators": indicators,
        "technology_markers": technology_markers,
    }


def origin_summary(target: Path, scaffolder: Any) -> dict[str, Any] | None:
    path = target / ".project-blueprint-origin.json"
    if not path.is_file():
        return None
    try:
        value = scaffolder.load_json(path)
    except (OSError, ValueError, json.JSONDecodeError):
        return {"status": "present_but_invalid"}
    if not isinstance(value, dict):
        return {"status": "present_but_invalid"}
    return {
        "status": "valid_shape_not_fully_validated",
        "blueprint_version": value.get("blueprint_version"),
        "profile": value.get("profile"),
        "harness_kernel_version": value.get("harness_kernel_version"),
    }


def build_plan(target: Path, profile: str) -> dict[str, Any]:
    scaffolder = load_scaffolder()
    scaffolder.require_runtime()
    if not target.is_absolute():
        raise ValueError("--target must be an absolute path")
    resolved = target.resolve()
    if not resolved.is_dir():
        raise ValueError("--target must be an existing directory")

    templates = scaffolder.collect_templates(profile)
    schemas = scaffolder.schema_outputs()
    intended = (
        set(templates)
        | set(schemas)
        | scaffolder.DERIVED_PATHS
        | {Path(".project-blueprint-origin.json")}
    )
    if profile == "high-assurance":
        intended |= scaffolder.HIGH_DERIVED_PATHS

    collisions = sorted(
        path.as_posix() for path in intended if (resolved / path).exists()
    )
    absent = sorted(
        path.as_posix() for path in intended if not (resolved / path).exists()
    )
    existing_top_level = sorted(
        path.name
        for path in resolved.iterdir()
        if path.name not in {".git", ".DS_Store"}
    )
    return {
        "schema_version": "project-blueprint.adoption-plan.v1",
        "authority": (
            "Read-only inventory and reconciliation guidance; not permission "
            "to modify, replace, or accept project content."
        ),
        "target": str(resolved),
        "requested_profile": profile,
        "blueprint_version": scaffolder.blueprint_version(),
        "existing": classify_existing(resolved),
        "origin": origin_summary(resolved, scaffolder),
        "existing_top_level_names": existing_top_level,
        "collisions": collisions,
        "candidate_new_paths": absent,
        "required_sequence": [
            "Read applicable target-project instructions root to leaf.",
            "Classify existing authority, governance, dossier, and handoff sources.",
            "Map direct and functional equivalents before proposing file changes.",
            "Preserve accepted target decisions and project facts.",
            "Resolve each collision through an authorized project-specific change.",
            "Add only controls justified by the selected profile triggers.",
            "Run target checks plus blueprint mutation tests on the exact result.",
            "Record migration provenance, limitations, and a safe resumption point.",
        ],
        "non_transfer_rules": [
            "Do not copy permissions, accepted decisions, implementation claims, or readiness.",
            "Do not overwrite existing files or silently change authority.",
            "Do not treat absent blueprint paths as proof of a project gap until functional equivalents are reviewed.",
        ],
    }


def render_markdown(plan: dict[str, Any]) -> str:
    lines = [
        "# Project Blueprint Adoption Plan",
        "",
        f"- Target: `{plan['target']}`",
        f"- Requested profile: `{plan['requested_profile']}`",
        f"- Blueprint version: `{plan['blueprint_version']}`",
        f"- Authority: {plan['authority']}",
        "",
        "## Existing signals",
        "",
    ]
    for key, value in plan["existing"]["indicators"].items():
        lines.append(f"- {key}: `{str(value).lower()}`")
    markers = plan["existing"]["technology_markers"]
    lines.append(
        "- technology markers: "
        + (", ".join(f"`{item}`" for item in markers) if markers else "none observed")
    )
    origin = plan["origin"]
    lines.extend(["", "## Existing blueprint origin", ""])
    if origin is None:
        lines.append("- none observed")
    else:
        for key, value in origin.items():
            lines.append(f"- {key}: `{value}`")
    lines.extend(
        [
            "",
            f"## Exact path collisions ({len(plan['collisions'])})",
            "",
        ]
    )
    lines.extend(
        [f"- `{item}`" for item in plan["collisions"]]
        or ["- none"]
    )
    lines.extend(
        [
            "",
            f"## Candidate new paths ({len(plan['candidate_new_paths'])})",
            "",
        ]
    )
    lines.extend(
        [f"- `{item}`" for item in plan["candidate_new_paths"]]
        or ["- none"]
    )
    lines.extend(["", "## Required reconciliation sequence", ""])
    for index, item in enumerate(plan["required_sequence"], 1):
        lines.append(f"{index}. {item}")
    lines.extend(["", "## Non-transfer rules", ""])
    lines.extend(f"- {item}" for item in plan["non_transfer_rules"])
    lines.extend(
        [
            "",
            "This plan is intentionally read-only. It identifies exact path "
            "collisions, not functional equivalence or authorization to edit.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument(
        "--profile",
        choices=("minimal", "standard", "high-assurance"),
        default="standard",
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        plan = build_plan(args.target.expanduser(), args.profile)
    except (OSError, RuntimeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(plan, indent=2, sort_keys=True))
    else:
        print(render_markdown(plan), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
