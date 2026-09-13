# Fabrication Release Checklist

Use this checklist before sending a board to fabrication or assembly. The goal
is a release package another person can reproduce without reading the designer's
mind.

## 1. Source and Revision Control

- [ ] Schematic, PCB, library, and BOM revisions agree.
- [ ] The released Git tag or commit is recorded.
- [ ] Temporary test changes are removed or explicitly documented.
- [ ] The board name, revision, and date appear on the silkscreen.
- [ ] DNP and assembly-variant rules are documented.

## 2. Design Rule Check

- [ ] ERC completed with no unexplained errors.
- [ ] DRC completed with no unexplained errors.
- [ ] DRC rules match the selected fabricator and stackup.
- [ ] Differential-pair and impedance rules match the selected interfaces.
- [ ] Copper-to-edge, hole-to-edge, and slot clearances pass.
- [ ] All nets are routed; intentional stubs are documented.

## 3. Gerber and Drill

- [ ] Gerber format is RS-274X or the format requested by the fabricator.
- [ ] Units and coordinate format are explicit.
- [ ] Board outline is on the correct mechanical/outline layer.
- [ ] All copper, mask, paste, silkscreen, and mechanical layers are included.
- [ ] Drill file is Excellon or the requested format.
- [ ] Plated and non-plated holes are distinguished.
- [ ] Gerbers open in an independent viewer and align with the drill and outline.
- [ ] No unintended artifacts, hidden text, or design notes are present.

## 4. Stackup and Impedance

- [ ] Layer count, thickness, copper weight, and material are specified.
- [ ] Controlled-impedance traces are identified in a fab drawing.
- [ ] The impedance target has a tolerance.
- [ ] The fabricator confirmed the stackup or supplied a test coupon.
- [ ] The final geometry matches the model used for width and gap.

## 5. BOM

- [ ] Every assembled designator appears exactly once.
- [ ] DNP parts are marked and excluded from assembly.
- [ ] Manufacturer part number, package, and quantity are present.
- [ ] Supplier part number is present when required by the assembler.
- [ ] Critical parts are verified against the exact datasheet and inventory.
- [ ] No placeholder values, obsolete parts, or ambiguous variants remain.
- [ ] Substitution rules and acceptable alternates are documented.
- [ ] Polarized and orientation-sensitive parts are identified.

## 6. CPL / Pick-and-Place

- [ ] Every assembled part appears exactly once.
- [ ] Designators match the BOM.
- [ ] X/Y units and coordinate origin match the assembler's template.
- [ ] Rotation values were checked against the assembler's part library or a
  known-good board.
- [ ] Top and bottom side are correct.
- [ ] Fiducials and panel orientation are correct.

## 7. Assembly and Test

- [ ] Paste apertures and stencil thickness fit the smallest pitch.
- [ ] Courtyard and component spacing allow placement and inspection.
- [ ] Fiducials are present where required.
- [ ] Test points are accessible after assembly.
- [ ] Programming and recovery access is available.
- [ ] Connector orientation and cable clearance are checked in 3D.
- [ ] Thermal relief and thermal vias are correct for the assembly process.

## 8. Order Package

- [ ] Gerber/drill archive is complete and has a stable name.
- [ ] BOM file uses the assembler's required columns.
- [ ] CPL file uses the assembler's required columns.
- [ ] Fab drawing includes stackup, finish, color, thickness, and tolerances.
- [ ] Assembly notes describe DNP, orientation, and special processes.
- [ ] The order quantity, board dimensions, and layer count are correct.
- [ ] A human reviewer signed off on safety and compliance items.

## Automated Audit

Run:

```bash
python scripts/audit_release.py path/to/release --json
```

The audit checks for common missing-file and table-consistency failures. It
cannot prove that a Gerber is electrically correct or that a fabrication
process will yield.
