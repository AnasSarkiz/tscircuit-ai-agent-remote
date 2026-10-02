# tscircuit AI agent remote

Revision A0: engineering project **in progress; no complete schematic or PCB exists**. Not ready for board routing or fabrication; untested prototype intent.

Private repository: https://github.com/AnasSarkiz/tscircuit-ai-agent-remote

The requested device is a cloud AI client: press TALK, speak, send a Wi-Fi request, display the response, then physically APPROVE or REJECT. Firmware implementation is outside this task.

The user approved a PCB envelope of up to **50 x 65 mm** on 2026-10-02. Final dimensions, mounting arrangement and enclosure geometry are not yet validated. Four copper layers are intended.

## Corrected encoder import

**ALPS EC11E15244G1 / LCSC C370970:** the user explicitly authorized correcting this imported component's symbol and footprint. Its five terminal holes are now **1.05 mm**, and its two mounting slots are **2.65 mm long**, within ALPS's 1.00–1.10 mm and 2.60–2.70 mm ranges. **B-001 is resolved locally for the reported dimensions.** The external supplier library has not been changed.

C370970 uses its existing native `<chip>` as a schematic box. Pin labels, centers, slot widths/orientation, outer pads, silkscreen, courtyard and models are unchanged. Other imports remain unmodified. Isolated component schematic/PCB review artifacts and before/after audits are saved under `evidence/`; these are not the handheld board or fabrication package. Historical failed-import evidence remains in Git and `evidence/imports/`. The board entry point reports the remaining incomplete design. No handheld board placement, routes or fabrication outputs exist.

## Commands

Run inside this directory. `bun install` installs pinned dependencies. `bun run format:check` and `bun run typecheck` check project tooling. `bun test` passes all four existing import-qualification tests. `bun run build` still reports that the complete board has not been authored. Component-only success does not establish board validation or fabrication readiness.

## Evidence and remaining work

See `VALIDATION.md`, `BOM.md`, `issues.md`, `references/sources.md` and `routes/README.md`. Continue in this task directory. No earlier board source or validation evidence was reused.

Import provenance: **JLCEDA/EasyEDA Official Library**, accessed through the supported JLCPCB importer. [JLCEDA](https://lceda.cn/) / [EasyEDA](https://easyeda.com/).
