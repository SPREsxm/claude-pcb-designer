# MCU Platform Quick Reference

## Platform Selection Matrix

| Platform | Core | Max MHz | Flash | SRAM | WiFi | BLE | 5V Tolerant | Eco-system | Best For |
|----------|------|:---:|-------|------|:---:|:---:|:---:|------------|----------|
| ESP32-S3 | Xtensa LX7 | 240 | 16MB | 512KB | ✓ | ✓ | ✗ | ESP-IDF, Arduino | IoT, WiFi/BLE, AI |
| ESP32-C3 | RISC-V | 160 | 4MB | 400KB | ✓ | ✓ | ✗ | ESP-IDF, Arduino | Low-cost IoT |
| ESP32-C6 | RISC-V | 160 | 8MB | 512KB | ✓ | ✓* | ✗ | ESP-IDF | WiFi6 + Thread/Zigbee |
| STM32F405 | Cortex-M4F | 168 | 1MB | 192KB | ✗ | ✗ | ✓(5V) | STM32Cube, HAL | Industrial, DSP |
| STM32F103 | Cortex-M3 | 72 | 512KB | 64KB | ✗ | ✗ | ✓(5V) | STM32Cube, libopencm3 | General purpose |
| STM32H743 | Cortex-M7 | 550 | 2MB | 1MB | ✗ | ✗ | ✗ | STM32Cube | High-perf, GUI, DSP |
| STM32G0 | Cortex-M0+ | 64 | 512KB | 128KB | ✗ | ✗ | ✓(5V) | STM32Cube | Low-power, low-cost |
| nRF52840 | Cortex-M4F | 64 | 1MB | 256KB | ✗ | ✓* | ✗ | nRF Connect, Zephyr | BLE mesh, Thread |
| nRF5340 | Cortex-M33×2 | 128 | 1MB | 512KB | ✗ | ✓* | ✗ | nRF Connect, Zephyr | Advanced BLE, LE Audio |
| nRF54L15 | Cortex-M33 | 128 | 1.5MB | 256KB | ✗ | ✓* | ✗ | Zephyr | Next-gen BLE, ultra-low power |
| RP2040 | Cortex-M0+×2 | 133 | 16MB ext | 264KB | ✗ | ✗ | ✗ | Pico SDK, Arduino | Low-cost, PIO flexible I/O |
| RP2350 | Cortex-M33/RISC-V | 150 | 16MB ext | 520KB | ✗ | ✗ | ✗ | Pico SDK | Secure, OTP, RISC-V |
| CH32V203 | RISC-V | 144 | 256KB | 64KB | ✗ | ✗ | ✓(5V) | MounRiver | Budget RISC-V, USB |
| CH32V307 | RISC-V | 144 | 512KB | 64KB | ✗ | ✗ | ✓(5V) | MounRiver | Ethernet + USB |
| CH582 | RISC-V | 60 | 512KB | 32KB | ✗ | ✓ | ✗ | MounRiver | Budget BLE |
| ATmega328P | AVR | 16 | 32KB | 2KB | ✗ | ✗ | ✓(5V) | Arduino | Simple, 5V, hobby |
| ATtiny85 | AVR | 20 | 8KB | 512B | ✗ | ✗ | ✓(5V) | Arduino | Tiny, simple, 5V |
| BL616 | RISC-V | 320 | 4MB | 480KB | ✓ | ✓ | ✗ | Bouffalo SDK | WiFi6 + BLE + Zigbee |

---

## ESP32 Family

### ESP32-S3 (Recommended for New Designs)
- Dual-core Xtensa LX7 @ 240MHz
- WiFi 4 (802.11 b/g/n), BLE 5.0
- 45 GPIOs, USB OTG native, Octal SPI PSRAM
- Vector instructions for AI/ML acceleration
- **Modules**: WROOM-1 (PCB ant), WROOM-1U (IPEX), MINI-1 (compact)

### ESP32-S3 Pin Allocation Tips
```
Always:
  GPIO0 → BOOT button (pull-up + button to GND)
  EN → RC delay (10kΩ+1µF)
  GPIO3 → JTAG (do not use if debugging needed)

Internal Flash Pins (DO NOT USE):
  GPIO26-32: Octal PSRAM/Flash (varies by module config)

Safe GPIOs for General Use:
  GPIO1-2, GPIO4-9, GPIO10-18, GPIO21, GPIO33-48

Avoid (strapping pins):
  GPIO0 (boot), GPIO46 (log), GPIO3 (JTAG), GPIO45/46 (VDD_SPI)
```

