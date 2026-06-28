# DFM (Design for Manufacturing) Checklist — 94-Point

Use this checklist before exporting Gerber files. Target fab: JLCPCB.
Each unchecked item is a potential manufacturing failure or yield loss.

---

## Fab Capability Limits (JLCPCB)

| Parameter | Min | Recommended |
|-----------|-----|-------------|
| Trace width (outer) | 3.5mil (0.09mm) | 6mil |
| Trace spacing (outer) | 3.5mil | 6mil |
| Trace width (inner) | 4mil | 6mil |
| Via hole | 0.2mm | 0.3mm |
| Via pad | 0.45mm | 0.6mm |
| Annular ring | 0.125mm | 0.15mm |
| Board outline tolerance | ±0.2mm | — |
| Slot width | 0.8mm | 1.0mm |
| Solder mask bridge (green) | 0.1mm | 0.15mm |
| Silkscreen line width | 0.15mm | 0.2mm |

---

## Pre-Export Checks

### 1. Schematic (items 1–16)

- [ ] 1. All ICs have power connected — verify every VDD/VCC/VDDIO pin
- [ ] 2. All ICs have GND connected — verify every VSS/GND pin
- [ ] 3. Decoupling caps (0.1µF) on every VDD pin, placed within 5mm of the pin
- [ ] 4. No unconnected CMOS inputs — floating inputs cause oscillation and excess current
- [ ] 5. No unconnected pins labeled "NC" that actually need pull-up/down
- [ ] 6. Pin conflicts resolved — no two peripheral functions share the same GPIO
- [ ] 7. I2C pull-ups present (4.7kΩ typical) — exactly one pair per bus
- [ ] 8. I2C pull-ups NOT duplicated across multiple boards/modules on the same bus
- [ ] 9. SPI MISO/MOSI/SCLK match between master and every slave device
- [ ] 10. SPI CS lines are dedicated per device (not shared)
- [ ] 11. Reset circuit correct: RC delay for power-on reset, button for manual reset
- [ ] 12. BOOT/IO0 strapping correct for target boot mode
- [ ] 13. Programming/debug header accessible (SWD/JTAG/UART exposed)
- [ ] 14. ERC (Electrical Rules Check) run with 0 errors
- [ ] 15. BOM complete — every component has a part number, value, and package
- [ ] 16. No schematic symbol pins mismatched to PCB footprint pads

### 2. PCB Layout — General (items 17–34)

- [ ] 17. Board outline defined on mechanical/outline layer (not keep-out, not copper)
- [ ] 18. Board outline is closed (no gaps, no overlapping lines)
- [ ] 19. No traces or copper within 0.5mm of board edge
- [ ] 20. All nets fully routed — 0 airwires / ratsnest remaining
- [ ] 21. DRC run with 0 errors, 0 warnings
- [ ] 22. DRC rules match fab capabilities (trace/space, annular ring, hole size)
- [ ] 23. Via annular rings ≥ 0.15mm (≥ 0.2mm for mechanical reliability)
- [ ] 24. Via holes ≥ 0.3mm (smaller costs extra, may reduce yield)
- [ ] 25. No vias under components unless tented AND component datasheet allows it
- [ ] 26. No acute angles on traces — all turns ≥ 90° use 45° or arc transitions
- [ ] 27. Silkscreen text height ≥ 0.8mm (≥ 1.0mm recommended for readability)
- [ ] 28. Silkscreen line width ≥ 0.15mm (≥ 0.2mm recommended)
- [ ] 29. Silkscreen does not overlap any pad or via
- [ ] 30. Component reference designators are readable and not hidden under components
- [ ] 31. Component-to-component clearance ≥ 0.2mm for hand-placed, ≥ 0.15mm for machine
- [ ] 32. Tall components (>5mm) do not shadow shorter components from reflow heat
- [ ] 33. Heavy components (>10g) have adequate mechanical support (not solder-only)
- [ ] 34. Flex/rigid-flex: bend radius ≥ 10× board thickness at flex sections

### 3. Copper Pours (items 35–42)

- [ ] 35. GND pour on bottom layer (2L) / layers 2+4 (4L) — fills all unused space
- [ ] 36. GND pour on top layer for 4L boards (fills gaps between routed traces)
- [ ] 37. Thermal relief (cross/spoke pattern) on all pads connected to copper pours
- [ ] 38. Via stitching along board edges — GND vias every 5–10mm
- [ ] 39. No isolated copper islands — every copper pour polygon connects to its net
- [ ] 40. Pour-to-board-edge clearance ≥ 0.3mm (for router tolerance)
- [ ] 41. Same-net spacing (pour-to-trace, pour-to-pad) ≥ 0.2mm
- [ ] 42. No narrow pour necks (< 0.2mm wide) — these can etch away

### 4. Antenna & RF (items 43–50)

- [ ] 43. 15mm × 15mm keep-out zone around PCB antenna — NO copper on ANY layer
- [ ] 44. Antenna at board edge, facing outward (not toward board center)
- [ ] 45. No metal objects near antenna — battery, USB connector, mounting holes ≥ 15mm away
- [ ] 46. GND plane void under antenna zone on all layers
- [ ] 47. No copper pour or traces in antenna keep-out on ANY layer
- [ ] 48. Antenna matching network populated OR 0Ω jumper in place (if tunable)
- [ ] 49. Microstrip/CPW trace width calculated for target impedance (50Ω) with actual stackup
- [ ] 50. Coaxial connector (IPEX/u.FL): pad-to-GND spacing correct per connector datasheet

