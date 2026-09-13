# EMC & Signal Integrity Quick Guide

For embedded boards with ESP32, high-speed SPI, and radio.

## Return Paths

**The #1 EMC rule:** Every signal has a return current that follows the path
of least impedance — which at high frequencies is the path directly under the
signal trace.

| Stackup | Return path | Quality |
|---------|------------|---------|
| 2-layer (no GND plane) | Returns wander, find path through GND pour | Poor |
| 4-layer (L2 = GND) | Returns directly under trace on L1 | Excellent |
| 4-layer (L4 = signal, L3 = GND) | Same, but coupling to L3 not L2 | Good |

**Consequence:** A slot or gap in the GND plane forces return currents to
detour, increasing EMI and crosstalk. Avoid cutting the L2 GND plane with
long traces. Use vias to drop signals to L4 if needed, and provide a return
via near the transition.

## Decoupling Capacitors

### Per IC
- Follow the datasheet's required capacitance and placement. A 0.1 uF ceramic
  capacitor is a common starting point, but some rails require a different
  value or a network of values.
- Place the smallest, highest-frequency capacitor as close as practical to the
  power/ground pin pair, with a short return loop.
- Connect cap GND to IC GND pin with short trace, then to GND plane with via

### Bulk
- 10µF–47µF on main 3.3V rail near regulator output
- 10µF on battery input near charger IC

### Layout
```
Good:                            Bad:
 ┌──────┐                        ┌──────┐
 │  IC  │                        │  IC  │
 │VDD GND│                       │VDD GND│
 └──┬─┬──┘                       └──┬──┬─┘
    │ │    ┌───┐                    │  └──────┐
    │ └────┤0.1│                    │         │  ┌───┐
    └──────┤µF │                    └─────────┼──┤0.1│
           └───┘                              └──┤µF │
                                                └───┘
  Cap between VDD & GND,             Long trace to cap =
  short loop area                    large loop = EMI
```

## SPI High-Speed (40 MHz)

### Series Termination
If the source impedance, edge rate, and trace length justify termination,
place the damping resistor at the source (MCU side), as close to the GPIO pin
as possible. Read the interface guidance and measure the actual waveform; not
every SPI bus needs 22 ohm series resistors.

### Length Matching
Match MOSI and SCLK lengths within the same SPI bus to ±2mm.
MISO doesn't need matching (different driver).

### Spacing
- SPI traces: keep >3× trace width spacing from other signals
- Don't run SPI parallel to I2C or UART for >5mm
- Cross at right angles if unavoidable

### Via Count
- Max 1 via per signal on high-speed SPI buses
- Each via adds ~0.5nH inductance and impedance discontinuity

## I2C Crosstalk Prevention

- Route I2C away from SPI SCLK (at least 10× trace width)
- Don't run I2C parallel to PWM signals (LEDs, buzzer)
- I2C is slow (400kHz) but sensitive — pull-ups are weak (4.7kΩ), so noise couples easily

## USB Differential Pairs

- Route D+ and D- as a **differential pair** (equal length, constant spacing)
- Target 90Ω differential impedance
- Keep total length < 50mm from MCU to connector
- Place ESD diodes **at the connector**, not at the MCU
- Shunt ESD current to GND plane with short vias

## Antenna Zone (ESP32)

### Keep-out: 15mm × 15mm × ALL LAYERS

```
Top view:
┌─────────────────────────────┐
│                             │
│  ┌──────────────┐           │
│  │   ESP32-S3   │  ╔══════╗│
│  │   WROOM-1    │  ║ANT   ║│
│  │              │  ║ZONE  ║│
│  └──────────────┘  ║      ║│
│                    ║15×15 ║│
│   ↑ board edge     ║mm    ║│
│                    ╚══════╝│
└─────────────────────────────┘
```

- No copper (not even GND plane) in this zone
- No components, no mounting holes, no battery, no metal
- Antenna faces OUTWARD from board edge

### If using IPEX (external antenna):
- 50Ω microstrip from module to IPEX connector
- Keep microstrip short (< 10mm)
- No components within 3mm of microstrip

## Ground Plane Stitching

```
Board edge stitching:
┌──────────────────────────────────┐
│ ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  │ ← GND vias every 5mm
│                                  │
│                                  │
│ ●                              ● │ ← Corners get vias
│                                  │
│                                  │
│ ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  │
└──────────────────────────────────┘
```

- Place GND stitching vias every 5–10mm along board edges
- More vias near RF sections
- Stitch between top and bottom GND pours, and to inner GND plane

## Quick EMI Smell Test

Before exporting Gerber, check:
- [ ] L2 GND plane has NO long slots or cuts
- [ ] Every VDD pin has decoupling that satisfies the datasheet and is placed
      as close as practical to the pin
- [ ] SPI MOSI/SCLK termination is present when justified, or intentionally
      omitted with a documented signal-integrity reason
- [ ] SPI traces don't run parallel to I2C for >5mm
- [ ] Antenna keep-out zone is clear on ALL layers (no GND plane)
- [ ] USB ESD protection is at the connector, short path to GND
- [ ] No floating copper islands (all pours connected to GND)
- [ ] No traces crossing split planes (with 4L, shouldn't happen)
