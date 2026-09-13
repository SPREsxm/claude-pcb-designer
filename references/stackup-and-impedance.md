# Stackup and Impedance

Choose a stackup from electrical, mechanical, manufacturing, and cost
requirements. A layer count alone does not guarantee performance; plane
continuity and return-current design do.

## Layer-Count Decision

| Requirement | 2-layer starting point | 4-layer starting point | 6-layer starting point |
|---|---|---|---|
| Low-speed MCU, low density | Usually adequate | Optional | Usually unnecessary |
| ESP32-class radio with PCB antenna | Possible with careful grounding | Strong preference | Optional |
| USB high-speed, fast SPI, RMII | Difficult to control | Strong preference | Useful for dense routing |
| DDR, MIPI, PCIe, gigabit Ethernet | Not adequate | Often inadequate | Usually required |
| Precision mixed-signal | Difficult without planes | Better with solid reference | Better with separate analog/digital regions |
| Harsh EMC environment | High risk | Recommended | Consider shielding and more planes |
| Lowest prototype cost | Best starting point | Higher cost | Highest cost |

At production volume, the per-board cost difference may be smaller than the
cost of re-spins, EMC fixes, or field failures.

## Stackup Templates

These are starting points. Keep the order and naming explicit in the fab
drawing.

### Two Layers

```text
L1  Signal, components, local power
L2  Ground pour plus short signal jumps
```

Use a continuous bottom ground pour, avoid long slots, and keep high-speed
signals on top over solid ground. Two layers can work for many MCU boards, but
return paths need deliberate layout.

### Four Layers: Signal / Ground / Power / Signal

```text
L1  Signal and components
L2  Continuous ground reference
L3  Power plane or slow signals
L4  Signal and ground fill
```

This is the common low-risk four-layer arrangement. L1 has excellent L2
reference. L4 references L3; if L3 is a power plane, it must be continuous and
well decoupled to ground at high frequency. Route critical L4 signals over
continuous L3 copper.

### Four Layers: Signal / Ground / Signal / Power

```text
L1  Signal and components
L2  Continuous ground reference
L3  Signal
L4  Power plane and ground fill
```

Useful when more routing space is needed, but L3 return paths need care and
the bottom power plane may be less convenient for assembly/thermal spreading.

### Six Layers

```text
L1  Signal / components
L2  Ground
L3  Signal
L4  Power
L5  Ground
L6  Signal
```

Use adjacent ground layers to isolate high-speed routing and improve EMC.
Exact ordering depends on the fabricator's symmetrical build.

## Controlled Impedance

Common targets:

| Interface | Target | Notes |
|---|---:|---|
| General RF and single-ended high-speed | 50 ohm | Confirm with the actual stackup |
| USB 2.0 high-speed | 90 ohm differential | Keep symmetry and avoid stubs |
| Ethernet MDI | 100 ohm differential | Follow PHY/magnetics reference design |
| LVDS/MIPI/HDMI-class differential | 100 ohm differential | Verify protocol-specific limits |

Absolute impedance depends on trace width, copper thickness, dielectric
thickness, dielectric constant, solder mask, and the reference plane. A generic
width table is not a substitute for the fabricator's model.

Use the planning calculator:

```bash
python scripts/pcbcalc.py microstrip --width-mm 0.20 --height-mm 0.20 --er 4.3
python scripts/pcbcalc.py stripline --width-mm 0.18 --height-mm 0.30 --er 4.3
python scripts/pcbcalc.py diff-microstrip --width-mm 0.18 --spacing-mm 0.18 --height-mm 0.20 --er 4.3
```

The calculator uses ideal zero-thickness closed-form models. It is useful for
screening and sanity checks, not for a controlled-impedance release.

## Reference Plane Rules

- The return current follows the path of least impedance, usually directly
  under the signal at high frequency.
- Do not route a critical signal across a plane split, void, connector cutout,
  or dense via field.
- Add a ground return via near every signal via on a high-speed net.
- Use symmetric via transitions for differential pairs.
- Keep the reference plane continuous under crystals, clocks, RF, USB, and
  converter feedback nodes.
- If a reference plane must change, provide a low-inductance return path close
  to the transition.

## Differential Pair Rules

- Define the target differential impedance before choosing width and gap.
- Keep the two traces the same layer, length, width, and environment.
- Tune intra-pair skew before pair-to-pair skew.
- Do not widen the gap to route around a via if it breaks symmetry; move the
  obstruction instead.
- Avoid unnecessary layer transitions and test-point stubs.
- Terminate according to the interface standard and transceiver datasheet.

## Plane and Via Design

- Use enough stitching vias to keep plane impedance low without creating slots.
- Stitch around high-speed interfaces, RF sections, connector returns, and
  board edges as appropriate.
- Verify antipads and clearance against the fab profile.
- Thermal pads need a via array sized for both electrical and thermal current.
- Via-in-pad requires filling and capping; do not leave open vias under a BGA.

## Fabricator Questions

Ask the fabricator for:

- controlled-impedance stackup and recommended trace geometry;
- dielectric material, prepreg/core thickness, and tolerance;
- copper weights and finished outer copper;
- minimum trace/space, drill, annular ring, and via pad;
- solder-mask and silkscreen capabilities;
- impedance test coupon availability;
- panel size, array rules, and assembly constraints.

Record the answers in `rules/fab-profiles.json` with a verification date.
