# Validation — A1 integrated placement preview (work in progress)

## Connector orientation implementation — 2026-10-04

Parent source commit `3d6649aea36a1beac5901591659110dae014415f`. J4 speaker
changed +90° → −90°, J8 motor changed −90° → +90°. Actual native GLB views
confirm their cavities now face left/right board edges. USB-C/J3 battery/J6
service retain outward CAD openings. J7 stays internal for the raised display;
exact flex/latch/vertical access and all enclosure-side plug clearances are open.
Imported definitions and electrical connectivity are unchanged.

Evidence: `evidence/connector-orientation-review-2026-10-04/`, native before/after
JSON/GLB, inspected full-board/close-up 3D and PCB top, regenerated ratsnest/13
A4 sheet images, geometry/connectivity comparison and command logs. Native build
and all five pre-routing checks exit0. Placement zero errors/three warnings:
J3/J4 inferred directions disagree with supplied CAD; J7 is an internal connector.
Warnings remain visible. No imported insertion metadata was edited. Format/types
pass; canonical tests 30 pass/one existing B-010 failure/272 assertions. Native
PCB snapshot updated only after inspection; schematic snapshot unchanged.
130 physical top-side components, zero traces/vias/native errors remain.

This is a placement-preview step, not completed placement or fabrication approval.
All existing stage gates, B-005/B-010/B-015 and real mechanical/electrical
qualification remain open. Routing disabled; background watcher paused. The
same implementation/source commit **0191b8e5db4c8c29dc7d75bcd43455cb1747200e**
reached GitHub main, with exact `ls-remote` verification. Normal native file-by-file
publication exited0 with 75 successes/zero failures, creating private minimal
release **0.0.2-wip-a1-connectors-outward**, including the fresh native
`dist/index/circuit.json`. Exact-version listing and readback verify all 75
byte hashes, zero missing/extra/mismatched/unverified files. One initial network
readback error for ControlsSheet.tsx was resolved by a targeted read-only retry;
both attempts are preserved. All stage inputs stayed byte-identical to the
manifest through publication/readback. Privacy true, ready_to_build true and
reported build/transpilation errors null; completed cloud build is not verified.
This outcome record changes no runtime input and needs no additional publication.

## Runtime-only package step — 2026-10-04

### Verified publication outcome

Board implementation/source commit **81e745660507007623d7c0ccc5076fce237aa4b9**
was pushed to `origin/main` and its exact remote SHA verified. The normal native
publisher completed with actual exit0, **75 successes/zero failures**, creating private
release **0.0.2-wip-a1-board-runtime**. Exact-version API listing contains precisely
the reviewed 75 files. All 75 remote contents match the local manifest byte-for-byte,
including `dist/index/circuit.json`; zero missing, extra, mismatched or unverified files.
No document, investigation script, test fixture or unused component/model was uploaded.

Readback reports `is_private=true`, `ready_to_build=true`, with null reported cloud
build/transpilation errors at that observation. This confirms publication, not a completed
cloud build or manufacturing approval. Native process receipt, safe upload log and full
hash/readback receipt are preserved in this directory. The earlier compressed method
was rejected by automatic approval review and was not used; standard native upload
succeeded after the genuine, verified CDN re-imports described below.

B-009 no longer blocks this runtime-only board publication. The oversized full-evidence
release history remains incomplete, and the registry upload-size limit was not fixed.
All fabrication/electrical/schema/BOM and physical-test gates retain their prior status.
This outcome-only record changes no runtime package input and requires no new registry
version or repeat upload. Background automation remains paused and routing disabled.

### Current method: standard native upload with genuine CDN imports

The user supplied `AnasSarkiz/magnetic-shutter-remote--01a0f81f` as the publishing
reference. Its genuine imported TSX files link to modelcdn.tscircuit.com. We verified
the installed CLI's supported default non-download import workflow and re-imported
32 exact JLC part numbers, preserving each existing native footprint-selection mode.
Only 27 complete native importer outputs whose changes were limited to model import
statements and model URLs were installed. No generated definition was hand-edited.
The five candidates with changed courtyards/pin labels remain review evidence only;
C5656610 was not re-imported, preserving the explicitly authorized 0.60 mm hole.
All 54 accepted CDN assets were fetched read-only and matched the original local
OBJ/STEP assets byte-for-byte. Source comparisons and hashes are preserved here.

The final runtime folder contains **75 files**: 70 transitive board source/model
files, four build manifests/config/lock files, and native `dist/index/circuit.json`.
The earlier 129-file local-model plan is preserved as
`initial-local-model-package-manifest.json`. Documents, tests, diagnostics, scripts,
unreferenced imports/models and installed dependencies remain outside the upload.

The original compressed-upload attempt was rejected by automatic approval review
before a publisher process started because older background instructions prohibited
that method. No compressed upload was performed. The user's reference led to this
supported source/import change, and publication now uses ordinary native file-by-file
upload with `--include-dist --private`, respecting the original method restriction.
This removes the previously oversized model from the upload without deleting required
module dependencies, patching component definitions, or bypassing build checks.

Independent revalidation and fresh native JSON are recorded in the `cdn-*` receipts.
All five native pre-route diagnostics, independent TypeScript/build, root formatting/
TypeScript and native snapshot passed. Tests remain 30 passes/one existing B-010 failure.
One tool session interrupted the final build before producing its artifact; the build
was restarted after confirming no competing process and its actual exit0 was preserved.
The final JSON element counts, PCB geometry, courtyards, pads, schematic data and
connectivity match the reviewed A1 artifact. Its only differences are 104 instances'
OBJ/STEP URL fields and the native filesystem checksum. The 54 remote models have
identical byte hashes; previous inspected PCB/schematic/3D views remain applicable.
The final package is 13,463,789 bytes across 75 files; largest file is 3,046,769 bytes.
The target remains private WIP `0.0.2-wip-a1-board-runtime`. Native process completion
and exact-version remote readback must both be verified before declaring publication
complete. Routing and fabrication remain unapproved; automation stays paused.

### Initial preparation (superseded file count and upload method)

The user requested a registry package containing only files needed to run the board,
including a built Circuit JSON. A source dependency walker now prepares `.publish/board`
without altering board source or imported definitions. It rejects missing/escaping
modules, unreviewed external modules and dynamic imports. The publish folder is excluded
from root tooling/Git; the preparer, reviews and evidence remain only in GitHub.

The package contains 124 transitive TS/TSX and referenced OBJ/STEP files, four build
manifest/config/lock files and the native `dist/index/circuit.json`: **129 files**.
No documents, investigation fixtures, scripts, tests, snapshots or installed dependencies
are included. Direct build dependencies retain exact official pins; the minimal Bun lock
is derived from the existing project lock by removing unused direct dependencies.

Independent installation, TypeScript check, native build and all five pre-route checks
passed. Root formatting and TypeScript checks passed. Root tests have 30 passes and the
one existing B-010 native schema failure (272 assertions). A network-enabled final build
restored actual supplier orientation metadata; the earlier sandbox-only build's supplier
lookup warnings are recorded, not used as the final upload artifact.

The final emitted JSON differs from the reviewed A1 artifact only in its native source
filesystem checksum. All physical geometry, connectivity and element counts match:
130 physical components, 73 source nets, 13 schematic sheets, zero PCB traces/vias.
The previously inspected A1 board/schematic views remain applicable. No checks or native
outputs were patched, and this packaging step does not change fabrication readiness.

Full previous publication `0.0.2-wip-a1-integrated-placement-preview` ended exit1:
1232 successes/118 reported failures. Exact readback found 108 of those failures present
byte-identically and ten missing; package private=true/ready_to_build=false. That release
remains incomplete. Its receipt is retained in `evidence/integrated-preview-publication-2026-10-04/`.

This new runtime package targets `0.0.2-wip-a1-board-runtime`, using the official native
`--compress --include-dist --private` workflow. Current reduced file count/size/hash
manifest and check results are in `evidence/minimal-board-publication-2026-10-04/`.
Publication outcome and exact-version readback will be recorded after native upload;
no successful upload or cloud build is claimed before verification. The user's newer
minimal-file publishing scope replaces the earlier full-evidence upload scope. Background
automation remains paused; board routing remains disabled.

Updated 2026-10-03, Europe/Tirane. **A complete native unrouted board now exists.**
This milestone implements the user's new priority to visualize the integrated
prototype before full component/mechanical qualification. It overrides the prior
preview gate only; it does not approve routing, fabrication or hardware operation.

| Stage | Status | Current evidence / remaining work |
|---|---|---|
| 1. Requirements | in progress | 50 × 65 mm preview after 50 × 55 trial; display/pack/NTC/mounting/current/stackup/RF tolerances provisional |
| 2. Schematic/BOM | blocked for fabrication | Complete integrated 13-sheet A4 schematic and genuine 122-part inventory authored; B-005 paste and electrical/load/privacy/temperature/component qualification unresolved |
| 3. Unrouted placement | in progress | Actual top PCB, ratsnest and native 3D generated/inspected; native overlap/pad/courtyard errors zero; connector access warnings disclosed; final physical fit not qualified |
| 4. Routing | not started | Explicitly disabled; zero PCB traces/vias; no genuine saved routes yet |
| 5. Board checks | in progress | Native preview build passes; current command receipts below; one pre-existing B-010 schema regression remains; no routed copper validation |
| 6. Prototype fabrication | blocked | B-005 polygon paste, qualification, final placement, routing, DRC and fabrication outputs incomplete |
| 7. Physical tests | not started | No prototype or measurements |
| 8. Store release | in progress | Private WIP publication required; no fabrication/hardware-tested claim |

## A1 implementation and evidence

Source parent: `98a3f7ece77d3b15d92cd21fcf333ff5c951a2e4`. The commit containing
this milestone is the A1 source revision. Dependency pins remain official core
0.0.2070/easyeda0.0.370/CLI0.1.2235/tscircuit0.0.2742; no runtime or imports patched.
New side switch C431540 was imported using the supported exact-footprint workflow.

Entry `main.tsx`; application-only modules in `src/board/`; immutable reviewed
fixtures retained. Root nets are shared across sheets. New native-output tests
verify rail/GPIO/external-port boundaries, unique shared nets, top-only population,
130 physical components (122 imported parts +8 copper pads), and zero traces/vias.
They do not establish dynamic privacy, full-schema acceptance or hardware safety.

