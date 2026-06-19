# Protection & Reliability Design

## ESD Protection

### ESD Standards for Product Design
| Standard | Level | Test Type | Application |
|----------|:-----:|-----------|-------------|
| IEC 61000-4-2 | ±8kV contact, ±15kV air | System | Consumer, industrial |
| ISO 10605 | ±15kV contact, ±25kV air | System | Automotive |
| HBM (JESD22-A114) | 2kV | Component | IC qualification |

### TVS Diode Selection
```
1. Vrwm ≥ Vsignal(max) + 10% margin
2. Vclamp < Vdamage of protected IC
3. Cline (capacitance) < acceptable for signal speed
4. Package: smallest, placed at connector
```

### Common TVS Diodes (LCSC/JLCPCB)
| Part | Vrwm | Channels | Cline | Package |
|------|:---:|:---:|:---:|---------|
| LESD5D5.0CT1G | 5V | 1 | 15pF | SOD-523 |
| SRV05-4 | 5V | 4 | 3pF | SOT-23-6 |
| USBLC6-2SC6 | 5.25V | 2 | 2.5pF | SOT-23-6 |
| PESD5V0S1BA | 5V | 1 | 2pF | SOD-323 |

### Placement Rule
```
CONNECTOR ── <5mm ── TVS ── <10mm ── IC
                     │
                   GND (short via to plane)
```
TVS diode MUST be at the connector, not at the IC.
The ESD pulse takes the shortest path to GND. If TVS is at IC, the trace acts as an antenna.

---

## Surge Protection (IEC 61000-4-5)

### Power Input Protection
```
VIN ── Fuse(PTC) ── TVS(SMBJ) ──┬── Internal circuit
                                 │
                                GND
```

### Data Line Protection
```
Connector ── Rseries(10Ω) ── TVS(clamp) ── IC
```
Series resistor limits current; TVS clamps voltage.

### Telecom / Long Cable
```
Line ── GDT(Gas Discharge Tube) ── Series R ── TVS ── IC
```
GDT handles large energy; TVS handles fast edges.

---

## EMI Filtering

### Power Input Filter
```
VIN ── Ferrite Bead ──┬── C1(10µF) ──┬── C2(0.1µF) ── Rail
                      │              │
                     GND            GND
```
π-section: FB ── C ── FB ── C for more attenuation.

### Ferrite Bead Selection
```
Choose bead with:
- Rated current > actual current × 1.5
- Impedance peak at noise frequency
- DCR low enough to not cause excessive drop

Example: BLM18PG121SN1 (120Ω at 100MHz, 2A, 50mΩ DCR, 0603)
```

### Common-Mode Choke
```
Signal ──┌──────┐── Signal
         │ CMC  │
Signal ──└──────┘── Signal (return)
```
- For USB, Ethernet, CAN, RS-485
- Suppresses common-mode noise without affecting differential signal
- Choose for target frequency range

---

## Isolation

### When to Isolate
- User-accessible connectors (safety)
- Long cable runs (ground loop prevention)
- Medical devices (patient safety, IEC 60601)
- Industrial sensors (noise immunity)

### Isolation Technologies
| Type | Max Voltage | Max Speed | Power Transfer | Cost |
|------|:---:|:---:|:---:|------|
| Optocoupler | 5kV | 10Mbps | ✗ | ¥ |
| Digital Isolator | 5kV | 150Mbps | ✗ | ¥¥ |
| Integrated DC-DC + Data | 5kV | 100Mbps | ✓ | ¥¥¥ |
| Transformer | >10kV | AC/Pulse | ✓ | ¥¥ |

### Common Isolators
| Part | Channels | Speed | Isolation | Package |
|------|:---:|:---:|:---:|---------|
| Si8621 | 2 (1+1) | 150Mbps | 5kV | SOIC-8 |
| ISO7741 | 4 (3+1) | 100Mbps | 5kV | SOIC-16 |
| ADUM1250 | I2C | 1Mbps | 2.5kV | SOIC-8 |
| ISO1050 | CAN | 1Mbps | 5kV | SOIC-16 |

---

## Overcurrent Protection

### PTC (Resettable Fuse)
```
Hold current: normal operating current × 1.5
Trip current: typically 2× hold current
Voltage rating: > max system voltage
```

### Electronic Fuse (eFuse)
- TPS2592x, TPS25200, etc.
- Adjustable current limit, overvoltage clamp
- Faster than PTC, but more expensive

---

## Reverse Polarity Protection

### Schottky Diode (Simple)
```
VIN ──|>─── Load
Schottky blocks reverse voltage
Cost: 1 diode + Vf drop (0.3-0.5V)
```

### P-Channel MOSFET (Low Loss)
```
VIN ── PMOS ── Load
      │
      Gate ── Resistor ── GND
      │
      Zener (protect gate)
Zero voltage drop when conducting!
```

---

## IPC Reliability Standards

| Standard | Scope | Key Requirements |
|----------|-------|------------------|
| **IPC-2221** | Generic PCB design | Conductor spacing, creepage, clearance |
| **IPC-2222** | Rigid PCB | Sectional design standard |
| **IPC-6012** | Rigid PCB qualification | Class 1/2/3 requirements |
| **IPC-A-610** | Acceptability | Visual acceptance criteria |
| **J-STD-001** | Soldering | Process requirements |
| **IPC-7351** | Land pattern | Footprint design standard |

### IPC Class Definitions
| Class | Description | Example |
|:---:|------|---------|
| 1 | General electronic | Toys, consumer gadgets |
| 2 | Dedicated service | Industrial, communications |
| 3 | High reliability | Medical, military, aerospace |

---

## Environmental Protection

### Conformal Coating
- Acrylic, silicone, or urethane coating
- Protects against humidity, dust, chemicals
- Mask connectors and test points before coating

### Potting / Encapsulation
- Full encapsulation for extreme environments
- Thermal conductivity consideration (potting increases θJA)
- Use thermally conductive epoxy for hot components

### IP Ratings (Ingress Protection)
| IP | Dust | Water |
|:---:|------|-------|
| IP54 | Protected | Splashing |
| IP65 | Dust-tight | Water jets |
| IP67 | Dust-tight | 1m immersion |
| IP68 | Dust-tight | >1m continuous immersion |
