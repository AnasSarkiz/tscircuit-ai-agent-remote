## A4 coverage trial qualification — 2026-10-04

The real source trial reaches82.712%physical PCB overlap, but current bare-panel availability/current manufacturer drawing, portrait FPC contact/pin1/fold, 0.8mm stackup/USB impedance, JST actual thickness acceptance and complete case/battery/harness tolerance fit remain open. These are design qualification tasks, not newly proven tool defects. Battery outer polarity remains unrouted. 431 unconnected/missing native connection errors remain and stage6 is not started. Existing B005/B010/B015/B009 are not cleared. [A4 review](evidence/a4-display-coverage-2026-10-04/review.md). No cross-chat message sent.

# Latest A2 checkpoint — 2026-10-04

**NOT FABRICATION READY.** This section supersedes conflicting historical A0/A1 selections and status below. A2 updates the genuine C11051 twelve-pin display connector, manufacturer display wiring, centre battery NTC, two native M2 mounting trials and provisional placement. Battery outer numbering remains pending; both outer contacts are unconnected/unrouted. Display/flex/enclosure/RF fit is still open; routing remains disabled. Full report: [A2 fabrication checkpoint](evidence/routing-intake-2026-10-04/fabrication-report.md).

A2 real blockers: battery outer numbering; screen tail/contact/raised assembly/RF clearance; backlight/current qualification; B-005paste (U4/U5 C5656610 9pads/5paste each, USB C16594812/8, charger C5431317/0); B-010162strict failures; B-01532blankBOMCommentfields; U14C7848CPLrotation unverified. Core4344paste PR was reverted4349, not resolved in checked2080. B-003 remains resolved. No routed copper exists; no actual route short/clearance diagnosis is asserted.

# Issues — A0

## RESOLVED LOCALLY B-001: C370970 terminal holes and mounting-slot lengths

Part: **C370970, ALPS EC11E15244G1**. Imported using pinned CLI 0.1.2228 with `--jlcpcb --use-exact-footprint --download`.

- Five terminal holes: 1.3000228 mm imported; manufacturer 1.00-1.10 mm.
- Two mounting slots: 3.200019 mm long imported; manufacturer 2.60-2.70 mm.
- Hole pattern row spacing 14.5 mm is correct (7 + 7.5 mm); no false row-spacing discrepancy is reported.
- Manufacturer 12.5 mm dimension is measured across outside slot edges, not between slot centers.

Affected gates: schematic/BOM import qualification (stage 2), placement/mechanics (stage 3), then routing, checks and fabrication (stages 4-6).

Evidence: `evidence/imports/C370970-audit.json`, original supplier JSON, `references/alps-ec11e15244g1-mounting.gif`, `references/alps-ec11e.pdf` and `evidence/datasheets/alps-ec11e-2.png`. Independent manufacturer-range tests reproduce both failures.

Original resolution rule prohibited local component edits. The user's subsequent explicit instructions authorized updating both C370970's symbol and footprint. The local import now has five **1.05 mm** terminal holes and two **2.65 mm** mounting-slot lengths, within the original unchanged manufacturer-range tests. Other geometry, centers, pin mappings, identity and models are preserved. This exception applies to C370970 only; no supplier library update is claimed.

Current evidence: `evidence/imports/C370970-footprint-change.json`, `evidence/encoder-footprint-circuit.json`, `evidence/encoder-footprint-pcb.svg` and PNG. Generated geometry was measured, the PCB preview inspected, and the isolated component placement check passed with zero errors/warnings. All four existing qualification tests pass without changing their limits. Final finished-hole tolerances, complete board integration, mechanical assembly and physical fit remain pending; this does not approve fabrication.

Historical alternative investigation: **C209762 / EC11J1525402** imported successfully through the supported workflow. ALPS marks this exact part Not Recommended for New Designs, so it was not selected or fully qualified. The user-authorized C370970 correction resolves the reported dimension issue instead.

Historical symbol-only change (revision 1f63764, 2026-10-02): removed C370970's custom `symbol` JSX prop. Native `chip` renders a box and preserves seven source pins (6–12). At that revision the footprint was unchanged and B-001 remained open. Audit: `evidence/imports/C370970-symbol-change.json`; preview: `evidence/encoder-chip-box-schematic.svg`. The subsequent authorized footprint correction is recorded above.

## Candidate rejection R-001: TPS63070RNMR C109322

