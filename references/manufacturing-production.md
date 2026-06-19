# Manufacturing & Production

## From Prototype to Production

### Quantities and Approaches
| Stage | Qty | Assembly Method | Testing |
|-------|:---:|-----------------|---------|
| Prototype | 5-10 | Hand-solder or manual PnP | Visual + manual |
| Pilot run | 50-100 | Small-batch SMT | Flying probe + manual functional |
| Production | 500+ | Full SMT line | ICT + AOI + functional |

---

## Stencil Design

### Thickness Guidelines
| Component Pitch | Stencil Thickness |
|----------------|:---:|
| ≥0.8mm pitch QFP | 0.15mm |
| 0.5mm pitch QFP/QFN | 0.12mm |
| 0.4mm pitch QFN/BGA | 0.10mm |
| Mixed pitch (common) | 0.12mm with stepped areas |

### Aperture Design
```
Chip passives (0603/0805): 1:1 or slightly reduced (90%)
Fine-pitch QFP: 80-90% width, same length
QFN thermal pad: window-pane pattern (50-60% coverage)
BGA: square with rounded corners, 1:1
```

### Stencil Material
- **Stainless steel**: standard, good for >0.5mm pitch
- **Electropolished**: smoother walls, better paste release for fine pitch
- **Nano-coating**: ultra-smooth, best for <0.4mm pitch

---

## Solder Paste

### SAC305 (Lead-Free, Most Common)
```
Composition: Sn96.5 Ag3.0 Cu0.5
Melting point: 217°C (eutectic)
Reflow peak: 235-250°C
Type 3 (25-45µm powder): good for >0.5mm pitch
Type 4 (20-38µm powder): for fine pitch and small apertures
Type 5 (15-25µm powder): for ultra-fine pitch, stencil printing challenging
```

### Storage
- Refrigerated: 0-10°C, shelf life 6 months
- Warm to room temp before use (4 hours)
- Stir before applying to stencil

---

## Pick-and-Place

### Component Packaging
| Package | Feed Method | Notes |
|---------|------------|-------|
| 0603/0402 passives | 8mm tape, 2mm/4mm pitch | Standard feeder |
| SOT-23, SOD-123 | 8mm tape, 4mm pitch | Standard feeder |
| SOIC-8/14/16 | 12mm/16mm tape | Standard feeder |
| QFP/QFN | 16mm-44mm tape | Standard feeder |
| Tray ICs (large QFP) | Tray feeder | Dedicated tray station |
| Cut tape | Loose piece feeder | Manual placement or custom jig |

### Panelization
```
Individual Board: 50×35mm
Panel: 2×3 array = 6 boards/panel

Panel Options:
- V-score (V-cut): straight lines only, clean edge
- Tab-route (mouse-bites): any shape, rougher edge
- Rails: 10mm on 2-4 sides for handling

Rail Features:
- Tooling holes: 3.2mm diameter (for panel alignment)
- Fiducial marks: 1mm circle + 2mm clearance
- Bad board mark: X on silkscreen
```

### Fiducial Marks
```
 ┌──────────┐
 │  ○       │  1mm Cu circle (no mask)
 │          │  2mm clear zone (no Cu, no silk)
 └──────────┘

Place on:
- Panel rails (global fiducials): 3 minimum, corners
- Near fine-pitch ICs (local fiducials): 2 per IC
```

---

## Reflow Profile

### Lead-Free (SAC305) Profile
```
    T
250 ┤                    ╱╲
235 ┤                   ╱  ╲
217 ┤    ┌─────────────╱    ╲─────  ← Liquidus (60-90s above 217°C)
200 ┤   ╱ ╲                  ╲
150 ┤──╱   ╲──────────────────╲──  ← Preheat (60-120s, 150-190°C)
100 ┤  ╱                       ╲
    └──┴──────┴──────┴──────┴──────→ time
     Preheat  Soak    Reflow  Cool

Cooling: < 4°C/s (fast but controlled)
Total time: 4-7 minutes
```

### Key Temperatures
```
Preheat: 1-3°C/s ramp to 150°C
Soak: 150-190°C, 60-120s (activates flux)
Reflow: >217°C, 60-90s (Peak: 235-250°C)
Cool: <4°C/s to <100°C
```

### Profile Verification
- Thermocouple on board (at hottest and coldest spots)
- Profile board: thermocouples on small passives + large ICs
- Adjust belt speed and zone temps to match profile

---

## Inspection

### Solder Paste Inspection (SPI)
- 3D laser scan of paste deposits
- Checks: volume, area, height, bridging, position offset
- Before component placement

### Automated Optical Inspection (AOI)
- Camera-based inspection after reflow
- Checks: missing components, tombstoning, bridging, solder quality, polarity
- Multiple camera angles for hidden joints

### X-Ray Inspection
- For BGA, QFN, and hidden joints
- Checks: voids (<25% typically acceptable), shorts, opens
- Can be inline (production) or offline (sampling)

---

## Common Assembly Defects

| Defect | Cause | Fix |
|--------|-------|-----|
| Tombstoning (one end lifted) | Uneven heating, pad size mismatch | Match pad sizes, balance thermal mass |
| Solder bridging | Too much paste, fine pitch | Reduce aperture, check stencil alignment |
| Insufficient solder | Too little paste, clogged aperture | Check stencil cleaning, increase aperture |
| Component shift | Uneven heating, convection force | Reduce airflow, check placement accuracy |
| Voiding (BGA/QFN) | Trapped flux, too-rapid ramp | Optimize soak time, reduce peak temp |
| Cold joint | Insufficient heat, contamination | Check profile, clean boards |
| Head-in-pillow (BGA) | Warpage, oxidation | Dry pack storage, optimized profile |

---

## Programming & Test Fixtures

### Programming Jig Design
```
┌──────────────────────────┐
│ Spring-loaded top plate  │
│ ┌──────────────────────┐ │
│ │ Pogo pins (SWD/UART) │ │ ← Spring-loaded test pins
│ └──────────────────────┘ │
│          ┌──┐            │
│          │PC│ ← DUT      │
│          └──┘            │
│ ┌──────────────────────┐ │
│ │ Base plate (alignment)│ │
│ └──────────────────────┘ │
└──────────────────────────┘
```

### Pogo Pin Selection
- **Flat/cone tip**: test pads
- **Spear/crown tip**: plated through-holes
- **Spring force**: 100-200g per pin
- **Travel**: 2-4mm recommended

---

## Packaging & Logistics

### ESD Protection
- All boards in ESD shielding bags
- Pink poly ≠ ESD shielding (only anti-static)
- Use metalized shielding bags (silver/gray)

### Moisture Sensitivity (MSL)
| MSL | Floor Life | Bake Before Reflow |
|:---:|-----------|:---:|
| 1 | Unlimited | No |
| 2 | 1 year | No |
| 2a | 4 weeks | No |
| 3 | 168 hours | After expiry |
| 4 | 72 hours | After expiry |
| 5 | 48 hours | After expiry |
| 6 | Mandatory bake | Always |

Check MSL for every IC — QFN/BGA are often MSL 3-4.

### Shipping
- Boards in ESD bags + desiccant + humidity indicator card
- Vacuum seal bag if MSL > 3
- Box with ESD foam for assembled boards
- Label: part number, revision, quantity, date
