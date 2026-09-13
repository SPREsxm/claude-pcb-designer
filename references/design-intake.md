# Design Intake

Use this reference before proposing an architecture, BOM, stackup, or layout.
The goal is to expose constraints that change the design early.

## Minimum Intake

### Product

- What does the board do, and what are its operating modes?
- Is this a prototype, pilot build, or production design?
- Expected quantity over the product lifetime?
- Expected service life, update strategy, and repair strategy?
- What is explicitly out of scope?

### Electrical

- Input source: USB, adapter, battery, PoE, vehicle power, solar, or other?
- Input voltage range, transient range, connector type, and maximum current?
- Required rails, tolerances, ripple, sequencing, and quiescent current?
- Peak, average, and sleep-mode load current for each rail?
- Battery chemistry, cell count, charging source, and protection requirements?
- Interfaces: list voltage, speed, direction, connector, and cable length.
- Analog accuracy, bandwidth, input range, and reference requirements?
- Radio bands, duty cycle, antenna type, and required range?

### Mechanical and Environmental

- Maximum board outline and height?
- Mounting-hole pattern, connector keep-outs, and cable bend radius?
- Enclosure material and proximity to metal or carbon fiber?
- Operating and storage temperature, humidity, vibration, shock, altitude?
- Ingress protection, conformal coating, potting, or cleaning requirements?
- Antenna location and required keep-out volume?

### Manufacturing and Test

- Preferred EDA tool, fabricator, assembler, and country of manufacture?
- Layer-count and cost targets?
- Assembly method: hand, prototype SMT, or production line?
- Test strategy: pogo fixture, ICT, flying probe, functional test?
- Programming method and required debug access?
- Preferred component sources and acceptable substitutes?
- RoHS, REACH, conflict-minerals, export-control, or customer restrictions?

### Compliance and Safety

- Target markets and required certifications?
- Mains, high voltage, lithium battery, medical, automotive, aviation, or
  other safety domain?
- Required standards or internal design rules?
- EMC class, ingress rating, flammability rating, or isolation requirement?
- Who is qualified to review and approve the final design?

## Intake Output

Before design work, produce:

1. a concise requirement summary with source and confidence;
2. a table of unknowns that can change the architecture;
3. a preliminary block diagram;
4. a power-tree sketch;
5. a risk list;
6. the next blocking question, if any.

Do not ask for every field mechanically. Infer the obvious and ask only when
the answer changes architecture, safety, compliance, or testability.

## Example Assumption Block

```text
Assumptions:
- Indoor prototype, 10 boards, 5-40 C, no vibration requirement.
- 5 V USB-C input; 3.3 V rail, 500 mA peak, 80 mA average.
- 4-layer stackup is acceptable if it materially improves RF/EMC behavior.

Open questions:
- Is the radio certified as a module and must its antenna configuration remain unchanged?
- Is the enclosure metal or plastic?
- Must the board survive a battery-reversal fault?
```

## Red Flags

Escalate or stop the design flow when any of these are true:

- mains or high voltage without a qualified safety reviewer;
- lithium battery pack without protection, cell balancing, and fault analysis;
- medical, automotive, aviation, or space claim without applicable standards;
- RF exposure or high-power transmitter without compliance planning;
- unknown mechanical envelope but the layout is already dense;
- no thermal path but the enclosure is sealed and the ambient is high;
- exact production quantities are required but component availability is unknown;
- a safety function depends on a single unverified component or firmware path.
