#!/usr/bin/env python3
"""Validate the pcb-designer skill package without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ALLOWED_FRONTMATTER_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}
LOCAL_REFERENCE_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_.-])" r"((?:references|scripts|templates|rules|examples)/[A-Za-z0-9._/-]+)"
)
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?$")
PLACEHOLDER_PATTERN = re.compile(r"<repo-url>|\[TODO:[^\]]*\]|TODO\(|FIXME\(|\bTBD\b")
MARKDOWN_LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


class ValidationError(Exception):
    pass


def extract_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        raise ValidationError("SKILL.md must start with YAML frontmatter")
    match = re.match(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.DOTALL)
    if not match:
        raise ValidationError("SKILL.md frontmatter is not closed with ---")
    return match.group(1)


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_frontmatter_simple(text: str) -> dict[str, Any]:
    """Parse enough YAML for this package's frontmatter without PyYAML."""
    result: dict[str, Any] = {}
    current_map: str | None = None
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()
        if indent == 0:
            if ":" not in line:
                raise ValidationError(f"Invalid frontmatter line: {raw_line}")
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value in {">", "|"}:
                result[key] = ""
                current_map = key
            elif value == "":
                result[key] = {}
                current_map = key
            else:
                result[key] = unquote(value)
                current_map = None
        elif current_map:
            target = result.get(current_map)
            if not isinstance(target, dict):
                target = {}
                result[current_map] = target
            if line.startswith("- "):
                target.setdefault("_list", []).append(unquote(line[2:]))
            elif ":" in line:
                key, value = line.split(":", 1)
                target[key.strip()] = unquote(value.strip())
            else:
                raise ValidationError(f"Invalid nested frontmatter line: {raw_line}")
    return result


def load_frontmatter(text: str) -> dict[str, Any]:
    raw = extract_frontmatter(text)
    try:
        import yaml  # type: ignore
    except ImportError:
        return parse_frontmatter_simple(raw)
    try:
        loaded = yaml.safe_load(raw)
    except yaml.YAMLError as exc:  # type: ignore[attr-defined]
        raise ValidationError(f"Invalid YAML frontmatter: {exc}") from exc
    if not isinstance(loaded, dict):
        raise ValidationError("frontmatter must be a mapping")
    return loaded


def validate_frontmatter(root: Path, text: str) -> list[str]:
    issues: list[str] = []
    frontmatter = load_frontmatter(text)
    unexpected = set(frontmatter) - ALLOWED_FRONTMATTER_KEYS
    if unexpected:
        issues.append("Unexpected frontmatter key(s): " + ", ".join(sorted(unexpected)))
    name = frontmatter.get("name")
    if not isinstance(name, str) or not name:
        issues.append("frontmatter name is required")
    else:
        if not re.fullmatch(r"[a-z0-9-]+", name):
            issues.append("frontmatter name must use lowercase letters, digits, and hyphens")
        if name.startswith("-") or name.endswith("-") or "--" in name:
            issues.append("frontmatter name has invalid hyphen placement")
        if len(name) > 64:
            issues.append("frontmatter name exceeds 64 characters")
    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        issues.append("frontmatter description is required")
    else:
        if len(description) > 1024:
            issues.append("frontmatter description exceeds 1024 characters")
        if "<" in description or ">" in description:
            issues.append("frontmatter description must not contain angle brackets")
    metadata = frontmatter.get("metadata")
    if isinstance(metadata, dict):
        version = metadata.get("version")
        if version is not None and not SEMVER_PATTERN.fullmatch(str(version)):
            issues.append(f"metadata.version is not semantic versioning: {version}")
    return issues


def validate_local_references(root: Path, text: str) -> list[str]:
    issues: list[str] = []
    for relative in sorted(set(LOCAL_REFERENCE_PATTERN.findall(text))):
        candidate = root / relative
        if not candidate.exists():
            issues.append(f"referenced local path does not exist: {relative}")
        elif candidate.is_file() and candidate.stat().st_size == 0:
            issues.append(f"referenced local file is empty: {relative}")
    return issues


