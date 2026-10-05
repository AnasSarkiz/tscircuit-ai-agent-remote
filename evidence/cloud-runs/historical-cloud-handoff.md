# AI Remote: Codex Cloud continuation checkpoint — 2026-10-05

Read this document first. This is the existing board, not a new design. The user
requested moving routing off their Mac because native routing repeatedly exhausts
its memory. **Do not launch routing on the Mac.** Continue in a published Codex
Cloud environment checking out this repository. No cloud execution or successful
environment publication is implied by the presence of these files.

## Repository and exact build

- Repository: https://github.com/AnasSarkiz/tscircuit-ai-agent-remote — public.
- Original A6 source checkpoint: `52f479592772cdcfac8f2290718ddef8f360419c`.
- Continue the cloud-migration commit on `main`, including its A7 source changes.
- Entry: `index.circuit.tsx`, delegating to `main.tsx`.
- Native generated build: `dist/index/circuit.json`, 2,948,515 bytes, SHA256
  `ff99af3edc2ea509109e4b9b70188668d813673aacae55890c5f9cbe5dc77bd8`.
- This is the byte-identical output of the last completed `RootCircuit` native
  render, not hand-edited JSON. `context/build-checkpoint.json` records its origin.
- Board source was restored byte-for-byte to that completed render's snapshot.
  Package setup scripts were added afterward; dependency versions remain those
  used by the render. Unbuilt routing trials are not active in the entry point.
- **138 traces, 116 vias, 275 native open-port errors, one inner1 GND pour.**
  Before A7:20 traces/2 vias/402 native open-port errors. These counts do not prove
  physical connectivity or zero accidental opens.
- Last tscircuit registry version is still
  https://tscircuit.com/AnasSarkiz/tscircuit-ai-agent-remote?version=0.0.2-wip-a6-bom-routing#files
  — A7 cloud preparation is not a new registry release.

## Accepted product and mechanical decisions

Handheld Wi-Fi/BLE AI control device, rounded rectangle/square appearance, dominant
front display, exactly one top-edge hold-to-talk actuator. Top-side PCB assembly.
ESP32-S3 module, two digital microphones, external 8-ohm speaker with I2S amplifier,
internal haptic motor, protected rechargeable 1S LiPo, USB-C charging/programming.
Do not restore abandoned APPROVE/REJECT controls or the old encoder concept.

- PCB **50 × 65 × 1.0 mm**, four layers; do not resize it.
- Enclosure maximum **60 × 75 × 16 mm**. The latest request supersedes the old
  15 mm maximum and old 0.8 mm board thickness.
- Main placement is frozen conditionally after the updated top/side/bottom model
  review. A physical prototype, FPC fold, harnesses and RF performance remain
  unverified. Small passive moves require a demonstrated copper/placement issue.
- The one A7 passive move is C4: from `(-2,-13.2),180°` to
  `(-2.25,-12.65),90°`, displacement 0.60415 mm. Earlier trial positions overlapped
  U2's actual courtyard; those failed artifacts are preserved.
- Use `evidence/a7-routing-2026-10-05/mechanical/mechanical.html` and
  `placement-freeze-review.json`. The refreshed model keeps major bodies in place,
  updates 1 mm PCB/16 mm case and models battery expansion. The allocated maximum
  stack is approximately 15.092 mm with the proposed JLC tolerance, not a physical
  fit certificate. C4's last small move does not change height but needs fresh CAD.
- Keep display, battery, FPC, screws, wiring and metal outside the ESP32 antenna
  keepout on every layer. Do not solve conflicts by enlarging the enclosure.

## Display, battery and connector decisions

**Display:** BuyDisplay **ER-TFT026-1**, standalone bare panel, no touch option;
integrated **ILI9341 driver**, not the 8051 evaluation/development board, and not
sourced through JLCPCB. Supplier:
https://www.buydisplay.com/download/manual/ER-TFT026-1_Datasheet.pdf
Verify the exact supplier product/drawings in the saved BuyDisplay references
before ordering. Logical pin mapping and level translation are authored; physical
FPC contact face, pin-1 orientation, portrait fold and mating orientation remain
unconfirmed. Approximately 82.7% nominal/81.7% allocated physical panel coverage
was studied; this is physical coverage, not pixel-area coverage.

