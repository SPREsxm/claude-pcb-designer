# Analog & Mixed-Signal Design

## Op-Amp Selection Guide

### Key Parameters
| Parameter | Precision | General Purpose | High Speed | Low Power |
|-----------|-----------|-----------------|------------|-----------|
| Vos (offset) | <100µV | <5mV | <5mV | <5mV |
| GBW | 1-10MHz | 1-10MHz | >50MHz | <1MHz |
| Slew Rate | 0.5-5V/µs | 0.5-5V/µs | >50V/µs | <1V/µs |
| Iq per amp | 0.5-2mA | 0.2-1mA | 5-20mA | <50µA |
| Noise (1kHz) | <10nV/√Hz | <30nV/√Hz | <5nV/√Hz | <50nV/√Hz |
| Cost | ¥¥¥ | ¥ | ¥¥¥ | ¥¥ |

### Selection Formula
```
Minimum GBW = Gain × Signal Frequency × 10 (for buffers)
Minimum GBW = Gain × Signal Frequency × 100 (for gain stages)
Slew Rate ≥ 2π × f × Vpeak
```

### Common Op-Amps (LCSC/JLCPCB)
| Part | Channels | GBW | Vos | Iq/ch | Package |
|------|:---:|:---:|:---:|:---:|---------|
| LM358 | 2 | 1MHz | 2mV | 0.5mA | SOIC-8 |
| LM324 | 4 | 1MHz | 2mV | 0.5mA | SOIC-14 |
| TL072 | 2 | 3MHz | 3mV | 1.4mA | SOIC-8 |
| OPA2333 | 2 | 350kHz | 2µV | 17µA | SOIC-8 |
| AD8605 | 1 | 10MHz | 65µV | 1mA | SOT-23-5 |
| MCP6002 | 2 | 1MHz | 4.5mV | 100µA | SOIC-8 |

---

## Common Op-Amp Circuits

### Non-Inverting Amplifier
```
          ┌── Rf ──┐
Vin ──────┤+       │
          │  Op-Amp├── Vout
GND ──┐   │-       │
      │   └── Rg ──┘
      └──────────────┘
Gain = 1 + Rf/Rg
```

### Inverting Amplifier
```
Vin ── R1 ──┬── Rf ──┬── Vout
            │-       │
GND ────────┤+       │
            └────────┘
Gain = -Rf/R1
```

### Differential Amplifier
```
V1 ── R1 ──┬── Rf ──┬── Vout
           │-       │
V2 ── R1 ──┤+       │
           └── Rf ──┘
Vout = (V2 - V1) × Rf/R1
Use 0.1% resistors for good CMRR
```

### Low-Pass Filter (Sallen-Key, 2nd Order)
```
Vin ── R ──┬── R ──┬── Vout (to op-amp +)
           │       │
          C1       C2
           │       │
          GND    Output of op-amp (buffer)
fc = 1/(2π × R × √(C1×C2))
Q = √(C1/C2)/2  (set C1=2C2 for Q=0.707, Butterworth)
```

---

## ADC Front-End Design

### Anti-Aliasing Filter
- Low-pass filter before ADC input
- fc ≤ Fs/2 (Nyquist) — in practice: fc ≤ Fs/5 for good alias rejection
- Order: 1st order for slow signals, 2nd-3rd for >Fs/10 bandwidth

### Driving ADC Inputs
- Most SAR ADCs need a driver op-amp to charge the internal sampling capacitor
- Driver must settle within the acquisition time (tACQ)
- Use RC filter between driver and ADC: R=10-100Ω, C=1-10nF

### ADC Reference
- External Vref IC for precision (>10 bits)
- Example: REF3033 (3.3V, 0.2%, 50ppm/°C)
- Place Vref close to ADC, decouple with 10µF + 0.1µF

### ESP32 ADC Notes
- 12-bit SAR, but effective ~9-10 bits due to noise
- Input impedance: low (~100kΩ), needs buffer for high-Z sources
- Max input: 3.3V (use divider for higher voltages)
- Sampling rate: max ~2MSPS (but WiFi/BLE reduce effective rate)
- Use `adc_atten` 11dB for full 0-3.3V range

---

## Current Sensing

### Low-Side Shunt
```
Load ──┬── VCC
       │
       Shunt (Rsense)
       │
       └── GND ────────┤+ OpAmp ├── ADC
                       │-
Vshunt ────────────────┘
```
- Pros: simple, common-mode near GND, cheap op-amp works
- Cons: load not grounded, GND shifted

### High-Side Shunt
```
VCC ── Shunt ──┬── Load
               │
               └── GND
Vshunt across shunt → differential amp or INA
```
- Pros: load grounded, detects shorts to GND
- Cons: needs high-CMRR diff amp or dedicated current-sense amp

### Current Sense Amplifiers
| Part | Type | Vcm Range | Gain | Package |
|------|------|-----------|:---:|---------|
| INA180 | High-side | 0-26V | 20/50/100/200 | SOT-23-5 |
| INA219 | I2C digital | 0-26V | Programmable | SOIC-8 |
| MAX4080 | High-side | 4.5-76V | 20/50/100 | SOIC-8 |
| ACS712 | Hall effect | Isolated | 66-185mV/A | SOIC-8 |

---

## Sensor Signal Conditioning

### Thermocouple (Type K)
- Signal: ~41µV/°C, very low level
- Needs: cold-junction compensation (CJC), instrumentation amp
- Recommended: MAX31855 (SPI, built-in CJC), MAX6675 (SPI, K-type)

### RTD (PT100/PT1000)
- Excitation: constant current source (0.5-1mA)
- Connection: 3-wire or 4-wire (eliminates lead resistance)
- Recommended: MAX31865 (SPI, PT100/PT1000)

### Piezoelectric / IEPE Sensors
- Needs: charge amplifier or high-Z buffer (JFET/CMOS input)
- Bias: AC couple, bias to mid-supply
- Filter: bandpass for frequency range of interest

### Photodiode
- **Photovoltaic mode**: 0V bias, low noise, slow
- **Photoconductive mode**: reverse bias, fast, higher dark current
- Transimpedance amplifier (TIA): Iphoto → Vout = Iphoto × Rf
- Recommended op-amp: low Ib (<10pA), low noise

---

## Analog Layout Rules

### Ground Planes
- Single solid GND plane (don't split into "analog GND" and "digital GND")
- Partition board: analog circuits on one side, digital on the other
- No digital traces crossing over analog section

### Guard Rings
```
Op-amp + input (high-Z): surround with GND ring connected to same potential
     ┌──────────┐
     │ GUARD    │
     │ ┌────┐   │
     │ │ +IN│   │ ← Guard ring prevents leakage currents
     │ └────┘   │
     │ GUARD    │
     └──────────┘
```

### Decoupling
- 0.1µF at each power pin (standard)
- Add 10µF bulk for analog sections
- Ferrite bead on analog VDD for noise filtering
