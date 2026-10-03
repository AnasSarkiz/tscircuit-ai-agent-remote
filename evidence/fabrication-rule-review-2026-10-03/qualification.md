# Four-layer fabrication rule study — untested prototype

Reviewed 2026-10-03 against JLCPCB's current capabilities, official stack-up table and interactive impedance calculator. These are proposed routing and ordering requirements; they are not evidence that the incomplete full board has compliant copper. Routing remains disabled until connectivity, BOM and placement gates pass.

Sources:
- https://jlcpcb.com/capabilities/Capab
- https://jlcpcb.com/impedance
- https://jlcpcb.com/pcb-impedance-calculator
- https://jlcpcb.com/help/article/user-guide-to-the-jlcpcb-impedance-calculator

## Candidate stack and USB pair

Four-layer rigid FR-4, nominal order thickness 1.6 mm, outer copper 1 oz, inner copper 0.5 oz, standard JLC04161H-7628. The calculator displays a finished stack thickness of 1.59 mm ±10%; the generic 1.6 mm capability range is 1.44–1.76 mm. Final mechanical allowances and order documents must distinguish those values and match the accepted manufacturer's stack.

From top to bottom: L1 outer copper 0.035 mm; 7628 RC49% prepreg 0.2104 mm; L2 copper 0.0152 mm; dielectric core 1.065 mm; L3 copper 0.0152 mm; prepreg 0.2104 mm; L4 copper 0.035 mm. Proposed allocation: top component/signals, L2 continuous ground reference, L3 power/ground as reviewed, bottom signals. RF antenna keepouts apply to every copper layer and nearby enclosure objects.

For the 90-ohm USB differential pair on L1 referenced to L2, non-coplanar, requested spacing 0.200 mm, the verified calculator result is width 0.2906 mm and spacing 0.1999 mm. Save exact result in impedance-calculator-result.json and calculator-accessibility.txt. calculator.jpg records the selected inputs and stack tab; the numerical result is below its viewport. The unused default 50-ohm single-ended row is not a board routing requirement. Calculator fit tolerance 0.5% is separate from the published physical impedance tolerance ±10%.

Final copper must use this geometry or a fresh manufacturer-backed calculation for the actual order stack. Neck-downs at USB/ESD/MCU pads, return-plane discontinuities, pair skew, stubs and any vias require review; the calculator alone does not qualify signal integrity. The routing API's support and generated geometry still need verification.

## Proposed nominal design rules

| Feature | Proposed ordinary routing rule | Current manufacturer basis / outstanding condition |
| --- | --- | --- |
| General signal track width | 0.20 mm | Multilayer 1 oz minimum 0.09 mm; current-carrying widths are separately calculated, not derived from this minimum. |
| Different-net general copper clearance | 0.20 mm | Track minimum 0.09 mm; SMT pad-to-pad minimum 0.15 mm. Fixed imported fine-pitch geometry must be measured individually. |
| Through via | 0.30 mm hole / 0.70 mm copper diameter | Nominal ring 0.20 mm, matching recommended multilayer 1 oz annular ring; absolute minimum 0.15 mm. Ordinary full-through layer span only. No implicit via-in-pad. |
| Via hole to unrelated track/inner copper | At least 0.20 mm | Measured from the hole edge. Same-net drill-to-pad checks remain necessary. |
| Ordinary PTH hole to unrelated track | 0.35 mm | Manufacturer recommendation 0.35 mm, minimum 0.28 mm; inner PTH hole-to-copper minimum 0.30 mm. |
| Ordinary NPTH to copper | At least 0.20 mm | Acoustic sealing structures need explicit process review; keepout configuration alone does not prove exported geometry. |
| Routed edge / slot to copper | 0.30 mm target | Published nominal minimum 0.20 mm. Regular routed outline tolerance ±0.20 mm; final mechanical tolerances require separate assessment. |
| General NPTH minimum | 0.50 mm | Generic through-hole diameter tolerance +0.13/−0.08 mm and hole-position tolerance ±0.075 mm. Confirm their applicability to intentional acoustic NPTHs. |
| Non-plated slots | Width at least 1.0 mm, rounded corners | Width tolerance ±0.20 mm; no rectangular corner assumption. No slot is introduced in this study. |
| Silkscreen | Stroke at least 0.15 mm, height at least 1.0 mm, pad separation at least 0.15 mm | Final generated legend must be measured, with readability inspected. |
| Mask | Green candidate; 1:1 opening candidate | Published minimum green mask bridge 0.10 mm; black/white 0.13 mm. Mask opening to neighboring track at least 0.09 mm. Inspect actual exports and imported pad openings. |

