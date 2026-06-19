# Testing & Debugging for PCB Design

## Test Point Strategy

### Minimum Test Points (Every Board)
| Net | Purpose | Pad Size |
|-----|---------|:---:|
| GND | Reference, probe clip | 2.0mm |
| 3V3 | Power verification | 1.5mm |
| UART TX | Serial debug output | 1.0mm |
| UART RX | Serial command input | 1.0mm |
| EN / RESET | Manual reset | 1.0mm |
| BOOT / IO0 | Bootloader entry | 1.0mm |

### Recommended Additional Test Points
| Net | Purpose |
|-----|---------|
| All power rails | Verify voltage levels |
| SPI MOSI/MISO/SCLK | Bus debug with logic analyzer |
| I2C SDA/SCL | Bus debug |
| Key GPIOs | Signal verification |
| Battery voltage (post-divider) | ADC calibration |

### Test Point Physical Design
```
             ┌────────┐
Probe pad:   │  □□□□  │  ≥1.0mm diameter
             │  □□□□  │
             └────────┘
             
Silkscreen:  "3V3"  ← Label every test point
```

- Place on one side (bottom preferred) for test fixture access
- No components within 3mm of test pad (probe clearance)
- Don't place under connectors or modules
- SMD test point component: e.g., Harwin S1751-46R (1.8mm pad)

---

## Debug Interfaces

### SWD (ARM Cortex-M / ESP32-S3)
```
MCU ── SWCLK ────┬── 10kΩ pull-up ── 3V3
     ── SWDIO ────┤
     ── GND ──────┤
                   └── 4-pin 1.27mm header
```
- Standard 2×2 or 1×4 1.27mm pitch header
- Keep traces < 50mm
- For ESP32-S3: GPIO39(TCK), GPIO40(TMS), also supports JTAG

### JTAG (Full)
```
MCU ── TMS ────┬── 10kΩ pull-up ── 3V3
     ── TDI ────┤
     ── TDO ────┤
     ── TCK ────┤
     ── GND ────┘
                └── 2×5 1.27mm header (ARM standard)
```

### Serial Console (Every ESP32 Board)
```
ESP32 U0TXD ──────────── CH340X RXD (or test point)
ESP32 U0RXD ──────────── CH340X TXD (or test point)
```
- Always bring UART to a header or USB-UART IC
- This is your lifeline when everything else fails

---

## Production Testing

### ICT (In-Circuit Test)
- Bed-of-nails fixture with spring-loaded pogo pins
- Tests: shorts, opens, resistance, capacitance, diode polarity
- **Requires test pads on every net** (one per net is sufficient)
- Test pad pattern: 100mil (2.54mm) pitch grid for standard probes

### Flying Probe
- No fixture needed (motorized probes)
- Slower per board, good for prototypes and small runs
- Same test coverage as ICT

### Functional Test
```
1. Power up → check all rails within ±5%
2. Bootloader → verify MCU responds on UART
3. Self-test firmware → check peripherals
4. RF test → check RSSI at known distance
5. LED blinks pattern → visual pass/fail
```

### Test Firmware Features
- UART command interface
- Read all sensor IDs (WHO_AM_I registers)
- Toggle all GPIOs
- Read ADC values
- Self-test all peripherals
- Report PASS/FAIL over UART

---

## Programming Strategy

### Pre-Programming (Socket)
- Program MCU before placement
- Use gang programmer for volume
- Label programmed ICs clearly
- Risk: ESD damage, bent pins

### ISP (In-System Programming)
- Program after assembly via SWD/JTAG/UART
- Pros: easier logistics, firmware updates possible
- Cons: needs header on board, slower per board

### Over-the-Air (OTA)
- ESP32 OTA via WiFi/BLE
- STM32 OTA via Ethernet/CAN
- Requires initial bootloader pre-programmed

---

## Debugging Common Issues

### Board Doesn't Power Up
1. Check VIN at connector
2. Check after reverse-polarity protection
3. Check regulator output
4. Check for shorts (thermal camera or IPA)

### MCU Not Booting
1. Check EN/RESET pin level
2. Check BOOT pin level
3. Check crystal oscillation (oscilloscope)
4. Check UART for boot messages

### Sensor Not Responding
1. Verify power at sensor VDD
2. Check I2C/SPI with logic analyzer
3. Read WHO_AM_I register
4. Check pull-up resistors present
5. Check CS line toggling

### RF Range Poor
1. Verify antenna keep-out zone clear
2. Check antenna matching (VNA)
3. Check power supply noise (oscilloscope on VDD)
4. Check for metal objects near antenna
