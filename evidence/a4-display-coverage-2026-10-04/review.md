# A4 physical display coverage trial — 2026-10-04

**Engineering prototype; NOT FABRICATION READY.** Parent public GitHub revision: `1ca49db16527d86674861c81b48b089801aca53d`. This is a real board implementation and provisional mechanical trial, not a qualified panel selection or production assembly.

## Coverage and implemented changes

The provisional BuyDisplay/EastRising ER-TFT026-1 no-touch display is portrait, with a 46 × 64 mm body centred at (−5.8, −0.8). Its actual overlap with the unchanged 50 × 65 mm PCB is 2,688.14 mm² / 3,250 mm² = **82.712%**. This excludes overhang, flex and enclosure bezel and conservatively uses the rectangular PCB area. The dimension and ±0.2 mm position allocation retains **81.737%**. Pixel-area coverage is a separate quantity and is not the user's target. The active-area offset is provisional.

The trial moves the top-assembled internal harness connectors into the right rail. Genuine untouched imports are J3 S3B-PH-K-S(LF)(SN), **C157929**, and J4/J8 S2B-PH-K-S(LF)(SN), **C173752**. They are through-hole side-entry parts, requiring manual/selective soldering. The actual native imported orientation is J3 rotation 0° and J4/J8 rotation 180°; all mating mouths face −Y along the internal rail. They do not require openings through the side wall. Mated housings and wire turns remain envelopes, not a verified harness.

J3 pin 2 remains PACK_NTC. Both outer pins remain unassigned and unrouted until the AKY2945/LP523450 keyed contact numbering is confirmed. The pack rotates to a 35 × 52.5 mm envelope behind the PCB at (0, −4.5). One M2 mounting trial moves to (22, −23); the other remains (−21.5, −29.5). These do not qualify actual screws, supports, battery restraint or a safe swelling allowance.

U27 becomes genuine **TPS60230RGTR/C1848364**. Panel cathodes 2–5 have four separate current sinks: D1–D4; D5 is open. R102 is genuine 10 kΩ RC0603FR-0710KL, giving nominal 15.6 mA/channel, 62.4 mA total by TI's typical equation. Actual temperature/rail/current bounds remain unqualified. Existing 50-pin, 0.5 mm top-contact J7 **AFC07-S50ECA-00/C262650** remains, and its panel n → connector (51−n) mapping is explicitly provisional for the new portrait fold. No display connector routes were created.

The PCB thickness is a **0.8 mm trial**, retaining four layers. This supersedes the old 1.6 mm USB impedance assumption. JLC's ±0.1 mm thickness range can extend below JST's 0.8 mm minimum applicable board thickness. Exact laminate stackup, fabrication tolerance and connector assembly acceptance must be resolved before freezing the board.

## Native model review and fit limits

The official native build generated the complete component CAD assembly (`board.glb`); top and side views were inspected. External display, battery, case, speaker/motor and mated harness shapes are labelled engineering envelopes, not custom electronic component definitions or physical hardware. The original four native traces and saved route files remain unchanged geometrically; no new routing was enabled. The CAD build with routing disabled still emits the **two existing MCU USB traces**, so `placement-only.json` is not described as fully unrouted.

Native CAD measurements put the tallest component under the screen at USB-C Z=3.651 mm. Display rear Z=4.05 mm gives a nominal CAD gap of 0.399 mm. The module manufacturer's maximum height plus provisional solder allocation gives a 0.2 mm screen gap. The tall header bodies lie beside the glass: minimum lateral gaps are approximately 0.850 mm at J3 and 1.825 mm at J4/J8. Header leads lie outside the rotated battery XY envelope. These measurements do not include unknown mating, solder, battery restraint, case flatness or flex tolerances.

The case remains at most **60 × 75 × 15 mm**. The conditional height allocation totals 14.87 mm, using 10% battery growth as an assumption, not a manufacturer guarantee. Nominal glass-to-antenna exclusion gap is 0.475 mm, reduced to 0.175 mm with the stated dimension/position allocation; other tolerances are unqualified. No metal, wiring or flex path through the antenna region is approved.

## Actual checks and remaining blockers

- Formatting and TypeScript pass. Tests: **38 pass, 2 retained failures, 389 assertions** across 14 files. The failures are the existing strict-schema fixture and the full-board fabrication gate.
- Native netlist, pin specification, source and schematic-placement checks pass for the implemented connections; final placement check passes after resolving overlaps and C40/R84 rotation suggestions. Supplier metadata/access warnings remain disclosed.
- Canonical build exits **1** with **426 unconnected-port errors + 5 missing-trace errors**. There are **four actual traces, zero vias**, with byte-equivalent geometric paths to the preserved A3 copper. This is not a fully routed board. `tsci check shorts dist/index/circuit.json` passes, but does not establish completion or current-carrying capability.
- Fresh Circuit JSON contains 134 physical components (126 purchased + 8 native testpoints), 496 PCB ports and 76 named nets. Strict native schema validation retains **166 failing elements**: 134 pcb_component, 15 pcb_group, 15 schematic_group, 2 pcb_hole. No outputs/schema/runtime were patched.
- Current board PCB and affected schematic sheets were visually reviewed; both changed preview snapshots were reviewed against the rendered PCB/affected schematic sheets, updated and verified with native snapshot exit 0. This accepts only the intended WIP preview changes, not unresolved fabrication checks. No fabrication Gerbers, assembly approval or physical testing is claimed.
- **Panel sourcing/current drawing is unresolved.** The current manufacturer's indexed Rev3 manual gives 46 × 64 × 2.55 mm; the accessible historical Rev1 drawing has 3.4 mm thickness and a different flex envelope. That historical drawing cannot qualify the current thin variant. No current purchasable bare-panel listing was verified; a development kit listing does not include the bare panel.
- The new portrait FPC shape, contact face, fold radius, pin-1 direction and actual connector engagement remain unqualified. The existing reverse mapping must not be routed as approved wiring until these are confirmed.
- Thin-board thickness/USB impedance, full mechanical tolerance budget, battery outer-pin polarity, mic/pad paste review and remaining full-board power/connection checks remain open. Existing native BOM/export and publication capacity issues are not hidden by this trial.

## Sources

[BuyDisplay current indexed manual](https://www.buydisplay.com/download/manual/ER-TFT026-1_Datasheet.pdf); current PDF visual download was unavailable. [Historical manufacturer drawing mirror](https://datasheet.octopart.com/ER-TFT026-1-EastRising-datasheet-36979851.pdf), inspected only as historical evidence. [TI TPS60230 datasheet](https://www.ti.com/lit/ds/symlink/tps60230.pdf), pin drawing inspected. [JST PH drawing](https://www.jst-mfg.com/product/pdf/eng/ePH.pdf), side-entry and mating drawings inspected. [JLC PCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities). Exact JLC imports succeeded; current production assembly stock is not guaranteed by that import success.

## Stage record and publication

Stage 1 in progress; stage 2 blocked; stage 3 in progress; stage 4 in progress (four preserved partial traces only); stage 5 blocked; stage 6 not started; stage 7 pending physical prototype; stage 8 WIP prototype only. Routing is limited to the preserved partial copper and `routeRemaining=false`.

The next public runtime package includes only transitive board sources, imported models, native saved routes, required configuration/dependencies and current `dist/index/circuit.json`; it excludes this report, scripts and other evidence. Intended version `0.0.2-wip-a4-display-coverage`. GitHub and anonymous registry hash receipts must be recorded before calling publication complete. Previous A3 publication had HTTP 413 on the required C262650 STEP model and remains historical incomplete evidence. The watcher stays paused; no issues are sent to another chat.
