---
name: pcb-designer
description: Design, review, calculate, and release printed circuit boards for embedded, IoT, mixed-signal, power, and RF projects. Use when the user mentions PCB, schematic capture, layout, stackup, BOM, Gerber, pick-and-place, DRC/ERC, DFM/DFA, impedance, EMI/EMC, thermal design, EasyEDA/嘉立创EDA, KiCad, JLCPCB, or board bring-up. Not for mechanical-only enclosure design or IC-level silicon design.
license: MIT
metadata:
  author: SPREsxm
  version: "3.0.0"
  repository: https://github.com/SPREsxm/claude-pcb-designer
  keywords:
    - pcb
    - hardware
    - embedded
    - schematic
    - layout
    - manufacturing
    - dfm
    - emc
    - kicad
    - easyeda
---

# PCB Designer

Use this skill as a senior hardware design partner. It covers requirements,
component selection, schematic review, stackup, placement, routing, power,
signal integrity, thermal design, manufacturing release, compliance, and
bring-up.

## Operating Rules

1. **Verify before asserting.** Datasheets, reference designs, current fab
   capabilities, and the user's actual files override generic guidance.
   Never invent pinouts, part numbers, LCSC IDs, ratings, prices, or stackup
   dimensions.
2. **Separate facts, assumptions, and recommendations.** State missing
   information that materially changes the design. Ask only blocking questions;
   otherwise make a conservative assumption and label it.
3. **Use deterministic tools.** For trace width, voltage drop, thermal rise,
   impedance, filters, regulator loss, or battery life, run
   `scripts/pcbcalc.py` instead of doing arithmetic from memory.
4. **Design for manufacture from the start.** Treat DRC/ERC, test access,
   assembly orientation, component availability, and fabrication limits as
   design inputs, not final paperwork.
5. **Protect safety.** Mains, high voltage, high current, lithium batteries,
   RF exposure, medical, automotive, aviation, and safety-critical work need a
   qualified human review and applicable standards. Do not claim certification
   or approval. State this boundary explicitly.
6. **Do not mutate design files blindly.** Inspect the project first. Preserve
   a backup or use version control before bulk edits. For EasyEDA live
   operations, pair with `easyeda-api`.

## Mode Router

Read only the references needed for the current task.

| User request | Read first | Also read when relevant |
|---|---|---|
| Start a new board | `references/design-intake.md` | Domain references below |
| Review schematic | `references/schematic-review.md` | `references/design-review-rubric.md`, interface/domain refs |
| Review layout or DRC | `references/design-review-rubric.md` | `references/dfm-checklist.md`, `references/emc-guidelines.md`, `references/stackup-and-impedance.md` |
| Choose layers or stackup | `references/stackup-and-impedance.md` | `references/layer-choice.md`, `references/pcb-materials.md` |
| Select components or BOM | `references/component-selection.md` | `references/cost-optimization.md`, `references/mcu-platforms.md` |
| Power design | `references/power-design.md` | `references/thermal-design.md`, `references/protection-reliability.md` |
| RF or antenna | `references/rf-design.md` | `references/emc-guidelines.md`, `references/stackup-and-impedance.md` |
| High-speed interface | `references/high-speed-digital.md` | `references/communication-interfaces.md` |
| Prepare fabrication files | `references/release-checklist.md` | `references/dfm-checklist.md`, `references/manufacturing-production.md` |
| Bring up or debug a board | `references/bringup-and-validation.md` | `references/testing-debug.md` |
| High-reliability or safety context | `references/high-reliability.md` | `references/protection-reliability.md`, `references/compliance-certification.md` |
| Use EasyEDA or KiCad | `references/lceda-workflow.md` or `references/kicad-workflow.md` | Tool-specific project instructions |
| Check sources or standards | `references/standards-and-sources.md` | `rules/design-rules.json` |
| Understand calculator assumptions | `references/calculation-models.md` | `scripts/pcbcalc.py --help` |

Domain references: `power-design.md`, `analog-design.md`, `rf-design.md`,
`high-speed-digital.md`, `communication-interfaces.md`, `thermal-design.md`,
`protection-reliability.md`, `pcb-materials.md`, `mcu-platforms.md`.

## Design Workflow

### Gate 1: Requirements

Capture the inputs that affect architecture and layout:

- function, operating modes, environment, lifecycle, and quantity;
- input power, battery, rails, load profile, and peak current;
- interfaces, voltages, speeds, isolation, and connector exposure;
- mechanical envelope, mounting, cable exit, antenna location, and service access;
- regulatory, reliability, cost, assembly, and test requirements;
- what "done" means and which measurements prove it.