The original import omits physical pin identities 8 and 13 and loses pin 1's PS/SYNC functional alias. TI assigns 7/8 to VOUT and 12/13 to VIN; grouped pads are electrically equivalent but do not satisfy exact pin identity qualification. This is not evidence of a short.

The supported import of genuine TI **TPS63802DLAR C2845237** retains all ten manufacturer pin numbers/functions and is an alternative candidate. No TPS63070 dependent circuit was authored. Old TPS63070 source and failed qualification evidence are retained; it is excluded from the proposed active BOM. TPS63802 placement, passives, complete power design and model qualification remain pending. This change resolves selection dependency on TPS63070, not the board validation stage.

## Other pending items

### RESOLVED LOCALLY B-002 — C5656610 / ICS-43434 acoustic opening

Unmodified import has a 0.3999992 mm acoustic hole. TDK DS-000069 v1.2 page 17 recommends a minimum 0.50 mm PCB opening. Original six pin identities/functions match page 10. This is a manufacturer-recommendation discrepancy, not a diagnosed short or absolute electrical-rating violation. The independent opening test fails; stage 2 and dependent stages 3–6 remain blocked.

Audit: `evidence/imports/C5656610-audit.json`. Prepared but **not applied**: `evidence/proposals/C5656610-acoustic-hole.diff`, diameter-only correction to 0.60 mm. Existing C370970 authorization does not cover this microphone, so approval for other documented import corrections was requested. Original microphone source/pads/models remain unchanged. The user requested waiting for an upstream correction. Fresh import with tscircuit 0.0.2736 / CLI 0.1.2232 on 2026-10-03 still measures 0.3999992 mm. Evidence: `evidence/update-check-2026-10-03/microphone-check.json`; the published fix is not verified. The user reaffirmed waiting for the upstream correction after this recheck; no local microphone edits or substitutions are authorized. No board routing is authorized before the remaining prerequisite gates pass.

TDK's manufacturer pages differ on lifecycle (Production/NRND versus EOL). Final selection/availability must be checked; this does not itself establish a bad import. Local datasheet download returned HTML, preserved as download evidence. Official PDF text was accessible through web tools; no local PDF render is claimed.

### Remaining design work

- Display: manufacturer documentation obtained for Waveshare 1.54inch LCD Module, ST7789, 240 x 240, 3.3 V operation, 50 x 35 mm module with PH2.0 eight-pin connection. Exact JLCPCB-sourced display/connector and permitted external assembly need final qualification; no display component or footprint has been authored.
- A free-text supported-import search for `1.54 LCD` selected the unrelated **DSK110 diode C908227**. That file is preserved as evidence of the search behavior and is not a display or active BOM selection. Future imports must use verified exact part numbers.
- Supplier catalogue stock/prices are inconsistent between catalogue/search endpoints. Exact JLCPCB assembly availability/classification and costs remain unverified.
- Accepted 2026-10-03: square, dominant screen, one top hold-to-talk button, top-side assembly only, speaker and rechargeable battery. See `REQUIREMENTS.md`. Prior encoder/extra-button/front-LED requirements are superseded; their imports remain historical evidence.
- Privacy: retain hardware microphone disable and prevent audio clock/data phantom power, using the single-control design. Exact architecture and Ioff buffer qualification remain pending; no software-only mute substitution.
- Battery: protected 1S nominal 3.7 V / 4.2 V-charge, 500–1000 mAh pack; exact MPN, sourcing/import, protection, thermistor, polarity and peak current rating remain pending. New SMT connector candidate C295747 is imported verbatim. Official JST drawing fetch returned 403; full footprint qualification is still pending. Charger/connector imports do not establish an integrated rechargeable system.
- Power budget, USB enumeration/current policy, passive component selection and regulator loop layout remain pending.
- A4 schematic, complete pin allocation, board outline/mounting, component placement, RF keepout and enclosure/ergonomics remain pending.
- Saved native routes and DRC/short repair remain pending because pre-routing gates have not passed.
- No physical prototype is available; no hardware results or physical photos are claimed.

## Tooling notes