Actual views, command logs, JSON, native GLB and 13-page A4 PDF are in
`evidence/integrated-preview-2026-10-03/`. The original overlapping 50 ×55 trial
is retained under `initial-50x55/`. Schematic display/clock coordinates were
moved inward after visual review found labels near/beyond the A4 border. Passive
orientations were improved based on the native pre-route placement diagnostic.

The ESP32 physical antenna area overhangs the upper edge; the four-layer keepout
excludes only U1 because the antenna/module itself intentionally occupies it.
No other component/copper exemption exists. Display body/active area are native
PCB notes and require a raised Z arrangement; they are not a populated display
footprint or verified CAD enclosure. The top actuation mechanism is provisional.
The 3D bottom is unpopulated, showing only board holes/connector overhang.

J3 C265101 uses assumed pack pin1 BAT/pin2 GND/pin3 NTC; exact mating harness is
unqualified. Charger USB100 defaults, ~297 mA nominal ISET candidate, default
open TMR/ITERM and real external TS are wired. USB suspend/entitlement, battery
readiness, pack PCM/current/NTC and thermal limits remain fabrication/operation
qualification blockers. No powered test is claimed. Backlight uses a provisional
100 Ω series resistor from VSYS with PWM MOSFET; brightness, low-VSYS headroom
and exact panel limits remain open. The side SPDT switches MIC_INPUT feeding the
hardware-HOLD-enabled 2.8 V mic LDO; switch throw mapping, inrush, bounce, partial
rail injection and privacy turn-off timing still require qualification. The
comparator and VMIC-powered open-drain clocks retain previous conditional bounds.

Native imported connector/transistor category and ground-role warnings remain
B-007 metadata limitations; actual named net connectivity is tested separately.
J6 internal service harness and J7 internal FPC generate connector-facing warnings
without explicit imported insertion-direction metadata. These are disclosed
preview limitations; no definition is patched to silence them. Actual mechanical
connector/FPC access must be qualified before fabrication. Exact-current stock,
land/mask/paste acceptance, silk readability and raised-display clearance remain
open; zero native placement errors alone do not complete stage3.

The final native full-board build and all five pre-route diagnostics exited 0.
Formatting, TypeScript checks and native snapshots also exited 0. Canonical tests
have 30 passes and one pre-existing B-010 failure. Strict full-board schema
validation separately rejects 156 native elements: 130 PCB components, 13 PCB
groups and 13 schematic groups. Raw outputs remain unchanged. The native
13-page A4 PDF and top/bottom GLB renders completed and were inspected.

Current build/tests/export results and source hashes are recorded in
`command-results.json`, `preview-summary.json`, `source-manifest.json` and logs
in the A1 evidence directory. Publication status is tracked separately from
board build success; earlier releases are version-specific historical records.
The user keeps the background watcher paused.

## Historical A0 validation (preserved; current A1 status above supersedes it)

# Validation — A0-reference-import-review (work in progress)

Updated: 2026-10-03 (Europe/Tirane). **B-008 is resolved on the four affected genuine imports using official easyeda0.0.370 and core0.0.2070; B-003 ground ports rechecked successfully. B-005 polygon paste remains a real assembly blocker. Native schema, complete hardware/component/mechanical qualification and fabrication outputs remain unfinished. No complete handheld schematic/PCB exists.** A0 is an untested engineering prototype, not a fabricated board revision.

| Stage | Status | Evidence and remaining work |
|---|---|---|
| 1. Confirm requirements | in progress | Accepted square, screen-dominant, one-button, top-side-only concept; 50 × 50 mm study target within approved 50 × 65 mm maximum; rechargeable pack/display mechanics/current budget/stackup unresolved |
| 2. Schematic and BOM | blocked | Historical B-001 corrected, encoder unselected; B-002 local 0.60 mm correction verified; B-003 generator issue resolved; B-004 search discovery, B-005 ground paste, and full component qualification, exact pack and circuit pending |
| 3. Placement before routing | not started | Depends on stages 1–2; isolated diagnostic fixtures exist, no complete-board placement |
| 4. Copper routing | not started | User authorized routing after prerequisite gates pass; no routes exist |
| 5. Automated and visual checks | not started | Preliminary import checks below do not complete board validation |
| 6. Prototype fabrication | not started | No full-board fabrication files; microphone-only unrouted diagnostic Gerber ZIP exists and fails stencil qualification |
| 7. Physical prototype | not started | No hardware or physical test evidence |
| 8. Store release | in progress | Standing publication authorization; private WIP source released with disclosed build blockers; no qualified release package |

## Source and dependencies

Project: `boards/tscircuit-ai-agent-remote--01a0fe57`. No earlier board was reused. The Git milestone containing this file identifies the source revision (`git rev-parse HEAD`). `evidence/source-manifest.sha256` is the historical 2026-10-02 milestone manifest, not a checksum of later changes. The update-check directory contains a separate current manifest. Manifests exclude themselves, Git metadata, dependencies, build output and logs. User-authorized C370970 edits are explicitly audited below; original import is preserved in revision 341dcaa.

Current pinned dependencies: tscircuit **0.0.2742**, @tscircuit/cli **0.1.2235**, direct @tscircuit/core **0.0.2070**, easyeda **0.0.370**, @tscircuit/props **0.0.682**, circuit-json **0.0.513**, TypeScript **5.9.3**, Biome **2.5.14**, @types/bun **1.4.2**. Runtime Bun **1.3.9**. `bun.lock` records transitive dependencies. Installation emitted peer-version warnings involving circuit-json 0.0.509, React/ReactDOM 19.3.0 and @tscircuit/alphabet 0.0.25; unresolved, not accepted board warnings.

Initializer succeeded; optional skill download failed under sandbox networking. Installed tscircuit skill and current official handbook were read. CLI help verified required netlist, pin_specification, source, schematic-placement, placement and shorts commands, PNG/SVG builds and snapshots. Native A4 API verified in installed @tscircuit/props: `<schematicsheet name displayName sheetIndex sheetSize="A4">`. No complete board sheet has been rendered/reviewed; the isolated encoder review is recorded below.

## Requirements

Approved maximum **50 × 65 mm** supersedes initial approximately 50 × 45 mm. The accepted design is square with a dominant front display, one top-edge hold-to-talk button and top-side PCB assembly only. A **50 × 50 mm** square is the initial study target, not a validated dimension. Four copper layers remain intended. Retain 5 V USB-C sink/native USB, protected 500–1000 mAh 1S rechargeable LiPo (nominal 3.7 V, 4.2 V charge), charger/power path, 3.3 V rail, ESP32-S3 antenna module, two digital microphones, color display, I2S amplifier/external 8 Ω speaker, internal haptic and service BOOT/RESET/test access. Encoder, exterior APPROVE/REJECT, privacy slider, separate exterior power control and front RGB indication are superseded. Hardware privacy architecture using the single-control interface remains unresolved. See `REQUIREMENTS.md`; firmware is outside scope.

JLCPCB is the intended board/assembly manufacturer. Final stackup, copper weight/thickness, trace widths, clearances, drill/via limits, current limits and layer spans have **not** been selected or validated. Do not treat default geometry as a manufacturing specification. Exact battery protection/thermistor/polarity/rating, display procurement/interface/mechanics, mounting, enclosure and RF clearance must be resolved before stage 1 passes.

ESP32-S3-WROOM-1-N8R8 octal PSRAM reserves GPIO35/36/37. Manufacturer antenna guidelines were consulted; no RF keepout is laid out. Hardware microphone privacy requires supply isolation and prevention of clock/data phantom power; Ioff buffer candidates are not electrically qualified.

## B-001 — C370970: resolved locally for reported drill dimensions

**ALPS EC11E15244G1, C370970.** Original supported import: `tsci import --jlcpcb C370970 --use-exact-footprint --download`. The user subsequently authorized removing the custom symbol and correcting this footprint. Import log, supplier record and `evidence/imports/C370970-audit.json` preserve original measurements; original source remains in revision 341dcaa. The external supplier library remains unchanged.

| Feature | Original import | Corrected local source/generated geometry | Official ALPS range | Result |
|---|---|---|---|---|
| Five terminal holes | 1.3000228 mm diameter | 1.05 mm | 1.00–1.10 mm | pass |
| Two mounting slots | 3.200019 mm long | 2.65 mm | 2.60–2.70 mm | pass |

Exact-part mounting GIF and EC11E catalogue page 2 drawing 2 were inspected: `references/alps-ec11e15244g1-mounting.gif`, `references/alps-ec11e.pdf`, `evidence/datasheets/alps-ec11e-2.png`. The 14.5 mm row spacing is correct. Manufacturer 12.5 mm measures outside slot edges, not center spacing; neither is falsely flagged.

Originally affected stages: 2–6. The user's explicit instruction “even thefootprint update it” overrides the workspace no-patch restriction for this C370970 correction. Only five holeDiameter and two holeWidth values were changed. Pin labels, all centers, slot widths/90° orientation, outer pads, silkscreen, courtyard and models remain unchanged. This resolves the reported nominal dimensions; full board stages remain pending.

C209762 / EC11J1525402 was researched/imported as an alternative but ALPS marks it **Not Recommended for New Designs**; unselected and not fully qualified. C370970 is now unselected because the user accepted a single-button design; its correction/evidence remain historical.

## Other preliminary evidence

C109322 / TPS63070RNMR was rejected for missing physical pin identities 8/13 (grouped same-net pads) and lost PS/SYNC alias. This is not a diagnosed short. Alternate C2845237 / TPS63802DLAR retains all ten pin identities/functions; two identity tests pass, but application design, passives, full footprint/model review and current limits remain pending. Official DLA0010A package/land pattern, pages 35–36, were rendered and inspected: `evidence/datasheets/tps63802-35.png` and `tps63802-36.png`.

Waveshare 1.54 inch display schematic page 1 was inspected (`evidence/datasheets/waveshare-1.54-1.png`). **J1 and PH connector J2 have opposite listed pin order:** J1 VCC/GND/DIN/SCK/CS/DC/RST/BL; J2 BL/RST/DC/CS/SCK/DIN/GND/VCC. Final module/connector procurement remains unresolved. Downloaded DXF is unreviewed; no display component was authored.

Free-text import `1.54 LCD` selected unrelated DSK110 / C908227; excluded from selected components. Initial formatting touched whitespace in four imports; restored through supported importer, original C109322 checksum matched. `imports/**` is excluded from formatting.

