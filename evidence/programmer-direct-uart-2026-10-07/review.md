# Standard UART connector and supply routing repair — 2026-10-07

**0.0.9-wip-standard-uart — engineering prototype, not ready to order.**
This revision implements the independent programmer repair. It does not implement the requested 2.8-inch LCD.

## Real implementation

J6 is now the genuine, untouched supported JLCPCB exact/download import **C160389 / JST BM03B-SRSS-TB(LF)(SN)**. Its source SHA-256 is `3472ba96022944cfae0bdd73c4330c3e873b5293d1ee179855923eee82a169d3`. PCB pose remains **(-17.4, -10.0) mm, 0° on top**. Contacts are 1 MCU_UART_RX, 2 GND, 3 SERVICE_UART_TX, 4/5 GND hold-downs. The old six-contact service connector's power, EN and BOOT contacts are removed; existing manual BOOT/RESET switches and separate power remain.

The public standard programmer v0.8.0 has TX/GND/RX at its three-contact target cable. A specifically numbered **1→1, 2→2, 3→3** JST SH three-contact cable connects programmer TX→target RX and programmer RX←target TX. This is a documented cable specification, not a tested cable assembly. The primary JST drawing has 2.9 mm unmated and 6.3 mm mated height: programming requires an open enclosure/display removal. No physical programming result is claimed.

UART RX and TX use authored native routes joining the preserved MCU/R38 copper. Two 0.2 mm top ground-pad links connect J6.2→J6.4→J6.5; they add no drills. A local audio-gate detour clears the new J6 hold-down. The obsolete J6 supply detour is replaced by a **0.8 mm bottom-layer V3V3 trunk** between its original distribution endpoints/vias; the obsolete top region is explicitly retired and retained historically. High-current routing stays on the outer layers. No purchased component other than J6 is moved or replaced. Original solver phase caches/imports remain unchanged.

## Evidence and validation

Final metrics and accepted native SHA are recorded in `final-qualification-summary.json` after actual native regeneration and independent checks. Earlier failures are retained. The raw general contact-preservation check correctly rejects renumbered/removed J6 contacts; the separate interface qualification maps all five retained roles and excludes only the three removed service contacts. Every other originally connected terminal pair remains mandatory.

The first new native exposed a 0.123887 mm audio/hold-down violation and two extra physical opens. The audio detour and actual UART copper fixed those. Three proposed ground-via escapes caused two incomplete native builds at 420/900 second budgets; neither produced accepted output. The source/event archives preserve both incomplete trials. Replacing them with two pad links completed native generation in 307.34 seconds with zero J6 errors, zero measured shorts/geometry violations, and 50 unchanged LCD errors. The subsequent width audit detected clipping of two obsolete top supply regions. The implemented 0.8 mm bottom bypass fixes that clipping: the completed 313.78 second native generation passes all 250 active region-width checks, preserves all 9,813 retained contact pairs and has zero J6 errors, measured shorts or geometry violations. A later documentation-only regeneration binds the corrected inventory wording to the published source; its separate outcome and comparison receipt are retained. No timeout is represented as a passing build.

Placement review now omits explicit phase indices in placement-only mode and enables the official root/platform routingDisabled controls. The earlier callback throw was caught by core and did not prevent routing. Stricter event capture demonstrated 13 forbidden starts before the legitimate source stage-control correction. Fresh native placement finishes with zero starts, zero copper records and zero native errors. Routed mode keeps its existing phase assignments. No generated native JSON or installed package bundle is patched.

## Actual completed qualification

| Check | Result |
| --- | --- |
| Native copper | 381 traces, 322 through vias, 273 pours |
| Shorts / geometry violations | **0 measured / 0 measured** by the independent native geometry audit |
| Connectivity | **50 native open-port errors: 46 J7 + 4 U27; 12 physically open nets** |
| J6 copper / prior connections | 0 J6 errors; all 9,813 retained numbered-terminal pairs preserved |
| Authored widths | All 250 active region widths pass; new supply bypass remains 0.8 mm |
| Purchased geometry | 124 parts unchanged; genuine J6 is the sole replacement; purchased pose moves: 0 |
| Ordinary vias | All 322: 0.30 mm drilled hole / 0.45 mm land / full board span; no blind/buried vias |
| High-current layer check | 67 native traces and 89 active authored trunks checked; top/bottom only |
| Source checks | Netlist, pin specification, source, schematic placement and placement pass |
| Code / routing regressions | TypeScript and formatting pass; **94 routing regressions pass** |
| Board test gates | **49 pass / 2 fail**: complete native connectivity and strict native schema |
| Actual schematic UI analysis | **15 style issues**, failed; CLI result is separately zero |
| Schematic explanations | All 135 native components covered across 13 circuit + 13 guide sheets |
| Source snapshots | Completed in 61.32 s; PCB and schematic differ from unchanged references; failed |
| Schema / fabrication | 169 native schema failures; 32 missing U16/U27 paste records; exports blocked |
| Current / trace widths | 381 traces / 623 wire segments measured; no trace below general 0.2 mm, 2 below explicit source minima, 65 below net nominal |

