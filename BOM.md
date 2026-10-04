## A6 current checkpoint — 2026-10-04

**Engineering prototype — NOT FABRICATION READY.** This supersedes historical A5 counts below. Genuine in-stock replacements are implemented: seven C22548→C21190 (eight C21190 total), six C105588→C22775. Active125 purchased PCB parts /43identities plus10native pads. Published core0.0.2083 polygon paste fixes13 formerly missing pads;32 pill pads still lack paste. Current native copper20traces/2vias; five missing backlight traces resolved, unconnected-port errors413→402. Genuine saved phase replay and actual added-copper geometry verified; all prior11traces/2vias unchanged.

Required five native checks and copper-free placement CAD build pass. Format/types pass; tests42pass/2retained failures and full native strict schema169failures. Diagnostic PCB-image shorts passes, but **required Gerber-based shorts check fails “Unsupported shape polygon”**. Canonical routed build exits1 with402 retained unconnected-port errors. Final layout/assembly/fabrication gates remain blocked. Fresh4layer/paste/detail/13A4/3D prototype previews inspected.

Battery centreNTC confirmed; outer numbered polarity is still absent from the exact supplier drawing and stays unrouted. BuyDisplay panel has integrated ILI9341 and82.712% nominal physical coverage; actual FPC/contactface/pin1 mating and current bare-panel availability remain unqualified. JST board-thickness tolerance requires a mechanical/stackup revision; current conservative height becomes15.07 mm at a qualifying1mm PCB, above15mm. PCB stays50×65 mm; case max60×75×15 mm. No fabricated confirmation, generic imports or orders.

[Detailed A6 review](evidence/a6-bom-routing-2026-10-04/review.md) · [Active inventory](evidence/a6-bom-routing-2026-10-04/inventory.md) · [Mechanical primary sources](evidence/a6-bom-routing-2026-10-04/mechanical-search.md). Parentfaa491d22d1a55210833a8ea3086ae56dc450245. Intended public version0.0.2-wip-a6-bom-routing; verify publication receipts before claiming upload complete. Watcher stays paused; no cross-chat issue messages.

---

## Current layout/BOM audit — 2026-10-04

Preliminary native placement/connectivity/shorts checks pass; final layout and assembly BOM remain **blocked**. Current 135 components = 125 purchased parts + 10 native pads. Fresh supplier audit:43/44 exact identities match; C22548 stock 5 versus 7 required, C105588 (six 100 Ω parts) has no in-stock result. Current native paste is missing on45 SMT pads: U16 (17), U27 (16), U4/U5 (8), J1 (4). Official BOM probe125 rows / 31 blank Comment fields / 125 supplier-code footprints. Fresh current 3D and 13 A4 sheets reviewed; display physical mating, pack outer polarity,0.8 mm stackup/case fit and full routing remain open. Tests42 pass / 2 retained failures. In-stock resistor alternatives were found but not substituted. [Full audit](evidence/layout-bom-audit-2026-10-04/review.md) · [Current inventory](evidence/layout-bom-audit-2026-10-04/inventory.md). Source/copper/imports unchanged; no new package retry, watcher resume or cross-chat message. **NOT FABRICATION READY.**

---

## A5 BOM change — 2026-10-04

J8/C173752 quantity reduced by one. Native TP_MOTOR_P/TP_MOTOR_N solder pads are PCB features, not purchased components. J6 remains. Earlier component counts below are historical; current total135 includes125purchased parts and10native testpoints. Motor remains external and its exact assembly/harness qualification is open. No manually repaired fabrication BOM is approved.

# Latest A4 — 82.7% physical display coverage trial

**WIP prototype; NOT FABRICATION READY.** This supersedes conflicting A3/A2 selections below. Provisional external BuyDisplay **ER-TFT026-1**, 46 × 64 mm portrait body, overlaps the unchanged 50 × 65 mm PCB by **82.712%** (81.737% with stated dimensional/position allocation). Overhang, flex and bezel are excluded. Bare-panel availability and the current drawing/FPC are still unconfirmed; this is not a qualified purchasable display selection.

Implemented genuine C157929/C173752 internal side-entry PH headers, TPS60230RGTR/C1848364 four-channel backlight with 10 kΩ nominal 62.4 mA total, moved placement/mounting trial, rotated battery envelope and **0.8 mm trial PCB**. The thin stackup and USB impedance need new qualification. Battery pin2=NTC; both outer contacts stay open. Four original native traces are preserved; most connections remain unrouted. Fresh canonical build retains 431 connection errors; 38 tests pass and two fabrication/schema gates fail. Placement and short checks pass without claiming full routing or fabrication approval.

