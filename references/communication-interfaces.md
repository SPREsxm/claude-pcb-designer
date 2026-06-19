# Communication Interfaces: Layout & Design Rules

## UART

### Standard UART
- Single-ended, 3.3V or 5V logic level
- Cross TX→RX between devices
- Baud rates: 9600 to 3Mbps typical for MCU UART
- Pull-up on RX (10kΩ) to prevent floating when unconnected

### Layout
- Non-critical routing (6mil width/space OK)
- Keep away from high-speed clocks (>10MHz)
- Max length: ~1m at 115200 baud, shorter for higher rates

---

## I2C

### Bus Design
```
Speed Modes:
Standard: 100kHz, max bus capacitance 400pF
Fast:     400kHz, max bus capacitance 400pF
Fast+:    1MHz,   max bus capacitance 550pF
```

### Pull-Up Calculation
```
Rp(min) = (Vcc - Vol(max)) / Iol
         = (3.3 - 0.4) / 0.003 = 967Ω → use ≥1kΩ

Rp(max) = tr / (0.8473 × Cbus)
         = 300ns / (0.8473 × 100pF) ≈ 3.5kΩ
         
Typical: 4.7kΩ (standard mode), 2.2kΩ (fast mode)
```

### I2C Best Practices
- One pair of pull-ups per bus (NOT per device)
- Pull-ups near the middle of the bus if possible
- Series resistors (50-100Ω) at each device for hot-swap protection
- Keep total bus length < 1m (capacitance limited)

### Layout
- Route SDA and SCL together (but not as diff pair)
- Keep away from switching nodes (DC-DC, PWM)
- Don't run parallel to SPI clock

---

## SPI (Serial Peripheral Interface)

### Electrical
- Push-pull drivers, no pull-ups needed (except MISO which can be open-drain)
- Speeds: 1-50MHz on MCUs
- 4-wire (SCLK, MOSI, MISO, CS) + additional CS per device

### High-Speed SPI (>20MHz)
- 22Ω series termination at driver (MCU) for MOSI and SCLK
- Star topology for shared bus
- Length match MOSI/SCLK to each device within ±2mm
- Dedicated CS per device (no resistor needed)
- Max 1 via per signal

### Layout
| Parameter | ≤20MHz | >20MHz |
|-----------|--------|--------|
| Trace width | 6mil | 6mil |
| Spacing | 12mil (2×W) | 18mil (3×W) |
| Max length | 100mm | 50mm |
| Termination | Optional | 22Ω at source |

---

## CAN Bus

### Physical Layer
```
MCU_CAN_TX ── CAN Transceiver ── CANH ──┬── 120Ω ──┬── CANH ── Transceiver
MCU_CAN_RX ── (e.g., SN65HVD230) ── CANL ──┴── 120Ω ──┴── CANL
```
- Differential: CANH (3.5V dominant, 2.5V recessive), CANL (1.5V dominant, 2.5V recessive)
- 120Ω termination at both ends of bus (NOT at every node)
- Stub length from bus to transceiver: < 30cm (1Mbps), < 3cm (5Mbps)

### Common CAN Transceivers
| Part | Speed | Standby | 3.3V I/O | Package |
|------|:---:|:---:|:---:|---------|
| SN65HVD230 | 1Mbps | ✓ | ✓ | SOIC-8 |
| MCP2551 | 1Mbps | ✗ | 5V | SOIC-8 |
| TJA1050 | 1Mbps | ✗ | 5V | SOIC-8 |
| TCAN1042 | 5Mbps | ✓ | ✓ | SOIC-8 |

### Layout
- CANH/CANL as differential pair
- 120Ω termination at each physical end of the bus
- Common-mode choke (e.g., ACT45B-510) for EMI on long cables

---

## RS-485 / RS-422

### Key Differences
| | RS-485 | RS-422 |
|---|--------|--------|
| Topology | Multi-drop (up to 32/256 nodes) | Point-to-point or multi-drop (1 driver, 10 receivers) |
| Duplex | Half or Full | Full |
| Termination | 120Ω both ends | 100Ω at receiver |