The physical measurement is not a full fabrication DRC pass. J3's unresolved outer contacts are not counted as connected nets. The explicit regulator minima and nominal-width branches require electrical/current qualification.

The faulty historical route-preservation assertion compared allocation-order native IDs. Replacing an eight-pad connector with a five-pad connector legitimately changes those IDs. Its corrected assertion requires the **entire exact wire geometry, widths, layers and real component/numbered endpoints**. Geometry and electrical partition requirements are retained. The initial failure and the intermediate helper error remain in the logs.

`schema-audit.json.gz` is the complete losslessly compressed failing schema output, with original and compressed checksums and verified round trip in `schema-audit-archive.json`; `schema-audit-summary.json` is only its index. `final-native/source-and-native-events.tar.gz` preserves the actual source and solver events. All incomplete builds/trials have separate retained source/event archives. The first snapshot run without references is explicitly marked uncompared; the later real comparison failed and did not update root references.

Fresh visual inspection covers the four-layer copper composite, the changed UART/top and supply/bottom areas, and the three changed schematic pages. The other 23 schematic PNGs exactly match their previously reviewed counterparts. Generated detail images alone are not treated as visual approval. The genuine USB-C import already uses the native `standard="usb_c"` schematic.

## Stock and cost

The exact official C160389 page at 20:07 UTC records `overseasStockCount=32191`, `canPresaleNumber=31559` and a $0.2743 reference price. The earlier 31,609 figure belongs to the initial dated receipt. Neither field establishes global warehouse totals, reserved assembler inventory or an order quote. The former C160405 had zero reported stock. The board still has 125 purchased components / 43 identities. All 43 exact identities were checked against official pages; initial HTTP429 responses and successful sequential rechecks are retained. Current public buyability covers 40 identities. U1/C2913201, D2/C94934 and U16/C54313 have `canPresaleNumber=0`; D2's zero overseas count conflicts with a positive search inventory and does not prove globally out of stock. `dated-stock-application.json` binds every actual reference/MPN to those records. The recomputed component reference subtotal is **$26.3055**, before setup/assembly/PCB/shipping/tax/external assemblies and minimum order quantities. No allocation or quote is claimed.

## Requested display: actual status

- Exact reviewed **candidate only: ER-TFT028A2-4, no touch / ILI9341**, manufacturer PDF archived at `../display028-integration-2026-10-07/primary/ER-TFT028A2-4_Datasheet.pdf`, SHA-256 `637fdf1c1d3e1bb76c9a3f534855007989b22854a9e32f2ed9caa483b4eae10c`.
- Landscape body **69.3 × 50.2 mm**; active **57.6 × 43.2 mm**; right-side FPC after 90° CCW rotation. Centered body covers 77.308% of 60×75 mm enclosure face. Overhang is expected and accepted by the request.
- **Final J7 pose is not qualified or implemented.** The old pose remains (8.2, -12.625) mm / 90°. No display-dependent purchased component is moved this revision.
- The exact 26.7 mm flat flex tail extends beyond the enclosure. Its numerical minimum bend radius is absent from the primary drawing. The required folded contact-face/numbering/latch-access arrangement cannot be inferred safely.
- The centered body overlaps the existing internal-antenna keepout by **59.5 mm²**. An external-antenna module is a candidate, not an implemented RF assembly; no exact antenna/cable/placement is qualified.
- The candidate backlight is **common cathode**, whereas the old four-sink circuit expects the opposite topology. Its four LED currents/sharing and new driver require qualification before wiring/routing. The old display pin map is not reused as if compatible.
- Preferred ER-TFT028A3-4 direct PDF remains inaccessible after fresh checks; applying the saved network draft is separate from current runtime access. No TLS/proxy/challenge bypass is used.

## Display implementation fields requested by the user

| Requested field | Actual current result |
| --- | --- |
| Display model | ER-TFT028A2-4 no-touch / ILI9341 is reviewed as a candidate; no new display is implemented |
| Finished landscape size | Body 69.3 × 50.2 mm; active area 57.6 × 43.2 mm |
| Position / coverage | Candidate centered on PCB; 77.308% enclosure-face body coverage; centered RF overlap 59.5 mm² |
| FPC / connector | 50 pins, 0.5 mm pitch, 0.30 ± 0.03 mm stiffened terminal; right-side exit after rotation; final folded face/numbering/bend/latch arrangement unqualified |
| Final J7 pose | Unassigned; actual old J7 remains (8.2, -12.625) mm / 90° on top |
| Purchased component changes | Genuine J6 replaced; all purchased poses retained; J7/U14/C42/C43 have not moved |
| Schematic changes | J6 direct RX/GND/TX with grounded hold-downs and matching explanation; old power/EN/BOOT service contacts removed |
| Physical routing changes | Actual UART RX/TX routes, two ground pad links, local audio-gate detour and full-width 0.8 mm bottom V3V3 bypass |
| Display/backlight routes | Not implemented; old display placeholder wiring remains deferred with 50 native errors / 12 open nets |
| Cost | 125 purchased placements / 43 identities; $26.3055 reference component subtotal, not an order quote |
| Order approval | **Not ready to order**; electrical, mechanical, stock, schema/paste/export/style/width gates remain |

