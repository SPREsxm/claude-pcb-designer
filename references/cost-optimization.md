# PCB Cost Optimization

Reduce BOM, PCB fabrication, and assembly costs without compromising quality.

---

## BOM Cost Reduction

### 1. Use LCSC Basic Parts
- JLCPCB charges **¥3/part surcharge** for extended library parts
- ~20,000 basic parts available — start here before searching extended
- **Impact**: 30 components × ¥3 = ¥90 saved per board

### 2. Minimize Unique Component Values
```
Before (bad):                    After (good):
R1: 10kΩ, R2: 4.7kΩ, R3: 22kΩ   R1: 10kΩ, R2: 10kΩ, R3: 10kΩ
C1: 0.1µF, C2: 1µF, C3: 2.2µF   C1: 0.1µF, C2: 0.1µF, C3: 0.1µF
                                 (consolidate to fewer unique values)
```
- Fewer unique values = fewer feeder slots on PnP machine = faster setup
- Better volume pricing on each reel
- **Impact**: ¥50-200 saved on assembly setup (small batch)

### 3. Standardize Package Sizes
- 0603 passives: cheapest overall for JLCPCB assembly
- 0402: cheaper parts, but assembly yield slightly lower
- 0805: more expensive parts, but easier hand-solder rework
- Pick ONE size for all passives where possible

### 4. Remove Non-Critical Components
Ask for each component: "What happens if we remove it?"
- Status LEDs (use the MCU's built-in LED or UART for status)
- Extra test points (keep minimum: GND, 3V3, TX, RX)
- Optional filter capacitors (start unpopulated, add if needed)
- Redundant pull-ups (one 4.7kΩ per I2C bus, not one per device)
- Fancy connectors (USB micro is ¥0.5, USB-C is ¥2 — worth it?)

### 5. Source Alternatives
| Original | Alternative | Savings |
|----------|------------|:---:|
| TI / Analog Devices IC | Chinese equivalent (when available) | 30-70% |
| Name-brand passives (Murata, TDK) | Samsung, Yageo, Walsin | 20-50% |
| Gold-plated connectors | Tin-plated (for internal connections) | 30-50% |

---

## PCB Fabrication Cost Reduction

### 1. Panel Utilization — The #1 Cost Driver
```
Board: 50×35mm
Single board area: 1,750mm²

Panel 100×100mm (JLCPCB's cheapest):
- Without optimization: maybe 3 boards/panel
- With tight packing (2mm gap): up to 5 boards/panel
→ Cost per board drops 40%

Rotate boards, pack tight, use V-cut (cheaper than router).
```

### 2. Layer Count
| Layers | 5pcs (50×50mm) | 100pcs |
|:---:|:---:|:---:|
| 2L | ~¥5 | ~¥80 |
| 4L | ~¥35 | ~¥350 |
| 6L | ~¥80 | ~¥900 |

Stay 2L if: slow MCU, no RF, no high-speed, prototype only
Go 4L if: ESP32/RF, SPI >20MHz, production, EMC important

### 3. Board Size
- JLCPCB's cheapest tier: ≤100×100mm
- If your board is 105×60mm → shrink by 5mm in one dimension → save 30-50%
- Tighten layout, use smaller packages, remove empty board space

### 4. Material Choices
| Choice | Cost vs Baseline |
|--------|:---:|
| Standard FR-4, 1.6mm, 1oz, green solder mask | Baseline |
| High-Tg FR-4 | +30-50% |
| 2oz copper | +20-40% |
| Non-green solder mask (blue/red/black) | +10-20% |
| ENIG instead of HASL | +50-100% |
| 0.8mm or 2.0mm thickness | +10-20% |

### 5. Panel Border / Rail Removal
- V-cut (V-score): cheapest, straight lines only
- Tab-route (mouse bites): 20-50% more expensive, any shape
- Use V-cut whenever your board has straight edges

---

## Assembly Cost Reduction

### 1. Single-Sided SMT
- JLCPCB assembly: ¥8 setup + ¥0.02/joint per side
- Double-sided = 2× setup cost
- If you can fit ALL components on one side → save ¥8 per design

### 2. Fewer Unique Line Items
- Each unique LCSC part number = 1 feeder slot
- JLCPCB standard: ~30 feeder slots included
- Extra feeders: ¥3-5 each
- Consolidate to fewer unique parts

### 3. Avoid Special Processes
| Process | Extra Cost |
|---------|:---:|
| Through-hole soldering (hand) | ¥3-5/joint |
| BGA placement + X-ray | ¥20-50/board |
| Conformal coating | ¥10-20/board |
| Press-fit connectors | Custom tooling |
| Wire soldering | ¥5-10/wire |

### 4. Standardize Component Rotation
- All ICs pin-1 same direction → faster programming, fewer placement errors
- All polarized caps same orientation
- Reduces setup time, no cost to you

---

## Quantity vs Cost Trade-offs

| Qty | PCB Cost/board (50×35mm 4L) | Assembly Surcharge | Notes |
|:---:|:---:|:---:|------|
| 5 | ¥7 | Per-joint + setup | Prototype |
| 10 | ¥3.5 | Per-joint + setup | Proto + spares |
| 50 | ¥1.5 | Setup amortized | Pilot run |
| 100 | ¥1.0 | Setup amortized | Small production |
| 500 | ¥0.5 | Minimal surcharges | Volume production |
| 1000+ | ¥0.3 | Negotiable | High volume |

**Sweet spot for small production**: 50-100 pcs.
PCB cost drops significantly; assembly setup is amortized but still small-batch.

---

## Cost Optimization Checklist

- [ ] All LCSC parts checked for "Basic" vs "Extended" status
- [ ] Unique resistor values consolidated (≤ 5 unique values if possible)
- [ ] Unique capacitor values consolidated (≤ 3 unique values if possible)
- [ ] Non-critical components identified and questioned
- [ ] Board fits in ≤ 100×100mm JLCPCB cheapest tier
- [ ] Panel utilization maximized (pack boards tight, rotate for fit)
- [ ] Layer count justified (2L unless ESP32/RF/high-speed/production)
- [ ] V-cut used instead of router where possible
- [ ] Single-sided SMT if feasible
- [ ] No BGA unless absolutely necessary (adds X-ray cost)
- [ ] Standard 1.6mm, 1oz, green, HASL used (no premium options without reason)
- [ ] Assembly test strategy matches quantity (manual for proto, ICT for volume)
