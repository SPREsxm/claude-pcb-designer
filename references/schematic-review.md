# Schematic Review

Review the schematic as a system before checking layout details. Findings must
be tied to a net, component, datasheet section, or explicit assumption.

## 1. Power

- Input protection, reverse polarity, overcurrent, overvoltage, and inrush.
- Rail voltage, tolerance, current, ripple, sequencing, and startup behavior.
- Regulator dropout, thermal dissipation, loop stability, and compensation.
- Every power pin connected to the intended rail and decoupled as specified.
- Unused pins terminated per datasheet, not merely marked "NC."
- Power-good, reset, watchdog, and brownout behavior defined.
- Battery charging, protection, balancing, temperature sensing, and transport
  requirements addressed.

## 2. Grounding and Reference

- Ground strategy is intentional and consistent with the stackup.
- Analog and digital return paths are not mixed blindly.
- High-current returns do not share sensitive reference paths.
- Connector shields and chassis grounds have a defined connection strategy.
- Isolated domains preserve creepage, clearance, and barrier integrity.

## 3. Digital and Interfaces

- Logic levels and direction are compatible at every boundary.
- Pull-ups, pull-downs, series termination, and bus capacitance are correct.
- Strapping, boot, reset, and mode pins have the required state at reset.
- Clock sources, PLL supplies, and jitter requirements are satisfied.
- Unused inputs are not floating; outputs do not fight each other.
- Hot-plug, partial-power, and back-power paths are analyzed.

## 4. Analog and Sensors

- Input range, common-mode range, reference, gain, and offset are correct.
- Anti-alias filter bandwidth and ADC drive settling are adequate.
- Noise, leakage, bias current, and temperature drift are budgeted.
- Kelvin connections are used for current sense and low-level measurements.
- Sensor orientation and mechanical alignment are represented correctly.

## 5. Radio and High-Speed

- Antenna type matches the module certification and mechanical design.
- RF path, matching network, and connector are compatible with the stackup.
- Differential pairs have the required impedance and termination.
- Length matching, return vias, layer transitions, and stubs are controlled.
- Interface power, reference clock, reset, and configuration pins are complete.

## 6. Testability and Manufacturability

- Programming and debug access is available on the assembled board.
- Critical rails, ground, reset, boot, and communication lines have test access.
- Reference designators, polarity, and pin-1 indicators are not ambiguous.
- DNP options and alternate configurations are documented.
- The BOM has no placeholder, obsolete, or unverified production parts.

## 7. ERC and Netlist

- ERC is clean or every suppression has a written justification.
- No unintended single-node nets, power conflicts, or unconnected pins.
- No hidden power pins, alternate pin functions, or symbol-pin mismatches.
- Net names are consistent and do not rely on undocumented assumptions.

## Review Output

Return findings in severity order:

```text
[Critical] U3 VDDIO is connected to 5 V; datasheet maximum is 3.6 V.
Evidence: U3 datasheet section 6.1; net +5V.
Impact: permanent damage on power-up.
Fix: move U3 VDDIO to +3V3 and verify level compatibility on all I/O.
Confidence: high.
```

If the schematic is unavailable, say which checks are impossible instead of
pretending to inspect it.
