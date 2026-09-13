# Fabrication Release

## Revision

- Board:
- Revision:
- Git commit / tag:
- Date:
- Fabricator:
- Assembler:

## Package Contents

| File / group | Present | Checked by | Notes |
|---|---:|---|---|
| Top copper | | | |
| Bottom copper | | | |
| Inner copper | | | |
| Top solder mask | | | |
| Bottom solder mask | | | |
| Top silkscreen | | | |
| Bottom silkscreen | | | |
| Board outline | | | |
| Drill file | | | |
| Fab drawing / stackup | | | |
| BOM | | | |
| CPL / pick-and-place | | | |

## Automated Audit

Command:

```bash
python scripts/audit_release.py <release-dir> --json --layers <n>
```

Result:

- Errors:
- Warnings:
- Reviewer decision:

## Manual Checks

- [ ] Gerbers open and align with the drill file.
- [ ] Board outline is closed and on the correct layer.
- [ ] Stackup and impedance are confirmed.
- [ ] BOM and CPL match.
- [ ] DNP and assembly variants are clear.
- [ ] Fiducials and panelization are correct.
- [ ] Silkscreen revision and polarity marks are correct.
- [ ] Supplier questions are answered.
- [ ] Safety and compliance review is complete.

## Go / No-Go

- Decision:
- Approved by:
- Date:
- Conditions / caveats:
