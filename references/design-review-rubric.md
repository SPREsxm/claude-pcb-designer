# Design Review Rubric

Use this reference for layout review, pre-fabrication review, or a formal
design audit. Findings lead the answer. Summaries come last.

## Review Evidence Ladder

Prefer evidence in this order:

1. measured data or a reproducible simulation;
2. exact component datasheet, errata, or reference design;
3. fabricator stackup and current capability page;
4. applicable standard or regulatory requirement;
5. project-specific rule;
6. generic engineering heuristic.

When only a heuristic is available, label it as such and state the confidence.

## Review Sequence

### 1. Manufacturing Blockers

- Board outline closed, unambiguous, and on the correct layer.
- Copper-to-edge, hole-to-edge, slot, and routed-feature clearances.
- Minimum trace, space, drill, annular ring, and solder-mask capability.
- All nets routed; DRC errors and warnings explained.
- Pads, mask openings, paste openings, and thermal reliefs manufacturable.
- Fiducials, panelization, tooling, and assembly orientation work.
- BOM and CPL match the design and contain no placeholders.

### 2. Power and Thermal

- Current path width, copper weight, via count, connector rating, and fuse margin.
- Regulator dropout, stability, inrush, and transient response.
- Power dissipation, copper area, thermal vias, and ambient inside the enclosure.
- Hot components not coupled into temperature-sensitive parts.
- Battery protection, charging, discharge cutoff, and fault behavior.

### 3. Return Paths and Signal Integrity

- Every high-speed signal has a continuous reference plane.
- No critical trace crosses a plane slot, split, void, or connector boundary.
- Layer transitions have nearby return vias.
- Differential pairs preserve impedance, symmetry, and intra-pair skew.
- Clocks, switching nodes, RF, and sensitive analog are physically separated.
- Termination is placed at the correct end for the topology.

### 4. EMC and Immunity

- Switching loops, rectifier loops, and hot loops are minimized.
- Input/output cables are filtered or protected as required.
- Ground stitching follows the intended current flow.
- Board-edge radiation and cable-driven radiation are considered.
- ESD current has a short, wide path to the intended return.
- Shield, chassis, and enclosure interfaces are defined.

### 5. Mechanical and Environmental

- Connectors are accessible with mating and cable-bend clearance.
- Mounting hardware, screw heads, and enclosure ribs do not collide.
- Board flex, vibration, shock, and stack-up height are controlled.
- Antenna keep-out includes copper, metal, battery, fasteners, and enclosure.
- Coating, potting, cleaning, and thermal interfaces do not block test access.

### 6. Test, Debug, and Service

- Rails and ground can be measured without shorting adjacent pins.
- Programming, recovery, and debug modes remain reachable.
- Test points match fixture pitch, probe type, and board side.
- Critical signals are labeled and not hidden under tall components.
- Rework and replacement paths exist for expensive or failure-prone parts.

### 7. Compliance and Lifecycle

- Applicable standards and certification path are identified.
- Creepage, clearance, isolation, fusing, and safety barriers are verified.
- Component temperature, voltage, current, and lifecycle derating are documented.
- Obsolescence, second source, and end-of-life risk are acceptable.
- Manufacturing and test documentation is complete enough to reproduce the board.

## Severity Assignment

| Severity | Test |
|---|---|
| Critical | Would stop fabrication, damage hardware, violate safety, or make the required function impossible |
| Major | Likely failure, intermittent behavior, low yield, reliability risk, or compliance risk |
| Minor | Cost, robustness, serviceability, or documentation improvement |
| Question | Missing fact that could change severity or conclusion |

Do not inflate preferences into critical findings. Aesthetic suggestions stay
minor unless they create a real manufacturing or usability failure.

## Finding Format

```text
[Major] Return path is broken under USB_D+
Evidence: U1 pin 12 routes across the L2 GND slot at the connector zone.
Impact: high-speed return current detours, increasing emissions and jitter.
Fix: move the connector ground via field or reroute the pair over continuous L2.
Confidence: high from the supplied layout image and net names.
```

## Review Summary

After the findings, report:

- number of findings by severity;
- files and revisions reviewed;
- what could not be verified;
- whether the design is ready for the next gate.

Never say "looks good" without listing the checks performed and the residual
uncertainty.

## Review Limits

A visual review cannot prove impedance, thermal performance, EMC compliance,
or safety. State which items require measurement, simulation, a fabricator
stackup, or a qualified reviewer.
