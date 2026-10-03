# tscircuit AI agent remote

Revision A0-display-logic-review (work in progress), updated 2026-10-03: **unrouted regulator application review added; B-002 acoustic diameter corrected locally; B-003 resolved using the official core release; B-005 missing microphone ground paste confirmed; no complete handheld schematic or PCB exists**. Not ready for routing or fabrication; untested prototype intent.

Private repository: https://github.com/AnasSarkiz/tscircuit-ai-agent-remote

Private tscircuit package: https://tscircuit.com/AnasSarkiz/tscircuit-ai-agent-remote
— last fully verified private source release is **0.0.2-wip-a0-core-alignment**
(274 files; Git 8bbde6e). MCU/USB source commit **02950fb** reached GitHub; native private release
**0.0.2-wip-a0-mcu-usb-review** failed with two timeouts and two HTTP413
file rejections, and remains ready_to_build=false (B-009). This is disclosed work-in-progress prototype source;
no complete-board build or fabrication approval is claimed.

The accepted device is the square, screen-dominant concept with one top-edge hold-to-talk button, a speaker and rechargeable battery. Hold, speak and release to send a Wi-Fi request; show and speak the response. All PCB electronics must assemble on the top side. The encoder and separate APPROVE/REJECT controls are removed from the active design. See `REQUIREMENTS.md` for the complete requirement changes and remaining interface decisions. Firmware implementation is outside this task.

The user approved a maximum PCB envelope of **50 x 65 mm**. A **50 x 50 mm square target** starts the mechanical study within that envelope; it is not yet validated. Four copper layers are intended. Accepted visual reference: [square product concept](assets/product-concepts/ai-remote-v1-infographic-v3.png); rendered placement is illustrative.

## Rechargeable battery

One protected **1S, nominal 3.7 V, 4.2 V-charge LiPo pack**, targeting **500–1000 mAh**, USB-C charging and operation while plugged in. BQ24074RGTR / C54313 and TPS63802DLAR / C2845237 remain the charger/power-path and 3.3 V regulator candidates. A top-side SMT battery connector, JST S2B-PH-SM4-TB(LF)(SN) / **C295747**, is now imported verbatim through the supported workflow. Exact pack, harness polarity, thermistor, charge current, protection, runtime and mechanical fit still need qualification. This is requirement/BOM preparation, not an integrated battery circuit.

## Published update check

Installed and pinned **tscircuit 0.0.2736 / CLI 0.1.2232** on 2026-10-03. Fresh C5656610 import still contains the **0.3999992 mm** acoustic opening; TDK recommends at least **0.50 mm**. **B-002 is not fixed in the tested published release.** This is historical recheck evidence; the subsequently authorized local correction is described below. Version metadata, import logs, checksums and diagnostic evidence are saved under `evidence/update-check-2026-10-03/`. Dependent placement/routing remain stopped.

## User-authorized microphone correction

C5656610 / ICS-43434 now uses a **0.60 mm** acoustic hole at the original center.
Every non-diameter byte in the imported file is unchanged. Raw supplier evidence
confirms that the original 0.3999992 mm hole comes from the LCSC-owned footprint;
the converter preserves it correctly. No supplier-library or converter change
was made.

Generated geometry confirms **0.60 mm**, nine unchanged copper pad shapes and
minimum hole-edge-to-copper clearance **0.2580203 mm**. The isolated placement
check passed with zero errors/warnings. Evidence and the original source are
saved in `evidence/microphone-local-correction-2026-10-03/`.

**B-003 is resolved:** official core 0.0.2058 now generates linked ground-pad
ports and passes the native component build/checks after supported dependency
alignment. **BLOCKING B-005:** native generation omits solder paste for the four
polygon ground pads. Diagnostic Gerber export confirms those openings are absent
from F_Paste. This assembly defect was reported to the authorized issue chat;
imported pad/paste geometry has not been patched. See the evidence below.

