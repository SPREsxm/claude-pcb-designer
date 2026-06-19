<p align="center">
  <img src="https://img.shields.io/badge/PCB%20Designer-v2.0.0-blue?style=for-the-badge" alt="version">
  <img src="https://img.shields.io/badge/Modules-23-brightgreen?style=for-the-badge" alt="modules">
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="license">
  <img src="https://img.shields.io/badge/Claude%20Code-Skill-orange?style=for-the-badge" alt="claude-code-skill">
</p>

<h1 align="center">🧠 PCB Designer</h1>
<h3 align="center">Claude Code Skill — Full-Stack Embedded Hardware Design</h3>

<p align="center">
  Turn Claude into a professional PCB engineer.<br>
  From schematic review to Gerber export — 23 modules covering every aspect of board design.
</p>

---

## Why This Skill?

Designing a PCB involves **dozens of decisions** across multiple domains — power, RF, signal integrity, thermal, DFM, compliance. Most engineers learn these over years of trial and error.

**This skill gives Claude instant expertise in ALL of them.**

Ask Claude anything about PCB design, and it draws from 17 reference documents covering the full lifecycle.

---

## What It Covers

<table>
<tr><th colspan="2">🧠 Design Intelligence</th></tr>
<tr><td>🔌 <b>Power</b></td><td>LDO thermal math, DC-DC topology (Buck/Boost/SEPIC), LiPo 1S-4S, solar MPPT, USB PD</td></tr>
<tr><td>📡 <b>RF & Antenna</b></td><td>Microstrip width calculation, Smith chart matching, PCB/ceramic/external antennas, shielding</td></tr>
<tr><td>⚡ <b>High-Speed</b></td><td>DDR routing, 50Ω/90Ω/100Ω impedance control, 3W/5W crosstalk, via stub effects</td></tr>
<tr><td>🌡️ <b>Analog</b></td><td>Op-amp GBW/slew rate selection, ADC front-end, anti-aliasing filters, current sensing</td></tr>
<tr><td>🔗 <b>Interfaces</b></td><td>CAN (120Ω termination), RS-485 (fail-safe bias), Ethernet (magnetics), USB 2.0, LVDS, MIPI, SDIO</td></tr>
<tr><td>🌡️ <b>Thermal</b></td><td>Power budget, θJA/θJC calculation, copper area vs °C/W, thermal via arrays</td></tr>
<tr><td>🛡️ <b>Protection</b></td><td>IEC 61000-4-2 ESD, TVS selection, surge, EMI π-filters, opto/magnetic/capacitive isolation</td></tr>
<tr><td>🧠 <b>MCU Platforms</b></td><td>ESP32-S3/C3/C6, STM32 F1/F4/G0/H7, nRF52/53/54, RP2040/RP2350, CH32V, ATmega</td></tr>

<tr><th colspan="2">🏭 Manufacturing & Production</th></tr>
<tr><td>⚙️ <b>DFM</b></td><td>94-point checklist: clearances, annular rings, silkscreen, thermal relief, acid traps</td></tr>
<tr><td>📐 <b>Materials</b></td><td>FR-4 vs Rogers/Isola, ENIG vs HASL vs OSP, HDI microvias, FPC, rigid-flex, metal-core</td></tr>
<tr><td>🏭 <b>Production</b></td><td>Stencil aperture design, SAC305 reflow profile, SPI/AOI/X-ray inspection, panelization, ESD packaging</td></tr>

<tr><th colspan="2">📋 Compliance & Verification</th></tr>
<tr><td>📋 <b>Compliance</b></td><td>FCC Part 15 ($3-15k), CE RED (€5-20k), UL, RoHS, REACH — with timeline estimates</td></tr>
<tr><td>🧪 <b>Testing</b></td><td>Test point strategy, SWD/JTAG/SWD header design, ICT fixture, flying probe, functional test</td></tr>
<tr><td>⚡ <b>EMC</b></td><td>Return paths, decoupling loop area, SPI termination, GND stitching, antenna keep-out</td></tr>