### 5. Silkscreen & Assembly Marks (items 51–58)

- [ ] 51. Pin 1 markers on all ICs (silkscreen dot or notch, visible after placement)
- [ ] 52. Component polarity marked: diodes, LEDs, tantalum/electrolytic caps, battery connector
- [ ] 53. Polarity marks visible AFTER component placement (not hidden under the component body)
- [ ] 54. Connector pinouts labeled (e.g., "TX", "RX", "5V", "GND", "+", "−")
- [ ] 55. Board name and version text on silkscreen
- [ ] 56. Date or revision code on silkscreen
- [ ] 57. Fiducial marks: ≥ 3 global (panel corners) + 2 local (near fine-pitch ICs)
- [ ] 58. Pick-and-place orientation: all polarized components in same rotation (0° or 90° batch)

### 6. Power Distribution (items 59–69)

- [ ] 59. Power traces wider than signal traces:
  - [ ] 59a. > 100mA → ≥ 0.3mm (12mil)
  - [ ] 59b. > 500mA → ≥ 0.5mm (20mil)
  - [ ] 59c. > 1A → ≥ 1.0mm (40mil) or dedicated copper pour
- [ ] 60. Bulk capacitor (10–100µF) on every power rail near the regulator output
- [ ] 61. Ferrite bead or inductor correctly placed on analog supply rails (if needed)
- [ ] 62. DC-DC switch node (LX/SW) loop area minimized — inductor + diode + output cap tight
- [ ] 63. LDO/regulator has adequate copper area for heatsinking (≥ 1cm² per 100mA dropout)
- [ ] 64. Battery reverse-polarity protection present (Schottky, P-FET, or PTC + TVS)
- [ ] 65. Fuse or PTC on battery input rated for expected max current × 1.5
- [ ] 66. Voltage sense/ADC lines are Kelvin-connected (separate from power path)
- [ ] 67. High-current paths use multiple vias (1 via per ~1A at 0.3mm hole)
- [ ] 68. Power input connector rated for expected current with 50% margin
- [ ] 69. No single-point-of-failure: multiple GND vias at power entry

### 7. High-Speed & Signal Integrity (items 70–78)

- [ ] 70. Controlled impedance traces: width calculated per stackup, noted in fab drawing
- [ ] 71. Differential pairs (USB, Ethernet, LVDS): length-matched within tolerance
- [ ] 72. SPI/parallel bus: all data lines length-matched to clock within specified tolerance
- [ ] 73. Series termination resistors placed at driver (source) side, within 5mm of pin
- [ ] 74. No traces crossing plane splits — reference plane is continuous under high-speed signals
- [ ] 75. Vias on high-speed nets: ≤ 2 per net; return GND via within 2mm of signal via
- [ ] 76. No stubs on high-speed traces (especially DDR address/command fly-by topology)
- [ ] 77. Clock traces: point-to-point, no branches, series terminated at driver
- [ ] 78. Crystal/oscillator: load capacitors match crystal spec, guard ring around circuit

### 8. Mechanical (items 79–85)

- [ ] 79. Mounting holes ≥ 3.2mm (M3) or ≥ 2.5mm (M2.5), per mechanical design
- [ ] 80. Keep-out zone around mounting holes ≥ 3mm radius — no copper, no components
- [ ] 81. Connectors accessible from board edge with mating clearance for cable/plug
- [ ] 82. Buttons/switches reachable through enclosure cutouts — verify with 3D model
- [ ] 83. Screw head clearance: no tall components within screw head radius of mounting holes
- [ ] 84. Board fits in target enclosure — verify 3D model alignment
- [ ] 85. Board thickness specified (0.8 / 1.0 / 1.2 / 1.6 / 2.0mm)

### 9. Post-Export Verification (items 86–94)

- [ ] 86. Gerber files open correctly in gerbv / JLCPCB online viewer / ZofzPCB
- [ ] 87. All required layers present: GTL, GBL, GTS, GBS, GTO, GBO, GKO/GML, TXT (drill)
- [ ] 88. Drill file format: Excellon (not Sieb & Meyer)
- [ ] 89. Board outline on its own layer (GKO) — NOT on a copper layer
- [ ] 90. BOM CSV columns: Designator, Manufacturer Part #, LCSC Part #, Quantity, Package
- [ ] 91. CPL (Pick & Place) columns: Designator, Mid X, Mid Y, Layer, Rotation
- [ ] 92. CPL rotation angles verified against component datasheet pin-1 orientation
- [ ] 93. Solder mask expansion checked — no mask slivers between fine-pitch pads
- [ ] 94. Netlist vs Gerber: all nets in schematic appear in PCB, no extra nets, no missing pads

---

## Common Mistakes (Top 10)

1. **Missing I2C pull-ups** — SDA and SCL float, bus won't work at all
2. **GPIO0/EN not pulled up on ESP32** — board won't boot without manual intervention
3. **Decoupling caps too far from IC** — ineffective above ~10mm trace length
4. **Antenna zone violation** — copper or components in keep-out kills WiFi range by 50-90%
5. **Wrong footprint** — always verify against actual component datasheet, not library defaults
6. **3.3V parts on 5V rails** — check absolute maximum ratings for every IC
7. **Silkscreen over pads** — removed during fabrication, can expose copper beneath
8. **Missing board outline layer** — fab will reject the order or charge for engineering review
9. **Acid traps** — acute angles (< 90°) in copper pour edges can trap etchant, cause over-etching
10. **No test points** — always add GND, 3.3V, UART TX/RX test pads for debugging