[Full A4 engineering review](evidence/a4-display-coverage-2026-10-04/review.md) · [Interactive A4 native model and display envelope](http://127.0.0.1:4949/evidence/a4-display-coverage-2026-10-04/mechanical.html). Current PCB count:134 physical components,496PCB ports,76named nets. Watcher remains paused and cross-chat issue messages remain disabled. Publication receipts are recorded separately; intended public package version `0.0.2-wip-a4-display-coverage`.

## Active A4 substitutions

| Reference | Exact part | Source | Quantity |
|---|---|---|---:|
|External provisional display|ER-TFT026-1 no-touch bare panel|BuyDisplay; no current bare-panel orderability verified|1|
|J3|S3B-PH-K-S(LF)(SN)|JLC C157929, genuine untouched import|1|
|J4|S2B-PH-K-S(LF)(SN)|JLC C173752, genuine untouched import; J8 removed in A5|1|
|U27|TPS60230RGTR|JLC C1848364, genuine untouched import|1|
|R102|RC0603FR-0710KL, 10 kΩ|existing genuine JLC import|1|
|J7 retained|AFC07-S50ECA-00|JLC C262650; portrait mating provisional|1|

No fresh whole-BOM assembly availability guarantee. External pack AKY2945/LP523450 centre contact NTC10k; outer polarity remains pending. PH headers are top-inserted through-hole parts and need manual/selective assembly qualification. Superseded A3 choices below are historical.

---

# Latest A3 BuyDisplay and first-copper checkpoint — 2026-10-04

**Engineering prototype — NOT FABRICATION READY.** This supersedes conflicting A2/A1 selections below. The external screen is now **BuyDisplay/EastRising ER-TFT022-1, bare 2.2-inch 240×320 TFT, no touch**, purchased separately from the PCB. JLCPCB supplies the board electronics and the genuine **AFC07-S50ECA-00/C262650 top-contact50-pin connector**, not the screen. Its54.36×40.3 mm landscape glass spans the full50 mm PCB width. The raised-glass/flex/height tolerance study remains open inside the unchanged50×65 mm PCB and60×75×15 mm maximum enclosure.

Electrical source wiring uses panel n→J7(51−n) for the planned right-edge single fold, SPI II mode1110,2.8 V logic/level translation and three separate TPS60231 current sinks. The old HS20HS072RX,12-pin connector and resistor-fed backlight are superseded. Battery centre2 staysPACK_NTC and the outer contacts stay open.

Actual partial copper now exists: two short MCU USB traces and two compact regulator switch traces,0vias. Original native routes/events and supported replay are preserved before moves; the regulator island/cache were moved together−8 mm X. The other nets are not routed. Current whole board:134physical components(126purchased+8testpoints),502PCB ports,75named nets. Required remaining-connection errors are retained; no fabrication outputs are approved. Full technical review: [BuyDisplay integration and fit limits](evidence/a3-routing-2026-10-04/buydisplay/review.md). [Live mechanical study](http://127.0.0.1:4949/evidence/a3-routing-2026-10-04/mechanical.html).

Native placement overlap/keepout errors are zero. Source, netlist and pin-specification checks have no errors; supplier metadata warnings and connector-access warnings remain disclosed. Four orientation suggestions were applied. The source-level schematic pin-map and imported connector orientation tests are distinct from physical panel operation. Full routing/schema/fabrication tests retain their failures; publication never means fabrication approval.

Source parent0300c2eed5d591b24dba9d2bdd59e17de0f94bf7. Intended public release0.0.2-wip-a3-buydisplay-first-copper; verify receipts before claiming it published. Background watcher remains paused. The user revoked cross-thread issue messages; no issues are sent to another chat.

## Active A3 substitutions

| Reference | Exact part | Supplier | Quantity |
|---|---|---|---:|
|External screen, not PCB population|ER-TFT022-1 no-touch bare panel|BuyDisplay/EastRising; no JLC part number|1|
|J7|AFC07-S50ECA-00|JLC C262650|1|
|U27|TPS60231RGTR|JLC C544659|1|
|C82/C83|CL10A105KB8NNNC,1uF|JLC C15849|2|
|C1|CL10A475KO8NNNC,4.7uF±10%|JLC C19666|1|

C11063 bottom-contact connector is an unselected trial. Active external pack remainsAKY2945/LP523450; connectorJ3centre2NTC and unresolved outer1/3 remain unchanged. PCB assembly includes126purchased components,8native testpoints excluded; no manually repaired fabrication CSV or claimed availability guarantee.

# Latest A2 checkpoint — 2026-10-04

**NOT FABRICATION READY.** This section supersedes conflicting historical A0/A1 selections and status below. A2 updates the genuine C11051 twelve-pin display connector, manufacturer display wiring, centre battery NTC, two native M2 mounting trials and provisional placement. Battery outer numbering remains pending; both outer contacts are unconnected/unrouted. Display/flex/enclosure/RF fit is still open; routing remains disabled. Full report: [A2 fabrication checkpoint](evidence/routing-intake-2026-10-04/fabrication-report.md).

A2 active J7 is AFC07-S12FCC-00/C11051; old C11050 is inactive. J3 active C265101 is PH3: pin2PACK_NTC;1/3unassigned pending outer polarity. HS20HS072RX/C5329582 and AKY2945 are external modules, not PCB population. Native export122purchasedrows plus8coppertestpoints excluded from BOM/CPL;32blankCommentfields and U14rotation unresolved.

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

## Regulated microphone clock review — 2026-10-03

| Candidate | Manufacturer MPN | JLCPCB/LCSC | Status |
| --- | --- | --- | --- |
| Hardware-enabled 2.8 V supply | TI TPS7A2028PDBVR | C2869847 | Existing genuine import reused as separate supply instance; independent review only |
| Open-drain dual clocks | Nexperia 74LVC2G07GW,125 | C24478 | Genuine unchanged import; conditional DC margins, timing/privacy still unqualified |
| Clock pullups | YAGEO RC0603FR-07330RL | C105881 | Genuine unchanged 330-ohm import; exact manufacturer sheet preserved |
| Unselected comparison buffer | TI SN74LVC2G07DCKR | C7849 | Genuine import; not populated in the candidate |

The 15-part fixture reuses C90053 (10 uF), C45000 (100 nF), C22548 (1 kohm),
C14675 (100 kohm), C105588 (100 ohm) and C98220 (10 kohm). These are fixture
quantities, not a completed board BOM. Native C5329581 LCD import remains
present; the envelope study uses its manufacturer drawing without editing it.

## Battery-readiness application candidate — 2026-10-03

U25 is genuine TPS3808G33DBVR / C43698 (SOT-23-6), imported unchanged. Supplier search reports 6,139 pieces on 2026-10-03; recheck final availability. The independent five-part candidate allocates R96/R97=C114622 470 kohm and C76/C77=C45000 100 nF. This is a hardware buck-enable review, not an integrated charger or qualified pack. Threshold/low-supply/dynamic policy and actual protected battery, NTC, harness and discharge capacity remain unresolved. No unrelated speaker/battery/resistor search result was selected. See battery-readiness qualification evidence.

## Additional hold candidate — unselected

ALPS SKSWCFE010/C255576 is a genuine unchanged two-contact/no-hole SMT candidate. Supplier dimensions are preserved, but lands differ from ALPS's current recommended pattern and final paste/mechanical/electrical acceptance is pending. Exact alternate SKSWCEE010/C202371 has identical supplier pads and was not imported or selected. See evidence/hold-control-alternate-review-2026-10-03/qualification.md; no fabricated replacement component is used.

B-015 blocks approval of native fabrication BOM metadata: official converter0.0.19 drops MPN/explicit resolver Comment for imported chips/connectors/switch. Exact JLCPCB codes remain correct. The characterized CSV is a tooling reproduction, not an ordering BOM; no manually repaired fabrication output is substituted.

## Independent hold readback candidate — 2026-10-03

| Instance | Exact manufacturer part | JLCPCB/LCSC | Candidate function |
| --- | --- | --- | --- |
| U26 | TI SN74LVC1G17DBVR | C7836 | Schmitt input on hardware HOLD; separate MCU readback output |
| R99 | YAGEO RC0603FR-0710KL | C98220 | 10kohm hardware signal ground bias |
| R100 | UNI-ROYAL 0603WAF1001T5E | C21190 | 1kohm buffer-to-MCU series resistor; genuine higher-stock alternative |
| C78 | Murata GRM188R71C104KA01D | C45000 | 100nF supply decoupling |

These are independent fixture allocations, not a complete production BOM. Current native stock: C7836=34179,C98220=22,C21190=8,013,731,C45000=3848. Prior C22548 stock5 prompted a supported genuine C21190 import/substitution in this candidate; other prior sheets retain their original parts. C25804/0603WAF1002T5E is imported but unselected: stock-filtered catalogue results are empty while its independent EasyEDA import succeeds. Final assembly stock, total quantities, exact resistor temperature/aging, supplier lands and complete hardware privacy remain open. No imported definition or fabricated substitute is authored. See evidence/hold-readback-review-2026-10-03/qualification.md.

## A0-reference-import-review — 2026-10-03

C105188/C94934/C20917/C15127 were regenerated intact through the published official easyeda0.0.370 JLC converter CLI; footprint/pin labels unchanged, native reference ownership verified. They remain application-review components, not a finalized complete-board BOM. C41348533/LEADER LD-SM-430 is an imported alternate SMT motor candidate only: polygon paste absent, third mounting-land electrical role/model/body/mechanics/current/reflow qualification pending. Additional speakers C20613566/C49246973/C7430168 failed exact library import and remain excluded. See current dated evidence; no unqualified substitute was selected.
