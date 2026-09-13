# High-Reliability and Safety-Critical Boards

This reference is for designs used in aerospace, launch vehicles, industrial
control, medical equipment, automotive systems, or other environments where a
single failure can cause harm or loss of mission.

This is not a substitute for the applicable standard or a qualified reviewer.
Always identify the controlling documents and approval authority first.

## Start With the Standard

Examples include:

- IPC-2221/IPC-2222 for generic and rigid-board design;
- IPC-6012 for rigid-board qualification;
- IPC-A-610 and J-STD-001 for assembly acceptance and soldering;
- DO-160 or equivalent for airborne environmental testing;
- ISO 26262/IATF expectations for automotive functional safety;
- IEC 62368-1 for safety in audio/video, IT, and communication equipment;
- IEC 60601 for medical electrical equipment;
- ECSS or NASA workmanship documents for space missions.

The project owner must identify the actual revision, class, and evidence
requirements. Do not claim compliance from a generic checklist.

## Reliability Design Practices

- Define mission-critical functions and single points of failure.
- Derate voltage, current, power, temperature, and mechanical stress.
- Partition high-current, high-voltage, RF, analog, and digital domains.
- Protect every externally accessible conductor against ESD and fault current.
- Define safe behavior for brownout, reset, clock loss, sensor failure, and
  firmware lock-up.
- Use watchdog, brownout, CRC, redundant sensing, or voting only where the
  system analysis shows they help.
- Specify trace and connector margins for the worst-case temperature, not the
  room-temperature prototype.
- Consider tin whiskers, conformal coating, potting, outgassing, and material
  compatibility when the environment requires it.
- Keep a complete manufacturing and inspection record.

## Environmental and Mechanical Stress

### Vibration and Shock

- Avoid long unsupported component bodies and heavy parts on small pads.
- Use staking, adhesive, brackets, or mechanical retention for large parts.
- Keep the board's first mode above the expected excitation range when
  practical.
- Use mounting points that do not create large unsupported panels.
- Verify connector retention and cable strain relief.

### Thermal Cycling

- Match CTE where possible and avoid rigidly constraining large packages.
- Place thermal vias and copper symmetrically where they affect warpage.
- Keep vias out of high-stress bend zones unless reliability data supports them.
- Validate solder-joint fatigue for wide-temperature missions.

### Contamination and Moisture

- Define cleaning, no-clean, coating, masking, and rework requirements.
- Keep high-impedance nodes away from flux, ionic contamination, and moisture.
- Provide conformal-coating keep-outs around connectors and test points.
- Verify that potting does not crack components or trap heat.

## Power and Fault Analysis

Analyze:

- input reverse polarity, overvoltage, undervoltage, and transient surge;
- single-component short and open failure modes;
- stuck-at and floating control paths;
- battery overcharge, overdischarge, overcurrent, and thermal runaway;
- connector mis-mating and hot unplug;
- external cable short to supply, ground, or another conductor;
- loss of the primary clock, reference, or communication bus;
- thermal runaway caused by a failed regulator or shorted load.

Document mitigation, detection, and safe-state behavior for each credible fault.

## Assembly and Verification Class

Class 3 or equivalent assembly requirements change:

- annular ring and hole-wall quality;
- solder-joint acceptance;
- inspection and traceability;
- rework limitations;
- conformal-coating and cleanliness requirements;
- documentation and nonconformance handling.

Do not mix Class 1, 2, and 3 language in one release package without stating the
applicable section and the reason.

## Evidence Package

For a high-reliability release, retain:

- approved requirements and assumptions;
- schematic and layout revision history;
- stackup, material, and process records;
- component qualification and derating data;
- DRC/ERC and manufacturing records;
- thermal, vibration, EMC, and functional test reports;
- failure analysis and corrective actions;
- approved deviations and waivers;
- final inspection and traceability records.
