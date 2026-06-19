# High-Speed Digital Design

Applies when signal rise time tr < 2× propagation delay (roughly >50MHz clock or tr < 1ns).

## Impedance Control

### Single-Ended
| Impedance | Application |
|:---:|------------|
| 40Ω | DDR3/DDR4 address |
| 50Ω | RF, general high-speed, DDR3 data |
| 60Ω | DDR2 data, some memory interfaces |

### Differential
| Impedance | Application |
|:---:|------------|
| 85Ω | PCIe (some) |
| 90Ω | USB 2.0/3.0 |
| 100Ω | Ethernet MDI, LVDS, MIPI, HDMI |

### Impedance Calculator Factors
- Trace width (wider = lower Z)
- Dielectric thickness h (thinner = lower Z)
- εr of substrate (higher εr = lower Z)
- For differential: spacing s (closer = lower Zdiff)

**Use Saturn PCB Toolkit or your fab's impedance calculator. Never guess.**

---

## Crosstalk Control

### 3W Rule (Minimum)
```
Trace-to-trace spacing ≥ 3 × trace width
Example: 6mil trace → 18mil spacing minimum
```

### 5W Rule (Recommended)
```
Spacing ≥ 5 × trace width for critical signals
6mil trace → 30mil spacing
```

### Guard Traces
```
GND ── gap ── AGGRESSOR ── gap ── GUARD ── gap ── VICTIM
```
- Guard trace between aggressor and victim
- Connected to GND with vias every λ/10
- Effective for parallel runs >10mm

### Layer Adjacency
```
Good:                          Bad:
L1: ──── HiSpeed ────          L1: ──── HiSpeed ────
L2: GND PLANE                  L2: ──── HiSpeed ────  ← PARALLEL = BAD
L3: ──── LoSpeed ────          L3: GND PLANE
```
Crucial: orthogonally route adjacent signal layers to minimize coupling.

---

## Length Matching

### Matching Rules
| Signal Group | Tolerance | Notes |
|-------------|:---:|-------|
| DDR data byte lane | ±5mil | Within same byte group |
| DDR address/command | ±25mil | Group match |
| SPI bus (MOSI/SCLK) | ±2mm (80mil) | Same bus only |
| USB D+/D- | ±5mil | Differential pair |
| LVDS pair | ±5mil | Within pair |
| HDMI TMDS pair | ±5mil | Within pair |
| MIPI D-PHY lane | ±5mil | Within lane |

### Serpentine Tuning
```
 ┌──┐ ┌──┐
─┘  └─┘  └──     ← Longer trace gets serpentine to match shorter trace
```
- Amplitude: 3× trace width minimum
- Spacing between serpentine sections: 3× trace width
- Place serpentine near the shorter trace's end, not randomly

---

## DDR Routing

### DDR3/DDR4 Topology

**Address/Command/Control: Fly-by**
```
MCU ──┬── Chip0 ──┬── Chip1 ──┬── Vtt termination
      │            │            │
      └── Resistor packs to Vtt
```
- Series term at driver, parallel term (Vtt) at end
- Route in daisy chain, matched to ±25mil

**Data: Point-to-Point**
```
MCU ──────────────────── DRAM
      DQ[0:7] ±5mil match per byte lane
      DQS ±5mil to DQ
      DM ±5mil to DQ
```
- DQS strobe: matched to its byte lane within ±5mil
- Layer: route entire byte lane on same layer

### Vref
- Vref = VDD/2
- Wide trace (20mil+), decoupled with 0.1µF + 1µF
- Keep away from noisy signals
- Tie to GND with 0.1µF at each DRAM

---

## Via Effects

### Via Stub
```
Signal ──┬── L1
         │
         ├── L2 (connected)
         │
         │   ← STUB: unused via barrel below L2 acts as antenna
         │      Causes null at λ/4 resonant frequency
         │
         └── L4 (unused end)
```

### Stub Impact by Data Rate
| Data Rate | Stub Length | Issue? |
|-----------|:---:|:---:|
| ≤1Gbps | Any | Minimal |
| 1-5Gbps | <1mm | OK |
| 5-10Gbps | <0.5mm | Required |
| >10Gbps | 0mm | Must back-drill or use blind via |

### Via Transition
- Each via adds ~0.5nH inductance
- Add GND vias near signal vias for return path
- For differential: symmetrical vias for both lines

---

## Clock Distribution

### Crystal Oscillator Layout
```
             ┌─────┐
XTAL_IN ─────┤     ├──── XTAL_OUT
             │ MCU │
             └─────┘
             │     │
            ┌┴┐   ┌┴┐
            │ │   │ │ C1, C2 (load caps)
            └┬┘   └┬┘
             │     │
         ┌───┴──┬──┴───┐
         │ XTAL │      │
         └──────┘      │
                       │
              GND GUARD RING
```
- XTAL + load caps as close as possible to MCU
- GND guard ring around crystal circuit
- No high-speed traces under or near crystal
- CL = (C1×C2)/(C1+C2) + Cstray (usually CL from datasheet)

### Clock Buffer / Fan-out
- Series termination (22-33Ω) at each output
- Keep clock traces away from data and I2C
- Length-match clock to its data group

---

## High-Speed Checklist

Before layout:
- [ ] Stackup defined with controlled impedance (fab to calculate trace widths)
- [ ] All high-speed signals identified and grouped
- [ ] Reference planes continuous under all high-speed traces

Before routing:
- [ ] Impedance requirements known (50Ω single, 90/100Ω diff)
- [ ] Length matching tolerances documented
- [ ] Via budget: max 2 vias per high-speed net
- [ ] No traces crossing plane splits

Before export:
- [ ] All differential pairs length-matched within tolerance
- [ ] All bus groups matched within tolerance
- [ ] Serpentine tuning follows 3W×3W rule
- [ ] Return vias near all signal layer transitions