## Historical corrected encoder import

**ALPS EC11E15244G1 / LCSC C370970:** the user explicitly authorized correcting this imported component's symbol and footprint. Its five terminal holes are now **1.05 mm**, and its two mounting slots are **2.65 mm long**, within ALPS's 1.00–1.10 mm and 2.60–2.70 mm ranges. **B-001 is resolved locally for the reported dimensions.** The external supplier library has not been changed.

C370970 uses its existing native `<chip>` as a schematic box. Pin labels, centers, slot widths/orientation, outer pads, silkscreen, courtyard and models are unchanged. This encoder is no longer part of the accepted one-button design; its correction and evidence are retained historically. The microphone now also has a diameter-only authorized correction. Other imports remain unmodified. Isolated review artifacts are not the handheld board or fabrication package. No handheld placement, routes or fabrication outputs exist.

## Commands

Run inside this directory. `bun install` installs pinned dependencies. `bun run format:check` and `bun run typecheck` check project tooling. `bun test` currently reports **9 pass / 1 fail**: the newly added native Circuit JSON schema regression reproduces B-010. Manufacturer pin/PSRAM/exposed-ground and existing import tests pass; historical encoder checks remain evidence, not active BOM approval. `bun run build` reports that the complete board has not been authored. The original proposal is preserved in `evidence/proposals/C5656610-acoustic-hole.diff`. The latest user instruction authorized applying it locally. The microphone component build now passes; B-005 paste generation blocks assembly qualification. Whole-board design remains incomplete.

## Evidence and remaining work

See `VALIDATION.md`, `BOM.md`, `issues.md`, `references/sources.md` and `routes/README.md`. Continue in this task directory. No earlier board source or validation evidence was reused.

