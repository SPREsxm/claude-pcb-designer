# Example: ESP32-S3 Flight Computer

This is a worked planning example, not a production schematic or pin
assignment. Verify every part, pin, and layout decision against current
datasheets and the exact module variant.

## Brief

- 50 mm x 35 mm four-layer data logger and flight computer.
- 1S LiPo with USB-C charging and protection.
- ESP32-S3 module with PCB antenna.
- SPI IMU, SPI accelerometer, SPI magnetometer, I2C barometer, microSD, RGB LED.
- 3.3 V rail with 500 mA peak and 90 mA average.
- Prototype quantity: 10 boards. Enclosure is non-metallic.

## Assumptions

- The radio module's antenna configuration remains unchanged.
- The board is inside a non-metallic enclosure with at least 15 mm of clear
  space in front of the antenna.
- Temperature is 5-40 C for the first prototype.
- MicroSD is not written continuously during peak radio transmission.

## Block Diagram

```text
USB-C --> protection/charger --> 1S LiPo --> protection --> 3V3 regulator
   |                                                             |
   +--> USB data / debug                                     3V3 rail
                                                                 |
                    +----------------+---------------------------+----------------+
                    |                |                           |                |
               ESP32-S3          SPI sensors               I2C barometer       microSD
                    |                |                           |                |
                 RGB LED       CS per device              pull-ups        decoupling
```

## Power Budget

Use the CSV calculator with realistic duty cycles:

| Rail | Load | Voltage | Peak current | Duty | Average power |
|---|---|---:|---:|---:|---:|
| 3V3 | ESP32-S3 Wi-Fi active | 3.3 V | 350 mA | 25% | 289 mW |
| 3V3 | Sensors | 3.3 V | 10 mA | 100% | 33 mW |
| 3V3 | microSD write | 3.3 V | 100 mA | 10% | 33 mW |
| 3V3 | LED and misc. | 3.3 V | 20 mA | 20% | 13 mW |
| 3V3 | Regulator loss | - | - | - | 40-90 mW |

Confirm the regulator's efficiency at light load, its startup behavior with the
LiPo, and its dropout as the battery approaches cutoff.

## Proposed Stackup

```text
L1  Signal + components
L2  Continuous ground reference
L3  Power and slow signals
L4  Signal + ground fill
```

Rules:

- Keep the antenna region clear on every copper and metal layer as required by
  the exact module datasheet.
- Reference all fast SPI, USB, and clock signals to continuous L2.
- Keep the switch loop and input/output capacitors tight at the regulator.
- Do not route under the crystal, RF matching network, or sensitive analog
  nodes.
- Stitch ground vias around the RF section, connector returns, and board edge.

## Placement Order

1. Board outline, mounting holes, USB-C, battery connector, and antenna edge.
2. ESP32-S3 module with antenna facing outward.
3. Charger, protection, regulator, and power entry.
4. microSD and its decoupling.
5. Sensors and their mechanical alignment.
6. Debug header, test points, and LED.

## Interface Plan

| Interface | Devices | Design notes |
|---|---|---|
| SPI0 | IMU, accelerometer, magnetometer | Dedicated CS per device; series damping may be needed at the source |
| I2C0 | Barometer | One pull-up pair per bus; verify bus capacitance |
| SDIO/SPI | microSD | Verify voltage, pull-ups, decoupling, and card-detect behavior |
| USB | Programming/debug | ESD at the connector; controlled differential impedance |
| UART | Console/recovery | Bring to test pads or a header |
| SWD/JTAG | Programming/debug | Keep accessible after assembly |

Do not copy the table into a schematic without checking the exact ESP32-S3
module pinout and GPIO constraints.

## Test Plan

- [ ] Input current before installing the SD card.
- [ ] 3V3 rail under idle, radio, and SD-write load.
- [ ] Reset, boot, programming, and recovery modes.
- [ ] SPI chip IDs for each sensor.
- [ ] I2C barometer ID and pressure sanity check.
- [ ] microSD read/write integrity.
- [ ] Wi-Fi range in the final enclosure, antenna facing the intended direction.
- [ ] Thermal soak at maximum ambient and peak load.
- [ ] Brownout behavior near battery cutoff.

## Release Actions

1. Run ERC and DRC with the selected supplier's rules.
2. Export Gerbers, Excellon drill, BOM, and CPL.
3. Run `scripts/audit_release.py <release-dir> --layers 4`.
4. Verify BOM/CPL rotations against the assembler's library.
5. Record the stackup, impedance targets, and any approved deviations.

## Risk Register

| Risk | Why it matters | Mitigation |
|---|---|---|
| Antenna keep-out violated | Radio range loss | Mechanical and copper keep-out review |
| SD write current overlaps radio peak | Rail droop or brownout | Bulk capacitance and load scheduling |
| SPI reflections at high clock | Data errors | Start slower, use source termination if measured ringing is excessive |
| Regulator thermal rise | Shutdown in sealed enclosure | Efficiency and thermal test at maximum ambient |
| Battery fault | Fire or damage | Protection, fault testing, and qualified review |
