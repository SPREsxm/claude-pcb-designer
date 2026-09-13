# Changelog

All notable changes follow [Keep a Changelog](https://keepachangelog.com/) and
semantic versioning.

## [3.0.1] - 2026-09-13

### Fixed

- Allowed the package validator to run from a repository checkout whose folder
  name differs from the skill name, such as `claude-pcb-designer`.
- Added a regression path for repository-root and installed-skill validation.

## [3.0.0] - 2026-09-13

### Added

- Deterministic calculator CLI for trace width, via current, impedance,
  regulator thermal margin, battery life, buck inductors, RC filters, voltage
  dividers, and CSV power budgets.
- Fabrication release auditor for Gerber/drill presence, BOM/CPL schema,
  designator consistency, and common packaging failures.
- Skill package validator and CI workflow.
- New references for design intake, component selection, schematic review,
  review severity, stackup/impedance, release, bring-up, high reliability, and
  standards.
- Templates for design briefs, review reports, fabrication release, power
  budgets, and bring-up logs.
- Worked examples for an ESP32-S3 board, a review, and a beginner-safe board.
- Cross-agent installer for Codex, Claude Code, and Agent Skills directories.
- Chinese README, citation metadata, contribution templates, and machine-readable
  design/fab profiles.

### Changed

- Reframed `SKILL.md` as a concise progressive-disclosure entrypoint instead of
  a monolithic manual.
- Corrected supplier-specific and datasheet-dependent wording across existing
  references.
- Updated EasyEDA/嘉立创EDA naming and workflow details.
- Removed blanket CSV/ZIP ignores so templates and evidence can be versioned.

### Security

- Added explicit safety boundaries for mains, high voltage, batteries, RF,
  medical, automotive, aviation, and space projects.

## [2.0.1] - 2026-06-28

### Fixed

- Audit findings and documentation consistency.

## [2.0.0] - 2026-06-19

### Added

- Comprehensive embedded, RF, power, manufacturing, and compliance references.
