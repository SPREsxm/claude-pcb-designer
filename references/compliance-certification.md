# Compliance & Certification

## Quick Reference by Market

| Market | EMC | Safety | Radio | Environmental |
|--------|:---:|:---:|:---:|:---:|
| **US** | FCC Part 15 | UL 62368 | FCC Part 15.247 | — |
| **EU** | EN 55032/55035 | EN 62368 | RED (2014/53/EU) | RoHS, REACH, WEEE |
| **UK** | UK SI 2016/1091 | UK SI 2016/1101 | UK RED | RoHS, WEEE |
| **Canada** | ICES-003 | CSA C22.2 | RSS-247 | — |
| **Japan** | VCCI | PSE | MIC (Article 2) | RoHS |
| **China** | GB/T 9254 | GB 4943 | SRRC | RoHS |
| **Global** | CISPR 32/35 | IEC 62368 | — | RoHS, REACH |

---

## FCC (United States)

### FCC Part 15 — Unintentional Radiator (All Digital Devices)
- Class A: Industrial/commercial (easier limits)
- Class B: Residential/consumer (stricter limits)
- Test: Conducted emissions (150kHz-30MHz), Radiated emissions (30MHz-1GHz, up to 6GHz)

### FCC Part 15.247 — Intentional Radiator (WiFi/BLE/2.4GHz)
- Frequency: 2400-2483.5MHz
- Power: ≤ 1W (30dBm) conducted
- DTS (Digital Transmission System): ≥ 500kHz bandwidth

### FCC Certification Process
```
1. Pre-compliance scan (in-house or rent chamber)
2. Select TCB (Telecommunication Certification Body)
3. Formal testing at accredited lab
4. File with FCC (gets FCC ID)
5. Label product with FCC ID
Timeline: 4-8 weeks typical
Cost: $3,000-$15,000 (depends on lab and complexity)
```

---

## CE Marking (European Union)

### Applicable Directives
| Directive | Scope | Standard |
|-----------|-------|----------|
| **RED** (2014/53/EU) | Radio equipment | EN 300 328 (2.4GHz) |
| **EMCD** (2014/30/EU) | EMC (non-radio) | EN 55032, EN 55035 |
| **LVD** (2014/35/EU) | Safety (50-1000V AC, 75-1500V DC) | EN 62368 |
| **RoHS** (2011/65/EU) | Hazardous substances | EN IEC 63000 |

### CE Process
```
1. Identify applicable directives
2. Test to harmonized standards
3. Create Technical Documentation File
4. Issue EU Declaration of Conformity (DoC)
5. Affix CE mark
Timeline: 4-12 weeks
Cost: €5,000-€20,000
```

### Self-Declaration vs Notified Body
- **Self-declaration**: EMC, LVD (most cases)
- **Notified Body required**: RED for certain radio types
- ESP32 pre-certified module simplifies RED compliance

---

## RoHS (Restriction of Hazardous Substances)

### Restricted Substances (Max Concentration)
| Substance | Limit |
|-----------|:---:|
| Lead (Pb) | 0.1% |
| Mercury (Hg) | 0.1% |
| Cadmium (Cd) | 0.01% |
| Hexavalent Chromium (Cr6+) | 0.1% |
| PBBs | 0.1% |
| PBDEs | 0.1% |
| DEHP, BBP, DBP, DIBP (phthalates) | 0.1% |

### Compliance Approach
- Use RoHS-compliant components (check datasheets)
- Lead-free assembly (SAC305 solder)
- Supplier declarations of conformity
- Test if needed ($500-2000)

---

## Using Pre-Certified Modules

### ESP32-WROOM Module Certifications
```
FCC: ✓ (modular approval)
CE: ✓
IC (Canada): ✓
MIC (Japan): ✓
SRRC (China): ✓
KCC (Korea): ✓
```

### What Modular Certification Covers
- Radio performance (power, frequency, spurious emissions)
- Antenna type: PCB trace or IPEX (module-specific)

### What You Still Need to Certify
- **Unintentional emissions**: digital part of your board
- **ESD immunity**: IEC 61000-4-2
- **Safety**: if > 50V DC or mains-powered
- Any antenna change voids modular certification

### Antenna Rule (FCC)
- Must use antenna of same TYPE and EQUAL OR LOWER gain as module's certified antenna
- If you change antenna type (PCB → external whip), you need NEW certification

---

## Pre-Compliance Testing

### Equipment (Rent/Buy for In-House)
- Spectrum analyzer + near-field probes (~$500 used)
- TEM cell (small) for radiated pre-scan (~$1000)
- LISN (Line Impedance Stabilization Network) for conducted (~$500)

### Common Failure Points
1. **Power supply noise**: DC-DC switching harmonics
2. **Crystal harmonics**: 40MHz ESP32 crystal × N
3. **Cables as antennas**: any unshielded cable radiates
4. **Poor grounding**: gaps in GND plane
5. **Missing ferrites**: on cables leaving the board

### Pre-Compliance Workflow
```
1. Measure conducted emissions (150kHz-30MHz) with LISN
2. Measure radiated emissions (30MHz-1GHz) in TEM cell or chamber
3. Identify peaks above limit
4. Fix: add ferrites, improve grounding, shield, filter
5. Re-measure
6. When confident: go to accredited lab
```

---

## Safety Certifications

### UL (Underwriters Laboratories, US)
- **UL 62368-1**: Audio/video, IT, communication equipment
- Process: submit samples, construction review, testing, factory inspection
- Cost: $5,000-$50,000 (depends on product complexity)
- Timeline: 6-12 weeks

### Key Safety Design Requirements
- Creepage/clearance: per IEC 62368 (voltage-dependent)
- Fusing: overcurrent protection on all power inputs
- Enclosure: flame rating (V-0 typically)
- Single-fault tolerance: no fire/shock hazard under any single failure

### Battery Safety
- **UN 38.3**: Transport safety testing (lithium batteries)
- **IEC 62133**: Battery cell safety
- **UL 2054**: Household/commercial batteries
- Critical: short-circuit, overcharge, crush, thermal abuse testing

---

## Documentation Package

For each certification, prepare:
```
1. Product description & block diagram
2. Schematic (full)
3. PCB layout (all layers)
4. BOM with manufacturer part numbers
5. User manual / installation guide
6. Label artwork
7. Test reports (if pre-compliance done)
8. DoC (Declaration of Conformity)
```