- Initial optional skill download failed in the sandbox; the installed tscircuit skill and official handbook were read directly.
- A first formatter run changed import whitespace. All four affected imports were restored with the supported importer; regulator checksum matched the original. `imports/**` is now excluded from formatting.
- Initial diagnostic-script TypeScript errors were corrected by making the script a module; no component source was patched.
- LCSC encoder datasheet download returned an HTML challenge despite HTTP 200. Preserved as `evidence/downloads/C370970-datasheet-challenge.html`; actual official ALPS PDF and mounting diagram were obtained and inspected.
- Initial GitHub creation was rejected by automatic approval review. A narrower empty-private-repository creation succeeded after proving the attached brief explicitly requested it. Repository identity: AnasSarkiz/tscircuit-ai-agent-remote.

## User-authorized local C5656610 correction — 2026-10-03

The user's latest direct instruction authorizes manual correction after confirming
that the supplier footprint is undersized. This supersedes the prior wait for
upstream for this local correction. Only the acoustic diameter changed from
0.3999992 to **0.60 mm**. A byte comparison proves all other imported source is
unchanged. Source center, pads, pin mappings and models are preserved.

Audit: `evidence/microphone-local-correction-2026-10-03/change-audit.json`.
Generated diameter is 0.60 mm, minimum hole-to-copper gap is 0.2580203 mm,
and the isolated placement check passes with 0 errors / 0 warnings. All five
existing import tests pass. Supplier raw data and the converter remain unchanged.
Previous B-002 failure and wait entries above are historical evidence.

## RESOLVED B-003 — C5656610 native ground-pad port generation

Historical reproduction before core alignment: the native renderer reported `source_ambiguous_port_reference` for MIC1.GND.
Pin 3 consists of four separated polygon pad shapes, matching the imported
supplier layout. The renderer requires matched shapes to overlap before it
creates a PCB port for that logical pin. It produces six logical ports but only
five PCB ports, with all four ground shapes carrying `pcb_port_id: null`.

Using the documented `MIC1.pin3` selector correctly creates a source trace to
GND; the PCB-port generation still fails. Changing selector aliases therefore
does not resolve this error. The corrected component build exits 1. No DRC
suppression or geometry/pin-map workaround was applied. This is not a diagnosed
short or proof that the four-segment supplier pad geometry is itself incorrect.

Evidence: `evidence/microphone-local-correction-2026-10-03/build.log`, `circuit.json`
and `change-audit.json`. Affected stage: 2 and dependent stages 3–6. Full-board
schematic, component selection, battery/display mechanics and placement are
also unfinished. Stop dependent routing until native port handling and all
prerequisite checks are resolved.

## Publication status

Standing authorization covers milestone pushes to GitHub main and private
tscircuit WIP source publication. The human explicitly authorized the corrected
C5656610 revision after the initial automatic-review rejection. GitHub main was
verified at 671eb00579db27cc4dc232fe701a4ba98e7a19ac; the complete private
tscircuit source publication is 0.0.2-wip-c5656610-hole-060-publication-record,
176 files. Cloud build was pending when checked; this does not approve fabrication.
The power-review milestone was subsequently verified at fa5375fdbe457343e31852dbb706146ee6fe5841 and private release 0.0.2-wip-a0-power-review (238 files); its receipt is retained in the next milestone.

## Historical B-003 release attempt — 2026-10-03

Core PR 4323 merged at 51b6b9789aa6e8c1d58d2ac98783f243aa4f1ebf. Published
core 0.0.2058 (gitHead e6d010593f4739747de9c3fc8ff9f6651b862c5d) contains
that change. Project pins are tscircuit 0.0.2742 / CLI 0.1.2235 / direct core
0.0.2058. Native CLI rendering still reproduces the microphone failure: six
source ports, five PCB ports, four ground pads with null PCB-port IDs and
source_ambiguous_port_reference. The CLI bundle lacks the new polygon-bounds
method even though the direct core bundle contains it. A fixed CLI release is
initially inferred to be needed. This inference was superseded by the active-runtime diagnosis and supported dependency alignment below. No local runtime
patch was applied. Evidence: `evidence/core-fix-2026-10-03/`. This release gap
was sent to the authorized issue chat. Independent regulator work continued.

## BLOCKING B-004 — catalogue search returns unrelated components

CLI 0.1.2232 and 0.1.2235 both return unrelated parts for:

- `tsci search --jlcpcb --json 'Waveshare 1.54'`: C275301 inductor / C2068886 fuse holder.
- `tsci search --jlcpcb --json 'GRM188R60J226MEA0'`: C7431187 oscillator / C269729 200 Ω resistor.

