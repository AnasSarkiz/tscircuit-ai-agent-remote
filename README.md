# tscircuit AI agent remote

Revision A0: initialized engineering project, **blocked before a complete schematic or PCB exists**. Not ready for routing or fabrication; untested prototype intent.

Private repository: https://github.com/AnasSarkiz/tscircuit-ai-agent-remote

The requested device is a cloud AI client: press TALK, speak, send a Wi-Fi request, display the response, then physically APPROVE or REJECT. Firmware implementation is outside this task.

The user approved a PCB envelope of up to **50 x 65 mm** on 2026-10-02. Final dimensions, mounting arrangement and enclosure geometry are not yet validated. Four copper layers are intended.

## Blocking component import

**ALPS EC11E15244G1 / LCSC C370970:** supported JLCPCB import produced five 1.3000228 mm terminal holes and two 3.200019 mm mounting slots. The exact ALPS drawing specifies terminal holes of 1.00-1.10 mm and slot lengths of 2.60-2.70 mm. Per the workspace instructions, imported component definitions cannot be patched and dependent work must stop.

Imported footprints and models remain intact. At the user's explicit request, C370970's custom schematic symbol was removed so its existing native `<chip>` renders as a box. Its pin labels and PCB geometry are unchanged. An isolated A4 schematic-only review is saved as `evidence/encoder-chip-box-schematic.svg`; it is not the board schematic or placement. Measurements, supplier records, manufacturer drawings and failing qualification checks remain in `evidence/` and `references/`. `main.tsx` remains an explicit blocking scaffold, re-exported by `index.circuit.tsx`. There are no board placement renders, routes or fabrication outputs.

## Commands

Run inside this directory. `bun install` installs the pinned dependencies. `bun run format:check` and `bun run typecheck` check the project tooling. `bun test` runs manufacturer import qualification and currently fails two encoder geometry checks. `bun run build` currently reports the explicit encoder blocker. No successful toolchain check implies PCB validation.

## Evidence and remaining work

See `VALIDATION.md`, `BOM.md`, `issues.md`, `references/sources.md` and `routes/README.md`. Continue in this task directory. No earlier board source or validation evidence was reused.

Import provenance: **JLCEDA/EasyEDA Official Library**, accessed through the supported JLCPCB importer. [JLCEDA](https://lceda.cn/) / [EasyEDA](https://easyeda.com/).
