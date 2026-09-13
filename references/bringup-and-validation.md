# Bring-Up and Validation

Bring-up is a controlled experiment. Change one thing at a time and preserve
evidence for every failure.

## Before Power

- Do not install expensive or hard-to-source parts for the first power test
  unless the design explicitly supports hot-plug testing.
- Inspect for solder bridges, missing parts, wrong orientation, and shorts
  between every rail and ground.
- Verify the current limit, polarity, and voltage of the source.
- Confirm the board revision and firmware revision.
- Have the schematic, assembly drawing, and net names available.

## First Power

1. Set a conservative current limit based on expected idle current.
2. Apply input voltage and watch current before touching the board.
3. Check input voltage after protection.
4. Check each rail for voltage, ripple, and current draw.
5. Check reset, enable, clock, and boot pins.
6. Confirm the device enters programming or debug mode.
7. Remove power immediately on unexpected heating, smell, or current rise.

Record the result in `templates/bringup-log.md`.

## Functional Bring-Up

### Digital

- read chip IDs and status registers;
- verify reset and boot behavior;
- test every interface at low speed before increasing speed;
- exercise all power states and recovery paths;
- test firmware update and factory reset.

### Analog

- measure reference and supply noise;
- verify offset, gain, and linearity at multiple points;
- check settling after a full-scale step;
- test at temperature and supply extremes when required;
- compare measured noise with the design budget.

### Power and Thermal

- record current in every operating mode;
- measure efficiency and regulator case temperature;
- test at minimum and maximum input voltage;
- test transient load steps;
- run a worst-case soak long enough to reach thermal equilibrium;
- verify battery cutoff, charging, and protection behavior.

### Radio and High-Speed

- verify the antenna matching network and return loss with a VNA;
- measure conducted power and receiver sensitivity with suitable equipment;
- test range in the intended mechanical configuration;
- capture eye diagrams or signal quality where the interface requires it;
- repeat with the enclosure, cables, and battery installed.

## Failure Log

For each failure, record:

```text
Symptom:
Board revision:
Supply/current:
Measurement setup:
Expected vs measured:
Persistence after power cycle:
Last intentional change:
Hypothesis:
Next experiment:
Result:
```

## Exit Criteria

Do not declare bring-up complete until:

- all rails are within tolerance under worst-case load;
- reset, clock, programming, and recovery modes work;
- every required interface passes at the specified speed and cable length;
- thermal limits are respected at maximum ambient;
- all known failure modes are tested or explicitly accepted;
- the design, BOM, firmware, and test records agree;
- the next reviewer can reproduce the result from the recorded evidence.