Expected: matching components or an explicit no-result response. None of those
returned parts was selected or substituted. Root cause is not established.
Evidence: `evidence/component-search-2026-10-03/`, including release rechecks.
Reported to `codex://threads/01a0f218-ce92-7671-b666-efccdef3aed2`. Search-based
display/capacitor discovery in stage 2 is blocked; verified exact-part imports
remain usable and continue. This is not a claim that all imports fail.

## B-003 closed after supported dependency alignment

The earlier missing-method CLI-bundle inference did not identify the active
renderer. CLI's native build uses importFromUserLand("tscircuit") and its
RootCircuit. The tscircuit installation retained nested core 0.0.2056. A supported
package.json override to official core 0.0.2058 and clean `bun install --force`
resolved this. Plain install changed the lock but left the stale nested files.
The final native microphone build and five checks exit 0, with four linked
ground contacts, nine source/PCB ports and their native internal connection.
No runtime or component-source workaround was used. Current logs and reviewed
artifacts are in `evidence/core-alignment-2026-10-03/`; the issue chat received
the measured resolution. Historical failed-release evidence above is preserved.
B-004 search discovery and full component/application qualification remain open.

## BLOCKING B-005 — C5656610 polygon ground pads have no solder paste

Reproduced on tscircuit 0.0.2742 / CLI 0.1.2235 / aligned core 0.0.2058.
The microphone fixture now passes native generation, but Circuit JSON contains
nine pcb_smtpad shapes and only five pcb_solder_paste records. Each of the four
polygon ground pad shapes lacks paste. Installed core's polygon SmtPad branch
inserts a copper pad without a corresponding paste record. No importer geometry
edit was made in this milestone.

Supported native diagnostic export:
`tsci export evidence/microphone-local-correction.circuit.tsx --format gerbers --output <absolute-path>/microphone-diagnostic-gerbers.zip`.
Export exits 0; circuit-json-to-gerber 0.0.109 emits only five rectangular flashes
and zero G36 regions in F_Paste.gbr. The four ground apertures are missing.
The ZIP is an unrouted component diagnostic, not the handheld fabrication package.

Evidence: `evidence/core-alignment-2026-10-03/microphone-stencil-defect.json`,
`microphone-circuit.json`, `F_Paste.gbr`, `microphone-diagnostic-gerbers.zip` and
`microphone-gerber-export-native.log`. Earlier failed export attempts were an
unsupported JSON-input invocation and an incorrectly relative output path;
the final native TSX export with absolute output path succeeded.

Affected stages: 2, 5 and 6; assembly/stencil qualification remains blocked.
Exact manufacturer aperture geometry still needs visual datasheet review. Official
TDK PDF fetch returned 403; alternate TDK/Mouser downloads returned HTML rather
than PDF. This availability limitation does not weaken the generated-file evidence.
Reported to `codex://threads/01a0f218-ce92-7671-b666-efccdef3aed2` with reproduction,
versions and evidence. Do not locally patch imported paste geometry or emit a
hand-authored fabrication substitute. Continue independent power, controls,
battery, interfaces and mechanical work while the upstream defect is investigated.

## BLOCKING B-006 — C79174 / Panasonic EVQPUC02K contacts and holes

The untouched exact import has four separate contacts and no declared internal
pairs. Panasonic ANCTB23E July 2025 printed page 2 specifies permanent pairs
1↔3 and 2↔4. Native generation confirms four source/PCB ports with no internal
connection. Its two 0.9000236 mm NPTH locating holes exceed the manufacturer
Ø0.75 +0.10/−0 recommendation (0.85 mm maximum). The issue chat confirmed the
raw supplier retains contact grouping that conversion loses; the oversized holes
originate in the supplier footprint. Stage 2 and dependent hold-control work stop.
No symbol, mapping or holes were patched. Evidence: button-discrepancies.json,
button-circuit.json and the reviewed Panasonic printed pages 1–2 under
`evidence/controls-review-2026-10-03/`; original manufacturer PDF in references.

## B-007 — C2149796 / TPS22919DCKR supply metadata limitation

Native pin_specification exits 0 with zero errors and one warning:
`source_no_power_pin_defined_warning: U8 has no pin with requires_power=true`.
The import declares ground and NC but not pin 1's power role. Manufacturer
SLVSEN5B page 3 and generated JSON verify the actual pin 1→V3V3 connection,
pin 2 ground, pin 3 hardware-only ON, pin 4 open, pins 5/6 VMIC. The issue chat
confirmed raw source electrical types are Undefined; converter data loss is not
established. Do not infer every IN label is a power pin or patch the definition.
Manual connection review passes, but the metadata warning stays visible and
complete application qualification is pending. No warning was suppressed.