### Fail-Safe Biasing
```
VCC ── Rb1 ──┬── A (non-inverting)
              ├── 120Ω
             Rb2 ──┬── B (inverting)
                   │
                  GND
Rb1 = Rb2 = 560Ω-1kΩ  ensures idle state is well-defined
```

### Common RS-485 Transceivers
| Part | Speed | Duplex | Nodes | Package |
|------|:---:|:---:|:---:|---------|
| MAX485 | 2.5Mbps | Half | 32 | SOIC-8 |
| SN65HVD75 | 20Mbps | Half | 256 | SOIC-8 |
| MAX3485 | 10Mbps | Half | 256 | SOIC-8 |

---

## USB

### USB 2.0 Full Speed (12Mbps)
- 90Ω differential impedance
- D+/D- matched within 5mil
- Max length: 1.5m (standard cable)
- ESD at connector, not at IC

### USB 2.0 High Speed (480Mbps)
- Impedance CRITICAL: 90Ω ±10%
- Tight length matching: ±5mil
- No vias if possible (1 via max)
- Solid GND reference plane (no splits under USB traces)

### Layout Checklist
- [ ] 90Ω differential pair from MCU to connector
- [ ] ESD diodes (e.g., LESD5D5.0CT1G) at connector
- [ ] ESD diode GND → plane with short, wide trace
- [ ] No stubs on D+/D- lines
- [ ] Series common-mode choke optional (for EMI)

---

## Ethernet (100BASE-TX)

### RMII Interface (MCU to PHY)
```
MCU ── 50MHz CLK, TXD[1:0], TX_EN, RXD[1:0], CRS_DV, MDC, MDIO ── PHY
```
- Single-ended, 50Ω recommended
- Length match data to clock within ±25mil
- MDC/MDIO: I2C-like, 2.2kΩ pull-ups

### MDI Interface (PHY to Magnetics)
```
PHY ── TX+/-, RX+/- ── Magnetics ── RJ45
```
- 100Ω differential pairs
- Place magnetics close to RJ45 (<25mm)
- Bob Smith termination: 75Ω + 1nF to GND through HV cap

### Common Ethernet PHYs
| Part | Speed | Interface | Package |
|------|:---:|-----------|---------|
| LAN8720A | 10/100M | RMII | QFN-24 |
| DP83848 | 10/100M | RMII/MII | LQFP-48 |
| W5500 | 10/100M | SPI (HW TCP/IP) | LQFP-48 |

---

## LVDS / MIPI DSI

### LVDS
- 100Ω differential (between pair)
- Pair-to-pair: 100mil spacing typical
- Ground reference: continuous plane
- Intra-pair skew: < 10mil

### MIPI D-PHY (Camera/Display)
- Multiple data lanes + 1 clock lane
- Lane-to-lane skew: < 100ps
- Intra-pair skew: < 5ps
- Microstrip or stripline, 100Ω differential
- Equalization may be needed > 1Gbps/lane

---

## SDIO / eMMC

### SDIO (up to 208MHz, SDR104)
- CLK: series term 22-33Ω near host
- CMD/DAT[0:3]: 50Ω, length-matched to CLK ±20mil
- Pull-ups: 10-50kΩ on DAT[3:0], CMD (for SD card detection)
- Keep traces under 50mm

### eMMC (HS400, 200MHz DDR)
- Same as SDIO layout rules
- DAT strobe (DS) matched to data byte lane
- VCCQ (1.8V/3.3V IO voltage): clean, decoupled

---

## I2S / PCM Audio

### I2S Bus
```
Master ── BCLK, LRCK (WS), DATA ── Slave
Master ── MCLK (optional, 256×Fs) ── Slave
```
- MCLK: most sensitive to jitter, keep clean
- BCLK: length matched to DATA within ±25mil
- Keep digital audio traces away from analog audio section
- Clock routing: star from master, not daisy-chained
