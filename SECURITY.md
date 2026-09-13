# Security Policy

## Reporting a Vulnerability

Please report security issues privately through the repository's GitHub
Security Advisory feature:

https://github.com/SPREsxm/claude-pcb-designer/security/advisories/new

Do not open a public issue for a vulnerability that could cause supply-chain,
file-handling, or automation harm.

## Scope

Relevant issues include:

- unsafe file deletion or path traversal in installer/audit tools;
- archive handling that can escape the intended extraction context;
- command injection or unsafe subprocess use;
- malicious references, scripts, or workflow changes;
- dependency or GitHub Actions compromise.

Hardware design errors, inaccurate supplier data, and incorrect engineering
calculations are engineering bugs, not security vulnerabilities. Report those
through the normal issue tracker with reproduction details.

## Safety Boundary

This project does not certify hardware and must not be treated as a substitute
for qualified review in safety-critical, regulated, high-voltage, battery, RF,
medical, automotive, aviation, or space applications.
