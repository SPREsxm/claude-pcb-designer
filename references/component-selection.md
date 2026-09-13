# Component Selection

Component selection is part of the architecture, not a BOM cleanup task.
Optimize for function first, then availability, manufacturability, testability,
and cost.

## Selection Order

1. Define electrical requirements, environmental limits, and package constraints.
2. Check the datasheet, errata, lifecycle status, and reference design.
3. Confirm package, pin count, supply voltage, and thermal limits.
4. Verify availability, lead time, minimum order, and assembly compatibility.
5. Confirm the footprint against the exact part and variant.
6. Check second-source or drop-in alternatives.
7. Record evidence and verification status in the BOM.

## BOM Verification Status

Do not treat a part number copied from a library as verified. Use:

| Status | Meaning |
|---|---|
| `verified` | Datasheet and supplier listing checked for the exact part/package |
| `provisional` | Electrically suitable, but availability or exact variant not checked |
| `example-only` | Teaching example; replace before production |
| `do-not-populate` | Deliberately omitted from assembly |

## Key Selection Criteria

### Active Devices

- Absolute maximum ratings with margin beyond the real operating range.
- Recommended operating conditions and derating requirements.
- Thermal path and maximum ambient temperature.
- Startup, shutdown, sequencing, and unused-pin behavior.
- Errata affecting reset, clocks, analog performance, or interfaces.
- Package pitch, solderability, inspection, and rework access.

### Connectors

- Mating cycles, insertion force, retention, and cable direction.
- Current rating per contact and temperature rise.
- Voltage rating, creepage/clearance, and touch safety.
- Keying, polarization, shrouding, and accidental disconnection risk.
- Whether the connector can be placed and inspected after assembly.

### Passives

- Derate voltage, current, power, and temperature.
- Prefer common values and sizes, but do not force a value that harms function.
- Check DC-bias behavior for ceramic capacitors; effective capacitance can fall
  sharply near rated voltage.
- Check ESR, ESL, ripple current, and self-heating for regulators and filters.
- Check resistor pulse rating and temperature coefficient when relevant.

### Crystals and Oscillators

- Match load capacitance, ESR, drive level, tolerance, and temperature range.
- Confirm the MCU's oscillator requirements and PCB layout constraints.
- Prefer oscillators for difficult environments or tight frequency tolerance.

### Protection Devices

- TVS working voltage, clamp voltage, capacitance, surge rating, and leakage.
- Fuse or PTC hold current, trip current, voltage rating, and ambient derating.
- Reverse-polarity topology and safe behavior during hot plug, brownout, and
  inductive load dump.

### Wireless Modules

- Use a module whose certification and antenna configuration match the product.
- Confirm keep-out, ground-plane, power-filter, and host-interface requirements.
- Do not assume a module certification automatically certifies the complete
  product or a changed antenna.

## Package and Assembly Strategy

| Requirement | Practical starting point |
|---|---|
| Hand assembly | 0805/0603 passives, SOIC, larger QFN with exposed pad |
| Prototype SMT | 0603/0402 passives, QFN, fine-pitch QFP |
| Dense production | 0402/0201, BGA, HDI, via-in-pad |
| Harsh environment | Larger packages, high-Tg material, conformal coating |

Smaller is not automatically better. Smaller packages reduce area but increase
inspection difficulty, placement sensitivity, and rework cost.

## Supplier Reality Check

Supplier numbers, stock, surcharges, and package variants change. Verify at
order time. When network access is unavailable, mark the part as unverified
instead of presenting a stale LCSC or distributor number as fact.

## BOM Template

```text
Designator(s),Qty,Value/Function,Manufacturer,MPN,Package,Supplier PN,Status,Notes
U1,1,3.3 V regulator,Example Corp,EXAMPLE123,SOT-23-5,,provisional,Verify thermal
R1-R4,4,10k 1%,Example,RES10K,0603,,verified,-
```

Do not merge different parts merely because their values match. Merge only
when voltage, tolerance, temperature coefficient, and footprint are compatible.

## Cost Discipline

- Consolidate values only when the electrical design remains sound.
- Prefer parts that the assembler stocks or can source reliably.
- Consider feeder count and assembly setup, not only unit price.
- Avoid single-source critical parts without a documented plan.
- Include the cost of test, programming, coating, and expected yield.