**J7:** Keep physical-contact-dependent J7 fanout unrouted. Continue all safe
upstream MCU, translator, display power and backlight wiring. The last native
error list includes 46 J7 port errors; classify required contacts, shields and
unused contacts individually rather than calling every error a required signal.

**Battery:** Selected external AKY2945 / LP523450 protected 1S 3.7/4.2 V,
1000 mAh pack, 10 kΩ NTC, JST PHR-3/2.0 mm harness. User confirmed manufacturer
drawing: red=BAT+, yellow=NTC, black=GND; yellow is physically the middle contact.
**J3 centre is PACK_NTC.** Outer contact numbering remains unconfirmed.
Leave both outer J3 contacts unrouted and unassigned; do not guess BAT+/GND.
Written supplier confirmation or keyed physical multimeter measurement is needed.
The native error count may omit unused/unassigned connector contacts; the two
physical J3 outer contacts remain intentional omissions regardless of that count.
Internal charger BAT wiring may continue. Prior stock was zero; supplier/current,
NTC curve, protection and physical qualification are not completed.

J1=USB-C, J3=battery, J7=display FPC, J4=external speaker. J6 is the retained
optional service UART interface; native USB handles normal programming. **J8 was
removed.** The haptic motor uses native M+/M− solder pads instead of a JST.
Do not restore J8. Connector access and plug directions require CAD/drawing review.

## Current official tooling and routing behavior

The user explicitly requested an update during A7. Installed/pinned official
versions: Bun1.3.9; tscircuit0.0.2744; core0.0.2090; CLI0.1.2237;
props0.0.688; circuit-json0.0.517; capacity-autorouter0.0.958;
checks0.0.237; easyeda0.0.370; circuit-to-svg0.0.440; modelprinter0.0.6.
Before changes, run `python3 scripts/cloud/verify_checkpoint.py` against `context/checkpoint-sha256.json`. After setup, source `scripts/cloud/env.sh` in each task shell to select the pinned Bun and geometry module path.

Use `bun.lock` and `bun install --frozen-lockfile`; no unmerged/local patches.

Current native router is `auto_local`, default/latest **Pipeline 9**, with separate
`autoroutingphase` components and real `pcbTracePaths` replay. Main effort is1x,
`routeRemaining=false`, routing disabled in placement-only builds. Capacity0.0.958
was already the latest when the wrapper/core/schema packages were updated.
For explicit pipeline selection, use the supported board `autorouterVersion`
prop. An attempted config-object placement of that field failed TypeScript; do
not cast around it. `context/proposals/main.tsx.diff` preserves the unbuilt
explicit board-prop proposal. Check emitted solver metadata to identify an actual
pipeline, rather than assuming an unsupported config field took effect.

Genuine saved phases are under `routes/a3`, `routes/a5`, `routes/a6`, `routes/a7`.
A7 adds hold readback, haptic enable, display enable, MCU amplifier BCLK/DIN,
charger NTC, service UART and a rerouted regulator power-good phase. Old feedback
paths are retained separately because C4 made the old PG path obstructed.
`src/board/ground-paths.json` contains explicit manually designed native GND paths;
these are **not fake autorouter caches**. They are consumed by supported `trace
pcbPath`. Coordinates use component display-origin offsets and rotation, not an
imported body's graphic centre.

Whole-net power and several signal native trials stalled or reached iteration
limits. Some processes blocked the event loop, so in-process timeout callbacks
did not provide reliable termination. Failed/unfinished output is not accepted
copper. Trial401 charger-ISET and402 charger-PGOOD were stopped/incomplete; the
coordinator later failed while reading an empty/truncated JSON after resource
pressure. Those results cannot be treated as passing or used as saved routes.
All raw evidence that existed is retained; missing final JSON is disclosed.