Import provenance: **JLCEDA/EasyEDA Official Library**, accessed through the supported JLCPCB importer. [JLCEDA](https://lceda.cn/) / [EasyEDA](https://easyeda.com/).

## A0 regulator review and current fix status

Current pins: tscircuit **0.0.2742**, CLI **0.1.2235**, core **0.0.2058**.
Core PR [4323](https://github.com/tscircuit/core/pull/4323) merged and is present
in the published release. Native CLI uses the locally imported tscircuit renderer;
a supported Bun override and clean installation aligned its nested dependency.
The earlier failed-release attempt is preserved in `evidence/core-fix-2026-10-03/`;
the verified resolution is in `evidence/core-alignment-2026-10-03/`.

Seven exact JLCPCB power parts were imported without edits. The draft A4
regulator application source is `src/power/regulated-3v3.tsx`; its isolated
review fixture and reviewed PNG/SVG/JSON are in `evidence/power-review-2026-10-03/`.
The fixture passes the five native placement-stage commands with no reported
errors or warnings and contains seven top-side components, zero PCB traces and
zero vias. This does not qualify the full board or the final power-loop layout.
`POWER.md` records battery, USB, thermal and effective-capacitance decisions
that remain open. Routing stays disabled until whole-board prerequisite gates pass.

Catalogue searches also returned unrelated components for an exact capacitor
MPN and a display query. This was reported to the authorized issue chat; verified
exact-part imports continued. Search evidence is saved under
`evidence/component-search-2026-10-03/`.

## Verified B-003 resolution — A0-core-alignment

The earlier CLI-bundle diagnosis was incomplete. Native build imports the local
tscircuit RootCircuit, which loaded its nested core 0.0.2056. The supported
Bun `overrides` entry now pins all core dependencies to official **0.0.2058**.
A clean `bun install --force` removed the stale nested copy; plain `bun install`
alone had left it installed. No package source or imported component was patched.

The actual microphone build and all five native checks now exit 0. Generated
geometry has nine source ports and nine PCB ports, all four ground pad shapes
linked, and an internal connection joining those four contacts. No ambiguous
port errors remain. Evidence is in `evidence/core-alignment-2026-10-03/`.
The regulator and project checks were repeated successfully after alignment.
B-003 is resolved for native component generation; final microphone application,
paste/mask, placement, routing and full-board qualification remain pending.
The complete-board entry continues to report unfinished design explicitly.

## B-005 microphone stencil blocker

C5656610 produces nine copper pad shapes but only five rectangular solder-paste
records. Its four polygon GND shapes have no paste record. Native diagnostic
Gerber export succeeds but F_Paste contains only those five rectangular flashes
and no ground-pad regions. This is an unrouted component diagnostic, not a
handheld fabrication package. Evidence: `evidence/core-alignment-2026-10-03/`
(`microphone-stencil-defect.json`, diagnostic ZIP and `F_Paste.gbr`).
Manufacturer stencil geometry review and the upstream generator/export fix remain
required. The issue was sent to the authorized issue chat; independent design
work continues. No full-board stage, fabrication readiness or physical test is
claimed by the isolated checks.

## Current controls review — 2026-10-03

The regulator now uses TI's 511 kΩ / 91 kΩ divider. A separate unrouted A4
microphone power/clock/comparator application was built and checked, with
preserved warnings. It excludes the blocked microphone and hold switch.
B-006 blocks C79174 contact/locating-hole qualification; B-008 blocks C105188's
missing schematic reference label; B-007 records C2149796's missing supply
metadata. All were sent to the authorized issue chat. Read `AUDIO.md`, `POWER.md`
and the current VALIDATION.md milestone. Requirements, full schematic, component
qualification and mechanics remain incomplete. No handheld routing/fabrication
or hardware-test pass is claimed. Standing authorization covers publication of
this WIP milestone to both configured remotes.

## Current independent engineering

Native MCU/USB A4 review and lower-bias regulator build/five checks pass as
unrouted diagnostics. Current schemas still reject generated group fields and
PCB display offsets (B-010); USB polygon paste (B-005) and ESD/comparator
reference text (B-008) remain blocked. Both switch candidates lose permanent
contact groups (B-006). Cases are reported to the authorized fix chat; no
imported definitions or native runtime were patched. Routing is disabled.

Display supply/level translation/backlight/FPC and protected-pack qualification
continue. A battery-sourcing exception question is pending, because the studied
NTC protected pack's PCM only supports 1 A continuously. No elapsed-time
approval is inferred. Publication remains incomplete until supported native
upload acknowledgement succeeds; the heartbeat stays active.

## Display logic review and tested core proposal — 2026-10-03

`DISPLAY.md` records the partial 2.8 V LCD interface: 19 exact imported top-side
parts, native A4, 45×32 mm diagnostic placement, routing disabled. Build and
all five checks exit 0; current PCB/A4 renders inspected; native snapshots match.
Manufacturer physical pin tests pass; board tests total 12 pass, 1 fail (B-010),
75 assertions. TypeScript/formatting pass. Backlight, full power sequencing,
unknown LCD supply current, cable, enclosure and actual handheld fit are pending.

A genuine B-010 source correction was tested in a separate upstream checkout:
new strict-schema regression passes205 assertions; related tests29 pass/0 fail/
1 existing skip, core TypeScript and ESM/declaration build pass. Proposal and
reviewed native snapshots are in `evidence/core-b010-proposal-2026-10-03/`, sent
to the authorized fix chat. No installed board runtime was patched or upstream
release published. B-010 remains open until an official fix is verified natively.
C11050 land comparison is a tolerance/revision qualification question, not a
proven supplier defect (B-011). No footprint patch was applied.


The independent Type-C hardware current detector is reviewed in `TYPE-C.md`;
native A4/PCB output and required checks are preserved in
`evidence/type-c-current-review-2026-10-03/`. It keeps the proposed charger in
default USB100 until higher current is advertised and controller power is stable.
The charger, protected pack, temperature circuit and system-load gating are still
unfinished. This does not enable routing or qualify a complete board.
