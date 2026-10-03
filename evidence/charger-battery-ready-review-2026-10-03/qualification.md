# Battery-readiness application review — unrouted candidate

This five-part independent circuit studies one hardware input to the main buck-enable pin. It does not integrate the charger, qualify a battery pack, prove battery presence, or complete any full-board validation gate. No MCU override, authored battery substitute, or patched component definition is present.

## Manufacturer connections and supplier identity

U25 is genuinely imported TPS3808G33DBVR, JLCPCB C43698, not the distinct -TP part returned in the same search. Supplier search on 2026-10-03 reports 6,139 pieces; final assembly availability must be checked again. Its imported source and models remain unchanged. TI Rev N (August 2026), page 4, identifies physical pins 1 RESET, 2 GND, 3 MR, 4 CT, 5 SENSE and 6 VDD. That page was rendered and inspected. The supplier footprint is rotated 180 degrees from the datasheet top-view illustration; physical pin identities, pin-1 mark, and imported model rotation agree.

Pin 6 and MR pin 3 connect to charger OUT (VSYS). SENSE pin 5 connects to the actual charger BAT terminal (PACK_BAT), not VSYS or a fictional battery. Pin 2 connects to GND; CT pin 4 remains open for the fixed nominal 20 ms delay (12–28 ms specified). RESET pin 1 controls only BUCK_ENABLE in this fixture.

R96 and R97 are existing genuine YAGEO RC0603FR-07470KL, C114622, 470 kohm, forming a pullup to VSYS and a pulldown to GND. C76 and C77 are existing genuine Murata GRM188R71C104KA01D, C45000, 100 nF; C76 bypasses VSYS, C77 shunts BUCK_ENABLE. The complete converter and its EN pin are not included here. These are application-review allocations, not a final board BOM.

## Static checks and limitations

TI explicitly states RESET is asserted and low impedance above POR but below its minimum operating supply, irrespective of SENSE (section 7.4.2). The POR maximum of 0.8 V is specified with RESET voltage at most 0.2 V, 15 uA reset load, and supply rise of at least 15 us/V. Below POR, RESET is undefined. The normal supply range is 1.7–6.5 V; do not treat the below-POR region as guaranteed behavior.

The exact YAGEO specification gives 1% initial tolerance and +/-100 ppm/C. From 25 C across -40..125 C, conservative addition gives +/-2%. Using independent resistor corners and a conditional combined 0.5 uA sink (TPS63802 EN 0.2 uA plus TPS3808 RESET 300 nA), the divider requires VSYS at least 2.688680 V for EN >=1.2 V. At VSYS 2.8 V the lowest calculated EN is 1.254547 V. The RESET leakage limit is specified at 6.5 V, so this calculation is conditional, not a universal guarantee at every supply. Aging and soldering shifts are not included.

At 4.5 V VSYS, worst-case pullup current into a zero-volt reset output is 9.7699 uA. This steady current is below the POR test load. Capacitor discharge current and fast reconnects are not bounded by that steady result. C77 nominal rise time constant is 23.5 ms; effective capacitance, load history and arbitrary supply ramps remain unqualified. The supervisor switching table uses 50 pF reset load, unlike this 100 nF shunt, and the 20 us assertion delay is typical rather than a maximum. No shutdown-time bound is claimed.

G33 falling trip is 3.02395–3.11605 V over -40..125 C. Maximum stated hysteresis adds up to 2.5% of VIT; final restart/cutoff policy must be selected against the actual pack. The unselected EEMB example pack can disconnect at up to 3.10 V, so this G33 candidate does not guarantee converter shutdown before its protection trips. The BQ24074 BAT-to-OUT 100 mV maximum is specified at 1 A, VIN=0 and BAT>3 V; extrapolation to the provisional larger combined load is prohibited.

BQ24074 BAT voltage alone cannot establish battery presence: its battery-detection routine discharges BAT and then applies precharge while testing an absent pack or open protector (section 9.3.5.4). A capacitor can temporarily meet the voltage threshold with no usable battery. Exact protected pack, harness polarity, NTC curve and tolerances, discharge rating, charging current/timer/window, absence/recovery policy, all raw-VSYS load isolation and dynamic behavior remain open. No fixed resistor substitutes for a thermistor; no timer or protection is disabled to hide a failure.

## Executed checks and visual review

Native CLI 0.1.2235, core 0.0.2058, tscircuit 0.0.2742 and Circuit JSON 0.0.510 remain pinned. Native build and netlist, pin_specification, source, schematic-placement and placement all exited 0. Original outputs are retained. Five top components, 14 SMT pads and 14 paste elements are emitted; zero PCB traces, vias or error elements. PCB PNG and native schematic PDF were inspected. The one-page PDF is landscape A4, 841.89 x 595.28 points; all five components and labels fit within its boundary. This deliberately spacious review fixture is not full-board placement. Native snapshot command exited 0 and its SVG outputs were reviewed against the rendered fixture.

TypeScript check exited 0 including the new boundary test. The canonical suite reports 22 pass, one existing fail, 213 assertions. The new nine-assertion manufacturer/hardware-boundary test passes. The full emitted JSON still has seven strict-schema failing elements (schematic_group, five pcb_component and pcb_group), reproducing B-010. The unchanged original JSON and audit script are preserved; no schema, runtime or check is weakened. Formatting follows the existing configuration, which excludes imported sources and evidence artifacts.

New exact 330 kohm, speaker and battery searches returned unrelated catalog parts (B-004); those results are saved and never selected. No new purchased-part placeholder was authored.

## Sources

- TI TPS3808 Rev N, August 2026: https://www.ti.com/lit/ds/symlink/tps3808.pdf — pages 3–7, 13; saved unchanged as tps3808.pdf.
- TI BQ24074 family Rev N: https://www.ti.com/lit/ds/symlink/bq24074.pdf — electrical conditions and section 9.3.5.4; previously saved at evidence/audio-charge-review-2026-10-03/bq24074.pdf.
- TI TPS63802 Rev D: https://www.ti.com/lit/ds/symlink/tps63802.pdf — logic/enable table and absolute limits; existing references/tps63802.pdf.
- YAGEO exact RC0603FR-07470KL: https://yageogroup.com/component-documentation/download/specsheet/RC0603FR-07470KL — saved unchanged; 1%, +/-100 ppm/C.

These findings keep stages 1–2 incomplete/blocked. No copper, shorts pass, fabrication release, physical test, or complete published revision is claimed.

## Prior source publication receipt

Git 435493d1574c19dfb2e732ed359cda79e4d1205d reached GitHub main. The supported native publisher exited 1 after 834 reported successes and nine failures. The command supplied a full version as `--version-tag`; the CLI prefixes the package version, so the actual registry release is **0.0.2-0.0.2-wip-a0-mic-clock-review**, not the originally recorded 0.0.2-wip-a0-mic-clock-review. Registry latest_version established that identity. The initial readback used the wrong release name and returned all404; it is preserved under `misidentified-version-initial-*` and must not be used as proof that those files are absent from the actual release. The corrected script and receipt use the actual registry name. Subsequent commands will pass only the suffix to --version-tag. Corrected readback proves all three timeout files have exact hashes, while all six HTTP413 files return404. Package private=true and ready_to_build=false. Publication remains incomplete. No privacy or ready flag is changed.

Git whitespace review flags native schematic SVG blank-space output, the unchanged manufacturer YAGEO PDF, and the imported TPS3808 STEP file (Git treats their CR line endings as trailing whitespace). These are preserved artifacts, not board DRC exceptions; no manufacturer/native output was rewritten to silence the findings. Authored-source formatting passes.