<tr><th colspan="2">📦 Patterns & Workflows</th></tr>
<tr><td>📦 <b>10+ Circuits</b></td><td>ESP32 boot, SPI star bus, I2C bus, LiPo charger, DC-DC buck, USB-C ESD, buzzer driver, battery ADC</td></tr>
<tr><td>🎨 <b>EDA Tools</b></td><td>立创 EDA Pro (primary) + KiCad 8.x — with keyboard shortcuts and export workflows</td></tr>
</table>

---

## Quick Start

```bash
cd ~/.claude/skills/
git clone https://github.com/SPREsxm/claude-pcb-designer.git pcb-designer
```

Done. Claude auto-loads it when you mention PCB design. Zero dependencies.

## Usage Examples

**Design a new board:**
> "I'm building an ESP32-S3 data logger with an ICM-42688 IMU (SPI), MMC5983MA magnetometer (SPI), MS5611 barometer (I2C), microSD card, and a 3.7V LiPo battery on a 50×35mm 4-layer board. Help me pick components and plan the layout."

**Review before fab:**
> "Review my schematic and PCB layout for DFM issues before I send it to JLCPCB."

**Tough trade-off:**
> "Should I use a 2-layer or 4-layer board? What's the cost difference at JLCPCB for 100 pcs?"

**Debug a problem:**
> "My SPI bus at 40MHz is unreliable. How should I route it, and do I need termination resistors?"

Claude invokes the skill automatically and applies the right reference documents.

---

## Stack

```
📁 pcb-designer/
├── SKILL.md                        ← 23 modules, main skill logic
├── README.md
├── LICENSE (MIT)
└── references/
    ├── lceda-workflow.md           ← 立创 EDA Pro: schematic → PCB → Gerber
    ├── kicad-workflow.md           ← KiCad 8.x alternative
    ├── power-design.md             ← LDO, DC-DC, battery, solar, USB PD
    ├── analog-design.md            ← Op-amps, ADC, filters, current sense
    ├── rf-design.md                ← Microstrip, antenna, matching network
    ├── high-speed-digital.md       ← DDR, impedance, crosstalk, length matching
    ├── communication-interfaces.md ← CAN, RS-485, Ethernet, USB, LVDS, MIPI
    ├── thermal-design.md           ← Power budgets, θJA, heatsink copper area
    ├── protection-reliability.md   ← ESD, surge, EMI, isolation, IPC standards
    ├── testing-debug.md            ← Test points, JTAG/SWD, ICT, production test
    ├── compliance-certification.md ← FCC, CE, UL, RoHS — costs & timelines
    ├── manufacturing-production.md ← Stencil, reflow, SPI/AOI, panelization
    ├── mcu-platforms.md            ← ESP32/STM32/nRF/RP2040/CH32V reference
    ├── pcb-materials.md            ← FR-4, Rogers, ENIG, HDI, FPC, metal-core
    ├── dfm-checklist.md            ← 94-point pre-export check
    ├── emc-guidelines.md           ← Return paths, decoupling, termination
    └── layer-choice.md             ← 2L vs 4L decision matrix
```

---

## Pair with easyeda-api-skill

For **programmatic control** of 立创 EDA Pro (auto-placement, routing, DRC via WebSocket):

| Skill | Role |
|-------|------|
| `pcb-designer` | 🧠 **Design brain** — what to do and why |
| `easyeda-api-skill` | 🤖 **Automation hands** — API control of EDA |

---

## License

MIT © [SPREsxm](https://github.com/SPREsxm)

## Contributing

Issues & PRs welcome. Areas to grow:
- Altium / OrCAD / Eagle workflow guides
- PCBWay / OSH Park fab support
- Motor drivers, battery gauges, RF module patterns
- More eval prompts for edge cases
