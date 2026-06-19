# KiCad Workflow (Alternative)

Use KiCad when you need:
- Open-source tool with no online dependency
- Better 3D visualization than LCEDA
- More advanced routing features (push-and-shove, differential pairs, length tuning)
- Cross-platform (Windows / macOS / Linux)

## Version

Use KiCad 8.0 or later (major UI improvements in 8.x).

## Workflow

### Schematic (Eeschema)
1. Create project → Schematic Editor
2. Add symbols: `A` key, search or browse libraries
3. Annotate: Tools → Annotate Schematic
4. Assign footprints: Tools → Assign Footprints
5. Electrical Rules Check (ERC): Inspect → Electrical Rules Checker → fix all

### PCB (Pcbnew)
1. Update PCB from schematic: Tools → Update PCB from Schematic
2. Set board outline on Edge.Cuts layer
3. Place components, route traces
4. Add copper pours: Place → Add Filled Zone → select GND net
5. Design Rules Check (DRC): Inspect → DRC → fix all

### Export for JLCPCB
1. File → Fabrication Outputs → Gerbers
   - Layers: F.Cu, B.Cu, F.Silkscreen, F.Mask, B.Mask, Edge.Cuts
   - Check "Use Protel filename extensions"
2. File → Fabrication Outputs → Drill Files (Excellon)
3. File → Fabrication Outputs → BOM (CSV)
4. File → Fabrication Outputs → Component Placement (CPL)

## KiCad vs LCEDA for This Project

| Aspect | KiCad | LCEDA |
|--------|-------|-------|
| LCSC parts integration | Manual (import BOM) | Built-in search |
| JLCPCB assembly | Extra steps | One-click |
| 3D viewer | Excellent (built-in ray tracer) | Good |
| Learning curve | Steeper | Gentler (Chinese UI) |
| Community plugins | Many | Few |
| Version control | Git-friendly (text files) | Binary .epro format |

**Recommendation**: Use LCEDA for this project (tighter JLCPCB integration).
Use KiCad if you plan to open-source the design or need advanced routing.