## Commands actually run

Commands run from this project directory. Logs under `evidence/tooling/`.

| Command | Actual result | Log |
|---|---|---|
| `bun run format:check` | exit 0 | format-check.log |
| `bun run typecheck` | exit 0 | typecheck.log |
| `bun test` | exit 1; original four checks pass, new microphone-opening check fails | import-qualification-current.log; B-002 below |
| `bun run build` | exit 1; complete board not yet authored | build-blocked.log |

Build guard in `main.tsx` prevents claiming an incomplete board built successfully. Tooling success does not establish electrical correctness. Earlier `import-qualification.log` records rejected TPS63070 checks, not current board results.

Required placement checks (`netlist`, `pin_specification`, `source`, `schematic-placement`, `placement`) have **not** run against the complete handheld circuit: none exists and stage 2 is incomplete. Isolated encoder placement review below does not pass the complete-board stage. Routed board build, `check shorts dist/index/circuit.json`, snapshot and copper-layer visual review have **not** occurred. No board DRC/shorts pass or snapshot acceptance is claimed.

## Routes and fabrication

Supported native route-cache type `{pcbTraces, cacheKey}` exists; cache-key generation/reuse still needs verification. `routes/README.md` records route preservation/repair intent. **No saved routes exist.** There is no copper to move or repair and no fabrication package.

Complete A4 sheets, bodies/courtyards, connector/test access, holes, each copper layer, critical power paths, mask/paste, outline, drills, assembler feedback and fabrication exports remain unreviewed. No accepted board warnings, physical measurements, hardware photos or test results are invented.

## Historical user-authorized chip-box symbol review — 1f63764, 2026-10-02

The user requested updating C370970's imported file to remove its custom symbol and use a native chip box. This explicitly overrides the imported-symbol no-edit rule for this schematic change only. The component already used `<chip>`; only its `symbol={...}` property was removed. Exact comparison against revision 341dcaa proves every byte outside that property is unchanged, including physical geometry, pin labels, supplier identity and CAD models. Before/after source and footprint checksums are recorded in `evidence/imports/C370970-symbol-change.json`.

Isolated fixture: `evidence/encoder-chip-box.circuit.tsx`, native A4 sheet, PCB generation and routing disabled. Command: `bunx --no-install tsci build evidence/encoder-chip-box.circuit.tsx --disable-pcb --routing-disabled --schematic-svgs --schematic-png`, exit 0. Log: `evidence/tooling/encoder-chip-box-build.log`. Preserved JSON/SVG/PNG: `evidence/encoder-chip-box-circuit.json`, `encoder-chip-box-schematic.svg`, `encoder-chip-box-schematic.png`. PNG visually inspected: rectangular chip box; source JSON retains exactly pins 6–12 with existing labels.

CLI reported three warnings for this isolated passive encoder: all pins underspecified, no requires_power pin, no requires_ground pin. Warnings remained visible; no pin attributes or checks were altered to hide them. At that symbol-only revision B-001 remained blocked and the footprint was byte-identical. This historical component-only preview did not approve complete-board stages.

At the symbol-only revision formatting/TypeScript passed and import tests reported 2 pass / 2 fail. Supplemental Git whitespace review found trailing whitespace on line 11 of the CLI-generated SVG; the native artifact was preserved exactly. Authored-source whitespace review passed separately. Current corrected-footprint results follow below.

## User-authorized footprint correction and component review — 2026-10-02

Audit: `evidence/imports/C370970-footprint-change.json`, including before/after checksums, exact changed attributes and generated measurements. Five terminal holes now measure 1.05 mm; two slots measure 2.65 × 1.5000224 mm at 90°. Existing outer pads give a minimum terminal annular ring of 0.3749982 mm and minimum slot annular ring of 0.3999865 mm. All original pin/pad locations are preserved; pitch/row spacing were not the reported failures.

Isolated native A4 component fixture: `evidence/encoder-footprint.circuit.tsx`. Built with `bunx --no-install tsci build evidence/encoder-footprint.circuit.tsx --routing-disabled --pcb-png --pcb-svgs --schematic-svgs`, exit 0. Initial sandbox supplier fetch failed; a repeat with network access succeeded without suppressing checks. Build log: `evidence/tooling/encoder-footprint-build.log`. Preserved output: `evidence/encoder-footprint-circuit.json`, `encoder-footprint-pcb.svg`, `encoder-footprint-pcb.png`, `encoder-footprint-schematic.svg`. PNG inspected; generated holes/slots measured from JSON; zero PCB traces confirms routing remains disabled.

`bunx --no-install tsci check placement evidence/encoder-footprint.circuit.tsx` passed with **0 errors / 0 warnings**; `evidence/tooling/encoder-footprint-placement.log`. Native build retains the same three pin-specification warnings for the isolated passive encoder; no attributes or check limits were changed. All four original import tests now pass. Complete-board schematic/BOM qualification remains pending.

The selected values target the middle of ALPS's hole/slot-length ranges. Stage 6 must confirm actual **finished plated** hole/slot tolerances with the fabricator, not assume tool diameters prove finished fit. Physical insertion/retention remains untested. This local correction does not repair the official supplier library, complete the handheld circuit or create fabrication files/routes.

The network-enabled build created `.tscircuit/cache/` supplier metadata. This generated runtime cache is excluded from source control, the source checksum manifest and authored-source formatting; its canonical content is not manually reformatted. PCB source/geometry tests and all validation limits remain unchanged.

## Historical B-002 diagnosis — locally corrected in the later milestone

Continued stage-2 component review after resolving B-001. Official TDK DS-000069 v1.2 page 10 confirms all six imported pin identities/functions. Page 17 recommends a PCB acoustic hole of at least **0.50 mm**; the unchanged imported footprint contains **0.3999992 mm**. This is below the manufacturer recommendation, not an absolute electrical-rating violation or diagnosed short. The physical microphone sound port is 0.375 mm; reliable alignment/acoustic integration requires the PCB opening review.

