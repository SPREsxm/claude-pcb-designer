# Calculation Models

Use this reference to understand what `scripts/pcbcalc.py` does, what it does
not model, and when to escalate to a field solver or measurement.

## Trace Width

The trace-width command uses the IPC-2221-style relation:

```text
I = k * dT^0.44 * A^0.725
```

Where:

- `I` is current in amperes;
- `dT` is conductor temperature rise in degrees Celsius;
- `A` is conductor cross-sectional area in square mils;
- `k` is 0.048 for external conductors and 0.024 for internal conductors.

The command solves for area, then width, applies a user-selected margin, and
estimates resistance and voltage drop at the resulting conductor temperature.

Limitations:

- copper surface roughness and etching tolerance are not modeled;
- adjacent copper, planes, air flow, enclosure, and duty cycle are ignored;
- current sharing between parallel paths is not modeled;
- IPC-2152 or measured data is preferred for critical designs.

## Via Current

The via command estimates the copper barrel cross-section as:

```text
A = pi * hole_diameter * plating_thickness
```

It applies the internal-layer IPC-2221-style relation, then a user-selected
derating factor. The output also estimates DC barrel resistance.

Limitations:

- current sharing between vias is not uniform;
- barrel plating thickness and hole wall quality vary;
- the board thickness and thermal path matter;
- filled/capped vias, plugged vias, and microvias may behave differently.

Do not use this estimate as the only basis for a high-current or safety path.

## Microstrip

The microstrip command uses the Hammerstad-Jensen closed-form model for an
ideal zero-thickness conductor over a ground plane. It returns characteristic
impedance, effective permittivity, and propagation delay.

Limitations:

- solder mask is not modeled;
- copper thickness is not modeled;
- finite ground width and nearby copper are not modeled;
- the stackup's actual dielectric thickness and er must be supplied.

The model is useful for early sizing and for solving a target width. A
controlled-impedance release needs the fabricator's model or a field solver.

## Stripline

The stripline command uses a centered, zero-thickness, symmetric stripline
approximation. It is appropriate for planning, not for final release without
the fabricator's geometry.

## Differential Microstrip

The differential command uses a common edge-coupled planning approximation:

```text
Zdiff = 2 * Z0 * (1 - 0.48 * exp(-0.96 * s/h))
```

Where `Z0` is the single-ended microstrip impedance, `s` is edge-to-edge
spacing, and `h` is dielectric height. It is most useful in the documented
range and should be replaced by the transceiver reference design and the
fabricator's solver for production.

## LDO Thermal

The LDO command uses:

```text
Pd = (Vin - Vout) * Iload
Tj = Ta + Pd * theta_JA
```

It compares junction temperature with the supplied maximum and optionally
checks the input-to-output voltage against dropout.

Use the datasheet's theta JA for the actual package, copper area, airflow, and
mounting. Thermal shutdown and current limit can prevent damage but do not make
an under-designed thermal solution acceptable.

## Battery Life

The battery-life command uses:

```text
runtime = capacity * usable_fraction * derating * efficiency / average_current
```

Every input must represent the real operating profile. Include sleep current,
radio duty cycle, sensor warm-up, regulator quiescent current, self-discharge,
temperature, aging, and cutoff behavior when they matter.

## Buck Inductor

The ideal buck inductor estimate uses:

```text
L = Vout * (Vin - Vout) / (Vin * fsw * delta_I)
```

It reports ideal duty cycle, ripple current, peak current, RMS current, and a
recommended saturation-current target.

It does not model switch drop, diode drop, efficiency, slope compensation, or
controller-specific ripple requirements. Check the controller datasheet before
choosing the final inductor.

## RC Filter and Voltage Divider

These commands use ideal first-order equations. For an RC filter, source and
load impedance, tolerance, leakage, and dielectric behavior can dominate. For
a divider, the load, ADC leakage, resistor voltage rating, and tolerance must
be considered.

## Power Budget

The power-budget command aggregates a CSV with rail, voltage, current, and duty
cycle columns. It treats duty-cycle current as an average estimate. It does
not replace a transient analysis or a regulator stability check.

## Validation Principle

For every important result:

1. run the calculator;
2. compare against the datasheet or supplier model;
3. measure the prototype;
4. record the difference and the design margin.
