# DFM (Design for Manufacturing) Checklist

Use this checklist before exporting Gerber files. Target fab: JLCPCB.

## Minimum Capabilities (JLCPCB 2-layer)

| Parameter | Min | Recommended |
|-----------|-----|-------------|
| Trace width | 3.5 mil (0.09mm) | 6 mil |
| Trace spacing | 3.5 mil | 6 mil |
| Via hole | 0.2mm | 0.3mm |
| Via pad | 0.45mm | 0.6mm |
| Annular ring | 0.125mm | 0.15mm |
| Board outline | — | Use mechanical layer |
| Slot width | 0.8mm | 1.0mm |

## Pre-Export Checks

### Schematic
- [ ] All ICs have power connected (check each VDD/VCC pin)
- [ ] All ICs have GND connected
- [ ] Decoupling caps (0.1µF) on every VDD pin, within 5mm of the pin
- [ ] No unconnected pins labeled as "NC" that should be pulled up/down
- [ ] Pin conflicts resolved (no two functions on same GPIO)
- [ ] I2C pull-ups present (4.7kΩ typical) — exactly one pair per bus
- [ ] SPI MISO/MOSI/SCK match between master and all slaves
- [ ] Reset circuit correct (RC delay for power-on, button for manual)
- [ ] Programming/debug header accessible

### PCB Layout
- [ ] Board outline defined on mechanical layer (not keep-out layer)
- [ ] No traces or copper within 0.5mm of board edge
- [ ] All traces connected (no airwires / ratsnest remaining)
- [ ] DRC: 0 errors, 0 warnings
- [ ] Via annular rings ≥ 0.15mm
- [ ] No acute angles on traces (< 90° turns use 45° or arcs)
- [ ] Silkscreen text ≥ 0.8mm height, ≥ 0.15mm line width
- [ ] Silkscreen does not overlap pads or vias
- [ ] Component reference designators are readable and not hidden

### Copper Pours
- [ ] GND pour on bottom layer (2L) / layers 2+4 (4L)
- [ ] Thermal relief on pads connected to pours
- [ ] Via stitching along board edges (every 5-10mm)
- [ ] No isolated copper islands (all pours connected to GND)

### Antenna / RF (ESP32 modules)
- [ ] 15mm × 15mm keep-out zone around PCB antenna (all layers)
- [ ] Antenna at board edge, facing outward
- [ ] No metal objects near antenna (battery, USB connector, mounting holes)
- [ ] Antenna area NOT covered by copper pour on any layer

### Silkscreen / Assembly
- [ ] Pin 1 markers on all ICs (dot or notch)
- [ ] Component polarity marked (diodes, LEDs, electrolytic caps, battery)
- [ ] Connector pinouts labeled (e.g., "RX", "TX", "5V", "GND")
- [ ] Board name and version text
- [ ] Date or revision code

### Power
- [ ] Power traces wider than signal traces
  - [ ] >100mA: 0.3mm minimum
  - [ ] >500mA: 0.5mm minimum
  - [ ] >1A: 1.0mm minimum or copper pour
- [ ] LDO has adequate copper for heatsinking
- [ ] Battery reverse-polarity protection (if applicable)
- [ ] Fuse or PTC on battery input (optional but recommended)

### Mechanical
- [ ] Mounting holes ≥ 2.5mm diameter (M2.5) or ≥ 3.2mm (M3)
- [ ] Keep-out around mounting holes (≥ 3mm radius, no copper)
- [ ] Connectors are accessible (USB on board edge)
- [ ] Buttons reachable (through enclosure or on edge)
- [ ] Board fits in target enclosure (if applicable)

## Post-Export Checks

- [ ] Gerber files open correctly in gerbv or JLCPCB online viewer
- [ ] All layers present: Top Copper, Bottom Copper, Top Silkscreen, Top Solder Mask, Bottom Solder Mask, Board Outline, Drill File
- [ ] Drill file format: Excellon
- [ ] Board outline on its own layer (GKO or GM1)
- [ ] BOM CSV has columns: Designator, LCSC Part #, Quantity
- [ ] CPL (Pick & Place) file has columns: Designator, Mid X, Mid Y, Layer, Rotation

## Common Mistakes to Avoid

1. **Missing pull-ups on I2C** — SDA and SCL will float, bus won't work
2. **GPIO0/EN not pulled up on ESP32** — board won't boot without manual intervention
3. **Decoupling caps too far from IC** — ineffective above ~10mm trace length
4. **Antenna zone violation** — copper or components in antenna keep-out kills WiFi range
5. **Wrong footprint** — always verify against the actual component datasheet
6. **3.3V parts on 5V rails** — check max voltage ratings for every IC
7. **Silkscreen on pads** — removed during fabrication, can expose copper
8. **Missing board outline layer** — fab will reject the order
9. **Acid traps** — acute angles in copper pours can trap etchant
10. **No test points** — add at least GND, 3.3V, UART TX/RX test pads for debugging
