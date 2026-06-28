---
name: pcb-designer
version: 2.0.0
description: >
  Comprehensive PCB design for embedded / IoT / mixed-signal projects.
  Use this skill whenever the user mentions PCB design, schematic capture,
  board layout, component selection, 立创 EDA, LCEDA, KiCad, EasyEDA, Altium,
  Gerber files, DFM, signal integrity, power design, RF, high-speed digital,
  thermal management, EMC, compliance, manufacturing, or wants to design,
  review, or manufacture a circuit board.
author: RocketBlackBox
tags:
  - pcb
  - hardware
  - embedded
  - schematic
  - layout
  - manufacturing
  - power
  - rf
  - high-speed
  - emc
  - compliance
  - esp32
  - stm32
  - jlcpcb
  - lceda
  - kicad
---

# PCB Designer v2 — Full-Stack Hardware Design

Comprehensive PCB design guidance for embedded systems, IoT devices,
mixed-signal designs, and sensor data-acquisition projects.

Covers the **entire lifecycle**: requirements → component selection →
schematic design → PCB layout → signal integrity → thermal →
manufacturing → compliance → production.

---

## Quick Start

```bash
cd ~/.claude/skills/
git clone <repo-url> pcb-designer
```

Pairs with `easyeda-api-skill` for automated EDA control.

---

## Reference Index

| Scenario | Reference |
|----------|-----------|
| 立创 EDA / LCEDA workflow | `references/lceda-workflow.md` |
| KiCad workflow | `references/kicad-workflow.md` |
| DFM pre-export checklist | `references/dfm-checklist.md` |
| 2-layer vs 4-layer decision | `references/layer-choice.md` |
| EMC & signal integrity | `references/emc-guidelines.md` |
| Power design (LDO/DC-DC/Battery) | `references/power-design.md` |
| Analog & mixed-signal | `references/analog-design.md` |
| RF & antenna design | `references/rf-design.md` |
| High-speed digital | `references/high-speed-digital.md` |
| Communication interfaces | `references/communication-interfaces.md` |
| Thermal design | `references/thermal-design.md` |
| Protection & reliability | `references/protection-reliability.md` |
| Testing & debugging | `references/testing-debug.md` |
| Compliance & certification | `references/compliance-certification.md` |
| Manufacturing & production | `references/manufacturing-production.md` |
| MCU platform references | `references/mcu-platforms.md` |
| PCB materials & processes | `references/pcb-materials.md` |
| Cost optimization | `references/cost-optimization.md` |

---

## 1. Design Process

### Standard Workflow
```
Requirements → Component Selection → Schematic Design →
  Schematic Review → PCB Layout → Routing →
  DFM Check → Export → Order
```

### 1.1 Requirements Clarification
Ask about:
- **MCU / SoC**: Model, package, pin count, frequency
- **Peripherals**: Sensors (SPI/I2C/UART/analog), displays, storage, radios, audio
- **Power**: Battery (chemistry, voltage, capacity), USB, PoE, solar, power budget
- **Mechanical**: Board size, mounting, enclosure, connector placement
- **Environment**: Temperature range, vibration, humidity, IP rating
- **Compliance**: FCC, CE, UL, automotive, medical
- **Budget**: BOM cost target, layer count, quantity (proto vs production)

---

## 2. Component Selection

### 2.1 Supply Chain Strategy
| Priority | Source | Notes |
|----------|--------|-------|
| 1st | LCSC Basic Parts | No JLCPCB assembly surcharge |
| 2nd | LCSC Extended | ¥3/part surcharge |
| 3rd | Digi-Key / Mouser | Consigned to JLCPCB |
| Last resort | Custom sourcing | Slow, logistics overhead |

### 2.2 Package Preference
| Density | Passives | ICs | Hand-solderable |
|---------|----------|-----|:---:|
| Ultra-compact | 0201 | WLCSP/BGA | ✗ |
| High density | 0402 | QFN/LGA | ✗ |
| **Sweet spot** | **0603** | **QFN/QFP** | ✓ (with practice) |
| Low density | 0805 | SOIC/SOP | ✓ |
| Through-hole | — | DIP | ✓ (easy) |

