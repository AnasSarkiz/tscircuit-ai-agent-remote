# Candidate BOM — A0

**Not an assembly/fabrication BOM.** Import success alone does not qualify a part. Reference designators will be assigned with the complete schematic.

| Function | MPN | LCSC | Package | Intended qty | Status |
|---|---|---|---|---|---|
| MCU/Wi-Fi | ESP32-S3-WROOM-1-N8R8 | C2913201 | Antenna module | 1 | Imported; complete review pending |
| Charger/power path | BQ24074RGTR | C54313 | QFN-16 + EP | 1 | Imported; battery/current/thermal design pending |
| 3.3 V buck-boost | TPS63802DLAR | C2845237 | DLA-10 2 × 3 mm | 1 | Imported; pin identities pass; application review pending |
| Digital microphones | ICS-43434 | C5656610 | LGA-6 bottom port | 2 | **B-002: 0.40 mm acoustic hole below TDK recommended 0.50 mm minimum**; fresh CLI 0.1.2232 import still 0.40 mm; correction/lifecycle review pending |
| I2S speaker amplifier | MAX98357AETE+T | C910544 | TQFN-16 + EP | 1 | Imported; full application review pending |
| USB-C receptacle | TYPE-C-31-M-12 | C165948 | USB2.0 hybrid mount | 1 | Imported; orientation/protection/mechanics pending |
| Battery connector candidate | S2B-PH-SM4-TB(LF)(SN) | C295747 | SMT right-angle, 2 mm pitch | 1 | Imported verbatim with CLI 0.1.2232; top-side assembly candidate; drawing/polarity/full qualification pending |
| Microphone clock buffer candidate | SN74LVC2G125DCUR | C21404 | VSSOP-8 | 1 | Imported; architecture/ratings pending |
| Microphone data buffer candidate | SN74LVC1G125DBVR | C23654 | SOT-23-5 | 1 | Imported; architecture/ratings pending |

## Rejected or unselected imports

| Part | LCSC | Reason |
|---|---|---|
| TPS63070RNMR | C109322 | Missing separate physical identities 8/13 and PS/SYNC alias; alternate TPS63802 under review |
| EC11J1525402 | C209762 | Alternative investigation only; ALPS Not Recommended for New Designs; unselected/unqualified |
| EC11E15244G1 | C370970 | Historical locally corrected encoder; removed from active design by accepted single-button concept |
| DSK110 | C908227 | Unrelated diode returned by display search; not active BOM |

All definitions/models originated through the supported JLCPCB importer. The user explicitly authorized C370970's native chip-box symbol and footprint correction: five holes to 1.05 mm and two slot lengths to 2.65 mm. Pin labels, supplier identity, all centers, other geometry and models remain unchanged. This is a local correction, not a corrected official supplier library. Other imports remain unmodified. Rejected imports are retained as evidence.

## Required parts still unselected

Screen-dominant display/module and connector; exact protected 1S 3.7 V, 4.2 V-charge LiPo pack (500–1000 mAh target), protection/thermistor/harness; speaker and speaker connector; haptic connector/MOSFET/flyback protection; single top-edge hold-to-talk control and compatible hardware microphone isolation; internal BOOT/RESET service access; regulator inductor and all passives; USB CC resistors, ESD/current protection and decoupling; programming/test connectors. No placeholders represent these parts. Separate encoder, APPROVE/REJECT buttons, privacy slider, exterior power control and front RGB LED are not part of the accepted concept.

The rechargeable pack and battery circuit are not yet integrated. C295747 is a real imported connector candidate, not a qualified battery pack. All electronic parts and connector solder joints must use top-side assembly; bottom-side population is prohibited by the accepted requirements. Exact current and thermal budgets remain pending.

Waveshare 1.54 inch LCD Module was researched, not selected as an imported component. PH2.0 J2 order is **BL/RST/DC/CS/SCK/DIN/GND/VCC**, opposite schematic J1 ordering. Contact orientation requires independent verification.

Catalogue identities/manufacturer sources checked on 2026-10-02; see `references/sources.md`. Final JLCPCB assembly allocation, basic/extended classification, external procurement, costs and exact availability remain unverified. Do not order from this document.