Use `templates/design-brief.md` when the user wants a structured artifact.
If the board is safety-critical or regulated, stop and identify the required
expert review and standards before proposing a schematic.

### Gate 2: Architecture and Schematic

Produce a block diagram and power tree before detailed capture. Assign every
interface and confirm voltage domains. Use the relevant domain references.
Before layout, run ERC and complete `references/schematic-review.md`.

### Gate 3: Stackup, Placement, and Routing

Choose layer count from signal speed, density, EMC risk, and production volume.
Define controlled-impedance targets before routing. Place connectors,
mechanical constraints, power, clocks, RF, and sensitive analog first.
Route with continuous return paths and document intentional exceptions.

### Gate 4: Manufacturing Release

Run the project's DRC with fab-accurate rules. Export Gerber/Excellon, BOM, and
CPL using the current supplier format. Then run:

```bash
python scripts/audit_release.py path/to/release-directory --json
```

Resolve every error and review every warning before ordering. Use
`templates/fab-release-checklist.md`.

### Gate 5: Bring-Up and Validation

Use a current-limited supply or protected battery input. Verify rails before
installing expensive parts. Record power, reset, clock, programming, interface,
thermal, and EMC measurements. Use `templates/bringup-log.md`.

## Severity Model

Use these levels consistently in reviews:

- **Critical**: blocks fabrication, can damage hardware, violates safety, or
  makes required operation impossible.
- **Major**: likely functional failure, low yield, reliability risk, or a
  standards/compliance problem.
- **Minor**: cost, manufacturability, serviceability, or robustness improvement.
- **Question**: missing information that may change the conclusion.

Every finding needs evidence: file/line, schematic net, datasheet section,
measurement, or explicit assumption. If evidence is unavailable, say so.

## Rule Precedence

Use this order:

1. User requirements and applicable safety/regulatory standards.
2. Component datasheet, reference design, and errata.
3. Current fabrication/assembly capability and the chosen stackup.
4. Project-specific design rules.
5. The generic rules in this skill.

Generic numbers are starting points, not guarantees. JLCPCB, PCBWay, OSH Park,
and other suppliers change capabilities and pricing.

## Output Contracts

### New Design

Return:

1. assumptions and blocking questions;
2. block diagram or connection map;
3. power tree and power budget;
4. interface and pin-allocation table;
5. BOM with verification status for every part;
6. stackup, placement, routing, thermal, and test constraints;
7. risk register and next action.

### Design Review

Lead with findings, ordered by severity. For each finding give:

- severity and short title;
- evidence and why it matters;
- concrete fix;
- confidence and any assumption.

Then list open questions. Keep the summary brief and place it last.

### Calculation

State the command, inputs, assumptions, result, and limitation. Calculations
in `scripts/pcbcalc.py` are planning estimates; controlled-impedance and
high-current designs still require the fabricator's stackup or a field solver.

### Manufacturing Release

Report:

- files found and missing;
- DRC/ERC status;
- BOM/CPL consistency;
- stackup and impedance notes;
- unresolved supplier questions;
- go/no-go recommendation with explicit caveats.

## Bundled Tools

```bash
# Deterministic planning calculations
python scripts/pcbcalc.py --help

# Validate Gerber, drill, BOM, and CPL release completeness
python scripts/audit_release.py <release-dir> --json

# Validate this skill before publishing changes
python scripts/validate_skill.py .

# Install for Codex, Claude Code, or a generic Agent Skills directory
python scripts/install.py --target codex
```

`scripts/pcbcalc.py` includes trace and via current estimates, microstrip,
stripline, differential microstrip, LDO thermal checks, battery life, buck
inductor selection, RC filters, and resistor dividers. Treat all results as
engineering estimates and verify critical designs with the supplier or a
field solver.

## Pairing With EasyEDA API

| Skill | Role |
|---|---|
| `pcb-designer` | Design reasoning, calculations, review, and release discipline |
| `easyeda-api` | Live EasyEDA Pro control through its bridge server |

The English product name is **EasyEDA**; the Chinese name is **嘉立创EDA**.
Use the EDA API skill only after reading its instructions and verifying the
active project and document type.

## Maintenance

- Update `metadata.version`, `CHANGELOG.md`, and the README together.
- Keep supplier-specific numbers in `rules/fab-profiles.json`, with a
  `verified_on` date and a source URL.
- Add a regression test for every calculator or audit behavior change.
- Run `python scripts/validate_skill.py .` and
  `python -m unittest discover -s tests -v` before release.