### 2.3 Common Components (LCSC)
| Function | Part | Package | LCSC # |
|----------|------|---------|--------|
| ESP32-S3 (PCB ant) | ESP32-S3-WROOM-1-N16R8 | Module | C2913201 |
| ESP32-S3 (IPEX) | ESP32-S3-WROOM-1U-N16R8 | Module | C2913203 |
| 3.3V LDO 1A | AMS1117-3.3 | SOT-223 | C6186 |
| 3.3V LDO low-noise | ME6211C33M5G | SOT-23-5 | C82942 |
| 3.3V Buck 2A | MT2492 | SOT-23-6 | — |
| LiPo charger 1A | TP4056 | SOP-8 | C382139 |
| USB-C 16P Female | TYPE-C-31-M-12 | SMD | C165948 |
| TF Card Push-Push | 9P Push-Push | SMD | C112217 |
| USB-UART | CH340X | MSOP-10 | — |
| WS2812B RGB LED | WS2812B-B/W | 5050 | — |
| 32.768kHz XTAL | 3215 12.5pF | SMD-3215 | C620155 |
| ESD Protection | LESD5D5.0CT1G | SOD-523 | — |

---

## 3. Schematic Review

Before layout, verify:
- [ ] Every VDD pin has 0.1µF decoupling within 5mm
- [ ] Bulk capacitance (10–47µF) on each power rail
- [ ] I2C: 4.7kΩ pull-ups on SDA+SCL (one pair per bus)
- [ ] SPI >20MHz: 22Ω series termination at source
- [ ] ESP32: EN pulled high (10kΩ+1µF RC), IO0 pulled high (10kΩ)
- [ ] Battery ADC divider: ≤3.3V at max battery voltage
- [ ] USB: ESD diodes at connector, not at MCU
- [ ] No floating inputs (unused CMOS inputs must be tied high or low)
- [ ] Programming/debug header accessible
- [ ] Test points: GND, 3V3, UART TX/RX minimum
- [ ] Pin conflicts resolved (no shared GPIO functions)
- [ ] Power sequencing correct (if multiple rails)

---

## 4. PCB Layout

### 4.1 Stackup Decision
| Factor | 2-Layer | 4-Layer | 6+ Layer |
|--------|---------|---------|----------|
| Cost (50×50mm, 5pcs) | ~¥5 | ~¥30 | ~¥80+ |
| Signal integrity | Fair | Good | Excellent |
| EMI control | Hard | Good | Easy |
| Suitable for | Slow MCU, proto | ESP32, production | DDR, RF dense |

**Recommended 4-layer stackup (JLCPCB JLC7628):**
```
L1: Signal + Components     ← Top
Prepreg (0.2mm)
L2: GND Plane (continuous)  ← Solid return path
Core (0.5mm)
L3: Power Plane (3.3V)      ← Low-Z distribution
Prepreg (0.2mm)
L4: Signal + GND fill       ← Bottom
```

### 4.2 Placement Order
1. **Fixed items**: connectors, mounting holes, antenna
2. **MCU/module**: center, antenna outward
3. **Power**: near input, away from sensitive analog
4. **High-speed**: closest to MCU, shortest paths
5. **Sensors**: near MCU, oriented for mechanical alignment
6. **Passives**: decoupling caps at IC pins (≤5mm)

### 4.3 Antenna Keep-Out (ESP32)
- 15mm × 15mm zone, **ALL layers NO copper**
- No components, traces, mounting holes, battery, or metal near it
- Antenna faces board edge OUTWARD

---

## 5. Routing Rules

| Signal | Min Width | Min Spacing | Special |
|--------|-----------|-------------|---------|
| Digital ≤20MHz | 6mil | 6mil | — |
| SPI 40MHz | 6mil | 18mil (3×W) | 22Ω series term, ±2mm match |
| SPI 20MHz | 6mil | 12mil (2×W) | Pull-ups |
| I2C 400kHz | 6mil | 12mil | Away from clocks |
| I2C 1MHz (Fast+) | 6mil | 18mil | Shorter traces |
| Power >100mA | 12mil | 12mil | Short |
| Power >500mA | 20mil | 12mil | Very short |
| Power >1A | Copper pour | 12mil | Multiple vias |
| USB D+/D- | 6mil | 6mil | 90Ω diff, length-matched |
| RF 50Ω | Calculated | — | Reference plane beneath |
| Audio analog | 10mil | 20mil | Guard traces optional |