Source audit: `evidence/imports/C5656610-audit.json`. Primary manufacturer PDF was read through web access; direct local download instead returned HTML, preserved as `evidence/downloads/TDK-ics-43434-download.html`, not treated as a PDF or visual package review. [Official datasheet](https://product.tdk.com/system/files/dam/doc/product/sw_piezo/mic/mems-mic/data_sheet/ds-000069-ics-43434-v1.2.pdf).

Prepared exact unapplied proposal: `evidence/proposals/C5656610-acoustic-hole.diff`, changing only the acoustic-hole diameter to **0.60 mm**, preserving its center, electrical pads and all other component content. No microphone component edit has been applied. User authorization so far covers C370970; the workspace instruction prohibits patching other imports. The user reaffirmed **"Wait for the upstream correction"** after the 2026-10-03 recheck. The proposal remains unapplied, and dependent stages 2–6 cannot pass yet.

Added an independent manufacturer-minimum test; the original four checks remain unchanged and pass, while the microphone opening test fails. Current logs distinguish this new failure from resolved B-001. No checks were relaxed or bypassed. Supplier lifecycle pages additionally conflict (TDK Product Center Production/NRND versus InvenSense EOL); final microphone selection/procurement remains unresolved and no active-production claim is made.

## Published-release recheck and accepted design — 2026-10-03

The user asked to check the upstream fix and accepted the square product concept,
top-side-only assembly, one top hold-to-talk button, speaker and rechargeable
battery. `REQUIREMENTS.md` is the authoritative requirement update; the original
brief and encoder evidence remain historical. Final size and mechanical fit are
unverified. No PCB has been laid out from the generated product illustration.

Queried the public npm registry directly and installed exact released versions
**tscircuit 0.0.2736 / CLI 0.1.2232**, with core 0.0.2052 and props 0.0.676.
Published metadata, original manifest/lockfile backup and installation log are
under `evidence/update-check-2026-10-03/`. The installation still reports the
circuit-json peer-version warning; it has not been accepted as a board warning.
The dependency change invalidates assuming earlier generated results apply to
this toolchain; current complete-board checks remain unperformed.

Fresh supported import command, run in the isolated recheck subdirectory:
`tsci import --jlcpcb C5656610 --use-exact-footprint --download`, exit 0. Source
still measures **0.3999992 mm**, as does the generated `pcb_hole.hole_diameter`.
The microphone source in the main import directory remains byte-identical to the
previous audit. B-002 remains **blocked**; no local microphone correction applied.
Audit: `evidence/update-check-2026-10-03/microphone-check.json`.

An isolated native A4 fixture was built with routing disabled to inspect the
fresh import: `microphone-import.circuit.tsx`. Diagnostic build exited **1**:
required power/ground are unconnected in this component-only fixture, and the
CLI reports an ambiguous `GND` alias across separate pads, suggesting `pin3` or
`3`. These errors were preserved, not suppressed; this is not a passing
schematic or import electrical qualification. Generated JSON, PCB PNG/SVG and
schematic SVG were preserved. PCB PNG inspected; JSON confirms one 0.3999992 mm
hole and **zero PCB traces**. No full schematic visual review is claimed.

Rechargeable system requirement: protected 1S nominal 3.7 V, 4.2 V-charge pack,
500–1000 mAh target, USB-C charging, power path and 3.3 V supply. BQ24074 and
TPS63802 imports remain candidates, not an integrated power circuit. The genuine
JST **S2B-PH-SM4-TB(LF)(SN) / C295747** was imported with the same supported
workflow and copied verbatim into `imports/`; TSX/STEP/OBJ hashes and provenance
are recorded in `C295747-import-provenance.json`. Supplier identity and SMT
right-angle construction were checked. Official JST drawing download returned
403; complete footprint, mating polarity, temperature sensing, pack protection,
current/thermal budget and fit remain pending. No battery pack MPN or runtime is
invented. Board assembly and fabrication gates have not passed.

Final checks for this update: formatting exit 0; TypeScript exit 0; `bun test`
exit 1 with **4 pass / 1 fail** (unchanged manufacturer-minimum microphone
failure). Logs are in the update-check directory. Authored-source whitespace
review passed. Existing full-board checks remain unavailable because the
complete circuit has not been authored; the main entry retains an explicit
incomplete-design guard. No passing fabrication or routing stage is claimed.

The user's final choice is to wait for the upstream correction. No local
microphone edit, alternative microphone substitution, scheduled monitoring or
dependent layout/routing work was initiated. The accepted concept and battery
requirements/import preparation are saved for resumption.

## A0-C5656610-local-hole — user-authorized implementation step

Date: 2026-10-03. The latest direct user instruction authorizes manually updating
C5656610's footprint after verifying the supplied investigation. This overrides
the no-patch rule for this acoustic-hole correction and supersedes the earlier
wait instruction. No broader imported pin-map or geometry modification is
assumed authorized.

Reviewed the linked investigation and copied its findings/raw response into
this task's evidence directory. Independently calculated the raw EasyEDA hole:
`0.7874 × 0.254 × 2 = 0.3999992 mm`. Supplier owner is `lcsc`, writable is false.
This corroborates the supplier-footprint origin; converter output preserves it.
TDK DS-000069 v1.2 page 17 recommends at least 0.50 mm. The chosen 0.60 mm target
is a local correction, not a manufacturer-required exact diameter.

Only `diameter="0.3999992mm"` changed to `diameter="0.6mm"` in the main import.
The original source is preserved in commit 32a05e5 and the new evidence folder.
An exact byte comparison, recorded before/after SHA-256 and generated geometry
prove the hole center and all non-hole content are unchanged. No supplier record
or converter code was modified. The old proposal and update-check evidence
remain historical; they do not describe the current corrected import.

Current evidence: `evidence/microphone-local-correction-2026-10-03/`.

| Check | Actual result |
|---|---|
| Formatting | exit 0 |
| TypeScript | exit 0 |
| Existing import qualification tests | exit 0; 5 pass / 0 fail; unchanged manufacturer limits |
| Corrected native A4 component build, routing disabled | exit 1; B-003 source_ambiguous_port_reference |
| Generated acoustic hole | 0.60 mm at (0.7650734, 0) mm |
| Generated copper pads | all 9 shapes unchanged from the baseline geometry |
| Minimum hole-edge-to-copper distance | 0.2580203036 mm, measured against polygon segments and rectangles |
| Isolated placement check | exit 0; 0 errors / 0 warnings |
| PCB traces | 0; routing remains disabled |
| Whole-board build | exit 1; main circuit remains incomplete |

The PCB PNG was inspected. The diagnostic schematic exists but is not a complete
microphone application or full-board schematic review. Ground and supply nets
were added in the fixture to exercise mandatory pin connectivity without fake
purchased components. The initial incorrect leading-dot shorthand selector was
corrected to the documented `MIC1.pin3` / `MIC1.pin5`; the unsuccessful initial
log is preserved and is not accepted evidence of a successful build.

**B-002 is resolved locally for the acoustic diameter. B-003 remains blocking:**
core rejects pin 3's four non-overlapping polygon pad segments, creates no PCB
port for GND, and leaves all four ground pads with null PCB-port IDs. The logical
GND source trace exists, so using a numeric alias does not fix native PCB-port
creation. No pin mapping, pad geometry, DRC or snapshots were changed to conceal
this error. Stage 2 remains blocked; complete-board checks and stages 3–6 have
not passed. This does not diagnose a short or validate physical acoustics/assembly.

The user explicitly authorized publication to both GitHub and tscircuit after
the initial automatic approval rejection. GitHub `main` was successfully pushed
and read back at c3e8570f2bc4a462c2856cab26bab7fc96afaeb8, containing correction
commit 54bb3c0f899923eca45ecbc85d08a385df6aa550.

Private tscircuit source version **0.0.2-wip-c5656610-hole-060** was published
with all 173 files uploaded and exit 0. The initial 0.0.1 prerelease remains a
partial upload: its compressed archive exceeded the server limit and one USB-C
STEP model timed out during individual upload. The complete retry preserves
that model and all other files. The CLI advanced package.json to 0.0.2.
Authenticated source readback confirms the corrected microphone matches the
local import. Registry credentials and account/session identifiers are omitted
from evidence. The release was marked ready_to_build; cloud build status was
pending when checked. Source publication does not establish a passing build.

Whole-board netlist checking was also attempted and stops at the explicit
incomplete-circuit guard. B-003 and stages 2–6 remain blocked or unfinished;
no routes or fabrication outputs exist. The standing publication instruction
allows clearly disclosed intermediate prototypes. No build, DRC, geometry or
pin-mapping check was bypassed for upload. Publication receipts and the CLI's
version increment are being synchronized as a separate documentation revision
under the non-latest tag `wip-c5656610-hole-060-publication-record`.
Remote results are recorded in `publication-status.json` in the evidence folder.
The receipt revision changes only documentation, evidence and the package
version advanced by the CLI. Imported components, dependencies and circuit
sources are unchanged, so the five passing import tests, typecheck, measured
geometry, placement result and recorded build blockers remain applicable.
Project formatting was rerun and passed after the receipt edits.

## A0-power-review milestone — 2026-10-03

The commit containing this section identifies this milestone; it starts from
671eb00579db27cc4dc232fe701a4ba98e7a19ac. Seven genuine power parts were imported
with supported CLI 0.1.2232 exact-footprint downloads, retaining unmodified
source/models. Exact MPN/LCSC, import commands and SHA256 are recorded in
`evidence/power-review-2026-10-03/import-manifest.json` and BOM.md.

Native application source: `src/power/regulated-3v3.tsx`. Isolated review entry:
`evidence/power-review-2026-10-03/regulated-3v3.circuit.tsx`. Native build exits 0
with PCB/SCH SVGs and PNGs. The first sandbox fetch warning was resolved by a
network-enabled rebuild without suppressions. Native netlist, pin_specification,
source, schematic-placement and placement commands all exit 0. Checks reporting
counts show zero errors/warnings; schematic-placement exits 0 without text.
`verification-results.json` records exact command exits and source hashes.
Formatting and TypeScript pass; all five existing import tests pass. Whole-board
build still exits 1 at its explicit incomplete-design guard. This is disclosed.

Reviewed current native regulator schematic/PCB PNGs and preserved SVG/JSON in
the same evidence folder. A4 sheet measures 297 × 210 mm. All seven PCB components
are top-side. JSON contains zero PCB traces and zero vias. Divider orientation
and short designators were corrected for readability before the final review.
This is a component application study, not the whole-board placement, RF review
or a routed power-loop layout. It does not pass stages 1–6 for the handheld.

POWER.md records manufacturer-backed pin wiring, preliminary 3.3 V divider and
charge-current calculations, USB default-power constraints, protected-pack/NTC
requirements and tentative load allocations. Pack, temperature window, exact
loads, effective capacitance/inductance, footprint qualification and thermal
limits remain unresolved. No nominal estimate is claimed as a verified rating.

Core PR 4323 merged; published core 0.0.2058 contains it. Nevertheless the native
CLI 0.1.2235 microphone fixture still exits 1 with ambiguous GND, five PCB ports
for six source ports and null links on all four ground pads. CLI bundles the
earlier renderer. Evidence: `evidence/core-fix-2026-10-03/`; B-003 remains open
and was reported with release evidence. Pinning direct core does not prove the
CLI uses it. Installation still reports a circuit-json 0.0.510 peer warning;
it is unresolved and not an accepted board warning.

B-004 is the reproduced unrelated catalogue-search result on old and current
CLI, saved in `evidence/component-search-2026-10-03/` and reported to the
authorized issue chat. No mismatched result was used. Exact power-part imports
and regulator review continued independently. Requirements, BOM/complete
schematic and mechanics remain unfinished; dependent routing stays disabled.

Standing authorization requires GitHub main push and private tscircuit WIP
publication of this step. Intended tag: `wip-a0-power-review`. Both remote
updates must be read back before calling this milestone fully published.

## A0-core-alignment milestone — 2026-10-03

Starts from fa5375fdbe457343e31852dbb706146ee6fe5841. The preceding regulator
milestone was verified on GitHub main and private tscircuit release
0.0.2-wip-a0-power-review: 238 uploaded files, exit 0, private and ready_to_build.
Source readback for package.json, regulator source, POWER.md and VALIDATION.md
matched exactly. Receipt: `evidence/core-alignment-2026-10-03/previous-milestone-publication.json`.
Cloud build status was unavailable in this readback; source upload is not a passing
whole-board build or fabrication approval.

Native CLI build constructs the locally imported tscircuit RootCircuit. Its
nested core 0.0.2056 caused the continuing B-003 failure; inspecting a bundled
method alone did not identify that active path. Official core 0.0.2058 is now
selected throughout the tree by Bun's supported package.json overrides. Plain
install updated the lock while leaving the old nested files; `bun install --force`
cleanly installed 292 packages and removed that nested copy. No package implementation
or imported component changed. Pinned versions otherwise remain unchanged.
[Bun documentation](https://bun.sh/docs/pm/overrides).

The real microphone build now exits 0. Native netlist, pin_specification, source,
schematic-placement and placement all exit 0; count-reporting commands have zero
errors/warnings. Ground polygon shapes all link to ports. Core emits nine
source ports and nine PCB ports, and a source_component_internal_connection
joining source_port_2/6/7/8 for the four physical ground shapes. No ambiguous
port or generated error remains. PCB/SCH PNGs inspected; hole/pad geometry is
preserved. Zero PCB traces/vias confirms routing remains disabled. This closes
B-003 for native component generation, not the complete microphone circuit or PCB.

Regulator build and all five native checks were repeated successfully on the
aligned renderer. Project formatting, TypeScript and all five import tests pass.
Final results, native artifacts and geometry checks are preserved in
`evidence/core-alignment-2026-10-03/`. The script's first artifact copy used an
incorrect output-directory suffix; the native build/checks had passed, and the
copy path was corrected. No native failure was hidden.

Complete-board schematic/BOM/requirements and mechanics remain unfinished.
No whole-board routes, DRC/shorts pass, fabrication package or physical tests exist. Stages 1–6
remain unfinished; B-004 search discovery continues in the authorized issue chat.
Intended private WIP publication tag: `wip-a0-core-alignment`; verify both remote
updates before reporting the milestone fully published.

### B-005 assembly defect discovered after native port resolution

The aligned microphone fixture has nine copper pads but only five solder-paste
records. All four ground polygons are absent from paste generation. Native TSX
Gerber diagnostic export exited 0; F_Paste.gbr contains five rectangle flashes
and no polygon regions. Geometry, defect counts and the diagnostic ZIP are saved
with this milestone. This is a real assembly/stencil blocker, sent to the authorized
issue chat. Stage 2 and dependent assembly/fabrication approval remain blocked.
No hand-authored paste or imported-definition correction was applied.

The export is only an unrouted isolated microphone fixture. It does not advance
whole-board stage 6. Supplier stencil drawing still requires visual PDF review;
TDK official download was unavailable and alternate downloads returned HTML.
Independent power, control, battery and mechanical development continues.

## A0-controls-review milestone — 2026-10-03

Starts from verified 8bbde6e95d7570ecef199278bd2d2521898d42e1. Prior GitHub main
and private tscircuit 0.0.2-wip-a0-core-alignment match; 274 uploaded files,
private and ready_to_build, with package.json/main.tsx/issues.md/VALIDATION.md
exact readback. Receipt: `evidence/controls-review-2026-10-03/previous-milestone-publication.json`.
This is source publication, not a successful whole-board build.

Current regulator divider is 511 kΩ / 91 kΩ (C188257 / C137671), nominal
3.3077 V. Provisional PWM static corners including resistor tolerance/drift and
FB bias are 3.1352–3.4849 V; exclusions and the 92.456 kΩ low-resistor maximum
are recorded in feedback-corner-review.json and POWER.md. No measured rail claim.

The native A4 isolated microphone-IC application contains 24 top-side components,
zero PCB traces/vias and no hardware button or microphones. It reviews VMIC
switch, supervisor, clock isolation, buffered hold sensing and comparator SD
reception. Comparator pin identities were checked against the visually reviewed
TI pin table. C100024 and C23654 remain unselected data-receiver candidates due
to low-level incompatibility. Circuit architecture, timing and privacy are not
qualified by this diagnostic fixture; see AUDIO.md.

The current regulator and isolation builds plus native netlist, pin_specification,
source, schematic-placement and placement checks all exit 0. Isolation's native
pin check retains one warning for U8's absent requires_power metadata (B-007).
Its build also warns that U7's imported custom symbol lacks reference text
(B-008), visibly confirmed in the newly generated current schematic PNG.
No checker or component was altered to hide these warnings. The regulator's
count-reporting checks have zero errors/warnings. Current results, source hashes,
Circuit JSON/SVG/PNG and geometry summaries are in
`evidence/controls-review-2026-10-03/`. Current PCB and schematic previews for
both fixtures were visually inspected; bodies fit their diagnostic outlines and
sheets fit native A4. Diagnostic spread-out placement is not final decoupling or
handheld mechanics. No whole-board placement gate is passed.

Earlier draft logs remain: unsupported schMaxWidth/schMaxHeight properties caused
TypeScript errors and were removed; supported native A4 sheets remain. Initial
isolation PCB resistor orientation failed placement, and draft schematic offsets
exceeded A4; actual placement/offsets were corrected before the current checks.
Initial previews without --schematic-png left a stale PNG; the comparator review
explicitly rebuilt the current PNG. No stale image is accepted as final evidence.

BLOCKING B-006: C79174 EVQPUC02K missing permanent contact pairs and oversized
locating holes, confirmed against visually inspected Panasonic July 2025 pages.
BLOCKING B-008: C105188 TLV3201AIDBVR missing schematic reference label.
B-007: C2149796 TPS22919 supply-classification warning; actual supply connection
manually verified, warning remains and final application qualification pending.
All were reported to authorized chat 01a0f218-ce92-7671-b666-efccdef3aed2.
B-005 microphone polygon paste and B-004 catalogue discovery remain unresolved.
B-003 remains resolved on official core 0.0.2058; microphone import is unchanged
since the previously authorized diameter-only correction. Stop dependent work
on blocked components and continue independent circuits.

Full-board stages 1/2 remain incomplete/blocked; 3–6 not started; physical stage
7 pending. No routes, shorts/DRC pass, snapshots, fabrication package or physical
measurements exist. Intentional full-board build guard remains. Intended WIP
publication tag: wip-a0-controls-review; both remotes require exact readback.

Current configured formatting and TypeScript checks exit 0; all five existing
manufacturer-based import tests pass (29 assertions). Authored-source whitespace
review passes. Native full-board build exits 1 at the intentional incomplete
design guard; full-board-guard-build.log preserves that result. No fabricated
output or weaker substitute bypasses the guard.

## A0-MCU/USB review in progress — 2026-10-03

Starts from controls-review GitHub main commit de5c6e45d7cf2e8077ad77be5abff97892fbb6f0.
Its private native publication failed: controls-review 406/410 uploads and four
TimeoutErrors; fresh-tag controls-retry1 409/410 and one TimeoutError. Both exit 1,
ready_to_build=false. All timed-out STEP files match authenticated remote bytes.
B-009 was reported; no successful source-publication claim or forced finalization.
Last fully completed private milestone is 0.0.2-wip-a0-core-alignment / 8bbde6e.
Failure receipts/logs are preserved under evidence/mcu-usb-review-2026-10-03.

New native A4 MCU/USB fixture has 16 top-side parts, zero PCB traces/vias/errors.
Build and all five native checks exit 0. Current PCB/SCH PNGs visually inspected;
60 × 50 mm is a spread-out diagnostic envelope, not final board dimensions.
Power/reset/USB polarity/BOOT physical module pin checks pass, reserved PSRAM
pins are unused, and all nine exposed-ground shape ports/internal group retained.
Service connector faces the left edge after an actual rotation correction;
capacitor schematic spacing was corrected and current renders rebuilt.
No handheld connectivity, placement or mechanical-fit gate is passed.

Native pin check retains eight metadata warnings; two chip-based imported
connectors also carry J-prefix convention warnings. They remain visible.
Manufacturer pin-role review is independent of incomplete imported metadata.
C94934 ESD has B-008 missing reference text, visibly confirmed. USB-C C165948
has B-005 missing paste on all four polygon VBUS/GND pads; native diagnostic
Gerber export exits 0 with 97 flashes and zero regions. This is an unrouted
fixture ZIP, not fabrication output. Both material issue updates were sent.

The new full native-output schema regression fails on 18 elements (B-010):
null schematic group subcircuit id, numeric PCB display offsets on 16 components,
null PCB group anchor alignment. Circuit-json 0.0.510 schema remains strict;
no output was patched. The fix chat independently confirmed the core source
still emits these invalid fields. Current tests: **9 pass, 1 fail**, 40 assertions.
TypeScript and formatting pass. All schema failures remain explicit. Full board
build still intentionally fails until the real circuit is authored.

Regulator feedback now uses untouched C364359 51.1 kΩ / C114639 9.1 kΩ,
nominal 3.3077 V, provisional PWM static corners 3.1820–3.4382 V. New native
network-enabled build and all five checks exit 0; pin/source report zero
errors/warnings. PCB and A4 previews inspected, zero traces/vias. Initial
sandbox build could not fetch supplier footprints; network-enabled native rerun
resolves that access failure. Retain both logs; no unavailable supplier review
was called passed. Seven component bodies fit the isolated fixture; final
power-loop layout/effective capacitance/inductance/thermal/transients pending.
POWER.md records assumptions and divider idle-current tradeoff.

Exact display/logic candidates were imported unchanged. LCD HS17QS178RX C5329581
requires 2.7–3.3 V logic and 40 mA backlight (Vf 3.0–3.4 V); interface/connector,
backlight/off-state behavior and mechanics unfinished. TPS7A2028 C2869847
accuracy requires VIN≥3.1 V; C7848 logic buffer and C11133 clock switch are
research candidates, not yet qualified. TLV757 C2863639 is rejected for headroom.
ALPS C110293 switch comparison is in progress, without imported-definition edits.

Battery decision is pending: candidate protected NTC pack's PCM limits continuous
current to 1 A versus provisional 1.488 A budget. A human question asks whether
separately sourced enclosure batteries may be allowed; no reply or exception
is assumed. All other electronics still require supported exact JLC imports.

Core 0.0.2059 and CLI 0.1.2236 were checked at official release sources: motor
assembly/frame changes, no verified relevant blocker fix. Pinned tested versions
remain unchanged. Continue independent engineering, report confirmed defects
to authorized chat, verify fixes through native workflows when available.
No full-board routes, DRC/shorts pass, snapshots, fabrication package or hardware
measurements exist. Heartbeat remains ACTIVE. GitHub/private publication of
this review is unfinished; never treat failed native releases as fully published.

C110293 / ALPS SKRTLAE010 alternative is also blocked: manufacturer circuit
diagram permanently joins pins 1↔3; untouched import/native generation has no
internal group. Native schematic exposes only 1/2 while footprint has 1–5.
The two Ø0.9000236 mm locating holes DO match ALPS's Ø0.9 recommendation; no
ALPS hole defect is alleged. Current official dimension/land/circuit GIFs were
visually inspected. This extends B-006 contact-import scope, not a permitted
component patch. Evidence: MCU/USB review switch-discrepancy.json and native
switch JSON/PNG/SVG. Do not integrate this unqualified alternate.

Authored-source whitespace check passes. Full Git whitespace scan reports native
SVG/log trailing whitespace and raw imported STEP CRLF endings; these generated
artifacts/imports are preserved byte-for-byte rather than reformatted. This
source-text finding is not a DRC result or imported-geometry waiver.

## A0-display-logic-review milestone — 2026-10-03

Independent partial LCD logic application implemented with19 exact imported
top-side PCB components, native A4,45×32 diagnostic canvas, routing disabled.
Current build and five required checks exit0. Rotated actual J7 to face the
right edge; moved C43 out of its courtyard and grouped schematic VLCD bypasses
to resolve the actionable warnings. Final schematic-placement output empty;
placement0errors/0warnings. Current PCB and schematic PNG/SVG inspected.
Native snapshot exits0 and matches; generated snapshots reviewed. Five imported
metadata/convention warnings remain visible, no component edits/suppressions.
Pin-map tests checked actual TI LDO/buffer physical pins and LCD/FPC contact
order, LED polarity, unused inputs and open outputs.12tests pass,1failsB-010,
75 assertions; TypeScript and formatting exit0. Current JSON has19top parts,
zero traces/vias/errors but21schema-invalid elements. This is diagnostic
evidence, not a full-board stage3–6 pass. DISPLAY.md records voltage/leakage
estimates, required sequencing and unfinished backlight/IDD/cable/mechanics.

Core source proposal, isolated from board dependencies, base18e1d11…(0.0.2061),
was reproduced/tested with upstream CI Bun1.4.0 and declared dependencies.
Unchanged baseline fails; correction passes strict schema/physical-pad
regression205assertions; related suite29pass/0fail/1existing skip,332assertions.
Core TypeScript and ESM/declaration build exit0. Five existing changed PCB
snapshots and new PCB/A4 snapshots visually reviewed. Proposal saved and sent
to fix chat; full core suite unrun and no upstream release/push performed.
Board remains pinned official0.0.2058, strict B-010 failure intact.
Task tooling excludes the separate upstream checkout and limits board test
discovery to ./tests; this does not remove any board tests or schema checks.

C11050 land comparison (B-011) is not a demonstrated imported footprint defect:
raw/import geometry matches; nominal0.20mm differences are at drawing's
±0.20mm boundary. Source drawing date2004.6.16; revision applicability and
physical FPC mating qualification remain pending. No imported edits.

Git02950fb exact readback verified on private main. Native private version
0.0.2-wip-a0-mcu-usb-review exited1 (535success/4fail). Both timed-out STEP
files arrived byte-for-byte;413-rejected SN74LVC245APWR.step and TPS7A20 PDF
are missing on exact release readback; ready_to_build=false. Receipt/log saved
in display evidence, material B-009 update sent. No forced ready flag, model
omission, publication success or full-build pass. This current milestone's
publication has not yet been attempted.

Whole-board requirements/schematic/mechanics remain unfinished; routing,
shorts/copper validation, fabrication exports and physical tests remain pending.
Protected battery sourcing exception still awaits the human reply.


## A0 amplifier application review and charge intake — 2026-10-03

Independent17part top-side46×32mm amplifier application added as an unrouted
native A4 diagnostic; complete-board source guard remains. Native build and all
five required checks exit0. C51 rotated180° to remove actionable placement
advisory; native PCB/A4 outputs reviewed.53rectangular pads/53native paste
shapes,zeroPCB traces/vias/errors.14tests pass/1strict B-010 test fails,
107assertions; TypeScript/format pass.19native schema-invalid elements are
saved separately. Missing Q1/Q2 imported reference text is B-008; snapshot
acceptance withheld. No schema/runtime/import edit or checker suppression.
Manufacturer physical amplifier/MOSFET/differential-output pin tests pass;
static gate/shutdown corner estimates are conditional, not measured behavior.

Exact new importsC265101/C132554/C2862740/C6617702 support independent battery
connector/USB controller/LDO/hold-switch intake. Full manufacturer/mechanical
qualification and actual charger/NTC/dead-pack policy remain pending. Protected
pack procurement exception awaits a human answer. B-012 speaker libraries
C3311258/C6230316/C50387211 unavailable. B-004 exact-MPN resistor search
returned unrelated components, unselected and reported. Native parts are not
modified to hide warnings or substituted by authored component definitions.

Gitc82e7deb display milestone verified remotely. Its nativeprivate package
0.0.2-wip-a0-display-logic-review exited1:582success/4fail. Both timeout files
arrived with exact hashes; both413 files missing404; ready_to_build=false.
Receipt and log preserved in audio/charge evidence. This amplifier milestone's
Git/package publication is still pending. All material issues were sent to the
authorized fix chat; useful independent work continues.

Whole-board stages1/2remain unfinished/blocked,3–6not started,7physicalpending.
No saved routes exist and no fabrication-ready, copper/shorts or hardware-test
claim is made. Save native routes before changes once prerequisite gates pass.

Exact queries were resolved with supplier-verified C114622 / RC0603FR-07470KL
and C482869 / RC0603FR-07430KL; both imported successfully, remain unwired
charging candidates. C7666 / TI SN74LVC1G08DBVR also imported for startup
qualification logic. No wrong search result was used in the circuit.


## A0 WIP — hardware Type-C current review, 2026-10-03

Source: `src/power/type-c-current-review.tsx`; full notes in `TYPE-C.md`; exact dependency/source hashes and command outputs in `evidence/type-c-current-review-2026-10-03/`. This independent 17-component native A4/top-side diagnostic has no routing. Native build and required netlist, pin_specification, source, schematic-placement and placement checks all exit 0. Current A4 and PCB images were actually inspected: inside boundary, no component overlap; R74/R75 labels remain legible at 180 degrees. Native output has 54 pads and 54 paste shapes, zero PCB traces/vias/emitted errors. C2862740's missing requires_power metadata warning is preserved (B-007); physical IN/EN/OUT pins were verified with TI's drawing.

Three manufacturer connection/corner tests pass. Canonical format/typecheck pass. Canonical board suite has 17 pass / 1 fail / 155 assertions: existing B-010 full-native-schema failure persists. The Type-C diagnostic independently has 19 invalid native schema elements; `schema-failures.json` preserves the failures. No schema/runtime edit, check suppression or full-board stage pass.

C22765 / 0603WAF1201T5E is a native-imported 1.2k candidate for future BQ24074 ILIM; not wired or temperature-qualified. The controller itself has no charger/pack/system-load-enable connection yet. Actual protection, TS limits, battery qualification, ramp timing, default-current dead-battery behavior, effective capacitance, current/thermal/mechanical fit still need completion. The pending battery-sourcing question is not assumed approved. Earlier complete-board stage statuses remain unchanged.

The C6617702 hold candidate is unmodified and remains unqualified: native cutout width 5.334 mm differs from the historical Panasonic 2012 drawing's 5.1 +0.1/-0 mm. Current manufacturer drawing confirmation remains pending. Its independent 2-component reproduction builds and all five native checks exit 0; PCB/A4 were inspected, but that does not qualify the imported cutout or actual edge mounting. It is forwarded to the authorized fix chat as a discrepancy, not declared a proven current supplier bug.

## A0 WIP — haptic driver review, 2026-10-03

Independent native A4/top-side regulator and flyback review added with10 actual
JLC imports. `HAPTICS.md` records manufacturer pin, voltage, default-off and
remaining qualification requirements. Native build and all five required checks
exit0. Network-enabled build resolves sandbox supplier lookup failures; retained
import metadata/reference advisories remain B-007/B-008.24 native pads/24 paste
shapes;zero PCB traces/vias/errors. PCB/A4 images actually inspected. Two new
manufacturer connection/physical-pad/polarity tests pass; canonical suite19pass,
1existing B-010 failure,177assertions. TypeScript passes;12 strict schema-invalid
elements preserved. No full-board gate or snapshot acceptance claimed.

**BLOCKING B-014 — C2942347 / LCM0720A3176F:** imported courtyard misses the
top-side motor body. Actual overlap reproduction passes placement0/0 yet puts
a resistor under that body. Fix chat confirmed converter body-bounds generation
defect. Native OBJ height3.85mm versus drawing-derived provisional2.65mm maximum
stack is a separate model qualification concern. C2895081 alternate import lacks
EasyEDA data. All supplier/library/model/reproduction evidence saved in
`evidence/haptic-review-2026-10-03/` and forwarded. Motor placement/integration
stays blocked; driver review does not substitute a generic motor.

The earlier high-current Type-C detector has a newly identified electrical
startup qualification gap: AND gate operation is undefined below1.65V supply,
where BQ EN2's guaranteed-high level starts at1.4V. A supervisor on one input
does not guarantee output low throughout that ramp. No fault transient has been
measured and no tscircuit defect is alleged. It remains unintegrated. Proposed
fixed USB100 with EN1/EN2 grounded needs actual pack, TS, charge-time, thermal,
dead-pack and system-load readiness review. `evidence/charger-safe-default-review-2026-10-03/startup-review.md`
preserves the scope and proposal; battery sourcing question remains unanswered.

Preceding source6700842b16f651adbc93bc899e9839412bfc3191 is verified on GitHub.
Supported private native version0.0.2-wip-a0-type-c-current-review exited1:
689reported successful uploads/33reported failed. Exact readback verifies28
reported timeout files byte-for-byte and five actual missing404 files;
private=true,ready_to_build=false. Readback includes native binary download,
not metadata alone. Logs/receipt/script saved with this review. B-009 persists;
no evidence omitted, forced ready flag, successful-publication or full-build
claim. This haptic milestone's remote publication remains pending.

Native generated SVG whitespace and a netlist-log trailing blank line remain
unchanged; git whitespace inspection reports those three non-geometric lines.
Installed CLI0.1.2235 supports `push --compress`: official source packs the same
enumerated files with lossless gzip and uses native upload_archive. This supported
publication mode will be tried without omitting models/evidence or forcing ready.

Whole-board stages1/2 remain unfinished/blocked;3–6not started;physical stage7
pending. No copper, saved routes or fabrication-ready package exists. Future
native routes must be saved before moving/rerouting and revalidated afterward.

Publication read-back: preceding amplifier Git revision `50bebdb6c283cf72ab4ab1e28321782e28065cf8` is pushed. Native private `0.0.2-wip-a0-amplifier-review` exits 1 (665 successes, 13 failures), ready_to_build=false. Amplifier TSX, bun.lock and three timeout STEP files have exact remote hashes; nine reported failures are actually absent. Four HTTP413 failures and remaining network failures remain B-009. Logs and receipt saved in this step's evidence folder; no ready flag or upload omission workaround.

## Regulated microphone clocks and nominal mechanical study — 2026-10-03

Parent source: a1e76d5f2879d74b68d882c3ea5576359b0ccc42. The new milestone
commit and evidence/microphone-open-drain-review-2026-10-03/source-manifest.json
identify the candidate. Its native A4 fixture uses 15 imported top parts,
37 pads and 37 paste entries, zero PCB traces/vias/error elements. Native build
and all five diagnostic checks exit 0 after rotating C74 by 180 degrees cleared
an initial placement orientation failure. Both logs are preserved; no imported
footprint was edited. Network-enabled build resolved sandbox supplier fetch
failures. PCB PNG and landscape A4 schematic PDF were inspected; snapshots match.
Formatting and TypeScript exit 0. Two new hardware-boundary tests pass. Canonical tests report 21 pass, 1 fail,
204 assertions (B-010). Strict candidate JSON has 17 invalid elements; original
JSON and every failing index/type are preserved. No schema/checker weakening.

ICS-43434 C5656610 I2S Table 5 specifies 1.8 < VDD < 3.3 V; the provisional
main rail reaches 3.43818 V. A dedicated TPS7A2028PDBVR C2869847 regulator
controlled by HOLD_HARDWARE gives a conditional 2.758–2.842 V with VIN >= 3.1 V
and load >= 1 mA. Nexperia 74LVC2G07GW,125 C24478 open-drain clocks are powered
from VMIC and pulled high only to VMIC by YAGEO 330-ohm C105881 resistors.
All imports are genuine and unchanged. The conservative total clock-load bound
is about 30 pF for TDK's 25 ns rise limit, accounting for the pulldown-limited
high level. Actual input capacitance, timing, partial-power AC feedthrough,
off-state injection and release-to-off deadline remain unqualified. IOZ's
5.5 V test condition is not expanded to an invented 2.8 V guarantee.
Privacy, complete microphone circuitry, switch and stencil remain pending or
blocked; detailed sources/conditions are recorded in qualification.md.

The dimension study in evidence/mechanical-envelope-review-2026-10-03 uses
actual C5329581 LCD dimensions, module pad coordinates/body-origin offset and
Espressif's 15 mm RF recommendation. The 50 x 50 mm trial fails; the approved
50 x 65 mm trial gives a nominal 15.82 mm LCD-to-antenna gap and 4.78 mm upper
land support margin. Raised LCD, tolerances, substrate removal, top button,
case, pack and speaker fit are unqualified. This does not prove all square
layouts impossible or establish a new exterior design. The sketch creates no
electronic component definitions or native placement/keepouts/cutouts.

Haptic parent publication: GitHub verified; private native version
0.0.2-wip-a0-haptic-driver-review exited 1 after archive HTTP413 and native
file-by-file fallback (771 reported successes, 13 failures). All seven timeout
files match exact readback hashes; six HTTP413 files remain 404. Package remains
private=true, ready_to_build=false; B-009 persists. Receipt/script are in the
clock evidence. Original private archive error payload remains in the tmp log;
the diagnostic copy replaces only that 97 MB payload line with original path,
length and hash, retaining errors and statuses. The CLI logging defect was
separately confirmed by the fix chat. No uploaded evidence was omitted and
no ready flag was forced. Current official core 0.0.2063 is unchanged; CLI
0.1.2237's current gitHead differs only by a package version bump. Required fixes
are not verified published. Pinned board dependencies remain unchanged.

Whole-board stage 1 remains in progress, stage 2 blocked, stages 3–6 not started
and physical stage 7 pending. No full copper routes or fabrication package
exists. Battery sourcing exception remains unanswered. Confirmed findings were
sent to the authorized fix chat; independent work continues.

## Battery-readiness candidate and latest publication review — 2026-10-03

Independent `src/power/battery-ready-review.tsx` uses genuine unmodified TPS3808G33DBVR / C43698 to sense charger BAT while powered from charger OUT. Five top parts, 14 SMT/paste pads, zero copper/vias/errors. Native build, all five diagnostics, A4 PDF export and snapshots exit 0; PCB, A4 schematic, snapshots and TI pin page visually inspected. Formatting and TypeScript pass; canonical suite 22 pass / one existing B-010 fail / 213 assertions. Seven strict native JSON failures persist. No full-board gate passes. Exact evidence and conditional static limits: `evidence/charger-battery-ready-review-2026-10-03/qualification.md`.

TI documents asserted RESET between POR and minimum operating supply, but arbitrary supply ramps, the 100 nF reset load, absence/open pack, capacitor history, cutoff relative to actual PCM, full VSYS load isolation and charging/NTC policy remain unqualified. G33 minimum trip 3.02395 V cannot ensure shutdown before the unselected example pack's maximum 3.10 V protection threshold. Protected rechargeable pack/harness/NTC choice still requires resolution. No battery or thermistor substitute was authored. New wrong-part searches are saved as supporting B-004 evidence and excluded from selection.

Latest official core remains 0.0.2063; importer easyeda remains 0.0.368; CLI remains 0.1.2237. Exact Circuit JSON 0.0.510-to-0.0.511 published source comparison changes missing-MPN warning fields only and does not fix B-010. No board dependency update applied.

GitHub revision 435493d1574c19dfb2e732ed359cda79e4d1205d was pushed and exact remote head verified. Supported native private `0.0.2-wip-a0-mic-clock-review` exited 1: 834 reported successes, nine failures (six HTTP413, three timeouts). Readback evidence is in this new review directory. Publication remains B-009; no omission, forced-ready flag or weakened checks. Source and artifacts at the previous milestone were held unchanged throughout its publisher run.

Publication identity correction: native --version-tag prefixes package version. Actual previous release is `0.0.2-0.0.2-wip-a0-mic-clock-review`. The initial single-prefix lookup was invalid and its404 results are excluded from absence conclusions; corrected readback is retained separately.

Corrected mic-clock readback: all three timeout files match exact hashes; six HTTP413 files are absent; package private=true and ready_to_build=false. This confirms B-009 without relying on the invalid initial lookup.

## Two-contact hold candidate, fabrication rules and BOM export review — 2026-10-03

Base Git revision d6826fa23d7160007f83bbc99a0c1204ae20e7e7 is pushed. The current milestone commit and new source manifests identify this additional independent review; no complete-board gate advances.

Genuine ALPS SKSWCFE010/C255576 native import is unchanged. Its two contacts and absence of locating holes avoid the four-contact ambiguity of earlier B-006 candidates, but it remains unselected: imported0.7999984×1.524mm lands differ from the current ALPS recommended pattern. Supplier raw pads are identical to the imported/native dimensions; this is an acceptance gap, not a proven converter defect. Native two-part hold fixture build/allfivechecks/snapshot/A4PDF/types/format pass, zero traces/vias/errors; four strict native JSON failures remain B-010. PCB/A4/snapshots/manufacturer drawing were inspected. The exact C202371 alternate supplier check has the same lands and was not imported/selected. Full switch mechanism, land/paste acceptance and release behavior remain unqualified. Evidence: evidence/hold-control-alternate-review-2026-10-03/qualification.md and hashes.

Current JLCPCB rule/stack review saves proposed four-layer standard JLC04161H-7628,1.6mm order thickness,outer1oz/inner0.5oz. Verified official calculator gives 90-ohm L1/L2 noncoplanar USB pair width0.2906mm/space0.1999mm; physical impedance tolerance±10%, distinct from0.5% calculator fit tolerance. Ordinary proposed trace0.20mm/clearance0.20mm, through via0.30mm hole/0.70mm diameter and other nominal manufacturing rules remain requirements, not actual copper measurements. Read-only native measurements give microphone hole0.60mm with minimum pad clearance0.2580203mm and minimum different-net rectangular SMT clearance0.1976628mm across51 fixture component instances, above JLC's0.15mm SMT-pad minimum. Conditional manufacturing tolerance sweeps are not asserted as DRC failures. Acoustic process/paste/full placement/routed copper remain unresolved. Exact native hashes, calculator AX/JPEG, measurement scripts/results and source links are in evidence/fabrication-rule-review-2026-10-03/qualification.md.

**BLOCKING B-015 — native BOM Comment metadata loss:** official latest circuit-json-to-bom-csv0.0.19 (also bundled by pinned CLI0.1.2235) emits blank Comment for genuine imported U1/C2913201, J1/C165948, U25/C43698 and SW4/C255576 despite native MPNs. Its documented resolver comment is independently reproduced as ignored too. Exact JLCPCB IDs remain preserved. JLC's current BOM specification requires descriptive Comment. This gates approval of the native stage6 BOM once earlier gates pass; stage6 is not reached. Footprint supplier-code fallback is separately unqualified; no actual assembler mismatch alleged. Public API reproduction, official isolated exact-version runtime/lock, native input hashes and NOT-FOR-FABRICATION CSV are saved in evidence/bom-export-review-2026-10-03. Fix chat independently confirms converter ownership. No library/component/output rewrite or relaxed schema is applied.

Saved-route source investigation verifies pinned native autorouting:end.pcbTracePaths and <autoroutingphase pcbTracePaths> APIs with per-phase/connection identity. Original events/full JSON must be preserved before route movement; every phase requires actual replay/geometry/connectivity/shorts validation. Omitted saved paths with an actual unavailable reason cannot be replaced by an empty/partial cache. Older pcbRouteCache behavior is unqualified and no new defect is claimed from source inspection alone. evidence/saved-route-api-review-2026-10-03/qualification.md records verified types/source and required round trip. No actual copper or saved routes exist.

Official core0.0.2064 changes only capacity-autorouter dependency and version, not B-010. Open core PR4283 currently contains an async PCB-port matching fix despite its older repro-only body; the preserved explicit-import board fixture has101source/101PCBports with numeric coordinates. No unmerged fix/runtime update applied and no future routing pass inferred. Whole-board stages1inprogress,2blocked,3–6notstarted,physical7pending; exact pack/harness/NTC/procurement question still unresolved. No order or fabrication-ready claim.

Final preceding battery milestone publication: native session48547 exited1,834reported successes/62failures for actual private0.0.2-wip-a0-battery-ready-review. Exact readback verifies55reported timeout files byte-for-byte; six previously known HTTP413 files and one new timeout file imports/SN74LVC1G17DBVR/SN74LVC1G17DBVR.tsx are currently404. Seven absent, no unverified files; private=true,ready_to_build=false. Evidence/readback/source hashes in the fabrication-rule review; material update sent to fix chat. Source was held unchanged throughout publisher run. B-009 persists; no full-publication claim or forced-ready/upload-omission workaround.

Current milestone checks: formatting and TypeScript exit0; canonical22pass/one existing strict-native-JSON B-010fail/213assertions/8files. Independent official BOM converter characterization exits0 and reproduces B-015; all raw native failures remain disclosed. No routing or full-board gate enabled. Current milestone remote commit/publication follows standing authorization and remains pending until verified.

Git whitespace inspection reports22,063warnings:22,054in the untouched supplier STEP (native line endings),twoin unchanged official BOM CSV,twoSVG lines,fournative calculator AX lines and one netlist-log EOF. Original bytes/hashes are preserved; summary and original diagnostic hash/path saved in whitespace-review.json. These are disclosed non-geometric formatting artifacts, not accepted DRC violations or a fabricated clean whitespace result.

## Hardware hold readback and top-control clearance review — 2026-10-03

Base fa90b5420f8e567270697c68132f311444a42424 was pushed and exact GitHub main verified. Its native private0.0.2-wip-a0-fabrication-review publisher exited1:957 reported successes/28 failures. Exact readback confirms22timeout files persisted with matching hashes and six known HTTP413 files remain404; no failed-file cases unverified or mismatched. private=true, ready_to_build=false. Evidence/log/readback receipt and script are preserved in evidence/hold-readback-review-2026-10-03. All enumerated source/artifact bytes stayed unchanged throughout that publisher and its readback. B-009 remains unresolved.

Independent src/audio/hold-readback-review.tsx uses unchanged genuine C7836 SN74LVC1G17DBVR input on hardware HOLD, a distinct buffered output through1kohm C21190 to MCU_HOLD_READ,10kohm C98220 ground bias and100nF C45000 decoupling. Its pin1NC stays open. The Schmitt input accommodates slow button transitions; no GPIO is directly wired to the microphone-enable net. This is an architecture/connectivity review, not full dynamic privacy qualification. Actual GPIO/boot pulls, low-voltage input leakage, contact bounce, capacitor history, partial-supply behavior, local decoupling loops and microphone off deadline remain open.

Native independent A4 build/allfive diagnostics/PDF/snapshots exit0; fourtop components,11SMT/11paste/11PCBports, zeroPCBtraces/vias/emitted errors. PCB/A4/snapshots/TI pin diagram and UNI-ROYAL package/land drawing visually reviewed. Strict unchanged nativeJSON fails sixelements B-010. Canonical formatting/TypeScript exit0; tests23pass/one existing B-010fail/228assertions. The additional boundary test verifies source pin identity, distinct input/output/readback nets, resistor values and openNC; it does not waive the full JSON gate or establish physical privacy. Original low-stock source/JSON/checks/snapshots were preserved before the genuine resistor change. Native group pcbStyle provides1mm reference labels without an imported-definition edit. Exact hashes and conditional electrical limits are in the dated qualification/source manifest.

Current native searches report C22548 stock5, C98220 stock22, C7836 stock34179, C45000 stock3848 and exact higher-stock C21190/0603WAF1001T5E stock8,013,731. Supported unchanged C21190 import is used in this candidate; other candidate sheets retain their prior exact parts and need final whole-BOM procurement review. C25804/0603WAF1002T5E was genuinely imported but remains unselected because both catalogue queries are empty. The fix chat confirms positive-stock filtering and independent EasyEDA libraries: this alone is not a bug or assembly-stock proof. Observation/report/response saved without creating a false new defect. Resistor temperature and initial-tolerance allocation2.1%, local loading and full supplier-land acceptance remain conditional; aging/final temperature policy pending.

Read-only top-control study moves the module physical center from(0,22) to(-8,22)mm on the50x65trial, increasing actual switch body/terminal-to-antenna gap from9.9495088 to17.9495088mm, above the15mm recommendation nominally. Native module origin accounts for3.775456mm body offset. All49native MCU lands retain minimum4.7805042mm edge margin; two switch lands retain1.238mm. LCD gap remains15.82mm with2.19mm body/shield plan overlap requiring raised fit. The diagram was inspected. No full native placement, keepout/cutout or electronic definitions are generated by the study. Top-edge actuation, RF/manufacturing tolerances, antenna substrate, square enclosure/dominant-screen coverage, exact battery/speaker and final vertical fit remain unqualified. Evidence: evidence/top-control-mechanical-review-2026-10-03/findings.md and native input/output hashes.

Latest checked official core0.0.2066 (b8fa4aae7c67d03e2d53160d44c4307269496545) adds bend diagnostics/tear-relief and checks dependency; no relevant blocker correction found in exact published-source diff. CLI0.1.2237/easyeda0.0.368/CircuitJSON0.0.511/tscircuit0.0.2742/BOM converter0.0.19 unchanged. PR4283 stays open at7fa3beb2f9c83878d1d65cec4e591f68e8fb4b50. Pinned board runtime remains unchanged. No full-board gate advances: stage1inprogress,2blocked,3–6notstarted,7physicalpending. No saved copper routes or fabrication package exists. This WIP step will be committed/pushed and natively privately published under standing authorization; actual remote results must be verified separately.

Current milestone Git whitespace inspection reports29,514warnings:29,508untouched supplier STEP CR lines, fournative SVG lines and twonetlist-log EOF lines. Original bytes preserved; diagnostic hash/path and per-file counts recorded in evidence/hold-readback-review-2026-10-03/whitespace-review.json. No whitespace-clean or DRC-pass claim is inferred.

Publication outcome for0573bf4492817ea0263827b6f0431fb7905d4959: supported private0.0.2-wip-a0-hold-readback-review publisher17411 exited1,1081reported successes/20failures. Exact readback confirms13reported timeout files byte-identical and seven404: six existing HTTP413 files plus imports/TLV3201AIDBVR/TLV3201AIDBVR.tsx (C105188), reported as a timeout. No failed-file mismatches or unverified cases. Package private=true/ready_to_build=false. Evidence/log/script/receipt are in evidence/hold-readback-publication-2026-10-03. Existing files stayed frozen through publication/readback; subsequent local watch/receipt notes are not part of that release. GitHub source0573bf4 succeeded, private publication remains incomplete B-009. No new implementation version, fabrication gate advancement, upload omission or forced readiness is inferred.

Official read-only release check05:18UTC: core2067 preserves supplied imported electrical attributes; easyeda369 accepts caller-supplied pinAttributes. Native fresh C2149796 import still only declares ground2/NC4, no supply1, so B-007 remains an enrichment gap rather than a newly proven converter defect. Exact source diff/native import/latest CLI source and fix-chat corroboration are in evidence/upstream-watch-2026-10-03-0511. No dependency/import-definition update; B-010 and separate geometry/BOM blockers remain. Versions rechecked unchanged approximately05:32UTC.

Independent read-only GPIO allocation proposal: evidence/gpio-allocation-review-2026-10-03 proposes15 unique peripheral/readback GPIOs, all15 matching unchanged C2913201 import contact labels and reviewed Espressif modulev1.8 table3-1. HOLD input21/contact23 avoids straps/USB/PSRAM; independent I2S0 microphone and I2S1 amplifier clock sets plus SPI2 LCD pins are proposed. Manufacturer reset/glitch/USB-OTG pad tables reviewed; GPIO18 and pad-JTAG pins excluded from output candidates. This is a candidate, not implemented native wiring or a full boot/privacy proof. Backlight, battery/status sensing and actual timing/partial-power qualification remain open. Source/dependencies remain unchanged; no native checks, fabrication gates or new board version are inferred from this static label review. Primary links and source hash are retained with the proposal.

## A0-reference-import-review — 2026-10-03

Human instruction: recheck actual assembly/routing blockers, continue independent work and seek genuine alternatives. B-009 publication and B-015 BOM descriptive metadata do not prevent schematic authoring or placement work; they remain publication/final-export gates. B-004 catalogue errors do not invalidate verified exact-part imports. B-007 is a visible role-metadata warning, not an established electrical connection failure. B-011 remains a tolerance/land acceptance question, not a proven fabrication defect. B-006/B-012/B-014 affect rejected or unselected candidates; actual replacements still require qualification. None of these classifications waive the earlier requirement/BOM/placement gates.

B-008 is resolved for C105188, C94934, C20917 and C15127: regenerated complete, unedited definitions using documented official `easyeda0.0.370 convert -i <C-number> -o <file>`; native core0.0.2070 owns each label on the correct schematic component. The four pin-label and footprint blocks are byte-identical to their preserved originals. Official generated CAD URLs replace local asset aliases; previous local assets remain preserved. Native tsci import on pinned2235 still returned the old definition; its converter uses a CDN browser endpoint, so the documented converter CLI was used instead. No imported definition or runtime was manually patched. Initial core installation exposed a missing props export; official props0.0.682 and circuit-json0.0.513 were aligned and installed with Bun's supported force refresh.

All four fixture builds and all20 required diagnostic checks exit0; all remain unrouted with zero traces/vias. Three native A4 PDF exports and snapshots exit0; corrected PCB/schematic images and rendered A4 pages were inspected. Correct references U7/D2/Q1/Q2 have native component ownership; missing-reference warnings are absent. B-003 has four linked ground pads/ports. B-005 persists: microphone has nine copper shapes but only five paste records; four polygon ground pads lack paste. USB polygon paste remains unqualified. Strict native schema still rejects comparator26/USB18/amplifier19 elements (B-010); the isolated microphone has zero strict schema failures. Canonical tests26pass/one existing B-010fail/235assertions/10files; formatting and TypeScript exit0. A saved upstream CLI excerpt was renamed `.ts.txt` preserving its bytes, because it is documentary source with absent upstream-relative files; no actual board code was excluded from TypeScript checking.

Alternatives: C20613566, C49246973 and C7430168 speaker imports each fail with no EasyEDA library. Broad `speaker` search again returns unrelated components, retained but not selected. C41348533/LEADER LD-SM-430 imports and native builds successfully. Manufacturer drawing inspected: SMT2.7V motor, operating2.3–3.2V, 11mm maximum length, reference PCB lands. Its three native lands are polygons with zero paste records, so it does not avoid B-005. No CAD model is provided; electrical role of third mounting land, body bounds/courtyard, mechanical fit, reflow and full driver application remain unqualified. It stays a candidate; no blocked part has been silently substituted.

Current evidence: `evidence/blocker-recheck-2026-10-03-1357/` (baseline definitions/dependencies, unmodified official generated imports, import receipts, native logs/outputs/A4 PDFs, source checks, strict schema failures, alternative supplier drawing/imports). Whole-board stages1inprogress/2blocked/3–6notstarted/physical7pending remain. No complete schematic, final placement, saved routes, copper or fabrication package exists. New implementation remote commit/private publication must be verified separately; source will be frozen during native publication.

Current main build was run and exits1 with the intentional incomplete-board guard (main-build-guard.log). This is not a full-board validation pass. Native private publication planned suffix wip-a0-reference-import-review; GitHub/private package results will be independently recorded after the source commit. Fix chat reports core PR4344 open for polygon paste; unpublished code was not installed.

Staged diff whitespace review reports13 supplier/native-output warnings: one untouched native motor import blank line, eight SVG/snapshot blank-line spaces and four native log EOF blank lines. Exact evidence/component bytes are preserved; these do not represent copper/assembly checks or accepted electrical warnings. Authored formatting passes. The unstaged diff check before staging had no findings; it did not inspect then-untracked evidence.