## Remaining fabrication gates

The display/backlight still account for 50 native open-port errors and 12 physically open nets. J3 outer battery polarity is unnumbered in the primary supplier drawing, unassigned and excluded from that open-net count. Full zero-DRC/connectivity therefore has not passed.

Rounded native paste generator fixes are tested in canonical core source but unreleased; active U16/U27 paste is still missing. The latest official core 0.0.2108 still lacks the repaired branch. Strict-schema, polygon Gerber/official-short-check, U14 supplier rotation, two explicit regulator route-width minima, named-net nominal-width/current-capacity review, schematic UI style and assembler/stackup/mechanical qualification remain separate unresolved gates. Frozen active dependencies are retained; a newer version alone does not fix these defects.

No fabrication order, working-hardware, cloud-CI pass or prototype-ready claim is made. Full validation gates are retained rather than weakened.

## Reproducibility and publication

The source/model files, frozen lockfile and runtime package are byte-identical between the qualified 313.78 second run and the final documentation correction; only README, BOM and VALIDATION change. `documented-native/source-comparison.json` records that boundary. The first corrected-documentation generation timed out at a 600-second budget (610.13 seconds including cleanup), so it is not an accepted build; its complete source/events are retained. The separately logged retry restores the root dependency link used by the earlier completed run. A changed dependency link or elapsed time alone is not proof of a performance cause. Native acceptance requires completed regeneration and an exact record comparison before publication.

Whole staged whitespace checking retains diagnostics from exact generated CSV, CAD/import and historical evidence bytes; authored source/checkpoint whitespace checking passes. The complete raw diagnostics are archived losslessly in `staged-whitespace-check.log.gz`. Genuine imports are not normalized to conceal these warnings.

The corrected-documentation native regeneration completed in **285.65 seconds** with the frozen dependency link. Its exact new SHA-256 is **`bcee32a49486610d7379583efb2b378846cc75f232272b50c717ad129c495704`**. Every native record except the source filesystem MD5 is exactly identical to the fully qualified 313.78 second output; every other metadata field is also identical. `documented-native/comparison.json` establishes that the earlier copper, width, continuity, UI, schema, visual and snapshot results apply without rewriting their original hashes. The archive preserves the actual completed source and native solver events.

**Publication verified:** [GitHub implementation commit 1642750](https://github.com/AnasSarkiz/tscircuit-ai-agent-remote/commit/1642750d10d7dcf905c9e2299417984f7749985f) and [public tsci 0.0.9-wip-standard-uart native preview](https://tscircuit.com/AnasSarkiz/tscircuit-ai-agent-remote/releases/f520e705-7b21-4a06-89d2-a66b70ced491/preview). All 128 registry files exactly match the staged bytes; all 128 GitHub runtime paths match the committed source (only supported package-script metadata differs between repository/package); the public preview native object is exactly identical. The release is listed, latest and ready-to-build. No manual readiness RPC was called: normal supported archive publication completed that state. All exact receipts are archived here. Publication is a WIP delivery; it does not imply cloud CI, programming hardware, full DRC or fabrication approval.

Routing provenance: the accepted J6/supply repair is explicitly authored native copper with preserved original saved phase paths. It is not labeled as a new successful Pipeline9 or FreeRouting solution. The exact full-board exported SRJ is `final-native.srj.json`; its receipt retains the qualified native source hash, and the documentation-only record comparison proves the published geometry is identical. Previous rejected Pipeline9/FreeRouting trials remain in their own evidence directories.

The battery primary assembly drawing was visually reinspected during publication: it explicitly labels red (+), yellow (NTC), and black (−), but does not provide a numbered mating-contact view for the outer contacts. The illustrated schematic terminals are not supplier contact-number confirmation. J3 outer contact routing is still deferred.

Cloud execution is separate: the first automatic job snapshotted the incomplete upload and failed to resolve the missing AFC07 STEP. Its complete public logs are retained. The later job has the completed model upload, successfully reaches the real saved routing phases, and was last observed waiting on PcbCopperPourRender with no completed result. No duplicate rebuild was requested and no cloud CI pass is inferred. The uploaded preview/native verification is independent of that unfinished source job.

Cloud onboarding draft **revision 29** is confirmed saved/read back. It retains the original installation script, repositories, earlier startup instructions and all 20 custom network hosts while adding the current WIP continuation priorities. **Save/Publish in environment settings is still required to apply it.** No current runtime application or fresh-task restoration is claimed.