---

## 6. Embedded Circuit Patterns

### 6.1 ESP32 Minimum Boot
```
3V3 ── 10kΩ ── EN ── 1µF ── GND
3V3 ── 10kΩ ── IO0 ── BUTTON ── GND
```

### 6.2 SPI Sensor Bus (40MHz, Star Topology)
```
MCU MOSI ── 22Ω ──┬── Sensor1 SDI
                   ├── Sensor2 SDI
                   └── Sensor3 SDI
MCU SCLK ── 22Ω ──┬── Sensor1 SCK
                   ├── Sensor2 SCK
                   └── Sensor3 SCK
MCU MISO ──┬─────── Sensor1 SDO
            ├─────── Sensor2 SDO
            └─────── Sensor3 SDO
Each sensor: dedicated CS line (no resistor needed)
```

### 6.3 I2C Bus
```
3V3 ── 4.7kΩ ──┬── SDA
               └── All devices SDA
3V3 ── 4.7kΩ ──┬── SCL
               └── All devices SCL
```

### 6.4 LiPo Charger (TP4056)
```
USB 5V ──┬── TP4056 VCC(pin4,8)
          ├── PROG(pin2) ── Rprog ── GND    (I=1000/Rprog)
          ├── BAT(pin5) ── BAT+
          ├── CHRG(pin6) ── LED_RED ── 2kΩ ── 5V
          ├── STDBY(pin7) ── LED_GREEN ── 2kΩ ── 5V
          └── 10µF caps on input & output
```

### 6.5 DC-DC Buck (MT2492 → 3.3V)
```
SYS_5V ── 10µF ── VIN(pin5)
EN(pin4) ── 10kΩ ── SYS_5V
SW(pin6) ── L(4.7µH) ──┬── 3V3 + 22µF output cap
                        FB(pin3) ──┬── R1(100kΩ) ── 3V3
                                   └── R2(22.1kΩ) ── GND
Vout = 0.6 × (1 + R1/R2)
```

### 6.6 USB-C with ESD
```
VBUS ── Schottky ── CHARGE_5V
CC1 ── 5.1kΩ ── GND
CC2 ── 5.1kΩ ── GND
D+ ── ESD ── GND ──┬── CH340X/GPIO
D- ── ESD ── GND ──┘
```

### 6.7 NPN Buzzer Driver
```
VCC ── BUZZER ── NPN_C
GPIO ── 1kΩ ── NPN_B
        10kΩ ── NPN_B ── GND (anti-float)
NPN_E ── GND
1N4148: cathode to VCC, anode to NPN_C (flyback)
```

### 6.8 Battery Voltage ADC
```
BAT+ ── R1(20kΩ) ──┬── GPIO_ADC ── 0.1µF ── GND
                   R2(30kΩ)
                   GND
Ratio: 30/(20+30)=0.6 → 4.2V→2.52V at ADC
```

---

## 7. DFM Checks

Full checklist at `references/dfm-checklist.md`. Quick checks:

### Minimum Fab Capability (JLCPCB)
| Parameter | Min | Recommended |
|-----------|-----|-------------|
| Trace/space | 3.5mil | 6mil |
| Via hole | 0.2mm | 0.3mm |
| Via pad | 0.45mm | 0.6mm |
| Annular ring | 0.125mm | 0.15mm |

### Pre-Export
- [ ] 0 DRC errors
- [ ] Board outline on mechanical layer
- [ ] Silkscreen ≥0.8mm height, not on pads
- [ ] No acute angles in copper
- [ ] Thermal relief on pads to pours
- [ ] No isolated copper islands
- [ ] All nets routed (no ratsnest)

---

## 8. EMC & Signal Integrity

See `references/emc-guidelines.md` for full details.

