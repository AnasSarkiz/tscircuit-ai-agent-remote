# Tested source proposal for B-010

Base: core main 18e1d11a6eaebaece6f6fb75fdfd2c680a468890, version 0.0.2061.
`core-b010.patch` contains the actual source correction, regression and reviewed
snapshot changes. The isolated checkout is excluded from board publication and
board tooling. No installed board runtime or imported component was patched.
No upstream push, PR, release or merge has been performed.

Native upstream dependency installation failed with Bun 1.3.9; the repository's
CI Bun 1.4.0 installed all 619 declared packages successfully. Same source,
same declared packages, no tarball/cache injection or dependency substitution.
Package manifest and exact validation dependency versions are preserved.

Unchanged upstream fails the new regression on numeric pcb_component offsets.
The correction emits millimeter strings for component and group offsets, omits
absent anchor_alignment and normalizes absent schematic subcircuit_id to
undefined. Group initial placement and anchor-alignment update paths both needed
the same correction. No physical layout algorithms or geometry were modified.

New regression passes (205 assertions); related group, anchor and edge/calc
suite: 29 pass, 0 fail, 1 existing skip, 332 assertions across 27 files.
TypeScript exits 0; package ESM and declaration build exits 0. Canonical formatter
ran on touched source. Full upstream suite has not been run.

All five changed existing PCB snapshots were viewed. Geometry and arrows remain
unchanged; labels change from fixed numeric formatting to schema-valid mm string
labels (e.g. X: 2mm). New PCB and A4 schematic snapshots were viewed. The fixture
uses upstream's existing untouched microphone import, not a new board component.
The current mixed-calc coordinate behavior is preserved; assertions use actual
imported pin-1 pad geometry rather than assuming a symmetric footprint center.

The board's pinned core remains 0.0.2058 and its strict schema regression still
fails B-010. This proposal is useful evidence for the authorized fix chat, not a
verified published fix or permission to resume blocked full-board validation.
