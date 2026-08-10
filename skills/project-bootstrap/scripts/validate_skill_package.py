#!/usr/bin/env python3
"""Validate this skill package without third-party runtime dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"\A---\n(?P<body>.*?)\n---(?:\n|\Z)", re.DOTALL)
OPENAI_FIELD_RE = re.compile(r'^  ([a-z_]+): ("(?:[^"\\]|\\.)*")$')


def parse_simple_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("SKILL.md must begin with closed YAML frontmatter")
    result: dict[str, str] = {}
    for number, line in enumerate(match.group("body").splitlines(), 1):
        if not line or line.startswith((" ", "\t", "#")):
            raise ValueError(
                f"SKILL.md frontmatter line {number} is not a simple mapping entry"
            )
        if ":" not in line:
            raise ValueError(f"SKILL.md frontmatter line {number} lacks ':'")
        key, value = line.split(":", 1)
        if key in result:
            raise ValueError(f"SKILL.md frontmatter duplicates {key!r}")
        result[key] = value.strip()
    return result


def validate_skill_md(skill_root: Path) -> list[str]:
    issues: list[str] = []
    path = skill_root / "SKILL.md"
    if not path.is_file():
        return ["SKILL.md is missing"]
    try:
        frontmatter = parse_simple_frontmatter(path)
    except (OSError, UnicodeError, ValueError) as error:
        return [str(error)]

    allowed = {"name", "description", "license", "allowed-tools", "metadata"}
    unexpected = sorted(set(frontmatter) - allowed)
    if unexpected:
        issues.append(f"SKILL.md has unexpected keys: {', '.join(unexpected)}")
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if not NAME_RE.fullmatch(name) or len(name) > 64:
        issues.append("SKILL.md name must be 1-64 lowercase hyphen-case characters")
    if not description:
        issues.append("SKILL.md description is required")
    elif len(description) > 1024:
        issues.append("SKILL.md description exceeds 1024 characters")
    elif "<" in description or ">" in description:
        issues.append("SKILL.md description must not contain angle brackets")
    return issues


def validate_openai_yaml(skill_root: Path) -> list[str]:
    issues: list[str] = []
    path = skill_root / "agents/openai.yaml"
    if not path.is_file():
        return ["agents/openai.yaml is missing"]
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        return [f"cannot read agents/openai.yaml: {error}"]
    if not lines or lines[0] != "interface:":
        return ["agents/openai.yaml must begin with the interface mapping"]

    fields: dict[str, str] = {}
    for number, line in enumerate(lines[1:], 2):
        if not line:
            continue
        match = OPENAI_FIELD_RE.fullmatch(line)
        if not match:
            issues.append(
                f"agents/openai.yaml line {number} must be a quoted interface scalar"
            )
            continue
        key, encoded = match.groups()
        if key in fields:
            issues.append(f"agents/openai.yaml duplicates interface.{key}")
            continue
        try:
            fields[key] = json.loads(encoded)
        except json.JSONDecodeError as error:
            issues.append(f"agents/openai.yaml line {number} is not valid quoted text: {error}")

    allowed = {
        "display_name",
        "short_description",
        "icon_small",
        "icon_large",
        "brand_color",
        "default_prompt",
    }
    unexpected = sorted(set(fields) - allowed)
    if unexpected:
        issues.append(
            "agents/openai.yaml has unsupported interface fields: "
            + ", ".join(unexpected)
        )
    for required in ("display_name", "short_description", "default_prompt"):
        if not fields.get(required):
            issues.append(f"agents/openai.yaml requires interface.{required}")
    short = fields.get("short_description", "")
    if short and not 25 <= len(short) <= 64:
        issues.append("interface.short_description must be 25-64 characters")

    skill_name = ""
    try:
        skill_name = parse_simple_frontmatter(skill_root / "SKILL.md").get("name", "")
    except (OSError, UnicodeError, ValueError):
        pass
    prompt = fields.get("default_prompt", "")
    if skill_name and f"${skill_name}" not in prompt:
        issues.append(
            f"interface.default_prompt must explicitly mention ${skill_name}"
        )
    for icon_key in ("icon_small", "icon_large"):
        icon = fields.get(icon_key)
        if icon:
            candidate = (skill_root / icon).resolve()
            try:
                candidate.relative_to(skill_root.resolve())
            except ValueError:
                issues.append(f"interface.{icon_key} escapes the skill directory")
            else:
                if not candidate.is_file():
                    issues.append(f"interface.{icon_key} does not resolve to a file")
    return issues


def main() -> int:
    if len(sys.argv) > 2:
        print("usage: validate_skill_package.py [skill-directory]", file=sys.stderr)
        return 2
    skill_root = (
        Path(sys.argv[1]).resolve()
        if len(sys.argv) == 2
        else Path(__file__).resolve().parents[1]
    )
    issues = validate_skill_md(skill_root) + validate_openai_yaml(skill_root)
    if issues:
        print("Skill package validation failed:", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1
    print(f"Skill package validation passed: {skill_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