### Key Rules
1. **Return paths**: never cut L2 GND plane with long traces
2. **Decoupling**: 0.1µF per VDD pin, ≤5mm from pin, short loop
3. **Termination**: 22Ω at source for high-speed SPI
4. **Spacing**: SPI 3×W from other signals, I2C away from clocks
5. **Stitching**: GND vias every 5–10mm along edges

---

## 9. EDA Tool Workflows

### 立创 EDA Pro (Primary)
See `references/lceda-workflow.md`.
- File → Export → Gerber (RS-274X, mm)
- File → Export → BOM (CSV)
- File → Export → Pick & Place

### KiCad 8.x (Alternative)
See `references/kicad-workflow.md`.
- Git-friendly text format, excellent 3D viewer

---

## 10. Design Review

Three-tier evaluation:
- 🔴 **Critical**: prevents manufacturing or causes failure
- 🟡 **Warning**: yield or reliability risk
- 🔵 **Suggestion**: performance, cost, or ease-of-assembly improvement

---

## 11. Power Design

See `references/power-design.md`.

### LDO Selection
- **Dropout voltage**: Vin_min - Vout < Vdropout(max)
- **Power dissipation**: Pd = (Vin - Vout) × Iload
- **Thermal**: Tj = Ta + Pd × θJA (must be <125°C)
- **PSRR**: critical for analog/RF rails

### DC-DC Topology
| Topology | Vin vs Vout | Complexity | EMI |
|----------|:---:|:---:|:---:|
| Buck | Vin > Vout | Low | Medium |
| Boost | Vin < Vout | Low | Medium |
| Buck-Boost | Either | Medium | High |
| SEPIC | Either | Medium | High |
| LDO (linear) | Vin > Vout | Minimal | Low (best PSRR) |

### Battery Management
- **1S LiPo (3.7V)**: TP4056 charger, DW01+FS8205 protection
- **2S-4S**: BQ-series charger + cell balancing
- **Fuel gauge**: MAX17048 (I2C), BQ27427
- **Solar**: CN3791 (MPPT), BQ24210

### Power Sequencing
- Ensure core voltage before I/O voltage
- Use RC delays or dedicated sequencer ICs
- Check MCU datasheet for power-up requirements

---

## 12. MCU Platforms

See `references/mcu-platforms.md`.

### Platform Selection Guide
| Platform | Best For | Max Clock | Wireless | Eco-system |
|----------|----------|:---------:|:--------:|:----------:|
| ESP32-S3 | IoT, WiFi/BLE | 240MHz | ✓ | Arduino, ESP-IDF |
| STM32F4 | Industrial, DSP | 180MHz | ✗ | STM32Cube, HAL |
| STM32H7 | High-perf, GUI | 550MHz | ✗ | STM32Cube |
| nRF52840 | BLE, Thread | 64MHz | ✓ | nRF Connect, Zephyr |
| nRF54L15 | Next-gen BLE | 128MHz | ✓ | Zephyr |
| RP2040 | Low-cost, PIO | 133MHz | ✗ | Pico SDK, Arduino |
| RP2350 | Secure, RISC-V | 150MHz | ✗ | Pico SDK |
| CH32V203 | RISC-V budget | 144MHz | ✗ | MounRiver |
| ATmega328P | Simple, 5V | 16MHz | ✗ | Arduino |
| CH582 | BLE budget | 60MHz | ✓ | MounRiver |

---

## 13. Communication Interfaces

See `references/communication-interfaces.md`.

| Interface | Speed | Topology | Key Rules |
|-----------|-------|----------|-----------|
| UART | ≤3Mbps | Point-to-point | Cross TX/RX |
| I2C | 100k/400k/1M | Multi-drop bus | Pull-ups, ≤400pF |
| SPI | ≤50MHz | Star, multi-CS | 22Ω term, ±2mm match |
| QSPI/OSPI | ≤133MHz | Point-to-point | Length match all data lines |
| CAN | ≤1Mbps | Differential bus | 120Ω term both ends |
| RS-485 | ≤50Mbps | Differential multi-drop | 120Ω term, fail-safe bias |
| USB 2.0 FS | 12Mbps | Point-to-point | 90Ω diff, ESD at conn |
| USB 2.0 HS | 480Mbps | Point-to-point | 90Ω diff, impedance critical |
| Ethernet 100M | 100Mbps | Point-to-point | RMII, magnetics, 50Ω |
| SDIO | ≤208MHz | Point-to-point | Length match, pull-ups |
| I2S | Variable | Point-to-point | Separate MCLK/BCLK/LRCK |
| LVDS/MIPI | ≤1.5Gbps/lane | Diff pair | 100Ω diff, tight matching |

