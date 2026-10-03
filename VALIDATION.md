# Validation — A0-display-logic-review (work in progress)

Updated: 2026-10-03 (Europe/Tirane). **Independent MCU/USB and improved regulator reviews added; B-003 remains resolved. B-005 includes USB polygon paste; B-008 includes ESD reference text; B-009 private source publication and B-010 native JSON schema remain blocked. No complete handheld schematic/PCB exists. Not fabrication ready.** B-001's reported dimensions are corrected locally with explicit user authorization. A0 identifies engineering intake and component review, not a fabricated board revision. No physical hardware is available.

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

Current pinned dependencies: tscircuit **0.0.2742**, @tscircuit/cli **0.1.2235**, direct @tscircuit/core **0.0.2058**, TypeScript **5.9.3**, Biome **2.5.14**, @types/bun **1.4.2**. Runtime Bun **1.3.9**. `bun.lock` records transitive dependencies. Installation emitted peer-version warnings involving circuit-json 0.0.509, React/ReactDOM 19.3.0 and @tscircuit/alphabet 0.0.25; unresolved, not accepted board warnings.

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
