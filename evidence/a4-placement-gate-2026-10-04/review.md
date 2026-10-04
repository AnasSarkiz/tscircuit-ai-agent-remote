# A4 placement gate review — 2026-10-04

## Outcome

**PCB footprint/component placement checks pass; the whole-board placement gate is BLOCKED on the external assembly interfaces. Additional routing remains disabled.** This is not an assertion of physical collisions: zero native placement errors and zero overlapping native CAD body bounding boxes were found.

The new `placement.circuit.tsx` builds the same `AiAgentRemote` through its native placement-only option. `routingDisabled=true`, saved phase replay, explicit USB pcbPath hints and the copper pour are disabled only in this inspection view. Canonical `index.circuit.tsx` retains its real four traces and saved regulator paths with `routeRemaining=false`. No imported definition, generated output, schema, check or fabrication test was patched. Run `bun run build:placement` for the inspection view and `bun run build` for the canonical partial-copper board.

The placement-native output contains zero traces, vias or pours. All source components/ports/nets/traces and all PCB components/ports/SMT pads/plated holes/NPTH holes/keepouts are exactly equal to the current canonical build, including IDs and coordinates. Regression checks compare both compiled native outputs. Existing canonical four traces and ground-pour geometry are exactly unchanged from the preserved A4 baseline. Warning/metadata output ordering changed on regeneration; the current canonical Circuit JSON hash therefore differs and is freshly committed/published.

## Checked evidence

| Check | Actual result |
|---|---|
|Native placement-only build|exit 0; zero copper routes, vias or pours|
|Required canonical netlist / pin specification / source / schematic-placement / placement|all exit 0|
|Native CAD body bounds (A4 models retained because exact component geometry/placements match)|126 purchased component models inspected; zero positive-volume AABB overlaps; eight native copper testpoints have no body model|
|Fresh placement PCB PNG|visually inspected; same positions and footprints as A4|
|Canonical native geometry|four preserved traces, zero vias; unchanged saved-route JSON and ground pour|
|Shorts on exact canonical dist/index/circuit.json|exit 0; applies only to the four current routes|
|Routing difficulty|76 heuristic regions; highest 5.4% near J7/R46, not an actual routing failure or success guarantee|
|Format / TypeScript / staged package TypeScript|exit 0|
|Tests|41 pass,2 retained failures,402 assertions; strict schema fixture and whole-board fabrication gate remain failing|
|Canonical build|exit 1;426 unconnected-port + 5 missing-trace errors retained|
|Preview snapshots|exit 0; unchanged existing approved WIP baselines|

Full native schema validation still has 166 failing elements, preserved in `schema-failures.json`. Automated placement checks do not validate solder paste, supplier orderability or an unmodelled flex/harness. The 431 unconnected/missing-trace errors are expected remaining routing work, **not** the reason for holding the placement gate.

## Bodies, access and mechanical limits

J3 native body-to-glass lateral gap is 0.8495 mm and body-to-case inside wall gap 3.2495 mm. J4/J8 corresponding gaps are 1.8250 mm and 4.1750 mm. All header body envelopes and underside leads stay outside the rotated pack's 35 mm-wide XY envelope; the conservative full-body lateral gaps are 0.5495 mm at J3 and 1.5250 mm at J4/J8. These are nominal CAD bounds, not tolerance guarantees or proven wire bend clearances.

All eight test pads are under the display body. The accepted assembly/test sequence must probe/program/check them before final display installation, or lift the screen during service. BOOT/RESET are internal and likewise require service access. USB-C remains bottom-edge accessible; its native shell protrusion is inside the case envelope. PH mated housings face down the internal right rail, allowing top assembly, but actual plug retention, wire turns and solder tails still need harness qualification.

The two mounting holes remain 2.2 mm NPTH with 6 mm-diameter all-layer copper keepouts. Actual screw heads, supports, driver access and case fastening are not selected/approved. The current TALK part **SKSWCFE010/C255576 is a top-push switch normal to the PCB**; a top-edge case button still needs a real actuator that transfers the edge press to that direction, or a qualified genuine side-actuated alternative. The MSK12C02 privacy switch also needs a case slider/linkage and travel clearance. Merely pointing a note toward the edge does not qualify either actuator.

## Specific prerequisites before additional routing

1. **Display J7 interface**: get a current BuyDisplay bare ER-TFT026-1 orderable option and visually review its exact outline/FPC drawing. Confirm the portrait tail path, pin1 end, conductor face, engagement and fold radius. The provisional panel n→J7(51−n) mapping must not be frozen or routed based on a presumed fold. The current manufacturer's searchable Rev3 text confirms the nominal 46 × 64 × 2.55 mm / 50-pin top-contact interface, but PDF graphic download/render remains unavailable. Fresh supplier search still only found accessories and a development kit, not a verified bare-panel listing. Indexed text alone does not approve the flex geometry.
2. **PCB thickness and stackup**: the 0.8 mm trial can reach 0.7 mm under the cited standard tolerance, below the PH header's 0.8 mm minimum applicable board thickness. Obtain a compatible manufacturer stackup/tolerance and redo USB impedance. The previous 1.6 mm / 90 ohm calculation is invalid for the current board. Existing short USB routes remain geometry-preserved trials, not impedance-qualified copper.
3. **Case/control/harness fit**: resolve the top-edge TALK actuator, privacy slider, current flex, mounting hardware and wire paths within 60 × 75 × 15 mm, maintaining antenna clearance. The 14.87 mm height allocation and 10% battery growth are conditional assumptions. Native body bounds establish nominal non-overlap only.
4. **Schematic/BOM/assembly acceptance**: battery J3 outer numbering remains explicitly pending and both outer pins stay open/unrouted. Mic/USB/charger paste qualification and remaining power-path/part-availability review remain open. Official core latest 0.0.2080 still includes the reverted polygon paste change (PR4344 was merged then reverted by4349); no relevant fix was installed during this review. B010/B015 are separate software/export validation issues and do not establish a physical placement collision.

A natural-language side-switch search found nothing; an exact ALPS family query returned three unrelated catalogue matches. All were rejected as alternatives, not imported/selected or treated as switches. No generic part or manually authored definition was substituted.

## Stage status and publication

Requirements: in progress; schematic/BOM: blocked; **placement:blocked** with native PCB checks passed; routing:existing partial experiments only, additional routing blocked; automated/fabrication gates remain blocked; physical prototype testing pending. This review does not change the display position, board outline, component population or physical placement. It adds a verifiable copper-free inspection mode and preserves the genuine saved routing state before future moves.

Intended public runtime version 0.0.2-wip-a4-placement-review includes the same current Circuit JSON and transitive board runtime/model/route dependencies only. This report, scripts and tests are excluded from that package. Exact remote results are recorded separately. A public registry update is not fabrication approval; previous required C262650 STEP HTTP413 remains an independent publication issue.

The background watcher remains paused and no issue messages are sent to another chat.

## Verified remote outcome

Source implementation9364e2c8 is public on GitHub; the fresh Circuit JSON matches anonymous remote bytes. Public tscircuit0.0.2-wip-a4-placement-review has91/92 matching runtime files including Circuit JSON; required C262650 STEP is404 after HTTP413, so B-009 remains open and ready_to_build=false. See [publication receipt](publication/review.md). Fresh current display PDF download returned403; no current visual FPC review was claimed. Outcome notes alter no runtime inputs.
