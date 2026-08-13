#!/usr/bin/env python3
"""One workflow-oriented interface for bootstrap and project-local commands."""

from __future__ import annotations

import subprocess
import sys
import json
from pathlib import Path


SCRIPT_ROOT = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_ROOT.parent


HELP = """Project Blueprint workflow interface

Bootstrap-source workflows:
  pb init [plan|apply] ...       guided new-project initialization
  pb adopt plan|apply ...        bounded established-project adoption
  pb upgrade plan|apply ...      three-way live-project upgrade
  pb detect --target PATH        read-only archetype and hook proposals
  pb maintain package ...        triggered package installation
  pb maintain collaboration ... progressive collaboration assessment

Project-local workflows (run from a generated project):
  pb work start|block|close|reopen|handoff|resume ...
  pb check [--json]
  pb doctor ...
  pb maintain refresh|registry|hooks ...
  pb transaction apply|rollback|recover ...

No command grants permission and there is no global force option.
"""


def execute(script: Path, arguments: list[str]) -> int:
    return subprocess.run(
        [sys.executable, "-B", str(script), *arguments],
        cwd=Path.cwd(),
        check=False,
        shell=False,
    ).returncode


def command_manifest() -> dict[str, object]:
    candidates = (
        SKILL_ROOT.parents[1] / "shared/source-contracts/commands.json",
        SKILL_ROOT / "assets/blueprint-source/shared/source-contracts/commands.json",
    )
    path = next((item for item in candidates if item.is_file()), None)
    if path is None:
        raise ValueError("authoritative command manifest is unavailable")
    value = json.loads(path.read_text(encoding="utf-8"))
    commands = value.get("commands", [])
    if not isinstance(commands, list) or any(not isinstance(item, dict) for item in commands):
        raise ValueError("authoritative command manifest commands must be objects")
    names = [item.get("name") for item in commands]
    roots = {str(name).split(".", 1)[0] for name in names}
    expected = {"init", "adopt", "upgrade", "detect", "check", "doctor", "work", "maintain", "transaction"}
    availability = {item.get("availability") for item in commands}
    bootstrap_roots = {
        str(item.get("name")).split(".", 1)[0]
        for item in commands
        if item.get("availability") == "bootstrap_source"
    }
    project_roots = {
        str(item.get("name")).split(".", 1)[0]
        for item in commands
        if item.get("availability") == "generated_project"
    }
    if (
        value.get("schema_version") != "harness.command-manifest.v1"
        or value.get("permission_grant") is not False
        or len(names) != len(set(names))
        or roots != expected
        or availability != {"bootstrap_source", "generated_project"}
        or bootstrap_roots != {"init", "adopt", "upgrade", "detect", "maintain"}
        or project_roots != {"check", "doctor", "work", "maintain", "transaction"}
    ):
        raise ValueError("authoritative command manifest is malformed or differs from the dispatcher")
    return value


def local(arguments: list[str]) -> int:
    launcher = Path.cwd() / "pb"
    if not launcher.is_file() or launcher.is_symlink():
        print("[FAIL] no generated-project `pb` launcher in the current directory", file=sys.stderr)
        return 2
    return subprocess.run([str(launcher), *arguments], cwd=Path.cwd(), check=False, shell=False).returncode


def main() -> int:
    try:
        command_manifest()
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        return 2
    arguments = sys.argv[1:]
    if not arguments or arguments[0] in {"-h", "--help", "help"}:
        print(HELP)
        return 0
    command, rest = arguments[0], arguments[1:]
    if command == "init":
        if not rest or rest[0] not in {"plan", "apply", "interactive"}:
            rest = ["interactive", *rest]
        return execute(SCRIPT_ROOT / "init_project.py", rest)
    if command == "adopt":
        return execute(SCRIPT_ROOT / "adopt_project.py", rest)
    if command == "upgrade":
        script = SCRIPT_ROOT / "upgrade_project.py"
        if not script.is_file():
            print("[FAIL] live upgrade planner is unavailable in this snapshot", file=sys.stderr)
            return 2
        return execute(script, rest)
    if command == "detect":
        return execute(SCRIPT_ROOT / "detect_project.py", rest)
    if command == "maintain" and rest:
        if rest[0] == "package":
            return execute(SCRIPT_ROOT / "package_project.py", rest[1:])
        if rest[0] == "collaboration":
            return execute(SCRIPT_ROOT / "collaboration_project.py", rest[1:])
    if command in {"work", "check", "doctor", "maintain", "transaction"}:
        return local(arguments)
    print(f"[FAIL] unknown workflow: {command}", file=sys.stderr)
    print(HELP, file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