---

## 14. Analog & Mixed-Signal

See `references/analog-design.md`.

### Op-Amp Selection
- **GBW** ≥ 10× signal frequency for buffer, ≥ 100× for gain stages
- **Slew rate** ≥ 2π × f × Vpeak
- **Input offset**: <1mV for precision, <5mV for general
- **Noise**: nV/√Hz for low-level signals
- **Rail-to-rail**: needed if signal swings near supply

### ADC Front-End
- Anti-aliasing filter: fc < Fs/2 (Nyquist)
- Driver op-amp: settle within ADC acquisition time
- Reference: dedicated low-noise Vref IC
- Input protection: clamp diodes to VDD/GND

### Current Sensing
| Method | Range | Accuracy | Isolation |
|--------|-------|:---:|:---:|
| Shunt + op-amp | μA–kA | ±0.1% | ✗ |
| Hall effect | 1A–1000A | ±1% | ✓ |
| CT (AC only) | 0.1A–100A | ±0.5% | ✓ |

---

## 15. RF & Antenna Design

See `references/rf-design.md`.

### Microstrip (2-layer, signal over GND plane)
- **Width for 50Ω**: ~2.9mm on 1.6mm FR4, ~0.5mm on 4-layer
- Use online calculators: TXLine, Saturn PCB Toolkit
- Keep RF traces short, no bends < 3× width radius

### Antenna Types
| Type | Size | Bandwidth | Cost | Use Case |
|------|------|:---:|------|----------|
| PCB trace (IFA/meander) | 15×8mm | Narrow | Free | ESP32 modules |
| Ceramic chip | 3×2mm | Narrow | ¥1-3 | GPS, BLE compact |
| External whip | 50-100mm | Wide | ¥10-50 | Gateway, base station |
| IPEX + flex PCB | Variable | Good | ¥5-20 | Enclosure integration |

### Matching Network
```
ANT ──┬── Series L/C ──┬── Shunt L/C ── RF_IC
      │                │
      └── π-network: 3 components (shunt-series-shunt or series-shunt-series)
```

---

## 16. High-Speed Digital Design

See `references/high-speed-digital.md`.

### Impedance Control
| Signal | Z0 Single | Zdiff |
|--------|:---:|:---:|
| 50Ω RF | 50Ω | — |
| USB D+/D- | — | 90Ω |
| Ethernet | — | 100Ω |
| LVDS | — | 100Ω |
| HDMI/DVI | — | 100Ω |

### Crosstalk Rules
- **3W rule**: spacing ≥ 3× trace width (acceptable)
- **5W rule**: spacing ≥ 5× trace width (excellent)
- Guard traces: grounded between aggressor/victim, stitched every λ/10

### DDR Routing
- Clock: point-to-point, series term at driver
- Address/control: fly-by topology, matched within ±25mil
- Data: byte-lane matching within ±5mil
- Vref: clean, decoupled, wide trace

### Via Stub Effect
- λ/4 stub can cause nulls at specific frequencies
- Back-drill or use blind vias for >5Gbps

---

## 17. PCB Materials & Processes

See `references/pcb-materials.md`.

### Substrate
| Material | εr | Tan δ | Tg | Cost | Use |
|----------|:---:|:---:|:---:|------|-----|
| FR-4 (standard) | 4.2-4.6 | 0.02 | 130°C | ¥ | Digital, low-freq |
| FR-4 (high-Tg) | 4.2-4.6 | 0.02 | 170°C | ¥¥ | Lead-free, automotive |
| Rogers 4350B | 3.48 | 0.004 | 280°C | ¥¥¥¥ | RF/microwave |
| Isola 370HR | 3.9 | 0.01 | 180°C | ¥¥¥ | High-speed digital |

