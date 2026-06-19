# RF & Antenna Design for Embedded Boards

## Microstrip Transmission Line

### Width for 50Ω Characteristic Impedance

Simplified formula for FR-4 (εr ≈ 4.4):

| Board | Layer Stack | 50Ω Width (approx) |
|-------|------------|:---:|
| 2L, 1.6mm | L1 signal, L2 GND | 2.9mm |
| 4L, 0.2mm prepreg | L1 signal, L2 GND | 0.35mm |
| 4L, 0.1mm prepreg | L1 signal, L2 GND | 0.19mm |

Use **Saturn PCB Toolkit** or **TXLine** for accurate calculation with your actual stackup.

### Microstrip Rules
- Keep RF trace as short as possible (< λ/4)
- No bends sharper than 3× trace width radius
- Reference plane (GND) must be continuous underneath
- Keep >3× trace width clear of other copper
- No vias in the RF path (each via adds ~0.5nH)

### Coplanar Waveguide (CPW)
```
        GND ── gap ── Signal ── gap ── GND
                    (all on same layer)
```
- Easier to achieve 50Ω on thick substrates (2-layer boards)
- Good for 2-layer designs where microstrip is too wide
- Gap width ≈ 0.15-0.3mm typical

---

## Antenna Types

### PCB Trace Antennas
| Type | Size (2.4GHz) | BW | Gain | Pattern |
|------|:---:|:---:|:---:|:---:|
| IFA (Inverted-F) | 15×8mm | 80-100MHz | 2-3dBi | Near-omni |
| Meander | 15×5mm | 50-80MHz | 1-2dBi | Omni |
| PIFA | 15×8mm | 80MHz | 1-3dBi | Omni |
| Patch | 30×30mm | 10-50MHz | 5-8dBi | Directional |

### Ceramic Chip Antennas
- Very compact (3×2×1mm typical)
- Narrow bandwidth, sensitive to ground plane size
- Need clearance zone around chip
- Examples: Johanson 2450AT18x100, Yageo AQJ453

### External Antennas
- IPEX/u.FL connector → external antenna
- Best performance, larger size/cost
- Use ESP32-S3-WROOM-1U (IPEX version, C2913203)
- No PCB antenna issues (no keep-out zone needed)

---

## Impedance Matching

### π-Network (Most Common)
```
           Series L/C
RF_IC ──┬──[===]──┬── ANT
        │          │
      Shunt       Shunt
      L/C         L/C
        │          │
       GND        GND
```
- 3 components provide flexible matching
- Start with components unpopulated (0Ω jumper)
- Tune empirically with VNA after PCB fabricated

### When to Match
- If antenna datasheet specifies matching needed
- If VNA shows S11 > -10dB at target frequency
- If range is significantly below expectation

### Smith Chart Basics
- Center = perfect match (50Ω)
- Inductive: upper half; Capacitive: lower half
- Series L: moves clockwise; Series C: counterclockwise
- Shunt L: counterclockwise; Shunt C: clockwise

---

## Antenna Placement

### ESP32 PCB Antenna Keep-Out
```
┌─────────────────────────────┐
│                             │
│  ┌──────────────┐  ╔══════╗│
│  │   ESP32-S3   │  ║ ANT  ║│
│  │   WROOM-1    │  ║ ZONE ║│
│  └──────────────┘  ║15×15 ║│
│                    ║ mm   ║│
│                    ║      ║│
│   ← board edge     ╚══════╝│
└─────────────────────────────┘
```

### Critical Rules
1. Antenna at board **edge**, facing **OUTWARD**
2. 15×15mm zone: **NO copper on ANY layer** (including GND plane)
3. No components, vias, mounting holes, or metal in zone
4. Battery, headers, USB connectors: at least 15mm from antenna
5. If using IPEX: microstrip from module to connector, keep <10mm

### Ground Plane Effect
- PCB antenna needs ground plane to radiate effectively
- Minimum ground plane: 20×40mm (one side of antenna)
- Larger ground plane → better efficiency (up to ~70×60mm)

---

## RF Shielding

### When to Shield
- Multiple radios on same board (WiFi + BLE + LoRa)
- Sensitive analog nearby (audio, precision ADC)
- Compliance testing shows emissions issues

### Shield Can
- SMD shield frame + removable lid
- Connect to GND plane with vias every 2mm around perimeter
- Leave gap for antennas (shield does NOT cover antenna zone)

### PCB-Level Isolation
- Stitching vias between RF and digital sections
- No traces crossing between RF and digital without filtering
- Separate LDO/DC-DC for RF rail (clean power)

---

## Common RF Issues & Fixes

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Poor range | Antenna mismatch | VNA tune matching network |
| Poor range | Copper in keep-out zone | Clear all layers in antenna zone |
| Poor range | Battery blocking antenna | Move battery away from antenna |
| Intermittent | Poor GND under RF trace | Ensure continuous reference plane |
| EMI fails | Harmonics from PA | Add low-pass filter at antenna |
| Desense | Transmitter leaking into receiver | Better isolation, separate antennas |

---

## FCC/CE RF Compliance Quick Guide

### Intentional Radiator (WiFi/BLE/LoRa)
- **FCC Part 15.247**: 2.4GHz, 1W max, frequency hopping or DTS
- **CE EN 300 328**: 2.4GHz wideband, 100mW EIRP
- **CE EN 300 220**: Sub-GHz SRD, duty cycle limits

### Pre-Compliance Checklist
- [ ] Antenna is the only radiating element (no cables acting as antennas)
- [ ] Shield over digital section
- [ ] Ferrite beads on all cables leaving the board
- [ ] No clock harmonics in the RF band
- [ ] Power supply filtered (common-mode choke)