## BLOCKING B-008 — C105188 / TLV3201AIDBVR missing schematic reference

The exact supported import's custom symbol has no reference-designator text.
Native build warns `U7 is missing schematic reference designator text` and the
current A4 render visibly lacks the comparator identifier. Pins and footprint
remain unmodified. Stage 2 schematic readability/import qualification is blocked;
no full-board integration or schematic completion is claimed. Reproduction:
`evidence/controls-review-2026-10-03/isolation-ics.circuit.tsx`, current build log,
JSON and PNG/SVG. Reported with B-006/B-007 to the authorized issue chat.

## Application correction — microphone SD levels

ICS-43434's 0.35/0.65 VDD guaranteed output levels do not meet both input limits
of direct ESP32-S3 or the proposed LVC/LV1T SD receivers. This is our application
selection issue, not a newly diagnosed supplier microphone defect. The review
now uses exact imported C105188 with a VMIC/2 reference and a provisional 16 kHz
voice target. Full switching/rail/load and power-off analysis remain pending.
The blocked microphone, switch and comparator are not integrated into a complete
board. Independent power, USB, MCU, charger and mechanical work continues.

## B-005 additional scope — C165948 TYPE-C-31-M-12

Current native MCU/USB fixture has four polygon VBUS/GND copper pads (13–16)
with no linked paste records. Diagnostic F_Paste Gerber has zero polygon regions;
97 flashes cover 93 rectangular SMD pads and four connector anchor paste records.
This extends the confirmed core/export assembly defect beyond microphone GND.
Evidence: `evidence/mcu-usb-review-2026-10-03/circuit.json`, `F_Paste.gbr`,
`diagnostic-only-gerbers.zip`. Reported once as a material update.

## B-008 additional scope — C94934 TPD2EUSB30ADRTR

Untouched exact import lacks custom-symbol reference text. Native current A4
render visibly lacks D2 and build emits the corresponding warning. Pins 1 D+,
2 D− and 3 GND were checked against TI. New application does not resolve this
import readability defect. Reported once; no symbol edit authorized/applied.

## BLOCKING B-009 — supported private publication timeouts

GitHub main contains controls commit de5c6e45d7cf2e8077ad77be5abff97892fbb6f0.
Native private release 0.0.2-wip-a0-controls-review exits 1: 406/410 successful,
four large STEP TimeoutErrors. Canonical fresh-tag retry controls-retry1 exits 1:
409/410 successful, one TimeoutError. Authenticated remote readback confirms
all timed-out model bytes match local files, but both releases remain
ready_to_build=false. Completion still requires official acknowledgement of
all files; no force-finalization or upload-success claim was made. Native gzip
bundle would exceed service size limit (41.3 MB base64 before missing file),
so compression is not a valid remedy. No runtime patch, model omission or token
persistence. Reported to authorized fix chat; evidence under MCU/USB review.
Last fully verified private source release remains 0.0.2-wip-a0-core-alignment.

## BLOCKING B-010 — native Circuit JSON/schema contract

Installed core 0.0.2058 / CLI 0.1.2235 / circuit-json 0.0.510 output is rejected
by its published schema: schematic_group.subcircuit_id=null, 16 pcb_component
numeric display_offset_x/y where string required, pcb_group.anchor_alignment=null.
Eighteen element failures are saved in circuit-json-schema-failures.json.
The explicit regression remains failing. Nine other meaningful tests pass,
including module supply/reset/USB/BOOT physical pins, PSRAM exclusion and all
nine native exposed-ground shape ports/internal group. Extra shape ports carry
pin41 hints rather than duplicate pin_number; the regression uses the documented
native identities. No JSON conversion, schema suppression or runtime patch.
Reported to authorized fix chat. Native five checks exiting 0 do not waive this
stage-5 blocker. Continue independent manufacturer circuit and mechanical review.

C110293 / ALPS SKRTLAE010 alternative is also blocked: manufacturer circuit
diagram permanently joins pins 1↔3; untouched import/native generation has no
internal group. Native schematic exposes only 1/2 while footprint has 1–5.
The two Ø0.9000236 mm locating holes DO match ALPS's Ø0.9 recommendation; no
ALPS hole defect is alleged. Current official dimension/land/circuit GIFs were
visually inspected. This extends B-006 contact-import scope, not a permitted
component patch. Evidence: MCU/USB review switch-discrepancy.json and native
switch JSON/PNG/SVG. Do not integrate this unqualified alternate.

