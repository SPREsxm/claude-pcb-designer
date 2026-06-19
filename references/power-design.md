# Power Design: LDO, DC-DC, Battery Management

## LDO Selection

### Step-by-Step
1. **Vout**: what voltage does the load need?
2. **Iload(max)**: maximum load current
3. **Vin(min)**: minimum input voltage (e.g., battery minimum)
4. **Vdropout**: Vin(min) - Vout must be > Vdropout(max)
5. **Pd**: (Vin(typical) - Vout) × Iload
6. **Tj**: Ta + Pd × θJA (must be < 125°C typically)
7. **PSRR**: needed for analog/RF rails (>60dB at ripple frequency)

### LDO Comparison
| Part | Vout | Imax | Vdropout | PSRR | Package | LCSC # |
|------|------|:---:|:---:|:---:|---------|--------|
| AMS1117-3.3 | 3.3V | 1A | 1.1V | 60dB | SOT-223 | C6186 |
| ME6211C33M5G | 3.3V | 500mA | 0.14V | 70dB | SOT-23-5 | C82942 |
| HT7333-1 | 3.3V | 250mA | 50mV | 60dB | SOT-89 | — |
| AP2112K-3.3 | 3.3V | 600mA | 250mV | 65dB | SOT-23-5 | — |
| TPS7A47 (adj) | 1.4-34V | 1A | 300mV | 82dB | QFN-20 | — |

### LDO Thermal Calculation
```
Pd = (Vin - Vout) × Iload
Tj = Ta + Pd × θJA

Example: AMS1117-3.3, 5V→3.3V, 500mA, Ta=50°C
Pd = 1.7 × 0.5 = 0.85W
θJA(SOT-223) ≈ 60°C/W (minimal copper)
Tj = 50 + 0.85 × 60 = 101°C ← OK

With 1cm² Cu pour: θJA ≈ 40°C/W
Tj = 50 + 0.85 × 40 = 84°C ← Better
```

### Power Dissipation Heatsinking
```
Approx θJA vs Copper Area (SOT-223, 1oz):
0mm²   → 60°C/W
25mm²  → 50°C/W
100mm² → 40°C/W
400mm² → 30°C/W
```

---

## DC-DC Converter Selection

### Topology Decision Tree
```
Vin always > Vout? ── YES ── Buck
Vin always < Vout? ── YES ── Boost
Vin can be both?   ── YES ── Buck-Boost or SEPIC
Need isolation?    ── YES ── Flyback / Forward
```

### Buck Converter (Step-Down)
- **Switching frequency**: 500kHz-2MHz typical
- **Inductor choice**: L = (Vin-Vout)×Vout/(Vin×fsw×ΔI×Iout)
- **Output cap**: low ESR ceramic, handle ripple current
- **Layout critical**: switch node loop must be TINY

#### Common Buck ICs
| Part | Vin Range | Vout | Imax | fsw | Package |
|------|-----------|------|:---:|:---:|---------|
| MT2492 | 4.5-16V | Adj | 2A | 500kHz | SOT-23-6 |
| MP1584 | 4.5-28V | Adj | 3A | 1.5MHz | SOIC-8 |
| AP63205 | 3.8-32V | 5V fixed | 2A | 500kHz | SOT-23-6 |
| TPS54331 | 3.5-28V | Adj | 3A | 570kHz | SOIC-8 |

### Boost Converter (Step-Up)
- Output voltage always higher than input
- Watch inrush current at startup
- Commonly used for: 3.7V→5V, 3.7V→12V

### Buck-Boost & SEPIC
- Use when Vin crosses Vout (battery going from 4.2V→3.0V for 3.3V rail)
- More complex, more expensive, higher EMI
- Alternatives: LDO (low current), Boost+LDO cascade

---

## Battery Management

### 1S LiPo/Li-ion (3.7V Nominal)
```
Charger: TP4056 (linear, 1A max), ME4057 (smaller)
Protection: DW01 + FS8205 (overcharge 4.25V, overdischarge 2.5V, short circuit)
Fuel gauge: MAX17048 (I2C, ±1%), BQ27427 (I2C, ±1%)
```

### 2S-4S Li-ion
```
Charger: BQ24610 (1-6S, 10A), BQ25890 (1S, USB PD)
Balancer: BQ769x0 family (3-15S, I2C/SPI)
Gauge: BQ34Z100 (1-16S, impedance track)
```

### Battery Life Estimation
```
Capacity(mAh) × Voltage(V) = Energy(mWh)
Energy(mWh) ÷ Average Power(mW) = Runtime(hours)

Example: 1000mAh 3.7V battery, average 50mA at 3.3V
Energy = 1000 × 3.7 = 3700mWh
Power = 50 × 3.3 = 165mW (load) + 17mW (90% eff) = 182mW
Runtime = 3700 / 182 ≈ 20 hours
```

### Solar Charging
```
Panel ── Schottky ── CN3791 (MPPT) ── Battery
                     CN3791: 4.95-28V input, 1-4S Li-ion
                     MPPT voltage: set via resistor divider
```

### USB Power Delivery (USB PD)
- **5V/3A**: Standard, works with any USB-C
- **9V/3A, 15V/3A, 20V/5A**: Requires PD negotiation
- PD controller ICs: CH224K (sink), FUSB302 (controller), STUSB4500
- ESP32-S3 can do PD via GPIO bit-banging (limited)

---

## Power Distribution on PCB

### Plane vs Star Distribution
```
Plane (preferred):              Star:
┌────────3V3────────┐           ┌─ IC1
│  IC1  IC2  IC3    │           │
│  IC4  IC5  IC6    │         3V3─┼─ IC2
└───────────────────┘           │
                                └─ IC3
Good: low impedance everywhere  Bad: higher impedance, IR drop
```

### Power Trace Width
```
1oz Cu, 10°C rise:
100mA  → 6mil
500mA  → 15mil
1A     → 30mil
2A     → 70mil
3A     → 120mil
5A     → Use copper pour + multiple vias
```

### Decoupling Strategy
```
Per IC:     0.1µF within 5mm of each VDD pin
Per rail:   10µF–47µF near regulator output
Per board:  100µF–470µF at power entry (bulk)
```
