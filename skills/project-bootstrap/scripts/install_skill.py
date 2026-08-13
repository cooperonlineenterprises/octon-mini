#!/usr/bin/env python3
"""Install a collision-safe snapshot of the project-bootstrap Codex skill."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def default_destination() -> Path:
    codex_root = os.environ.get("CODEX_HOME")
    base = Path(codex_root).expanduser() if codex_root else Path.home() / ".codex"
    return base / "skills" / "project-bootstrap"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--destination", type=Path, default=default_destination())
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def blueprint_root(skill_source: Path) -> Path:
    candidates = (
        skill_source.parents[1],
        skill_source / "assets" / "blueprint-source",
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


def main() -> int:
    if sys.version_info < (3, 11):
        print("ERROR: Python 3.11+ is required.", file=sys.stderr)
        return 2
    args = parse_args()
    source = Path(__file__).resolve().parents[1]
    destination = args.destination.expanduser().resolve()
    if destination.exists():
        print(
            f"ERROR: destination already exists; refusing replacement: {destination}",
            file=sys.stderr,
        )
        return 3
    if not destination.parent.is_dir():
        print(
            f"ERROR: destination parent must already exist: {destination.parent}",
            file=sys.stderr,
        )
        return 2
    print(f"Source: {source}")
    print(f"Destination: {destination}")
    if args.dry_run:
        print("Dry run complete; no files written.")
        return 0
    try:
        repository_root = blueprint_root(source)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    with tempfile.TemporaryDirectory(
        prefix=".project-bootstrap-install-", dir=destination.parent
    ) as temporary:
        stage = Path(temporary) / destination.name
        shutil.copytree(
            source,
            stage,
            ignore=shutil.ignore_patterns(
                ".DS_Store", "__pycache__", "*.pyc", "blueprint-source"
            ),
        )
        bundle = stage / "assets" / "blueprint-source"
        bundle.mkdir(parents=True)
        for directory in (
            ".github",
            "dossier",
            "harness",
            "shared",
            "patterns",
            "migrations",
            "docs",
        ):
            shutil.copytree(
                repository_root / directory,
                bundle / directory,
                ignore=shutil.ignore_patterns(".DS_Store", "__pycache__", "*.pyc"),
            )
        for filename in (
            "VERSION",
            "VELOCITY_ROADMAP.md",
            "VELOCITY_VALIDATION.md",
            "blueprint.json",
            "CHANGELOG.md",
            "RELEASE.md",
            "GIT_WORKFLOW.md",
            "ARCHITECTURE_DECISIONS.md",
            "ARCHITECTURAL_PATTERN_INTEGRATION_REVIEW.md",
            ".gitignore",
            "AGENTS.md",
            "README.md",
            "pyproject.toml",
        ):
            shutil.copy2(repository_root / filename, bundle / filename)
        staged_checks = (
            [
                sys.executable,
                "-B",
                str(stage / "scripts" / "validate_skill_package.py"),
                str(stage),
            ],
            [
                sys.executable,
                "-B",
                str(stage / "scripts" / "verify_reference_evidence.py"),
            ],
            [
                sys.executable,
                "-B",
                str(stage / "scripts" / "validate_blueprint.py"),
            ],
        )
        for command in staged_checks:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode:
                print(
                    "ERROR: staged installed skill failed package validation: "
                    + (result.stderr.strip() or result.stdout.strip()),
                    file=sys.stderr,
                )
                return 4
        smoke_target = Path(temporary) / "smoke-project"
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                str(stage / "scripts" / "scaffold_project.py"),
                "--target",
                str(smoke_target),
                "--project-name",
                "Installed Skill Smoke Test",
                "--profile",
                "minimal",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode:
            print(
                "ERROR: staged installed skill failed its generation smoke test: "
                + (result.stderr.strip() or result.stdout.strip()),
                file=sys.stderr,
            )
            return 4
        os.replace(stage, destination)
    print("Installed project-bootstrap skill snapshot.")
    print(
        "The staged package, bundled blueprint, and profile builds passed; "
        "inspect the installed SKILL.md before first project use."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