## B-009 additional scope — MCU/USB native upload

Git02950fb published natively as0.0.2-wip-a0-mcu-usb-review:535reported success,
4failures,exit1. Timeout models SN74LVC1G125/TPS63802 have matching remote hashes.
HTTP413-rejected SN74LVC245STEP and TPS7A20PDF return404; ready_to_build=false.
This is not only an acknowledgement issue. Receipt and log in display evidence;
reported as material update. No file dropping/forced finalization.

## B-010 tested upstream source proposal — still blocked on board

Base18e1d11…core2061, strict native regression baseline fails; minimal corrected
source passes205assertions. Group offsets also require mm strings in both initial
and anchor update paths. Related suite29pass/0fail/1existing skip, TypeScript/
ESM/declaration build pass. Proposal/versions/snapshots saved in
evidence/core-b010-proposal-2026-10-03 and sent to fix chat. Board runtime2058
unchanged:12pass/1fail75assertions. Official fix publication/verification pending.

## B-011 correction — C11050 land qualification question

Initial nominal comparison was reported for review, then corrected. Raw supplier
and import match. Drawing2004.6.16 has X.X ±0.20 mm; both0.20mm nominal pad
differences lie at this boundary. No supplier/converter defect demonstrated,
and no local footprint patch is justified. Revision applicability and cable
mating fit remain pending. Follow-up clarification sent to fix chat.


## B-008 additional exact parts — amplifier diagnostic

C20917 / AO3400A and C15127 / AO3401A imported custom symbols omit reference
text, reproduced in native amplifier output. Reported to authorized fix chat.
Symbols untouched; qualification/snapshot acceptance withheld. Prefix/type
advisories and absence of MOSFET power pins are not treated as electrical defects.

## B-012 — speaker supplier libraries unavailable

Native exact imports C3311258 / PUI AS04008PS-4W-R, C6230316 / Taoglas
SPKM.20.8.A and C50387211 / XHXDZ23MM-8Ω2W-JFHM report no EasyEDA
library data. Stage2 speaker qualification/integration stops; no authored
speaker or generic substitution. First two independently confirmed by fix chat.
Evidence: audio-charge-review-2026-10-03 speaker import logs. Continue actual
supplier search and independent amplifier/charging work.

## B-004 additional exact manufacturer queries

RC0603FR-07470KL discovers C16195750 unrelated inductor;
RC0603FR-07430KL discovers C326810 unrelated510kΩ2010 resistor. Native
import logs preserved; both unselected. Reported as query matching, not data loss.

## B-009 — display publication exact receipt

Gitc82e7deb is verified on private main. Native version
0.0.2-wip-a0-display-logic-review exits1,582successes/4failures. Timeouts
SN74LVC1G17/TPS3839STEP reached server with matching hashes; HTTP413
SN74LVC245STEP/TPS7A20PDF return404. ready_to_build=false. Exact receipt
and log in audio/charge evidence; material update sent. No dropped models,
forced readiness, publisher bypass or success claim.


### 2026-10-03 Type-C review update

- B-006: C6617702 / EVQ-P4HB3B imported cutout is 5.334 mm wide; historical Panasonic drawing max 5.2 mm. Current drawing confirmation is needed; candidate stays unqualified and import untouched. Exact drawing/provenance/reproduction under `evidence/type-c-current-review-2026-10-03/`. Sent to fix chat.
- B-009: native amplifier publication has 665 successes / 13 failures, with nine failed files actually absent and ready_to_build=false. Exact hashes distinguish late-arriving uploads. Saved log/read-back receipt in the same evidence folder and forwarded to fix chat.
- B-010: hardware Type-C diagnostic has 19 strict schema failures; existing full-board test remains failing. Native build/five checks do not clear this blocker.
- Battery procurement question remains unanswered. Charger/pack/TS/system enable are not integrated by the new current-detector fixture.

## B-014 — C2942347 haptic motor body and model qualification

