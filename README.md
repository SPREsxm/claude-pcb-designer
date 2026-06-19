# PCB Designer — Claude Skill for Embedded Hardware Design

A [Claude Code](https://claude.ai/code) skill that turns Claude into an
embedded PCB design assistant. It provides expert guidance on schematic
review, component selection, PCB layout, DFM checks, and manufacturing
export — targeting JLCPCB / LCSC assembly with 立创 EDA or KiCad.

## What This Skill Does (v2.0)

**23 design modules** covering the full PCB lifecycle:

| Domain | Coverage |
|--------|----------|
| 🔌 **Power** | LDO selection, DC-DC topology, battery management, solar, USB PD |
| 📡 **RF & Antenna** | Microstrip calculation, impedance matching, antenna types, shielding |
| ⚡ **High-Speed** | DDR routing, impedance control, crosstalk (3W/5W), via effects |
| 🌡️ **Analog** | Op-amp selection, ADC front-end, filters, current sensing |
| 🔗 **Interfaces** | CAN, RS-485, Ethernet, USB 2.0, LVDS/MIPI, SDIO, I2S |
| 🛡️ **Protection** | ESD (IEC 61000-4-2), surge, EMI filtering, isolation, IPC standards |
| 🌡️ **Thermal** | Power budget, θJA calculation, copper heatsinking, thermal vias |
| 🧪 **Testing** | Test points, SWD/JTAG, ICT, functional test, programming |
| 📋 **Compliance** | FCC, CE, UL, RoHS, REACH — with cost and timeline estimates |
| 🏭 **Production** | Stencil, reflow profile, SPI/AOI, panelization, packaging |
| 🧠 **MCU Platforms** | ESP32, STM32, nRF52/53/54, RP2040/RP2350, CH32V |
| 📐 **Materials** | FR-4 vs Rogers, ENIG vs HASL, HDI, FPC, rigid-flex |
| ⚙️ **DFM + EMC** | 94-point checklist + signal integrity guide |
| 🎨 **EDA Workflows** | 立创 EDA Pro + KiCad 8.x |
| 📦 **10+ Circuit Patterns** | ESP32, SPI star bus, I2C, LiPo charger, DC-DC buck, USB-C ESD, buzzer driver, battery ADC |

## Installation

```bash
# Navigate to Claude skills directory
cd ~/.claude/skills/

# Clone this skill
git clone https://github.com/<your-username>/claude-pcb-designer.git pcb-designer
```

The skill auto-loads when Claude detects a PCB-related task. No dependencies,
no npm install — it's a pure knowledge skill.

## Usage

Just mention PCB design tasks naturally to Claude:

> "I'm building an ESP32-S3 data logger with SPI sensors and a microSD card on a 50x35mm 4-layer board. Help me pick components and plan the layout."

> "Review my schematic for DFM issues before I send it to JLCPCB."

> "Should I use a 2-layer or 4-layer board for my ESP32 project?"

Claude will invoke this skill automatically and follow the design process.

## Pairing with easyeda-api-skill

For **direct control** of 立创 EDA Pro (automated component placement, routing,
DRC), install the companion skill:

```bash
cd ~/.claude/skills/
git clone <easyeda-api-skill-url> easyeda-api-skill-main
```

| Skill | Role |
|-------|------|
| `pcb-designer` | Design knowledge & guidance (this repo) |
| `easyeda-api-skill` | Programmatic EDA control via WebSocket bridge |

## File Structure

```
pcb-designer/
├── SKILL.md                            # Main skill definition (23 modules)
├── README.md                           # This file
├── LICENSE                             # MIT License
├── .gitignore
├── evals/
│   └── evals.json                      # Evaluation prompts
└── references/
    ├── lceda-workflow.md               # 立创 EDA Pro workflow
    ├── kicad-workflow.md               # KiCad alternative workflow
    ├── dfm-checklist.md                # Pre-export DFM check (94 items)
    ├── layer-choice.md                 # 2L vs 4L decision guide
    ├── emc-guidelines.md               # EMC & signal integrity
    ├── power-design.md                 # LDO, DC-DC, battery management
    ├── analog-design.md                # Op-amps, ADC, current sensing
    ├── rf-design.md                    # Microstrip, antenna, matching
    ├── high-speed-digital.md           # DDR, impedance, crosstalk
    ├── communication-interfaces.md     # CAN, RS-485, Ethernet, USB, LVDS
    ├── thermal-design.md               # Power budgets, heatsinking
    ├── protection-reliability.md       # ESD, surge, isolation, IPC standards
    ├── testing-debug.md                # Test points, JTAG/SWD, ICT, programming
    ├── compliance-certification.md     # FCC, CE, UL, RoHS, REACH
    ├── manufacturing-production.md     # Stencil, reflow, AOI, packaging
    ├── mcu-platforms.md                # ESP32, STM32, nRF, RP2040, CH32
    └── pcb-materials.md               # FR-4, Rogers, ENIG, HDI, FPC
```

## Supported Tools

| Tool | Level | Notes |
|------|-------|-------|
| **立创 EDA Pro** | Primary | Tightest JLCPCB/LCSC integration |
| **EasyEDA (Standard)** | Good | Web version, same as LCEDA Std |
| **KiCad 8.x** | Alternative | Open-source, cross-platform |

## License

MIT — see [LICENSE](./LICENSE) for details.

## Contributing

Issues and PRs welcome. Key areas for contribution:
- More embedded patterns (motor drivers, RF modules, battery gauges)
- Additional fab house support (PCBWay, OSH Park, Aisler)
- Altium / Eagle / Fusion 360 workflow guides
- Evaluation prompts covering edge cases