### Surface Finish
| Finish | Shelf Life | Flatness | Cost | Lead-free |
|--------|:---:|:---:|------|:---:|
| HASL (有铅) | 12mo | Poor | ¥ | ✗ |
| HASL (无铅) | 12mo | Poor | ¥ | ✓ |
| ENIG | 12mo | Excellent | ¥¥ | ✓ |
| ENEPIG | 12mo | Excellent | ¥¥¥ | ✓ |
| OSP | 6mo | Excellent | ¥ | ✓ |
| Immersion Silver | 6mo | Good | ¥¥ | ✓ |

### Advanced Processes
- **Blind via**: L1→L2 or L3→L4 (outer to inner)
- **Buried via**: L2→L3 (inner to inner)
- **Microvia**: <0.15mm hole, laser-drilled, HDI
- **Via-in-pad**: filled + capped, for BGA fanout
- **FPC**: flexible polyimide, 1-2 layers typical
- **Rigid-flex**: FR-4 + FPC laminated together
- **Metal-core (MCPCB)**: aluminum/copper base for LEDs/power

---

## 18. Thermal Design

See `references/thermal-design.md`.

### Power Budget
- List every IC's max current × voltage = power (W)
- Sum to get total board power
- Identify hot spots (>0.5W in one location)

### Thermal Resistance
- θJA: junction-to-ambient (from datasheet)
- θJC: junction-to-case (for heatsink design)
- Tj = Ta + Pd × θJA  →  must stay < Tj(max), usually 125°C

### Copper Area for Heatsinking
```
Approximate: 1cm² of 1oz Cu ≈ 50°C/W (natural convection)
For 2oz Cu: ~30°C/W per cm²
```

### Thermal Vias
- Array of 0.3mm vias under thermal pad
- 1mm pitch grid, filled with solder or epoxy
- Connect to GND plane on L2 + copper pour on bottom

---

## 19. Protection & Reliability

See `references/protection-reliability.md`.

### ESD Protection
| Level | Voltage | Standard | Protection |
|-------|:---:|----------|------------|
| HBM | 2kV | JESD22-A114 | On-chip diodes |
| CDM | 500V | JESD22-C101 | On-chip |
| IEC 61000-4-2 Contact | ±8kV | System-level | TVS at connector |
| IEC 61000-4-2 Air | ±15kV | System-level | TVS + shielding |

### TVS Diode Selection
- Vrwm ≥ Vsignal (standing voltage)
- Vclamp < Vmax of protected IC
- Place at connector, short path to GND plane

### Surge Protection (IEC 61000-4-5)
- Power input: TVS + PTC fuse
- Data lines: series resistor + TVS clamp
- Telecom: GDT (gas discharge tube)

### EMI Filtering
- **Common-mode choke**: on power input, USB, Ethernet
- **π-filter**: C-L-C topology for power rails
- **Ferrite bead**: series on power, choose for target frequency

### Isolation
| Type | Voltage | Speed | Cost |
|------|:---:|:---:|------|
| Optocoupler | 5kV | ≤10Mbps | ¥ |
| Digital isolator (SiO2) | 5kV | ≤150Mbps | ¥¥ |
| Transformer | >10kV | AC/pulse | ¥¥ |
| Capacitive | 5kV | ≤150Mbps | ¥¥ |

### IPC Reliability Standards
- **IPC-2221**: Generic design standard
- **IPC-6012**: Rigid PCB qualification
- **IPC-A-610**: Acceptability of electronic assemblies
- **J-STD-001**: Soldering requirements
- **IPC-7351**: Land pattern standard

---

## 20. Testing & Debugging

See `references/testing-debug.md`.

### Test Points
- **Minimum**: GND, 3V3, UART TX, UART RX
- **Recommended**: all power rails, key signals, unused GPIOs
- Pad size: ≥1.0mm for pogo pin, ≥1.5mm for multimeter probe
- Keep test points on one side (usually bottom) for test fixture

