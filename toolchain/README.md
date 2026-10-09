# Qualified canonical runtime fixes

The board pins the three package artifacts in `packages/`. These are local builds
of the exact public upstream commits in `provenance.json`, with canonical source
fixes and regression tests retained under each package's `source/` directory.
They are project packages, not claimed upstream releases. No installed bundle
was edited, no yalc link is published, and no generated board JSON was repaired.

Core emits string position offsets with millimetre units, omits unset optional
group/hole ownership metadata, and creates pill paste from emitted pad geometry.
Circuit JSON supports board-level silkscreen without inventing a purchased
component owner; malformed ownership, text and layer data remain rejected.

Canonical tests and package builds use Bun 1.4.0, matching upstream core CI.
The board uses Bun 1.3.9 and its frozen lockfile. The real CLI coupon confirms the
installed packages are used in generated native output. Package SHA-256 values
are recorded in `provenance.json`; publication staging copies these exact bytes.

Build and native qualification receipts are in
`evidence/pcb-completion-2026-10-08/`. Successful toolchain tests are not a claim
of complete routing or fabrication readiness.

The current schema build is based on upstream 0.0.521 to satisfy the released
CLI's 0.0.520 or newer schema interface. Core remains based on 0.0.2090 so saved
routing semantics do not change. Group offset regressions cover explicit zero
coordinates, which revealed the two residual mounting-group errors. Reviewed
anchor snapshot changes affect numeric text formatting (for example `1.50mm`
to `1.5mm`); component and group copper positions are unchanged.

The Gerber library fixes G85 slot commands at their canonical source: both
endpoints appear in one Excellon block at four-decimal precision. All 35 scalar
Excellon regressions pass, and the complete library builds with TypeScript
declarations. The upstream visual suite remains unverified because its
optional development dependencies could not be fetched (HTTP 503). Fresh actual
exports are independently parsed using PyGerber 2.4.3 and PCB-tools 0.1.6, with
strict Gerber parser errors enabled. This artifact builds the public library;
it does not replace or claim qualification of the standalone upstream CLI.

Retained source files are patches for three separate upstream projects, not
complete projects inside this board. Board TypeScript excludes the toolchain patch/build archive; each canonical package was type-built in its complete original
checkout. Board source and imported package declarations remain type-checked.

Core also enforces routing-disable controls during subcircuit updates. The
regression reproduced routing despite disabled platform and board flags; both
now remain unrouted while the enabled control still creates actual copper.
Ten focused core regressions and the complete typed package build pass.