Supported imported LCM0720A3176F courtyard excludes most of the top-side motor
body. Deliberate real-resistor overlap at its center returns placement0errors/
0warnings; native PCB and3D were inspected. Fix chat confirms converter
body-bounds/courtyard generation defect from raw EasyEDA body data. Exact model
height3.85mm differs from manufacturer drawing-derived provisional2.65mm maximum
stack; that model concern remains separately unclassified. Alternate C2895081
has no importable EasyEDA library. Stage2/3 motor qualification blocked; no
import edit or authored substitute. Evidence: `evidence/haptic-review-2026-10-03/`.
All three concerns sent to the authorized fix chat.

### Haptic milestone — other open issues

- B-007/B-008: C963429 supply metadata, C20917 underspecified pins and missing
  reference text remain visible; manufacturer physical pins reviewed.
- B-010:12 strict native haptic schema failures; canonical suite19pass/1fail.
- B-009: Type-C package exited1,689successful/33failed upload reports;28timeout
  files byte-verified, five actual404,private=true,ready_to_build=false.
- Hardware Type-C startup gap is an electrical qualification issue, not a
  demonstrated library bug. Do not integrate the high-current detector until
  guaranteed low EN2 behavior across partial supply is established. Fixed
  USB100 direction remains unqualified; pack sourcing permission is pending.


### Regulated microphone clock milestone — remaining qualification

- Hardware: C5656610 I2S Table 5 specifies 1.8 < VDD < 3.3 V; the provisional
  main rail reaches 3.43818 V. The dedicated 2.8 V supply/open-drain clock
  candidate has better static margins; total clock capacitance must fit about
  30 pF. Timing, partial-power behavior and off deadline remain unqualified.
- B-010: 17 strict native candidate JSON failures; canonical tests 21 pass, 1 fail.
- B-009: haptic a1e76d5 private publication exits 1: archive HTTP413/native
  fallback 771 successes, 13 failures. Seven timeout files match exact hashes;
  six actual HTTP413 files are missing. Package is private=true, ready=false.
  Native error logging duplicates private archive content; fix chat reproduced
  this separately. Raw log retained privately in tmp; diagnostic copy substitutes
  only the payload line with its path, byte count and hash. No upload omissions.
- Mechanical: this 50 x 50 mm trial fails land support and RF separation. The
  approved 50 x 65 mm trial gives a nominal 15.82 mm LCD-to-antenna gap, but raised
  LCD, tolerances, substrate, top button and case fit remain pending. This does
  not prove all square layouts impossible or validate a replacement for the
  accepted square exterior. No imported definition was modified.

### 2026-10-03 battery-readiness and publication evidence

C43698 TPS3808G33DBVR imports successfully and supplies an independent documented low-voltage-reset candidate. Seven native Circuit JSON errors reproduce B-010; battery readiness/presence, dynamic reset current/timing, actual pack cutoff/NTC and charger policy remain open hardware qualification, not an importer defect. Unrelated exact resistor, speaker and battery results reproduce B-004 and were excluded.

B-009 persists at Git 435493d: supported private mic-clock publication reports 834 uploaded and nine failures, including six HTTP413 files and three timeout files. Readback receipts are retained in `evidence/charger-battery-ready-review-2026-10-03`. Circuit JSON 0.0.511 changes only missing-MPN warning metadata and does not resolve B-010; no dependency update applied.

Publication identity correction: native --version-tag prefixes package version. Actual previous release is `0.0.2-0.0.2-wip-a0-mic-clock-review`. The initial single-prefix lookup was invalid and its404 results are excluded from absence conclusions; corrected readback is retained separately.

## B-015 — native BOM exporter loses MPN and resolver Comment

Affected genuine imported parts reproduced: C2913201 (ESP32-S3-WROOM-1-N8R8), C165948 (TYPE-C-31-M-12), C43698 (TPS3808G33DBVR), C255576 (SKSWCFE010). Official latest circuit-json-to-bom-csv0.0.19, also bundled in pinned CLI0.1.2235, leaves Comment empty even though native manufacturer_part_number is present; a documented resolvePart comment is also ignored. JLCPCB IDs remain exact. Blocks final native stage6 BOM approval after earlier gates; no assembler misidentification or fullboard fabrication claim. Footprint C-number fallback is separately unqualified. Evidence/public API runtime/lock/input hashes: evidence/bom-export-review-2026-10-03/qualification.md. Sent to authorized fix chat01a0f218-ce92-7671-b666-efccdef3aed2; independently confirmed. No imported definition, library, schema or output patched. Continue independent work while official fix is pending.

