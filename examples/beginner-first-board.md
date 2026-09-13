# Example: A Safe First Board

For a first board, optimize for learning and debuggability rather than minimum
size or cost.

## Recommended First Project

- USB-C powered sensor board.
- One low-pin-count MCU module or a large-pitch MCU package.
- One I2C sensor and one SPI sensor.
- 3.3 V regulator with generous input/output capacitance.
- Exposed test points for 5 V, 3.3 V, ground, reset, boot, and UART.
- Two-layer board with a solid ground pour on the bottom.
- No lithium battery, mains, RF power amplifier, or high-current load.

## First-Board Rules

1. Start with a known-good module or reference design.
2. Put test access on every rail and every debug signal.
3. Use larger packages and do not mix several fine-pitch parts on the first build.
4. Keep the power path and ground return visible and short.
5. Add series resistors or jumpers for optional signals.
6. Add polarity and orientation marks that remain visible after assembly.
7. Review the exact footprint against the datasheet before ordering.
8. Order a small batch and inspect one board under magnification before power.

## Bring-Up Order

1. Inspect assembly and check for shorts.
2. Apply a current-limited 5 V input without the MCU installed if the design
   allows it.
3. Verify 3.3 V and ground.
4. Install the MCU and verify reset, boot, clock, and programming.
5. Test the I2C bus at low speed.
6. Test the SPI bus at low speed, then increase gradually.
7. Record every measurement and every failure.

## What Not to Learn On

- mains voltage;
- lithium battery charging;
- high-power radio transmitters;
- dense BGA or DDR routing;
- safety-critical control;
- medical, automotive, aviation, or space hardware.

Use a qualified review and the applicable standards for those projects.