No minimum-width exception, DRC suppression or imported-footprint change is introduced. Track-width manufacturing tolerance is ±20%; power-path design must account for actual narrow sections, copper thickness, temperature and intended current. The 0.70 mm ordinary via is not assumed to qualify for the soldermask-filled opaque via process, whose published maximum diameter is 0.50 mm. Tenting, plugging and filled/capped via-in-pad are different processes; final mask/process selection remains open.

Assembly tooling/panelization is not yet selected. If an SMT panel is required, JLCPCB specifies 5 mm handling rails, 2 mm tooling holes and 1 mm fiducials centered 3.85 mm from panel edges. These are panel features, not permission to enlarge the product PCB beyond the approved maximum 50 ×65 mm. Precision routed outline ±0.10 mm requires additional conditions (minimum 50×50 mm and at least three 1.5 mm tooling holes); this study does not assume that option.

## Measured microphone acoustic hole

measure-microphone-hole.py reads the untouched native C5656610 fixture JSON and records its SHA256. The authorized hole correction remains 0.60 mm at its original center. Minimum nominal drill-edge to imported pad boundary is 0.2580203 mm; all nine pad shapes were measured, including the four quarter-ring ground polygons. This measures the input native geometry, not exported full-board copper.

Under the generic published diameter tolerance, 0.60 mm yields 0.52–0.73 mm, with the minimum above TDK's 0.50 mm recommendation. A conditional maximum diameter/position sweep yields 0.1180203 mm residual pad clearance. That sweep is not reported as a fabrication or DRC failure: published nominal rules can already budget process tolerances, and their applicability to the intentional acoustic NPTH must be confirmed. Do not double-count tolerances or enlarge the hole again on that basis.

The manufacturer also describes NPTH pad annular-ring allowances for a sealing-film process that can remove copper. That generic process must not be applied blindly to the microphone's acoustic ground/seal geometry. Acoustic seal, paste generation (existing B-005) and assembler acceptance remain unresolved. No imported land, paste or ring is manually changed.

## Validation status

Independent read-only geometry measurement ran successfully; calculator inputs, selected stack and exact numerical result were inspected and saved. No full-board routing, shorts, current/thermal validation, exported Gerber/drill inspection, assembler acceptance, order or physical test is claimed. Stages 3–6 remain gated by outstanding component/tool/design qualification.

Additional nominal land measurement: measure-rect-pad-clearances.py reads the preserved MCU/USB, Type-C, display and new alternate-switch native fixtures. It uses actual source-port connectivity keys to exclude same-net pairs, reports unknown-connectivity exclusions, and measures only axis-aligned rectangular lands within each component. Across 51 component instances with measurable different-net pairs, minimum clearance is 0.1976628 mm; no measured pair is below the manufacturer's 0.15 mm different-net SMT-pad requirement. Non-rectangular lands, plated-hole annuli, mask/paste, inter-component placement and full routed copper are explicitly outside this measurement; they are not inferred to pass. The minimum is slightly below the proposed ordinary trace clearance of 0.20 mm, which is distinct from the 0.15 mm fixed SMT-pad requirement. Exact native input hashes and closest pairs are in rect-pad-clearances.json.

Official release watch at 04:20 UTC found core 0.0.2064. Exact published-head comparison from 0.0.2063 changes only the capacity-autorouter dependency to ^0.0.954 and package version. It does not fix native B-010 schema failures. No dependency update or library patch is applied to the board on that basis; watch and comparison records are saved.

Read-only official open-PR review found core PR4283 concerning asynchronous USB-C footprint loading with a custom schematic pin arrangement. Its description still says repro-only, while its current diff includes a late PCB-match dirty-phase fix. No unmerged dependency or copied patch is applied. The board's preserved explicit-import MCU/USB fixture has 101 source ports and 101 PCB ports, with no missing source-to-PCB association or nonnumeric PCB coordinates. That scoped result does not prove asynchronous part-loading or future copper routing. Original native SHA256 and PR evidence are saved separately; full routing remains gated.
