# Contributing

Thanks for improving PCB Designer. The project values correctness, clear
evidence, and reproducible engineering decisions over volume.

## Development Setup

Requirements:

- Python 3.10 or newer;
- Git;
- no third-party Python packages for the runtime tools.

Run the checks:

```bash
python scripts/validate_skill.py .
python -m unittest discover -s tests -v
python scripts/pcbcalc.py --help
python scripts/audit_release.py --help
```

## Content Standards

### Engineering Claims

- Tie non-obvious claims to a datasheet, standard, supplier page, reference
  design, or clearly labeled heuristic.
- Do not present remembered supplier capabilities or prices as current.
- State the conditions under which a rule applies.
- Prefer "verify against the datasheet" over a false universal rule.
- Keep safety-critical guidance conservative and identify the human review
  boundary.

### References

- Put substantial detail in `references/`, not the main `SKILL.md`.
- Keep one topic per file and link it from the mode router.
- Avoid duplicating the same rule in multiple references.
- Include units and worst-case conditions where they matter.
- Use ASCII for code and identifiers. Non-ASCII is acceptable for Chinese
  product names and localized documentation.

### Calculators

- Add a test for every formula or boundary condition.
- Make units explicit in argument names and output keys.
- Label model limitations in the result and in `--help`.
- Prefer standard-library Python unless a dependency is essential.

### Supplier Profiles

Each profile in `rules/fab-profiles.json` should include:

- a stable profile ID;
- source URL when available;
- `verified_on` date;
- `verification_status`;
- process-specific limits and notes.

If you cannot verify the source, use `unverified` or `generic`.

## Pull Request Checklist

- [ ] `scripts/validate_skill.py` passes.
- [ ] Unit tests pass.
- [ ] New behavior has a regression test.
- [ ] README or CHANGELOG updated when user-facing behavior changes.
- [ ] No supplier-specific value is presented as current without verification.
- [ ] No generated fabrication output, secret, or private design is committed.
- [ ] Safety and compliance implications are stated.

## Review Style

Reviews should lead with findings in severity order. Each finding should state
the evidence, the impact, the fix, and the confidence. Keep summaries brief and
secondary to the findings.

## License

By contributing, you agree that your contribution is licensed under the MIT
License in this repository.