Additional B-006 candidate review: C255576 has two actual contacts and no locating holes, but is unselected pending supplier-land/current-ALPS-pattern acceptance and mechanism/electrical review. Raw and converted pad dimensions match; no new converter defect or model-height defect alleged. C202371 supplier alternate has the same lands. Detailed evidence saved under hold-control-alternate-review-2026-10-03.

B-009 latest exact readback: battery-ready private release0.0.2-wip-a0-battery-ready-review native834success/62fail;55timeout files match, six prior413missing plus new actual404 timeout imports/SN74LVC1G17DBVR/SN74LVC1G17DBVR.tsx. Seven currently missing, no unverified files. Ready=false/private=true. Exact receipt and native log saved under fabrication-rule-review-2026-10-03 and sent to fix chat; do not call all62 missing.

### 2026-10-03 hold-readback and top-control continuation

B-009 current parent fa90b5420f8e567270697c68132f311444a42424: native private0.0.2-wip-a0-fabrication-review exits1 with957reported successes/28failures. All22timeouts are byte-verified present; six priorHTTP413 files remain404, no unverified cases. private=true/ready=false. Exact receipt/log/readback and sent update are saved under hold-readback-review-2026-10-03. Publication remains incomplete; no files omitted, checks weakened or readiness forced.

B-009 current0573bf4492817ea0263827b6f0431fb7905d4959: native private0.0.2-wip-a0-hold-readback-review exits1 with1081reported successes/20failures.13timeout files are byte-verified present; six priorHTTP413 files plus timeout imports/TLV3201AIDBVR/TLV3201AIDBVR.tsx (C105188) are404. No mismatched/unverified failed files; private=true/ready=false. Exact evidence in hold-readback-publication-2026-10-03, result sent to authorized fix chat. GitHub0573bf4 pushed; publication incomplete. These local outcome/watch notes were created after enumeration, pending a future implementation revision; no new board version or full-publication claim.

B-010 remains reproduced by six unchanged native elements in the independent hold-readback candidate. Canonical23pass/one existing strict JSON fail/228assertions; native build/allfive diagnostics/A4/snapshots/types/format pass only within their stated scopes. Hardware leakage, power-ramp/bounce/off timing, selected MCU pin/pulls and decoupling loops remain unqualified; this is not a complete privacy circuit or full-board gate pass.

Procurement observation: native C22548 stock5 and C98220 stock22 require final whole-BOM quantity/availability review. Genuine unchanged C21190/0603WAF1001T5E stock8,013,731 is used only in the new readback-series candidate. C25804/0603WAF1002T5E is genuinely imported but unselected: empty native stock-filtered searches and separate EasyEDA library success do not prove a bug or JLC assembly availability. Sent to fix chat; its independent finding is saved in supplier-search-observation.json. No false new B-number assigned.

Top-control nominal study addresses one RF placement conflict: shifting the MCU physical center left8mm increases the switch body/terminal-to-antenna gap9.95→17.95mm on the50x65trial, with actual native pads still supported. Raised LCD/tolerances/substrate, enclosure/control mechanics, pack/speaker and dominant front coverage remain open. No native placement/keepout/cutout or component definition was created by this sketch. Core0.0.2066's published changes concern bends/tear-relief/checks dependency, not these blockers. Board dependencies remain pinned; no copper or fabrication files exist.

## Current reassessment — 2026-10-03, A0-reference-import-review

**B-008 resolved on board:** C105188/C94934/C20917/C15127 reimported through official easyeda0.0.370 CLI and validated with core0.0.2070. Physical footprint and pin-label blocks unchanged; native U7/D2/Q1/Q2 reference text belongs to the correct component. All four builds/all20 diagnostics pass, three A4 exports/snapshots visually reviewed. B-003 rechecked successfully. Earlier B-008 entries are historical reproductions.

**Assembly blocker B-005 persists:** current microphone four polygon grounds still have no solder paste. Native C41348533/LD-SM-430 alternate motor imports successfully, but its three polygon lands also have zero paste; candidate remains unselected. Three additional speaker imports C20613566/C49246973/C7430168 lack supplier library data (B-012). No invented substitutions or component patches. Full power/privacy/pack/hold mechanics/speaker qualification and final placement still gate whole-board routing. B-010 remains a strict automated-check blocker, not permission to hide native failures. B-009/B-015 gate publication/final fabrication exports and do not stop independent circuit authoring. B-007/B-011 are documented qualification questions, not newly proven manufacturing defects. Evidence: `evidence/blocker-recheck-2026-10-03-1357/`.