### ESP32 Minimum Circuit
```
3V3 ── 10µF ──┬── VDD3P3(pin2)
              ├── VDD3P3_CPU
              └── 0.1µF at each VDD pin

EN(pin3) ── 10kΩ ── 3V3  (pull-up)
          └── 1µF ── GND   (RC delay ~10ms)

IO0(pin27) ── 10kΩ ── 3V3  (pull-up for normal boot)
            └── Button ── GND  (press for download mode)

IO46(pin18) ── internal VDD_SPI (do not pull up/down externally)
```

---

## STM32 Family

### F1 Series (Cortex-M3, General Purpose)
- **STM32F103C8T6** ("Blue Pill" MCU): 64KB Flash, 20KB RAM, 72MHz
- 5V-tolerant I/O (great for interfacing with 5V sensors)
- CAN, USB, 2×SPI, 2×I2C, 3×UART
- Package: LQFP-48

### F4 Series (Cortex-M4F, DSP)
- **STM32F405RGT6**: 1MB Flash, 192KB RAM, 168MHz, FPU
- 3×SPI, 3×I2C, 4×UART, 2×CAN, USB OTG
- Package: LQFP-64

### G0 Series (Cortex-M0+, Budget)
- **STM32G070RBT6**: 128KB Flash, 36KB RAM, 64MHz
- 5V-tolerant I/O, USB-C PD capable
- Package: LQFP-64

### STM32 Boot Circuit
```
BOOT0 ── 10kΩ ── GND  (boot from Flash)
NRST ── 10kΩ ── 3V3  (pull-up)
      └── Button ── GND  (reset button)

SWD: SWCLK + SWDIO + GND (3-pin programming)
```

---

## Nordic nRF52/nRF53/nRF54

### nRF52840 (BLE 5.4 + Thread/Zigbee)
- Cortex-M4F @ 64MHz, 1MB Flash, 256KB RAM
- USB 2.0, NFC-A, 12-bit ADC
- Package: QFN-73 (7×7mm), WLCSP

### nRF Design Notes
- **DEC**: special decoupling (not just 0.1µF — follow datasheet exactly)
- **DCDC**: enable internal DC-DC for lower power (LC filter on DCC/DEC pins)
- **NFC**: antenna on dedicated pins (can be used as GPIO if NFC disabled)
- **32MHz crystal**: required for radio operation (32.768kHz optional for low-power timing)

---

## RP2040 / RP2350 (Raspberry Pi)

### RP2040
- Dual Cortex-M0+ @ 133MHz (default), overclockable
- 264KB SRAM, NO internal Flash (external QSPI required)
- Unique: **PIO** (Programmable I/O) — 8 state machines for custom protocols
- USB 1.1, 2×UART, 2×SPI, 2×I2C
- Package: QFN-56 (7×7mm)

### RP2040 Design Notes
- **External Flash**: W25Q128JV (16MB) or similar QSPI
- QSPI traces: length-match CLK+DO+DI+CS to ±25mil
- **Crystal**: 12MHz fundamental
- **Pico SDK**: C/C++ with CMake

---

## Pin Assignment Quick Tips

### Don't Use These Pins for GPIO (Without Careful Reading)
```
ESP32:    GPIO0, GPIO2, GPIO5, GPIO12, GPIO15 (strapping)
          GPIO26-32 (PSRAM/Flash — depends on module config)

STM32F1:  PA13, PA14 (SWD — can use as GPIO if SWD disabled)
          PB2 (BOOT1)

nRF52840: P0.09, P0.10 (NFC — can use as GPIO if NFC disabled)

RP2040:   All GPIOs are equal (except QSPI bus for flash)
```

### Always Bring Out
```
- 1x UART (TX, RX, GND) — serial console
- SWD/JTAG (SWCLK, SWDIO, GND) — programming + debug
- BOOT/RESET buttons
- At least 1 LED (for blink = alive indication)
- At least 1 spare GPIO to test pad
```