## Real copper issues and the next engineering work

1. **Fix a confirmed via clearance first.** Last completed build has the U2 GND
   via at `(-3.45,-14.2)`, hole0.3/pad0.7, only **0.19205296 mm** from the bottom
   REG_PG trace; required0.2. A small proposed move to `(-3.35,-14.15)` is saved in
   `context/proposals/RegulatorSheet.tsx.diff`. It was not built/accepted. Rebuild,
   rerun all trace/via/plane checks and compare cached PG geometry after applying.
2. Regulator local input/output stubs and capacitor trunks are authored: U2 input
   and output necks0.275 mm, approximately0.65 mm centre-line length, then C4
   VSYS1.0 mm/C5 V3V3.8 mm. Their endpoints physically overlap. Measure exact
   actual copper and current/thermal basis; this is not completed distribution.
   U2 GND2→via, GND3→2(.3), GND8→3(.28) are explicit paths.
3. Review original short L1/L2 saved routes against TI: .275→.4→.7→1.0 mm. Native
   constant-thickness segments use the **starting point's width**, not the maximum
   adjacent width. .275 mm necks must remain extremely short; measure loop area.
4. Continue VSYS/V3V3/VBUS/internal PACK_BAT, charger ISET/PGOOD/CHG/enable, MCU
   support, microphones, amplifier LRCLK/enable/speaker pair, motor pads, backlight,
   upstream LCD logic, USB and controls. The full task is preserved verbatim at
   `context/user-requests/current-routing-request.txt`.
5. Remaining ground escapes include U16/U3 ground/exposed-pad groups and microphone
   pin3 polygons. Conservative planners failing are not proof of impossibility.
   Ordinary drills must clear pads including same-net pads. Thermal-via exceptions
   require manufacturer-backed review and an explicit fabrication treatment.
6. ICS43434 ground numeric anchor is one supplier quadrant centroid near the .6 mm
   acoustic hole. A .2 mm centre-start trace has approximately .243 mm actual hole
   clearance versus .25 required. Verify exact shape geometry and supported pad
   edge clipping/paths; do not patch the imported geometry or generated JSON.
7. Audit actual connections: one-port manual stubs/native port markers do not
   prove a shared net is globally joined. Prove GND vias touch the actual L2 solid
   BREP plane and review islands, apertures and bottlenecks.
8. The latest core emitted two GND width warnings identifying a remote shared-net
   trace. The actual U2 bridge records still show .3/.28 widths. Preserve warnings
   and investigate attribution; do not suppress them or infer tool correction.

Nominal starting widths: signal.20–.25; VSYS/internal PACK1.0; V3V3.8; VBUS.5;
speaker and haptic wider than logic. Audit actual necks/lengths/vias/current, not
nominal configuration. L1 short signals/local power; L2 continuousGND; L3 power/
slow signals; L4 signal routing. Antenna keepout copper-free on all four layers.

### USB calculation already performed

Official JLC calculator: four layers, nominal1 mm, outer1oz/inner.5oz, L1 referenced
to L2, noncoplanar differential90Ω. Selected standard **JLC04101H-7628**, finished
1.02 mm±10%. Result **width.2979/gap.2101 mm**. Copper/dielectrics:
L1.0350 / 7628.2104 / L2.0152 / core.5000 / L3.0152 / 7628.2104 / L4.0350 mm.
Saved UI readback: `evidence/a7-routing-2026-10-05/usb-1mm-calculator-readback.json`.
Fit.5% is a calculator fit, not fabrication impedance tolerance. Old .2906/.1999
geometry is superseded. Existing short MCU USB paths were widened, but the full
J1/ESD/resistor/MCU pair is unfinished. Native .5 mm pad pitch produces a .2021 mm
pad-exit gap: review this local neck separately. Do not claim complete90Ω USB or
matched lengths until the actual pair is routed and measured.

