# PCB Design Brief

## 1. Objective

- Product or function:
- Board revision:
- Prototype / pilot / production:
- Quantity and build date:
- Owner and reviewer:

## 2. Requirements

### Electrical

| Item | Requirement | Source / note |
|---|---|---|
| Input power | | |
| Input range | | |
| Rails | | |
| Maximum current | | |
| Average current | | |
| Sleep current | | |
| Battery / charging | | |
| Interfaces | | |
| Analog accuracy | | |
| Radio bands | | |

### Mechanical

| Item | Requirement | Source / note |
|---|---|---|
| Maximum outline | | |
| Maximum height | | |
| Mounting pattern | | |
| Connector access | | |
| Antenna keep-out | | |
| Enclosure material | | |

### Environment and Compliance

| Item | Requirement | Source / note |
|---|---|---|
| Temperature range | | |
| Humidity / ingress | | |
| Vibration / shock | | |
| EMC / radio | | |
| Safety | | |
| Reliability class | | |
| Other regulations | | |

## 3. Block Diagram

```text
[Power input] -> [Protection] -> [Regulator] -> [Loads]
                                      |
                                      +-> [MCU] -> [Sensors]
                                                 -> [Radio]
                                                 -> [Debug/test]
```

## 4. Power Budget

Use `templates/power-budget.csv` with `scripts/pcbcalc.py power-budget`.

## 5. Critical Constraints

| Constraint | Why it matters | Verification |
|---|---|---|
| | | |

## 6. Assumptions and Unknowns

| Item | Status | Impact if wrong |
|---|---|---|
| | | |

## 7. Acceptance Criteria

- [ ] All rails within tolerance at maximum load.
- [ ] Programming and recovery access verified on assembled hardware.
- [ ] Required interfaces pass at specified speed and cable length.
- [ ] Thermal limits verified at maximum ambient.
- [ ] Release package passes `audit_release.py`.
- [ ] Applicable safety and compliance reviews completed.
