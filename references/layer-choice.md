# 2-Layer vs 4-Layer PCB: Decision Guide

## Quick Decision Matrix

| Factor | 2-Layer | 4-Layer |
|--------|---------|---------|
| **Cost (5pcs, 50×50mm)** | ~¥5 ($0.70) | ~¥30 ($4) |
| **Cost (5pcs, 100×100mm)** | ~¥20 ($3) | ~¥80 ($12) |
| **Signal integrity** | Fair | Good |
| **EMI / EMC** | Harder to control | Easier (solid GND plane) |
| **Routing difficulty** | High (no dedicated planes) | Low (2 internal layers free up routing) |
| **Power distribution** | Must route wide traces | Dedicated power plane |
| **Impedance control** | Hard (no reference plane) | Easy (ref plane on L2 or L3) |
| **Suitable for** | Simple MCU, low-speed, prototype | ESP32, RF, high-speed, production |

## Recommended Stackups

### 2-Layer (JLCPCB default: JLC2313)
```
────────── Top (Signal + Power)
  1.6mm FR4
────────── Bottom (GND fill + Signal)
```
- Pour GND on bottom. Route critical signals on top.
- Jumpers (0Ω resistors) can bridge gaps in GND pour.
- Keep high-speed traces short and over GND pour.

### 4-Layer (JLCPCB: JLC7628)
```
────────── L1: Signal (Top)
  Prepreg
────────── L2: GND (continuous)
  Core
────────── L3: Power (3.3V pour) + signals
  Prepreg
────────── L4: Signal (Bottom)
```
- L1 signals reference L2 GND → clean return paths
- L3 power plane provides low-impedance distribution
- This is the standard JLCPCB 4-layer stackup

## When to Go 4-Layer

Strongly consider 4-layer when:
1. **ESP32 / WiFi / BLE** on board — poor grounding causes radio issues
2. **Multiple SPI buses** running at >20 MHz
3. **Mixed analog + digital** — dedicated planes isolate noise
4. **USB high-speed** (480 Mbps)
5. **Dense board** with < 10mm × 10mm and > 30 components
6. **Production run** > 100 pcs — the per-board cost difference shrinks at volume

## When 2-Layer Is Fine

Stick with 2-layer for:
1. **Simple MCU boards** (Arduino Nano, STM32F103, ATmega)
2. **First prototype** — iterate fast, upgrade to 4L for v2
3. **Cost-sensitive** products in high volume
4. **Low-speed designs** (I2C, UART, < 10MHz SPI)
5. **Through-hole** or hand-solderable designs

## Real-World Example: Rocket Black Box

| Revision | Layers | Reasoning |
|----------|--------|-----------|
| **v0.1 (prototype)** | 2-layer | Test layout, verify sensor placement, cost ¥5 per board |
| **v1.0 (flight)** | 4-layer | ESP32 WiFi reliability, clean sensor signals, production quality |

The v0.1 prototype on 2-layer lets you:
- Verify the schematic is correct
- Test sensor communication and sampling
- Check mechanical fit
- Identify layout issues before investing in 4-layer

Then v1.0 on 4-layer gives you:
- Reliable WiFi for data download
- Clean SPI signals at 40 MHz
- Better EMI performance (won't interfere with other rocket electronics)