## Fabrication blockers that must not stop independent routing

- U16 BQ24074 and U27 TPS60230:32 missing pill-shaped paste apertures.
- Required Gerber-based shorts tool: `Unsupported shape polygon` failure. Native
  `tsci check shorts ... --mode pcb` diagnostic passed on the latest completed
 138-trace output; it is not the required Gerber pass or complete DRC approval.
- Strict native schema failures remain. Last A6 baseline169; remeasure A7, do not
  copy the old count into a new claim.
- Native BOM Comment/MPN and assembler footprint/CPL qualification unresolved.
- J3 outer BAT+/GND numbering and J7 physical mating unconfirmed.
- Registry C262650 J7 connector STEP11.4MB fails HTTP413. Do not omit the model,
  force readiness, or repeatedly retry unchanged publication.
- Full electrical/current/startup/privacy/power/thermal/mechanical qualification,
  assembler feedback and final fabrication review remain unfinished.

C22548 shortage was replaced with genuineC21190; C105588 with genuineC22775.
Final complete-BOM availability must still be checked. C98220 qty20 versus prior
stock22 needs assembly quantity reserve review. Use actual BOM/import records.
**B-003 ground identity was officially fixed already.** Do not wait for it again.
Do not report historical unselected component issues as current assembly parts.

## Resource-safe cloud setup and continuation

Official environment procedure:
https://learn.chatgpt.com/docs/environments/cloud-environments

Create/select an environment for **AnasSarkiz/tscircuit-ai-agent-remote**. During
setup, run `bash scripts/cloud/setup.sh` in the repository root. This installs
pinned Bun/dependencies and the geometry analysis library; it does not build or
route the board. Keep environment privacy Only me unless the user requests sharing.
No local credential, `.env`, Keychain token or tscircuit session is in this repo.
Initial routing uses local imports/assets and needs no publication credentials.
Use the Package managers policy for dependency setup; add other hosts only when
required and approved. Do not turn on unrestricted networking as a convenience.

Use the Linux-only resource supervisor for heavy operations:

```sh
bun run cloud:run -- --seconds 900 --log evidence/cloud-runs/route-01.log -- \
  bun evidence/a7-routing-2026-10-05/capture-native.tsx evidence/cloud-runs/route-01
```

If Bun is installed in the repository's `.tools/bun`, use
`.tools/bun/bin/bun` instead of `bun`. Run **one** native operation at a time.
The supervisor reads the VM/cgroup memory limit, reserves35% for the environment,
tracks process-group RSS, and terminates on memory/time limits with an explicit
outcome JSON. Termination means unfinished, never passed. It is an operational
guard, not a solver/DRC override. It has a concurrency lock. Do not bypass it to
run a giant whole-board solver or launch multiple builds simultaneously.

Keep failed trials and native inputs/events, but compress repeated historical
records losslessly instead of keeping gigabytes of duplicate CAD/SVG text.
Archive receipts and SHA256 manifests verify every original byte. Historical
`native-*` trial directories now have corresponding ZIP archives; read a needed
member directly or extract only that member. Do not unpack every archive at once.
Saved runtime routes remain ordinary JSON under `routes/`, independent of archives.
Do not resume the old unbounded coordinator script unchanged.

Recheck supported APIs in installed types/help. `autorouterVersion` belongs on
the board for typed explicit selection. Public `trace pcbPath` may be used for
deliberate manual routing. Never synthesize cache JSON from a hand-designed path,
patch runtime/schema/imports, hand-edit circuit JSON, weaken tests/DRC, hide errors,
or accept snapshots merely to pass. Root skill is vendored at
`.agents/skills/tscircuit/SKILL.md`; local personal skills are not automatically
synced to cloud. Captured handbook pages are in `context/handbook` with official
links; refresh when network access allows.

## Gates, authority and final reporting

