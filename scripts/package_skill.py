#!/usr/bin/env python3
"""Create a portable ZIP package for skill marketplaces and GitHub releases."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

try:
    from .validate_skill import load_frontmatter, validate_package
except ImportError:
    from validate_skill import (  # type: ignore[no-redef]
        load_frontmatter,
        validate_package,
    )

ROOT_FILES = (
    "SKILL.md",
    "README.md",
    "README.zh-CN.md",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CITATION.cff",
    "llms.txt",
)
ROOT_DIRS = ("agents", "references", "scripts", "templates", "rules", "examples")
EXCLUDED_NAMES = {"__pycache__", ".DS_Store", ".gitkeep"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def skill_version(root: Path) -> str:
    text = (root / "SKILL.md").read_text(encoding="utf-8")
    metadata = load_frontmatter(text).get("metadata", {})
    version = metadata.get("version") if isinstance(metadata, dict) else None
    if not version:
        return "0.0.0"
    return str(version)


def package(root: Path, output: Path) -> Path:
    issues = validate_package(root)
    if issues:
        raise ValueError("refusing to package an invalid skill: " + "; ".join(issues))
    output.parent.mkdir(parents=True, exist_ok=True)
    prefix = "pcb-designer"
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in ROOT_FILES:
            path = root / name
            if path.exists() and path.is_file():
                archive.write(path, f"{prefix}/{name}")
        for directory_name in ROOT_DIRS:
            directory = root / directory_name
            if not directory.exists():
                continue
            for path in sorted(item for item in directory.rglob("*") if item.is_file()):
                if path.name in EXCLUDED_NAMES or path.suffix in EXCLUDED_SUFFIXES:
                    continue
                archive.write(path, f"{prefix}/{path.relative_to(root).as_posix()}")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--output")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    version = skill_version(root)
    output = (
        Path(args.output).resolve()
        if args.output
        else root / "dist" / f"pcb-designer-v{version}.zip"
    )
    try:
        package(root, output)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}")
        return 1
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
