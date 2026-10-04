# Layout and BOM audit — 2026-10-04

**Verdict: preliminary placement checks pass; final layout and assembly BOM are NOT approved. NOT FABRICATION READY.**

Reviewed source commit `cec97000fe0cf2f799b1e84a455a4479f4ff93ed`; last implementation `314cb1b36d0a9b6d641c018ce27288eb47815c95`. Canonical `dist/index/circuit.json` SHA256 `f4319f271856f07477340c3342ce9a576236be438913be4aca5bd9786487d1c5` (2,728,724 bytes). No board wiring, placement, imports, dependencies or saved copper was changed by this audit. Core0.0.2070, CLI0.1.2235, tscircuit0.0.2742, props0.0.682 and CircuitJSON0.0.513 remain installed.

## Verified now

All five required native checks (netlist, pin_specification, source, schematic-placement, placement) and the existing-copper shorts check exit0. Formatting and TypeScript exit0. Tests retain42 pass / 2 fail / 418 assertions: the native MCU schema fixture and full-board zero-errors fabrication gate. These failures are not waived.

The fresh native placement/CAD build exits0. Source connections and physical placement records equal the canonical board; placement-only output contains zero traces, vias or pours. The canonical routed JSON hash remains unchanged. Current native PCB and 3D views were inspected. All 135 native components are top-side, in the accepted 50 × 65 mm board arrangement, including the intentional module antenna overhang; 125 are purchased and 10 are native test/solder pads. References are unique; every purchased part has an exact JLC number and MPN. J8 is absent. The two motor pads are present and preserve their VMOTOR and switched-return connections. Two M2 mounting holes and all-layer clearance features remain native features.

Thirteen current native A4 schematic sheets were rendered and reviewed for page boundaries and gross arrangement, alongside the manufacturer connection tests. Imported reference-label omissions and crowded labels remain, including amplifier-enable/Q2 labels; this review does not approve final schematic annotation or establish full electrical qualification.

## Connector and external-part review

| Item | Current state | Verdict |
|---|---|---|
|J1 USB-C C165948|Bottom-edge access; existing USB source/partial copper preserved|Orientation acceptable in the current native preview; actual cable/case and thin-stackup impedance remain open|
|J3 battery C157929|Internal side-entry PH3, mouth along−Y; centre2=PACK_NTC; outer1/3open|Centre NTC correct. BAT+/GND numbered outer contacts unresolved: cannot connect the pack yet|
|J4 speaker C173752|Internal side-entry PH2, mouth along−Y|Preview orientation consistent with supplier drawing; actual mating housing/wire bend and external speaker qualification pending|
|J6 service C160405|Internal optional UART/BOOT/EN service connector retained|Backup access only; normal programming intended through USB-C; physical harness/access not tested|
|J7 display C262650|50-pin 0.5 mm top-contact;90° rotation; mouth towards+X|Inherited fold arrangement, not qualified for the portrait panel. Contact face, pin1, fold radius and engagement still required|
|Motor pads|Top2mm M+/M− pads,1mm copper gap/2mm edge gap|Native geometry and source connectivity pass; solder harness/strain relief pending|

Provisional external BuyDisplay ER-TFT026-1 has an integrated ILI9341 controller and a manufacturer50-contact pin map. The source SPI II1110,2.8V logic and four separate LED-return assignments match that logical map **only if the provisional panel n→J7(51−n) fold/contact assumption is confirmed**. The8051development-kit page is not the standalone panel purchase. Current bare-panel orderability and current thin-variant drawing remain unqualified. Display routing stays deferred.

The prior measured display body overlap82.712% satisfies the physical-coverage target conditionally, but does not prove enclosure assembly. The0.8mm four-layer board tolerance, PH-header minimum PCB thickness, USB impedance, antenna exclusion, raised display, protected pack swelling/restraint, screws, actuator and actual harness clearances remain open. A rendered board alone cannot prove those fits. The hard enclosure maximum remains60×75×15mm.

## BOM and assembly blockers found/reconfirmed

Exact official JLC catalogue searches were run for all 44 active unique supplier numbers.43 returned exact matching manufacturer identities; no returned identity mismatch. C22548 stock 5 is below 7 required. C105588 (six100Ω resistors) has no exact in-stock result; that does not prove it lacks supplier library data. C98220 stock 22 versus 20 required and C107701 stock 8 versus 5 required also leave little assembly/rework margin. No whole-order availability or reservation is approved.

