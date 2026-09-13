# Example: Review Findings

This example shows the expected review style for a hypothetical two-layer
ESP32 board.

## Finding 1

**[Critical] Antenna keep-out contains pull-up resistors**

- Evidence: R12 and R13 are placed inside the module antenna keep-out area.
- Impact: the module datasheet requires a clear keep-out; components and their
  copper alter the antenna match and can substantially reduce range.
- Fix: move the resistors outside the keep-out and restore clear copper on all
  layers as specified by the exact module datasheet.
- Confidence: high if the module is the PCB-antenna variant.

## Finding 2

**[Major] I2C runs parallel to SPI clock for 25 mm**

- Evidence: SDA/SCL are routed adjacent to SCLK for approximately 25 mm with
  less than one trace width of spacing.
- Impact: coupling can cause intermittent I2C errors, especially at higher SPI
  clock rates or with weak pull-ups.
- Fix: separate the runs, cross at a right angle if necessary, or place a
  properly stitched ground guard between them. Verify with an oscilloscope and
  logic analyzer after the change.
- Confidence: medium-high; the exact risk depends on edge rate, spacing,
  stackup, and termination.

## Finding 3

**[Major] No reverse-polarity or battery fault protection shown**

- Evidence: the battery connector connects directly to the charger and system
  rail.
- Impact: a miswired battery or connector fault can damage the charger, the
  regulator, and the load.
- Fix: define the fault model and add the appropriate protection topology.
  Require human review for the lithium-battery safety case.
- Confidence: high that protection is absent; the correct topology depends on
  the charging and load architecture.

## Question

**What is the maximum temperature inside the enclosure?**

The layout shows a linear regulator and a sealed enclosure. The thermal
conclusion cannot be verified without the ambient temperature, copper area,
airflow, and regulator datasheet thermal curve.

## Summary

The board is not ready for fabrication until the antenna keep-out and battery
fault behavior are resolved. The SPI/I2C coupling issue should be fixed before
layout release because re-spins are more expensive than rerouting.
