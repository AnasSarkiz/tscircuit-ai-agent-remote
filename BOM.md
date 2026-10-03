# Candidate BOM — A0

**Not an assembly/fabrication BOM.** Import success alone does not qualify a part. Regulator review references are provisional; final designators require the complete schematic.

| Function | MPN | LCSC | Package | Intended qty | Status |
|---|---|---|---|---|---|
| MCU/Wi-Fi | ESP32-S3-WROOM-1-N8R8 | C2913201 | Antenna module | 1 | Imported; complete review pending |
| Charger/power path | BQ24074RGTR | C54313 | QFN-16 + EP | 1 | Imported; battery/current/thermal design pending |
| 3.3 V buck-boost | TPS63802DLAR | C2845237 | DLA-10 2 × 3 mm | 1 | Imported; pin identities pass; application review pending |
| Digital microphones | ICS-43434 | C5656610 | LGA-6 bottom port | 2 | B-002 locally corrected to 0.60 mm with user authorization; B-003 resolved on aligned official core 0.0.2058; B-005 ground paste missing; lifecycle/full qualification pending |
| I2S speaker amplifier | MAX98357AETE+T | C910544 | TQFN-16 + EP | 1 | Imported; full application review pending |
| USB-C receptacle | TYPE-C-31-M-12 | C165948 | USB2.0 hybrid mount | 1 | Imported; orientation/protection/mechanics pending |
| Battery connector candidate | S2B-PH-SM4-TB(LF)(SN) | C295747 | SMT right-angle, 2 mm pitch | 1 | Imported verbatim with CLI 0.1.2232; top-side assembly candidate; drawing/polarity/full qualification pending |
| Microphone clock buffer candidate | SN74LVC2G125DCUR | C21404 | VSSOP-8 | 1 | Imported; architecture/ratings pending |
| Microphone SD receiver candidate | TLV3201AIDBVR | C105188 | SOT-23-5 | 1 | Imported; comparator application review; B-008 missing reference label; final timing/rail review pending |

| Regulator inductor | DFE201612E-R47M=P2 | C668312 | 0806, 470 nH | 1 | Imported verbatim; TI recommended series; footprint/current qualification pending |
| Regulator input capacitor | GRM188R61A106ME69D | C90053 | 0603, 10 µF, 10 V, X5R | 1 | C4 review; effective capacitance and footprint qualification pending |
| Regulator output capacitor | GRM188R61A226ME15D | C84419 | 0603, 22 µF, 10 V, X5R | 1 | C5 review; effective capacitance and footprint qualification pending |
| Regulator high feedback | RC0603FR-0751K1L | C364359 | 0603, 51.1 kΩ, 1% | 1 | R5 lower-bias-error divider; provisional static corners recorded |
| Regulator low feedback | RC0603FR-079K1L | C114639 | 0603, 9.1 kΩ, 1% | 1 | R6 lower-bias-error divider; provisional maximum 9.2456 kΩ |
| PG pullup / control candidate | RC0603FR-07100KL | C14675 | 0603, 100 kΩ, 1% | TBD | R7 and isolation-review applications; final allocation pending |
| Charger current candidate | RC0603FR-073KL | C126358 | 0603, 3 kΩ, 1% | TBD | Imported only; 296.7 mA nominal candidate, pack selection pending |
| Bypass capacitor candidate | GRM188R71C104KA01D | C45000 | 0603, 100 nF, 16 V, X7R | TBD | Imported only; application allocation pending |

## Rejected or unselected imports

| Part | LCSC | Reason |
|---|---|---|
| TPS63070RNMR | C109322 | Missing separate physical identities 8/13 and PS/SYNC alias; alternate TPS63802 under review |
| EC11J1525402 | C209762 | Alternative investigation only; ALPS Not Recommended for New Designs; unselected/unqualified |
| EC11E15244G1 | C370970 | Historical locally corrected encoder; removed from active design by accepted single-button concept |
| DSK110 | C908227 | Unrelated diode returned by display search; not active BOM |

All definitions/models originated through the supported JLCPCB importer. The user explicitly authorized C370970's native chip-box symbol and footprint correction: five holes to 1.05 mm and two slot lengths to 2.65 mm. Pin labels, supplier identity, all centers, other geometry and models remain unchanged. This is a local correction, not a corrected official supplier library. The user also authorized C5656610's acoustic hole diameter correction to 0.60 mm; all other microphone bytes and its center remain unchanged. Other imports remain unmodified. Rejected imports are retained as evidence.

## Required parts still unselected

Screen-dominant display/module and connector; exact protected 1S 3.7 V, 4.2 V-charge LiPo pack (500–1000 mAh target), protection/thermistor/harness; speaker and speaker connector; haptic connector/MOSFET/flyback protection; single top-edge hold-to-talk control and compatible hardware microphone isolation; internal BOOT/RESET service access; remaining charger/audio/logic passives; USB CC resistors, ESD/current protection and decoupling; programming/test connectors. No placeholders represent these parts. Separate encoder, APPROVE/REJECT buttons, privacy slider, exterior power control and front RGB LED are not part of the accepted concept.

