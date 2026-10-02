# Issues — A0

## BLOCKING B-001: Encoder import does not match the exact ALPS mounting specification

Part: **C370970, ALPS EC11E15244G1**. Imported using pinned CLI 0.1.2228 with `--jlcpcb --use-exact-footprint --download`.

- Five terminal holes: 1.3000228 mm imported; manufacturer 1.00-1.10 mm.
- Two mounting slots: 3.200019 mm long imported; manufacturer 2.60-2.70 mm.
- Hole pattern row spacing 14.5 mm is correct (7 + 7.5 mm); no false row-spacing discrepancy is reported.
- Manufacturer 12.5 mm dimension is measured across outside slot edges, not between slot centers.

Affected gates: schematic/BOM import qualification (stage 2), placement/mechanics (stage 3), then routing, checks and fabrication (stages 4-6).

Evidence: `evidence/imports/C370970-audit.json`, original supplier JSON, `references/alps-ec11e15244g1-mounting.gif`, `references/alps-ec11e.pdf` and `evidence/datasheets/alps-ec11e-2.png`. Independent manufacturer-range tests reproduce both failures.

Required resolution: qualify a corrected official import for this exact part, or a different genuine JLCPCB encoder whose unmodified import matches its own datasheet. No local edits to the symbol, footprint, hole geometry, port mappings or model are permitted. The current encoder cannot enter a released BOM or layout.

Alternative investigation: **C209762 / EC11J1525402** imported successfully through the supported workflow. ALPS marks this exact part Not Recommended for New Designs, so it is not selected. This investigation does not resolve B-001; its footprint has not been fully qualified.

User-authorized symbol change (2026-10-02): removed C370970's custom `symbol` JSX prop. The existing native `chip` now renders a rectangular box. Exact source comparison confirms only that property was removed; pin labels, footprint and models are unchanged. Schematic-only A4 review builds successfully and preserves all seven source pins (6–12). This does **not** repair the hole/slot dimensions or resolve B-001. Audit: `evidence/imports/C370970-symbol-change.json`; preview: `evidence/encoder-chip-box-schematic.svg`.

## Candidate rejection R-001: TPS63070RNMR C109322

The original import omits physical pin identities 8 and 13 and loses pin 1's PS/SYNC functional alias. TI assigns 7/8 to VOUT and 12/13 to VIN; grouped pads are electrically equivalent but do not satisfy exact pin identity qualification. This is not evidence of a short.

The supported import of genuine TI **TPS63802DLAR C2845237** retains all ten manufacturer pin numbers/functions and is an alternative candidate. No TPS63070 dependent circuit was authored. Old TPS63070 source and failed qualification evidence are retained; it is excluded from the proposed active BOM. TPS63802 placement, passives, complete power design and model qualification remain pending. This change resolves selection dependency on TPS63070, not the board validation stage.

## Other pending items

- Display: manufacturer documentation obtained for Waveshare 1.54inch LCD Module, ST7789, 240 x 240, 3.3 V operation, 50 x 35 mm module with PH2.0 eight-pin connection. Exact JLCPCB-sourced display/connector and permitted external assembly need final qualification; no display component or footprint has been authored.
- A free-text supported-import search for `1.54 LCD` selected the unrelated **DSK110 diode C908227**. That file is preserved as evidence of the search behavior and is not a display or active BOM selection. Future imports must use verified exact part numbers.
- Supplier catalogue stock/prices are inconsistent between catalogue/search endpoints. Exact JLCPCB assembly availability/classification and costs remain unverified.
- Privacy: disconnect microphone supply mechanically and prevent phantom power through audio clock/data. Buffered interfaces with Ioff support are candidate architecture; electrical validation is pending.
- Battery: exact 500-1000 mAh cell, protection, thermistor, polarity and peak current rating remain pending.
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
