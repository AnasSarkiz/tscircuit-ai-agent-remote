# B-015 — native BOM Comment metadata loss

Confirmed 2026-10-03 in the official latest circuit-json-to-bom-csv@0.0.19 (gitHead6d67954bc069ebe3b6547a305e10e0d9c7296f79), installed only in this isolated characterization runtime. Board dependencies and imported definitions remain unchanged. Installed CLI@0.1.2235 bundles the same public converter behavior and calls convertCircuitJsonToBomRows({ circuitJson }) from its Gerber ZIP export, without resolvePart.

Actual unchanged native fixtures carry manufacturer_part_number, including U1 ESP32-S3-WROOM-1-N8R8/C2913201, J1 TYPE-C-31-M-12/C165948, U25 TPS3808G33DBVR/C43698 and SW4 SKSWCFE010/C255576. Official conversion emits empty Comment for these parts while preserving exact JLCPCB Part #. Across MCU/USB, battery supervisor and hold candidate fixtures, blank Comment counts are5,1,1 respectively. No exact supplier part number was lost or changed, and no actual assembler misidentification is claimed.

A second public API call provides resolvePart returning the actual native manufacturer_part_number as its documented comment field. The converter still emits empty Comment for U1/U25/SW4. Its source uses only part_info.manufacturer_mpn_pairs for Comment and never reads part_info.comment or source_component.manufacturer_part_number for that column. This reproduces metadata loss without custom components, filtering native JSON, changing schemas or monkey-patching the converter.

Footprint columns also fall back to supplier codes for all16/5/2 fixture rows. Accurate package information for final assembly still requires a separate data-flow review; this is recorded as a qualification concern, not assumed to have the same root cause as Comment loss.

JLCPCB's current BOM guide (updated2026-09-09) requires Comment, Designator and Footprint data. The metadata loss blocks approval of the native fabrication BOM in stage6 once earlier whole-board gates are satisfied; it does not imply that the incomplete board has reached stage6. The standalone CSV is named NOT-FOR-FABRICATION-bom-characterization.csv and is a converter reproduction only. No Gerbers, actual fabrication package, routing, ready/order claim or physical test was produced. The untouched native input's separate B-010 schema failures remain recorded; this converter probe does not resolve or waive them.

Sources and evidence:
- https://jlcpcb.com/help/article/bill-of-materials-for-pcb-assembly
- https://jlcpcb.com/help/article/advice-for-bom-and-cpl-files-preparation
- https://github.com/tscircuit/circuit-json-to-bom-csv
- Installed CLI source lib/shared/export-snippet.ts and bundled converter: node_modules/@tscircuit/cli/dist/cli/main.js around349167 and354224.
- runtime/characterize.mjs, official exact-version package manifest/bun.lock, install.log, native-bom-characterization.json and input SHA256s.

No board output or converter was manually repaired. Reported to the user-authorized fix chat; continue independent qualified work while awaiting the official correction.
