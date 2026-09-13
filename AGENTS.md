# Repository Instructions for Coding Agents

This repository packages a PCB design skill for Codex, Claude Code, and other
Agent Skills runtimes.

## Core Rules

1. Keep `SKILL.md` concise and route details to `references/`.
2. Never invent component data, supplier capability, pinout, price, or stackup.
3. Label estimates and model limitations.
4. Update tests with every calculator or auditor behavior change.
5. Keep supplier-specific data in `rules/fab-profiles.json` with verification
   status.
6. Preserve the safety boundary for regulated and safety-critical hardware.
7. Use `apply_patch` for manual edits.

## Validation

Run before committing:

```bash
python scripts/validate_skill.py .
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```

## Release Checklist

- bump `metadata.version` in `SKILL.md`;
- update `CHANGELOG.md`;
- update the README badge or release notes if needed;
- run all validation;
- commit and tag `vX.Y.Z`;
- push the branch and tag.
