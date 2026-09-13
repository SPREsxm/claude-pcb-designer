# Standards and Sources

Use this reference to decide what must be verified before making a design claim.
Standards and supplier capabilities change; always confirm the current revision.

## Source Hierarchy

| Priority | Source | Use |
|---:|---|---|
| 1 | Product requirements and safety plan | Defines the problem and acceptance criteria |
| 2 | Component datasheet, errata, and reference design | Pinout, ratings, layout, thermal data |
| 3 | Fabricator stackup and capability documents | Trace, space, drill, material, impedance |
| 4 | Applicable standards | Safety, EMC, reliability, workmanship |
| 5 | This skill's references | Planning, review, and common practice |

If sources conflict, follow the higher-priority source and document the conflict.

## Common Design and Workmanship Standards

| Standard | Subject |
|---|---|
| IPC-2221 | Generic PCB design |
| IPC-2222 | Rigid organic PCB design |
| IPC-2223 | Flexible PCB design |
| IPC-2226 | HDI design |
| IPC-6012 | Rigid PCB qualification and performance |
| IPC-6013 | Flexible PCB qualification and performance |
| IPC-7351 | Land-pattern and footprint design |
| IPC-A-610 | Acceptability of electronic assemblies |
| J-STD-001 | Soldering and assembly process requirements |
| IPC-2152 | Current-carrying capacity in PCB conductors |
| IPC-2141 | Controlled-impedance design |

Use the controlled document, not a summary, when acceptance or certification is
at stake.

## EMC and Safety Planning

Determine at intake:

- target markets and required marking or certification;
- intended emissions class and immunity requirements;
- whether a radio module's certification remains valid with the chosen antenna;
- mains, isolation, creepage, clearance, fusing, and touch-current requirements;
- battery transport, charging, and abuse requirements;
- medical, automotive, aviation, space, or industrial environmental standards.

Pre-compliance testing is not certification. A declaration or certificate must
come from the appropriate body and the applicable process.

## Supplier Data

Record supplier-specific values with:

```json
{
  "name": "example-fab",
  "source_url": "https://example.invalid/capabilities",
  "verified_on": "2026-09-13",
  "min_trace_mm": 0.10,
  "min_space_mm": 0.10,
  "min_drill_mm": 0.20,
  "notes": "Example only; replace with current verified data."
}
```

Never present a remembered number as current. If the URL or revision cannot be
checked, label the value `unverified`.

## Citation Rules for Answers

When citing a source:

- name the document and revision or date;
- identify the section or table when possible;
- explain how it applies to the user's design;
- state when the source is unavailable or when you relied on a heuristic.

Do not cite a source you did not actually inspect.
