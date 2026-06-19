# PCB Materials & Advanced Processes

## FR-4 Substrate

### Standard vs High-Tg
| Property | Standard FR-4 | High-Tg FR-4 |
|----------|:---:|:---:|
| Tg (glass transition) | 130-140°C | 170-180°C |
| Td (decomposition) | 300°C | 350°C |
| εr @ 1GHz | 4.2-4.6 | 4.0-4.4 |
| Tan δ @ 1GHz | 0.02 | 0.015-0.02 |
| Lead-free compatible | Borderline | ✓ |
| Cost multiplier | 1× | 1.3-1.5× |

**Use high-Tg for**: lead-free assembly, automotive, any design with >2 reflow cycles.

### JLCPCB Stackup Options
```
JLC2313 (2L, 1.6mm, 1oz):     JLC7628 (4L, 1.6mm, 1oz):
─────────────────────          ─────────────────────
L1: 1oz Cu                     L1: 1oz Cu + plate
Core: 1.5mm                    Prepreg: 0.2mm
L2: 1oz Cu                     L2: 0.5oz Cu
                               Core: 0.5mm
                               L3: 0.5oz Cu
                               Prepreg: 0.2mm
                               L4: 1oz Cu + plate
```

---

## High-Frequency Materials

### When to Upgrade from FR-4
| Application | Min Material | Why |
|-------------|-------------|-----|
| WiFi/BLE 2.4GHz | FR-4 (OK) | Short traces, pre-certified module |
| 5GHz WiFi | FR-4 (marginal) | Higher loss, tighter impedance |
| LoRa 868/915MHz | FR-4 (OK) | Sub-GHz, tolerant |
| mmWave (>24GHz) | Rogers | FR-4 loss too high |
| Satellite comms | Rogers/Isola | Phase stability over temperature |
| Precision RF test | Rogers | Consistent εr over frequency |

### High-Frequency Material Comparison
| Material | εr | Tan δ | Tg | 4L Cost |
|----------|:---:|:---:|:---:|:---:|
| FR-4 (standard) | 4.4 | 0.02 | 130°C | ¥30 |
| FR-4 (high-Tg) | 4.2 | 0.018 | 170°C | ¥45 |
| Rogers 4350B | 3.48 | 0.0037 | 280°C | ¥300 |
| Isola IS680 | 3.0 | 0.003 | 200°C | ¥200 |
| Panasonic Megtron 6 | 3.6 | 0.002 | 210°C | ¥250 |

---

## Surface Finishes

### Finish Comparison
| Finish | Shelf Life | Solderability | Flatness | Wire-bondable | Lead-free | Cost |
|--------|:---:|:---:|:---:|:---:|:---:|:---:|
| **HASL (SnPb)** | 12mo | Excellent | Poor | ✗ | ✗ | ¥ |
| **HASL (无铅)** | 12mo | Good | Poor | ✗ | ✓ | ¥ |
| **ENIG** | 12mo | Excellent | Excellent | ✓ | ✓ | ¥¥ |
| **ENEPIG** | 12mo | Excellent | Excellent | ✓ | ✓ | ¥¥¥ |
| **OSP** | 6mo | Good | Excellent | ✗ | ✓ | ¥ |
| **Immersion Ag** | 6mo | Good | Excellent | ✓ | ✓ | ¥¥ |
| **Immersion Sn** | 6mo | Good | Excellent | ✗ | ✓ | ¥¥ |
| **Hard Gold** | 24mo | Good | Excellent | ✓ | ✓ | ¥¥¥¥ |

### Recommendation by Application
```
Consumer / IoT (budget):     HASL (无铅)
Consumer / IoT (quality):    ENIG
Prototype (fast turnaround): HASL (has shorter fab queue)
RF / precision analog:        ENIG (flat, consistent impedance)
Fine-pitch BGA/QFN:          ENIG or OSP (flat pads)
Edge connectors:              Hard Gold (durability)
```

---

## Copper Weight