The rechargeable pack and battery circuit are not yet integrated. C295747 is a real imported connector candidate, not a qualified battery pack. All electronic parts and connector solder joints must use top-side assembly; bottom-side population is prohibited by the accepted requirements. Exact current and thermal budgets remain pending.

Waveshare 1.54 inch LCD Module was researched, not selected as an imported component. PH2.0 J2 order is **BL/RST/DC/CS/SCK/DIN/GND/VCC**, opposite schematic J1 ordering. Contact orientation requires independent verification.

Catalogue identities/manufacturer sources checked on 2026-10-02 and 2026-10-03; see `references/sources.md`. Final JLCPCB assembly allocation, basic/extended classification, external procurement, costs and exact availability remain unverified. Do not order from this document.

## A0-controls-review milestone — 2026-10-03

All new imports use the supported exact-footprint/download workflow and remain
unmodified. `evidence/controls-review-2026-10-03/import-source-manifest.json`
records their source checksums. The single hold switch EVQPUC02K / **C79174**
is blocked by B-006 (lost 1↔3 / 2↔4 internal contact pairs, locating holes
0.9000236 mm instead of Panasonic's maximum 0.85 mm). Do not integrate it.

Independent microphone isolation application candidates:

| Function | Exact MPN | LCSC | Application status |
|---|---|---|---|
| VMIC switch | TPS22919DCKR | C2149796 | B-007 supply metadata warning visible; actual pin 1 wiring verified against TI |
| VMIC startup supervisor | TPS3839K33DBZR | C96333 | VMIC threshold and delay review; final rail/leakage/timing pending |
| Supervisor inversion | SN74LVC1G14DBVR | C7835 | Review fixture only |
| Hold-state isolation | SN74LVC1G17DBVR | C7836 | Review fixture; no MCU-to-button control path |
| SD comparator | TLV3201AIDBVR | C105188 | VMIC/2 reference; B-008 label defect; not qualified for integration |
| Control/reference resistor | RC0603FR-0710KL | C98220 | 10 kΩ, 1%; candidate allocations |
| GPIO isolation / VMIC bleed | RC0603FR-071KL | C22548 | 1 kΩ, 1%; candidate allocations |
| Contact current limit candidate | RC0603FR-07100RL | C105588 | 100 Ω, 1%; unused until switch qualifies |

The isolated review excludes the blocked button and microphone. Every populated
PCB component is top-side; fixture dimensions are not the handheld envelope.
Native generation/connectivity/placement pass with the documented metadata and
symbol warnings. It is not a tested privacy circuit or a complete schematic.
See `AUDIO.md`. C23654 / SN74LVC1G125DBVR and newly imported C100024 /
SN74LV1T34DBVR are rejected as microphone SD receivers: their input low thresholds
do not cover the microphone's guaranteed VOL. No imported definitions were changed.

Previous 8bbde6e core-alignment publication was verified on GitHub and private
release 0.0.2-wip-a0-core-alignment (274 files); receipt is saved with this milestone.

## MCU/USB and display foundation — 2026-10-03

| Function | Exact MPN | LCSC | Status |
|---|---|---|---|
| USB ESD | TPD2EUSB30ADRTR | C94934 | Native pin/placement study passes; B-008 missing reference label |
| USB series resistors | RC0603FR-0722RL | C107701 | Two 22 Ω; manufacturer application connection reviewed |
| USB CC pulldowns | RC0603FR-075K1L | C105580 | Two 5.1 kΩ; sink only; do not imply current entitlement |
| Reset service current limiter | RC0603FR-074K7L | C99782 | 4.7 kΩ with push-pull supervisor; application limits pending |
| MCU reset supervisor | TPS3839G33DBZR | C485802 | 3.08 V nominal threshold; current rail corners/delay review |
| Service connector | SM06B-SRSS-TB(LF)(SN) | C160405 | 6 contacts, two anchors; VREF is sense only; harness/mechanics pending |
| Enclosure LCD | HS17QS178RX | C5329581 | Bare 1.77 inch; 2.8 V logic/40 mA backlight; external mounting/FPC pending |
| LCD supply candidate | TPS7A2028PDBVR | C2869847 | 2.8 V ±1.5% at VIN≥3.1 V; partial logic application reviewed |
| LCD logic buffer candidate | SN74LVC245APWR | C7848 | 2.8 V, tolerant MCU inputs; partial logic application reviewed |
| Hardware clock switch candidate | TS5A23157DGSR | C11133 | Dual SPDT, off-state clocks grounded; privacy application not yet authored |

All supported imports remain unchanged. Historical 511 kΩ/91 kΩ feedback parts
remain evidence, unselected in the current regulator application. C2863639
TLV75728PDBVR is unselected: its accuracy conditions require 3.3 V input for a
2.8 V output, above the provisional main-rail minimum. Current MCU fixture
contains 16 top-side parts and is diagnostic, not the final handheld size/BOM.
USB-C C165948 also has B-005 polygon paste omissions. Exact complete display,
battery, switch, speaker and haptic qualification remains unfinished.

C110293 / ALPS SKRTLAE010 alternative is also blocked: manufacturer circuit
diagram permanently joins pins 1↔3; untouched import/native generation has no
internal group. Native schematic exposes only 1/2 while footprint has 1–5.
The two Ø0.9000236 mm locating holes DO match ALPS's Ø0.9 recommendation; no
ALPS hole defect is alleged. Current official dimension/land/circuit GIFs were
visually inspected. This extends B-006 contact-import scope, not a permitted
component patch. Evidence: MCU/USB review switch-discrepancy.json and native
switch JSON/PNG/SVG. Do not integrate this unqualified alternate.

Display logic application now contains 19 actual top-side PCB parts. J7 is
AFC07-S10FCC-00 / C11050 (10-contact 0.5 mm FPC), not an invented connector.
Its nominal land differences lie at the drawing tolerance boundary; revision
and actual mating fit remain pending. R40/R47–51 use C14675 100 kΩ; R41 uses
C22548 1 kΩ; R42–46 use C98220 10 kΩ. C40=C90053 10 µF, C41=C84419 22 µF,
C42/C43=C45000 100 nF. The bleed/pulldown choices and manufacturer pin review are
in DISPLAY.md. C165143 TPS61160 is imported but unselected/unwired pending
backlight topology and low-Vf/off-state review. No complete-board BOM is claimed.


## A0 amplifier and charge-intake milestone — 2026-10-03

| Candidate | MPN | Exact JLCPCB/LCSC | Status |
|---|---|---|---|
| Amplifier enable NMOS | AO3400A | C20917 | Native imported; manufacturer pins1G/2S/3D; B-008 reference text missing |
| Amplifier enable PMOS | AO3401A | C15127 | Native imported; manufacturer pins1G/2S/3D; B-008 reference text missing |
| Three-wire battery/NTC connector | S3B-PH-SM4-TB(LF)(SN) | C265101 | Native imported; candidate, pack/contact polarity/ratings still pending |
| Type-C UFP hardware current detector | TUSB320LAIRWBR | C132554 | Native imported; startup/supply/current policy review pending |
| Dedicated controller3.3V LDO | TPS7A2033PDBVR | C2862740 | Native imported; not yet wired/qualified |
| Alternate top-edge hold switch | EVQ-P4HB3B | C6617702 | Native imported; manufacturer cutout/ground-contact geometry pending |

C295747 remains the amplifier's real two-wire differential speaker connector
candidate. C105588 / RC0603FR-07100RL supplies the100Ω amplifier gate/enable
series resistors; C22548 1kΩ, C98220 10kΩ and C107701 22Ω are exact prior
imports. Quantity/allocation remains provisional until the complete board exists.

No importable speaker was found for C3311258 (PUI), C6230316 (Taoglas),
C50387211 (XHXDZ); B-012 blocks them. Exact-MPN queries incorrectly selected
C16195750 / CIGT201610EHR47MNE and C326810 / RC2010JK-07510KL; both
are rejected/unwired evidence of B-004, not BOM substitutions. All definitions
remain untouched. Source checksums in the audio/charge milestone manifest.

Exact queries were resolved with supplier-verified C114622 / RC0603FR-07470KL
and C482869 / RC0603FR-07430KL; both imported successfully, remain unwired
charging candidates. C7666 / TI SN74LVC1G08DBVR also imported for startup
qualification logic. No wrong search result was used in the circuit.


### Type-C diagnostic — 2026-10-03

TUSB320LAIRWBR C132554, TPS7A2033PDBVR C2862740, TPS3839K33DBZR C96333, SN74LVC1G14DBVR C7835 and SN74LVC1G08DBVR C7666 use only their unmodified native imports in the independent current detector. VBUS detector resistors are exact C114622 470k and C482869 430k. C22765 / 0603WAF1201T5E is a newly imported 1.2k ILIM candidate; not yet wired or qualified. C6617702 remains unqualified for its imported edge cutout. No substitute battery or speaker has been authored.

## Haptic intake and driver review — 2026-10-03

| Candidate | Manufacturer MPN | Exact JLCPCB/LCSC | Status |
|---|---|---|---|
| Haptic motor | LEADER LCM0720A3176F | C2942347 | Native import; B-014 courtyard defect and separate model-height qualification; not integrated |
| Alternate motor | LEADER LCM0720A3134F | C2895081 | No importable EasyEDA library; not a verified substitute |
| Enabled3V motor regulator | TI TPS7A2030PDBVR | C963429 | Native import;1IN/2GND/3EN/4NC/5OUT verified; independent driver review only |
| Flyback diode | MDD SS14 | C2480 | Native import;1cathode/2anode verified against manufacturer SMA drawing |

Q9 reuses exact C20917; R82=C22548 1k, R83=C105588100Ω, R84=C9822010k,
R85=C14675100k. C70=C9005310µF, C71=C8441922µF, C72=C45000100nF.
These quantities belong to the independent fixture and are not a complete-board
BOM. Voltage, startup/stall, EMI, biased-capacitance, reflow/fixture and mechanics
remain open in `HAPTICS.md`; no motor import was patched or substituted.
