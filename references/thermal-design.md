# Thermal Design

## Power Budget

### Step 1: Power Budget Table
Create a table of every power-consuming component:

| Designator | Component | Vsupply | Imax | Pmax(mW) | Duty Cycle | Pavg(mW) |
|------------|-----------|:---:|:---:|:---:|:---:|:---:|
| U3 | ESP32-S3 | 3.3V | 300mA | 990 | 30% | 300 |
| U4 | ICM-42688 | 3.3V | 3mA | 10 | 100% | 10 |
| U7 | MT2492 | 5V | 500mA | 250 (loss) | 100% | 250 |
| ... | ... | ... | ... | ... | ... | ... |
| **Total** | | | | | | **∑Pavg** |

### Step 2: Identify Hot Spots
- Any component with Pd > 500mW needs thermal attention
- Multiple components in same area → cumulative heating

---

## Thermal Resistance

### Junction Temperature
```
Tj = Ta + Pd × θJA

Where:
Tj  = junction temperature (°C)
Ta  = ambient temperature inside enclosure (°C)
Pd  = power dissipation (W)
θJA = junction-to-ambient thermal resistance (°C/W)
```

### Typical θJA Values
| Package | θJA (min Cu) | θJA (1cm² Cu) | θJA (4cm² Cu) |
|---------|:---:|:---:|:---:|
| SOT-23 | 250 | 180 | 130 |
| SOT-23-5 | 200 | 150 | 110 |
| SOT-223 | 60 | 40 | 25 |
| SOIC-8 | 150 | 100 | 70 |
| QFN-20 (exposed pad) | 50 | 30 | 20 |
| QFN-48 (exposed pad) | 35 | 22 | 15 |
| TO-252 (DPAK) | 50 | 30 | 20 |

### Ambient Temperature Reality Check
```
Outside: -20 to 40°C
Inside enclosure: +15 to 30°C above ambient (no ventilation)
  → Ta(inside) = 55-70°C on a hot day

Design for Ta = 70°C minimum for outdoor/automotive!
```

---

## Copper Area for Heatsinking

### Rule of Thumb
```
1oz Cu, natural convection:
  θCA ≈ 50°C/W per cm² of copper area (single layer)
  θCA ≈ 30°C/W per cm² (2oz Cu)
  θCA ≈ 25°C/W per cm² (top + bottom connected by vias)
```

### Thermal Via Array
```
Under thermal pad (QFN, DFN):
  ┌───┬───┬───┐
  │ ○ │ ○ │ ○ │  ← 0.3mm vias, 1mm pitch
  ├───┼───┼───┤
  │ ○ │ ○ │ ○ │  ← Connected to:
  ├───┼───┼───┤     L1: thermal pad
  │ ○ │ ○ │ ○ │     L2: GND plane
  └───┴───┴───┘     L4: copper pour (heatsink)
```
- Via hole: 0.3mm
- Via pad: 0.6mm
- Pitch: 1mm
- Fill vias with solder or leave unfilled (thermal epoxy optional)

---

## Application Examples

### LDO Thermal Check
```
AMS1117-3.3, SOT-223, 5V→3.3V, Iload=800mA
Pd = (5 - 3.3) × 0.8 = 1.36W
Tj = 50 + 1.36 × 40 = 104°C (with 1cm² Cu)
Tj = 50 + 1.36 × 60 = 132°C (minimal Cu) ← TOO HOT!

Fix: Add 4cm² Cu → θJA ≈ 25°C/W → Tj = 84°C ✓
Or: Use DC-DC buck (efficiency ~90%) → Pd ≈ 0.3W only
```

### Battery Charger
```
TP4056, SOP-8, 5V USB input, 4.0V battery, 800mA charge
Pd = (5 - 4.0) × 0.8 = 0.8W
TP4056 has thermal regulation → reduces current when Tj > 120°C
Solution: 4cm² Cu pour under IC → keeps Tj < 100°C at full current
```

### DC-DC Converter
```
MT2492, SOT-23-6, 5V→3.3V, Iout=1A, efficiency ~90%
Ploss = 3.3 × 1.0 × (1/0.9 - 1) ≈ 0.37W
Most loss is in the inductor and IC switching
Keep switch node small, use wide traces for power path
```

---

## Enclosure Thermal Management

### Passive Cooling
- Ventilation holes: top + bottom for convection airflow
- Mount hot components near enclosure walls (conduct to case)
- Thermal pads/gap filler to conduct heat to metal enclosure

### Active Cooling
- Fan: > 0.5W total board power = consider fan
- Fan size: 20mm-40mm for small embedded boards
- Fan control: PWM + tachometer feedback

### Temperature Monitoring
- On-board NTC thermistor near hot spots
- MCU ADC reads temperature, can throttle or shutdown
- Example: 10kΩ NTC, B=3435, voltage divider with 10kΩ to VCC

---

## Quick Thermal Checklist
- [ ] Power budget calculated for all ICs
- [ ] Hot spots identified (>500mW dissipation)
- [ ] LDO Pd < 1W (or use DC-DC)
- [ ] Thermal pad ICs have via array to GND plane
- [ ] Copper area under hot ICs maximized
- [ ] Enclosure ventilation considered
- [ ] Tj < 125°C for all ICs at max Ta
