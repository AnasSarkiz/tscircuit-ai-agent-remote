# A1 connector orientation review — 2026-10-04

Board source parent: `3d6649aea36a1beac5901591659110dae014415f`.
The user's request is to verify real connector openings using the 3D models and
turn them toward board edges where appropriate. This review does not authorize
routing or establish final enclosure/cable fit.

## Reviewed result

| Connector | Genuine part | Board opening after review | Change |
| --- | --- | --- | --- |
| J1 USB-C | TYPE-C-31-M-12 / C165948 | Bottom, −Y | Existing orientation retained |
| J3 protected pack/NTC | S3B-PH-SM4-TB(LF)(SN) / C265101 | Right, +X in supplied CAD | Existing −90° placement retained |
| J4 speaker | S2B-PH-SM4-TB(LF)(SN) / C295747 | Left, −X in supplied CAD | +90° → −90° |
| J6 internal service | SM06B-SRSS-TB(LF)(SN) / C160405 | Right, +X | Existing +90° placement retained |
| J7 display FPC | AFC07-S10FCC-00 / C11050 | Internal, toward +Y | Retained for raised display; final panel/flex unselected |
| J8 haptic motor | S2B-PH-SM4-TB(LF)(SN) / C295747 | Right, +X in supplied CAD | −90° → +90° |

Before/after views show J4/J8's rear solder tails facing the edge originally;
after rotation their mating cavities face the edge and the tails face inward.
Only two board placement rotations changed. Imported definitions, pin identities,
model transforms, supplier data and all source wiring are unchanged.

JST describes these S-series PH and SH headers as side-entry types:
https://www.jst-mfg.com/product/pdf/eng/ePH.pdf and the saved
`references/jst-sh.pdf`. Supplier 3D models are supporting placement evidence,
not a replacement for final mating-housing drawings and real assembly checks.

The battery, speaker and motor are internal enclosure assemblies. Their plugs
need space outside the PCB perimeter inside the enclosure; they do not require
external openings in the case. J6 also needs its service harness inserted with
the case open. Exact plug bodies, harness bend radii, enclosure wall gaps and
display removal/service access remain unqualified. J7's latch faces the proposed
raised display; flex insertion, bend and latch clearance require the exact final
panel, contact orientation and vertical stack. It is not declared fit-qualified.

## Checks and evidence

Native complete-board build with routing disabled, PCB/SVG outputs and GLB
completed with exit0 before and after. `before/board.glb` and `after/board.glb`
are actual native outputs. `render-connectors.ts` renders those saved GLBs from
whole-board and individual connector viewpoints; all final views were inspected.
`after/pcb-top.png` was inspected; the ratsnest and all 13 schematic sheet views
were regenerated. Schematic elements and electrical source connectivity are
identical to the fresh before build; only source filesystem hash metadata differs.
`comparison.json` records full geometry differences and native warning contents.

All five native pre-routing checks exit0. Placement: **zero errors, three
warnings**, on J3/J7/J4. Core infers cable direction through
`guessCableInsertCenter`, and passes it to the orientation check without writing
that temporary center into the saved component. J3/J4 inference disagrees with
the visible supplied CAD cavities; J7 is intentionally internal. These warnings
are preserved, not suppressed or fixed by changing imported metadata. The CAD /
inference discrepancy and real cable clearance remain fabrication review items.

Format and TypeScript pass. Canonical tests retain **30 passes / one existing
B-010 strict-schema failure**, 272 assertions; historical fixture tests do not
validate the new placement. Native snapshots initially differed as expected;
after inspection only the PCB snapshot was updated, schematic snapshot unchanged.
Zero traces/vias, 130 top-side physical components and zero native errors remain.

The stale first package build was stopped before publishing after detecting its
old staging input. Staging was recreated and the corrected package rebuilt.
Only the reviewed fresh package build may be published. Publication excludes
this evidence directory and all documents/scripts, retaining required board
sources, genuine model assets, manifests and generated `dist/index/circuit.json`.

Still an unrouted prototype. B-005 paste, B-010 schema, B-015 fabrication BOM,
electrical qualification, exact screen/pack/load selection, mechanical fit,
routing, copper DRC and fabrication review remain open. The watcher stays paused.

## Verified publication

Implementation `0191b8e5db4c8c29dc7d75bcd43455cb1747200e` reached GitHub main.
The normal native file-by-file publisher exited0, 75 successes/zero failures,
creating private `0.0.2-wip-a1-connectors-outward`. Final exact readback verifies
all 75 hashes, no missing/extra/mismatched/unverified files. One initial URLError
on ControlsSheet.tsx was resolved by a targeted read-only retry; the original
receipt and retry are retained. All stage inputs stayed frozen and matched the
manifest after completion. The package includes native `dist/index/circuit.json`
and excludes documents, evidence/scripts/tests and unused assets. Registry
ready_to_build is true, errors null; completed cloud build is not established.