Genuine alternatives found: C21190/0603WAF1001T5E (1kΩ,0603,1%,100mW,100ppm/°C), stock 8,013,731; C22775/0603WAF1000T5E (100Ω,same catalogue ratings), stock 7,325,193. C21190 is already genuinely imported and used at R100. Neither was substituted by this audit. A substitution must use the supported import, manufacturer/land review, fresh build and affected placement/routing checks; catalogue equivalence alone does not qualify it.

**B-005 actual native paste omissions:**45 unmasked SMT pads have no corresponding native paste element, verified against current output, installed core shape branches and the rendered native paste mask:

| Part | Missing native paste |
|---|---|
|U16 BQ24074RGTR/C54313|All 16 pill-shaped terminals plus polygon exposed pad: 17|
|U27 TPS60230RGTR/C1848364|All 16 pill-shaped terminals; its rectangular exposed pad does have paste|
|U4/U5 ICS-43434/C5656610|Four polygon ground pieces per microphone:8 total|
|J1 TYPE-C-31-M-12/C165948|Four polygon SMT pads13–16; separate plated anchors do not cover these pads|

The charger/backlight terminal omissions prevent approval of the reflow stencil/assembly output. Existing rect-pad paste also needs final area/window review. No component, runtime, stencil or Circuit JSON was manually patched.

The unchanged official BOM converter0.0.19 emits 125 purchased rows but 31 blank Comment fields and 125 supplier-code footprint fallbacks. This is a fresh reproduction on the current full board, not just historical fixtures. `native-bom-probe.json` is diagnostic evidence, **not an approved fabrication CSV**. Accurate assembler BOM/CPL and orientation feedback remain required (B-015).

## Remaining copper and separate software/publication gates

The canonical board has 11 traces and 2 vias with prior native saved-route/replay evidence. The unchanged native output retains 413 unconnected-port errors and 5 missing-trace errors; zero shorts on existing copper does not establish complete routing. Full power loops, current capacity, every required signal, complete clearances and the final stackup still need validation. The saved Q9/C20917 gate phase has a non-unique native port-selector export failure; charger routing attempts previously exhausted native iterations. No false route cache or successful route claim was introduced.

Full strict-schema failures remain 169 native elements (B-010), separately from physical manufacture. Public A5 package has94/95verified files and matching Circuit JSON, but the required C262650STEP remains missing after HTTP413 (B-009). Those software/package failures do not themselves prove a connector is physically wrong, and they do not waive paste, power, fit or routing approval.

B-003 ground identity remains resolved in the current design; it is not the present blocker. No physical board, protection test, temperature/current measurement, verified screen operation or prototype-order approval exists. Stages 1/3/4 remain in progress, 2/5 blocked, 6 not started, 7 pending. Background automation stays paused; no cross-chat issue messages are sent.

## Evidence and commands

- `summary.json`, `inventory.json` and `inventory.md`: complete native inventory and45 paste omissions; inventory is not an assembler BOM.
- `supplier-receipt.json`, `supplier/`, alternative receipts: exact queries, quantities, identities and dated stock observations.
- `native-check-exits.json` and per-check logs: six native checks. `local-check-exits.json` and logs: format/types/tests.
- `cad-build-receipt.json`, `fresh-placement-comparison.json`, `current-native-3d.png`, `current-placement.png`: fresh CAD/source-geometry equality and unchanged canonical hash.
- `sheet-1.png` through `sheet-13.png`: current A4 render review. `native-paste-mask.png/svg`: unchanged native paste render. `native-bom-probe.json`: official converter output.
- Commands: `tsci check netlist|pin_specification|source|schematic-placement|placement index.circuit.tsx` (separate calls), `tsci check shorts dist/index/circuit.json`, `bun run format:check`, `bun run typecheck`, `bun test ./tests`, `tsci build placement.circuit.tsx --pcb-png --pcb-svgs --schematic-svgs --3d --glbs`, exact `tsci search --jlcpcb --json C-number` calls and installed official renderer/converter APIs. No native build/check failure was hidden.

Manufacturer reference: [BuyDisplay ER-TFT026-1 manual](https://www.buydisplay.com/download/manual/ER-TFT026-1_Datasheet.pdf), pages5/9–11; [TI TPS60230](https://www.ti.com/lit/ds/symlink/tps60230.pdf); [JST PH](https://www.jst-mfg.com/product/pdf/eng/ePH.pdf); preserved AKY2945specification and the user's confirmed centre-NTC instruction. Logical connection tests are distinct from physical mating proof.

Public runtime remains [A5](https://tscircuit.com/AnasSarkiz/tscircuit-ai-agent-remote?version=0.0.2-wip-a5-motor-pads#files); this audit changes evidence only and does not create a new board version or repeat the unchanged failed upload.