The user explicitly authorizes continuing safe routing while fabrication-tool
and supplier qualification issues remain. This changes routing priority, not
fabrication approval. Never claim all stages passed or that copper is complete
while accidental required connections remain. Preserve actual stage results.
Only genuine JLC electronic definitions; existing explicit exceptions are the
historical C370970 correction and C5656610 hole.6. External display/battery/harness
are authorized purchased assemblies; do not turn them into invented imported ICs.

- Do not send issues/messages to any other chat: that authorization was revoked.
- Keep the background watcher paused.
- No new subagents/delegation without explicit applicable authorization.
- No ordering, upstream PR landing, eFuse edits or fabricated physical test results.
- Both board destinations must remain public. GitHub pushes/board publications
  have standing authorization, but **this routing milestone defers registry
  publication**. Do not spend it retrying C262650 uploads.
- Board-only tscircuit packages contain runtime source/imports/models/routes and
  corresponding generated circuit JSON, not handoff docs, scripts or trial archives.

Run format/types/tests, native netlist/pin/source/schematic/placement checks,
fresh routed build, native PCB shorts plus independent complete copper/via/pour
geometry/connectivity, and retain the required Gerber check failure until fixed.
Rebuild fabrication artifacts from the final validated revision. Inspect every
copper layer, detailed regulator/USB/power/audio/mic areas, top/bottom3D and opens.
Required final metrics/tables/images and priorities are in the full routing brief.

Current state: **ROUTING PARTIAL; accidental required-connection count not yet
fully classified. FABRICATION READY = NO. Physical prototype not tested.**

## Context index

- `AGENTS.md`: current precedence and full inherited workspace gates.
- `context/user-decisions.md`: accepted corrections and latest authority.
- `context/user-requests/`: original pasted product/priorities/A2/A3/A7 briefs.
- `README.md`, `REQUIREMENTS.md`, `VALIDATION.md`, `BOM.md`, `issues/`: prior
  engineering history; use dates and latest overrides, not stale first-stage claims.
- `context/build-checkpoint.json`: exact generated output/source restore receipt.
- `context/proposals/`: changes proposed after that render, not accepted copper.
- `evidence/a7-routing-2026-10-05/`: current routing/mechanical/USB/update/audit
  records, archived real trials, and incomplete-trial disclosures.
- `evidence/a6-bom-routing-2026-10-04/`: prior BOM/placement/publication checks.
- `imports/`, `references/`, `routes/`, `src/board/`, `tests/`: real design assets.

Conversation context is curated here and in original briefs; this is not a claim
that every historical chat/tool transcript was exported. No secrets are included.


## Migration verification, 2026-10-05

Canonical TypeScript passes. Static tests: 40 pass, 4 fail, 406 assertions across 16 files. Retained failures: strict native schema, placement fixture equality, original-four-trace equality, and zero-unresolved-error fabrication gate. These were not suppressed or rewritten. Logs are context/local-typecheck.log and context/local-tests.log. Cloud helper syntax checks pass; Mac guards reject heavy execution. The Linux supervisor/install path is not yet run in an actual cloud VM.

The latest native replay's event/start JSON files are preserved in native-latest-replay/native-records.zip with exact per-file hashes, alongside the accessible circuit.json and source-snapshot. Extract into that same directory before historical scripts expecting raw event/start files. Archive verification was completed before removing duplicate originals; this is genuine original data, not reconstructed routing.

Root AGENTS.md, repository tscircuit skill, board-cloud-start skill, original human briefs and curated decisions are included. This captures the relevant continuation context; no claim of full automatic conversation export.

Formatting currently reports13 errors in the frozen board replay source; context/local-format.log preserves the result. Reformat only with subsequent native rebuild/replay validation. No Mac routing resumes.

In the actual Linux environment, run `python3 scripts/cloud/smoke_test.py` before heavy work. It exercises success, timeout, small memory termination and exclusive locking with tiny Python child processes, retains logs/receipt and launches no native routing. It has only been syntax-checked locally; Linux outcomes remain unverified.