def validate_json_files(root: Path) -> list[str]:
    issues: list[str] = []
    for path in sorted(root.rglob("*.json")):
        if ".git" in path.parts:
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            issues.append(f"invalid JSON in {path.relative_to(root)}: {exc}")
    return issues


def validate_markdown_links(root: Path) -> list[str]:
    issues: list[str] = []
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for raw_target in MARKDOWN_LINK_PATTERN.findall(text):
            target = raw_target.strip().strip("<>")
            if " " in target:
                target = target.split()[0]
            target = target.split("#", 1)[0]
            if not target:
                continue
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            candidate = (path.parent / target).resolve()
            try:
                candidate.relative_to(root.resolve())
            except ValueError:
                issues.append(
                    f"markdown link escapes the package in {path.relative_to(root)}: {target}"
                )
                continue
            if not candidate.exists():
                issues.append(f"broken markdown link in {path.relative_to(root)}: {target}")
    return issues


def validate_evals(root: Path) -> list[str]:
    issues: list[str] = []
    path = root / "evals" / "evals.json"
    if not path.exists():
        return ["evals/evals.json is missing"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"could not parse evals/evals.json: {exc}"]
    evals = data.get("evals") if isinstance(data, dict) else None
    if not isinstance(evals, list) or not evals:
        return ["evals/evals.json must contain a non-empty evals list"]
    ids: set[Any] = set()
    for index, item in enumerate(evals, start=1):
        if not isinstance(item, dict):
            issues.append(f"eval {index} is not an object")
            continue
        item_id = item.get("id")
        if item_id in ids:
            issues.append(f"duplicate eval id: {item_id}")
        ids.add(item_id)
        if not isinstance(item.get("prompt"), str) or not item["prompt"].strip():
            issues.append(f"eval {index} has no prompt")
        rubric = item.get("rubric")
        if not isinstance(rubric, dict):
            issues.append(f"eval {index} has no rubric")
        else:
            keywords = rubric.get("required_keywords")
            minimum = rubric.get("min_keywords_matched")
            if not isinstance(keywords, list) or not keywords:
                issues.append(f"eval {index} has no required_keywords")
            if not isinstance(minimum, int) or minimum < 0:
                issues.append(f"eval {index} has an invalid min_keywords_matched")
            elif isinstance(keywords, list) and minimum > len(keywords):
                issues.append(f"eval {index} minimum exceeds the keyword count")
    return issues


def validate_placeholders(root: Path) -> list[str]:
    issues: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.name == "validate_skill.py":
            continue
        if path.suffix.lower() not in {".md", ".json", ".py", ".yaml", ".yml", ".txt", ".cff"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in PLACEHOLDER_PATTERN.finditer(text):
            issues.append(f"placeholder '{match.group(0)}' in {path.relative_to(root)}")
    return issues


def validate_package(root: Path) -> list[str]:
    issues: list[str] = []
    skill_path = root / "SKILL.md"
    if not skill_path.exists():
        return ["SKILL.md is missing"]
    text = skill_path.read_text(encoding="utf-8")
    try:
        issues.extend(validate_frontmatter(root, text))
    except ValidationError as exc:
        issues.append(str(exc))
    issues.extend(validate_local_references(root, text))
    issues.extend(validate_json_files(root))
    issues.extend(validate_markdown_links(root))
    issues.extend(validate_evals(root))
    issues.extend(validate_placeholders(root))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="skill directory")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    issues = validate_package(root)
    payload = {
        "root": str(root),
        "valid": not issues,
        "issue_count": len(issues),
        "issues": issues,
    }
    if args.json:
        print(json.dumps(payload, indent=2))
    elif issues:
        for issue in issues:
            print(f"ERROR: {issue}")
    else:
        print(f"Skill package is valid: {root}")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