### Debug Interfaces
| Interface | Pins | Use |
|-----------|:---:|-----|
| SWD (ARM) | SWCLK+SWDIO+GND | Programming + debug |
| JTAG | TMS+TDI+TDO+TCK+GND | Boundary scan |
| cJTAG (2-wire) | Same as SWD | ARM debug alternative |
| UART | TX+RX+GND | Serial console, log output |

### Production Test
- **ICT (In-Circuit Test)**: bed-of-nails, checks component values
- **Flying probe**: no fixture, slower, good for prototypes
- **Functional test**: power up, run self-test firmware
- **Programming**: pre-program MCUs or ISP on-board

---

## 21. Cost Optimization

See `references/cost-optimization.md` for full analysis.

### Quick Wins
- **LCSC Basic Parts**: save ¥3/part vs extended library
- **Consolidate values**: fewer unique resistor/capacitor values
- **≤100×100mm**: JLCPCB's cheapest PCB tier
- **V-cut** over router for rectangular panels
- **Single-sided SMT** if possible (2× setup cost for double-sided)

---

## 22. Compliance & Certification

See `references/compliance-certification.md`.

### Key Certifications
| Certification | Region | Scope | Est. Cost |
|---------------|--------|-------|:---:|
| **FCC Part 15** | US | Intentional/unintentional radiator | $3k-15k |
| **CE (RED)** | EU | Radio Equipment Directive | €5k-20k |
| **UKCA** | UK | Post-Brexit equivalent of CE | £3k-15k |
| **RoHS** | EU/Global | Hazardous substance restriction | $500-2k |
| **REACH** | EU | Chemical substance registration | Compliance declaration |
| **UL** | US/Global | Safety certification | $5k-50k |
| **AEC-Q100** | Global | Automotive IC qualification | IC-level only |

### Pre-Compliance Testing
- Rent EMC chamber (~$200/hr) before formal testing
- Use near-field probes + spectrum analyzer for in-house pre-scan
- Common failure points: power supply noise, unshielded cables, poor grounding

---

## 23. Manufacturing & Production

See `references/manufacturing-production.md`.

### Stencil Design
- **Thickness**: 0.1mm (fine pitch) to 0.15mm (standard)
- **Aperture**: 1:1 for chips, reduce 10-20% for passives
- **Electropolished**: for fine pitch (<0.5mm)

### Reflow Profile (Lead-Free SAC305)
```
150°C─190°C: Preheat, 60-120s
>217°C: Liquidus, 60-90s
Peak: 235°C─250°C, 10-30s
Cooling: <4°C/s
```

### Inspection
- **SPI** (Solder Paste Inspection): before placement
- **AOI** (Automated Optical Inspection): after reflow
- **X-ray**: for BGA/QFN hidden joints

### Programming & Testing
- Pre-program MCUs before placement (socket programmer)
- Or ISP (In-System Programming) via SWD/UART after assembly
- Functional test jig with pogo pins

### Packaging
- **ESD bags**: moisture-sensitive components
- **Tape & reel**: for automated pick-and-place
- **Trays**: for large/expensive ICs (QFP, BGA)

---

## Output Format

When asked to **design a PCB**, provide:
1. **Block diagram** showing major components and connections
2. **Power budget** — estimated current per rail
3. **Schematic notes** — key connections, pin assignments, values
4. **BOM** — table with reference, part, package, LCSC#, qty, unit cost
5. **Layout guidance** — placement order, critical routing, keep-out zones
6. **DFM reminders** — fab-specific pre-export checks

When asked to **review a PCB**, use three-tier:
- 🔴 **Critical issues**
- 🟡 **Warnings**
- 🔵 **Suggestions**

---

## Pairing with easyeda-api-skill

| Skill | Role |
|-------|------|
| `pcb-designer` (this) | **Design brain** — what to do and why |
| `easyeda-api-skill` | **Automation hands** — execute in EDA via bridge |

```bash
cd ~/.claude/skills/
git clone <pcb-designer-repo> pcb-designer
git clone <easyeda-api-repo> easyeda-api-skill-main
```