### Thickness Options
| oz | µm | mil | Use |
|:---:|:---:|:---:|-----|
| 0.5oz | 17.5 | 0.7 | Inner layers (4L) |
| 1oz | 35 | 1.4 | Standard outer layers |
| 2oz | 70 | 2.8 | High current, improved thermal |
| 3oz | 105 | 4.2 | Power boards |
| 4oz+ | 140+ | 5.6+ | Very high current |

### Trace Width vs Current (1oz, 10°C rise)
```
500mA  → 15mil  (0.38mm)
1A     → 30mil  (0.76mm)
2A     → 70mil  (1.78mm)
3A     → 120mil (3.05mm)
5A     → 250mil (6.35mm) → use copper pour
```

---

## Advanced PCB Processes

### Blind & Buried Vias (HDI)

**Blind Via (L1→L2)**
```
L1 ──●──  (visible from top, drill stops at L2)
L2 ──●──
L3 ─────  (no via on L3, L4)
L4 ─────
```
Laser-drilled microvia (0.1mm hole typical).

**Buried Via (L2→L3)**
```
L1 ─────  (not visible from either surface)
L2 ──●──
L3 ──●──
L4 ─────
```
Drilled before lamination.

### Microvia (HDI)
- **Laser-drilled**: 0.075-0.15mm hole
- **1:1 aspect ratio**: depth ≤ diameter
- **Stacked**: multiple blind vias on top of each other
- **Staggered**: offset blind vias (more reliable)
- Used for: BGA fanout, high-density routing

### Via-in-Pad
```
┌─────┐
│ ██  │  ← Solder pad
│  ○  │  ← Via (filled + capped)
└─────┘
```
- Via drilled, plated, filled (epoxy or Cu), capped (plated flat)
- Allows via directly in BGA pad → saves space
- More expensive: ¥100-300 extra per design

---

## Flexible & Specialty PCBs

### Flexible PCB (FPC)
- Polyimide base (not FR-4)
- 1-2 layers typical (can be multi-layer)
- Can bend, fold, or flex repeatedly
- Lower εr (3.2-3.5) than FR-4
- Connector: ZIF (Zero Insertion Force) or hot-bar soldered

### Rigid-Flex
```
─── FR-4 ───┬─── Polyimide flex ───┬─── FR-4 ───
            │                     │
      Rigid-to-flex transition
```
- Combines rigid and flexible sections
- No connectors between rigid sections
- Complex, expensive, long lead time
- Used for: wearables, folding products, aerospace

### Metal-Core PCB (MCPCB)
- Aluminum or copper base instead of FR-4
- Single layer Cu on top, dielectric, then metal core
- **Excellent** thermal performance
- Used for: high-power LEDs, power supplies
- Can't do multi-layer easily

### Heavy Copper PCB
- 4-20oz Cu
- Used for: power distribution, bus bars, welding equipment
- Special etching, wider trace/space minimums

---

## Solder Mask Colors

| Color | Properties | Notes |
|-------|-----------|-------|
| **Green** | Standard, best resolution | Best for fine pitch |
| **Blue** | Good resolution | Popular for dev boards |
| **Red** | Good resolution | Popular for OSH Park |
| **Black** | Lower resolution, harder to inspect | Looks premium |
| **White** | Lower resolution, reflects light | LED boards |
| **Yellow** | Good resolution | Retro aesthetic |
| **Matte Black** | Hardest to inspect, fingerprints | Premium look only |

**Recommendation**: Green for production, any color for prototypes.
Black is harder to rework (hard to see traces).

---

## Silkscreen

### Printing Methods
| Method | Resolution | Durability | Cost |
|--------|:---:|:---:|------|
| Ink-jet | Good | Good | ¥ |
| Screen printing | Fair | Excellent | ¥ |
| LPI (photo-imageable) | Excellent | Good | ¥¥ |

### Design Guidelines
```
Minimum text height: 0.8mm (readable), 1.0mm (recommended)
Minimum line width: 0.15mm (0.2mm recommended)
Clearance to pads: ≥0.2mm
Font: sans-serif, no thin strokes
```
