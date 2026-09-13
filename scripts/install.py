#!/usr/bin/env python3
"""Install the current skill package into a Codex, Claude, or Agent Skills path."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

INSTALL_ITEMS = (
    "SKILL.md",
    "LICENSE",
    "README.md",
    "references",
    "scripts",
    "templates",
    "rules",
    "examples",
)


def default_target(target: str, custom_path: str | None) -> Path:
    home = Path.home()
    if target == "codex":
        codex_home = os.environ.get("CODEX_HOME")
        base = Path(codex_home) if codex_home else home / ".codex"
        return base / "skills" / "pcb-designer"
    if target == "claude":
        return home / ".claude" / "skills" / "pcb-designer"
    if target == "agents":
        return home / ".agents" / "skills" / "pcb-designer"
    if target == "custom":
        if not custom_path:
            raise ValueError("--path is required when --target custom is used")
        return Path(custom_path).expanduser().resolve()
    raise ValueError(f"unsupported target: {target}")


def safe_remove(target: Path, allowed_parent: Path) -> None:
    resolved = target.resolve()
    parent = allowed_parent.resolve()
    if resolved == parent or parent not in resolved.parents:
        raise RuntimeError(f"refusing to remove unexpected path: {resolved}")
    shutil.rmtree(resolved)


def install(
    source: Path,
    target: Path,
    force: bool,
    dry_run: bool,
) -> list[str]:
    source = source.resolve()
    if not (source / "SKILL.md").exists():
        raise FileNotFoundError(f"not a skill package: {source}")
    actions: list[str] = []
    if target.exists() and not force:
        raise FileExistsError(f"target already exists: {target}; rerun with --force to replace it")
    if target.exists() and (target / ".git").exists():
        raise RuntimeError(
            f"target is a Git checkout and will not be replaced: {target}; "
            "update it with git pull instead"
        )
    if target.exists() and not (target / "SKILL.md").exists():
        raise RuntimeError(
            f"refusing to replace a directory that is not an installed skill: {target}"
        )
    if dry_run:
        actions.append(f"would create {target}")
        for item in INSTALL_ITEMS:
            if (source / item).exists():
                actions.append(f"would copy {item}")
        return actions

    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        safe_remove(target, target.parent)
        actions.append(f"replaced {target}")
    else:
        actions.append(f"created {target}")
    target.mkdir(parents=True, exist_ok=False)
    for item in INSTALL_ITEMS:
        source_item = source / item
        if not source_item.exists():
            continue
        destination = target / item
        if source_item.is_dir():
            shutil.copytree(
                source_item,
                destination,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
            )
        else:
            shutil.copy2(source_item, destination)
        actions.append(f"copied {item}")
    return actions


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target",
        choices=("codex", "claude", "agents", "custom"),
        default="codex",
    )
    parser.add_argument("--path", help="destination for --target custom")
    parser.add_argument("--source", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--force", action="store_true", help="replace an existing install")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        target = default_target(args.target, args.path)
        actions = install(Path(args.source), target, args.force, args.dry_run)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    for action in actions:
        print(action)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
