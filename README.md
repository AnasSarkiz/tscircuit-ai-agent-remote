# tscircuit AI agent remote

Revision A0-power-review, updated 2026-10-03: **unrouted regulator application review added; B-002 acoustic diameter corrected locally; B-003 remains blocked in the CLI renderer; no complete handheld schematic or PCB exists**. Not ready for routing or fabrication; untested prototype intent.

Private repository: https://github.com/AnasSarkiz/tscircuit-ai-agent-remote

Private tscircuit package: https://tscircuit.com/AnasSarkiz/tscircuit-ai-agent-remote
— corrected source published as **0.0.2-wip-c5656610-hole-060-publication-record**, with all 176
files uploaded. The next milestone is `wip-a0-power-review`, pending verification of both remote updates. This is a work-in-progress prototype source release. The build
remains blocked as described below; publication does not approve fabrication.

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

**BLOCKING B-003:** the native renderer rejects pin 3's four separated ground-pad
shapes as an ambiguous port, leaving those shapes with null PCB-port links.
The component build still exits 1, even with the documented `MIC1.pin3` selector.
No geometry, pin mapping or check was changed to hide this failure. This does
not indicate a diagnosed short, and B-002's hole correction remains verified.

## Historical corrected encoder import

**ALPS EC11E15244G1 / LCSC C370970:** the user explicitly authorized correcting this imported component's symbol and footprint. Its five terminal holes are now **1.05 mm**, and its two mounting slots are **2.65 mm long**, within ALPS's 1.00–1.10 mm and 2.60–2.70 mm ranges. **B-001 is resolved locally for the reported dimensions.** The external supplier library has not been changed.

C370970 uses its existing native `<chip>` as a schematic box. Pin labels, centers, slot widths/orientation, outer pads, silkscreen, courtyard and models are unchanged. This encoder is no longer part of the accepted one-button design; its correction and evidence are retained historically. The microphone now also has a diameter-only authorized correction. Other imports remain unmodified. Isolated review artifacts are not the handheld board or fabrication package. No handheld placement, routes or fabrication outputs exist.

## Commands

Run inside this directory. `bun install` installs pinned dependencies. `bun run format:check` and `bun run typecheck` check project tooling. `bun test` passes all five import checks, including the C5656610 acoustic-opening check; historical encoder checks remain as evidence, not active BOM approval. `bun run build` reports that the complete board has not been authored. The original proposal is preserved in `evidence/proposals/C5656610-acoustic-hole.diff`. The latest user instruction authorized applying it locally. B-003 still prevents a clean microphone build and dependent board work.

## Evidence and remaining work

See `VALIDATION.md`, `BOM.md`, `issues.md`, `references/sources.md` and `routes/README.md`. Continue in this task directory. No earlier board source or validation evidence was reused.

Import provenance: **JLCEDA/EasyEDA Official Library**, accessed through the supported JLCPCB importer. [JLCEDA](https://lceda.cn/) / [EasyEDA](https://easyeda.com/).

## A0 regulator review and current fix status

Current pins: tscircuit **0.0.2742**, CLI **0.1.2235**, direct core **0.0.2058**.
Core PR [4323](https://github.com/tscircuit/core/pull/4323) merged and is present
in the published core release. The CLI still bundles the earlier renderer:
the real microphone fixture still exits 1, produces five PCB ports instead of
six, and leaves four GND pad shapes unlinked. Adding the fixed core dependency
does not resolve the native CLI failure. See `evidence/core-fix-2026-10-03/`.

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
