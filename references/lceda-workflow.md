# 立创 EDA (LCEDA) Workflow

## Choosing the Right Version

| Version | Use case | Pros | Cons |
|---------|----------|------|------|
| **LCEDA Pro** (离线客户端) | Multi-sheet, complex designs | Fast, full-featured, offline | Windows/Linux only |
| **LCEDA Standard** (Web) | Quick prototypes, single-sheet | No install, easy sharing | Slower, limited for large designs |
| **EasyEDA** (International) | Same as Standard, English UI | Same as Standard | Less LCSC integration |

**Recommendation**: Use LCEDA Pro for the Rocket Black Box and any design
with more than ~20 components.

## LCEDA Pro Workflow

### Step 1: Create Project

1. Open LCEDA Pro → 新建工程
2. Name: `project-name`
3. The `.epro` file is created alongside `.esch` (schematic) and `.epcb` (PCB)

### Step 2: Schematic Capture

1. **Add components**: Press `Shift+F` or click 元件库
   - Search by LCSC part number (e.g., `C2913201` for ESP32-S3-WROOM-1)
   - Or search by description (e.g., "AMS1117 3.3V SOT-223")
   - Check "基础库" (basic parts) to avoid JLCPCB extended part fees
2. **Place and wire**: `W` key for wire tool, `G` for GND, `P` for VCC
3. **Net labels**: Use net labels (`N` key) instead of long wires for clarity
4. **Annotate**: Tools → 标注 → 自动标注 (assigns reference designators)
5. **DRC**: 设计 → 设计规则检查 (schematics DRC)

### Step 3: PCB Layout

1. **Convert schematic to PCB**: 设计 → 更新PCB (Update PCB)
2. **Set board outline**: Draw on mechanical layer or use 板框工具
3. **Place components**: Rough placement first, then refine
4. **Route traces**: 
   - `Ctrl+W` or click 布线 to start routing
   - `Tab` during routing to change width
   - `Shift+S` to show only current layer
   - `*` key to switch layers (adds via)
5. **Copper pours**: 放置 → 铺铜 → Select GND net
6. **DRC**: 设计 → DRC → fix all errors

### Step 4: Export for JLCPCB

1. **Gerber**: 文件 → 导出 → Gerber
   - Format: RS-274X
   - Units: mm
   - Include board outline layer
2. **BOM**: 文件 → 导出 → BOM → CSV
3. **Pick & Place (CPL)**: 文件 → 导出 → 坐标文件
4. **Zip all files** and upload to jlcpcb.com

## LCSC Part Selection Tips

### Understanding LCSC Categories
- **基础库 (Basic)**: No extra fee for JLCPCB assembly. ~20,000 parts.
- **扩展库 (Extended)**: ¥3/part surcharge for assembly. Most parts.
- **优选 (Preferred)**: In stock at JLCPCB's Shenzhen warehouse, faster assembly.

### Search Tips
- Filter by "基础库" when possible to save assembly costs
- Use "在库" (in stock) filter to avoid backordered parts
- Check the "SMT" column — parts must support SMT for JLCPCB assembly
- For passives, pick 0603 or 0805 for hand-solderability

### Common LCSC Part Numbers for Embedded Projects

```
ESP32-S3-WROOM-1-N16R8    C2913201
AMS1117-3.3 SOT-223        C6186
TP4056 SOP-8               C382139
USB-C 16P Female           C165948
TF Card Slot Push-Push     C112217
SSD1306 128x64 I2C Module  C50552 (or similar)
4.7kΩ 0603 Resistor        C23162
10kΩ 0603 Resistor         C25804
22Ω 0603 Resistor          C24868
0.1µF 0603 Capacitor       C14663
10µF 0805 Capacitor        C15850
100µF 6.3V Tantalum B      C7173
SMD Button 6x6x5mm         C11135
Red LED 0603               C2286
```

## Keyboard Shortcuts (LCEDA Pro)

| Key | Action |
|-----|--------|
| `W` | Wire / Route |
| `G` | Place GND symbol |
| `P` | Place VCC symbol |
| `N` | Place net label |
| `Shift+F` | Search component |
| `R` | Rotate component |
| `X` | Flip horizontally |
| `Y` | Flip vertically |
| `Ctrl+W` | Start routing (PCB) |
| `Tab` | Change trace width (during routing) |
| `*` | Add via / switch layer (during routing) |
| `Shift+S` | Single layer view |
| `M` | Measure distance |
| `Q` | Toggle unit (mm ↔ mil) |
