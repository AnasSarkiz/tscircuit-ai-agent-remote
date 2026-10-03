# Sources checked on 2026-10-02

- User brief: user-brief.txt. Latest direct instruction authorizes progressing through routing to prototype fabrication after the pre-routing gates pass.
- [Workspace instructions](../../../AGENTS.md), especially mandatory imports and validation stages. No component definitions may be authored or patched.
- [tscircuit handbook code guide](https://github.com/tscircuit/handbook/blob/main/guides/code.md)
- [tscircuit repository initialization guide](https://github.com/tscircuit/handbook/blob/main/guides/bootstrapping-repos.md)
- [Espressif ESP32-S3-WROOM-1 datasheet v1.8](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf)
- [Espressif module placement guidelines](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/pcb-layout-design.html)
- [TI TPS63070 datasheet SLVSC58B](https://www.ti.com/lit/ds/symlink/tps63070.pdf), section 6 page 3, physical pin names/numbers.
- [TI BQ24074 datasheet SLUS810N](https://www.ti.com/lit/ds/symlink/bq24074.pdf), section 7 pages 7–9.
- [MAX98357A/MAX98357B datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/max98357a-max98357b.pdf)
- [JLCPCB rigid PCB capabilities](https://jlcpcb.com/capabilities/Capabilities)
- LCSC candidate identities: https://www.lcsc.com/product-detail/C2913201.html, https://www.lcsc.com/product-detail/C54313.html, https://www.lcsc.com/product-detail/C109322.html, https://www.lcsc.com/product-detail/C910544.html, https://www.lcsc.com/product-detail/C5656610.html.

Import provenance: JLCEDA/EasyEDA Official Library, accessed by the supported `tsci import --jlcpcb` workflow. [JLCEDA](https://lceda.cn/) / [EasyEDA](https://easyeda.com/). The user explicitly authorized C370970's native chip-box symbol and local footprint correction (five holes to 1.05 mm, two slot lengths to 2.65 mm). Original source is preserved in revision 341dcaa; before/after audits are under `../evidence/imports/`. Models and all other imports remain verbatim. No external supplier-library correction is claimed. The raw regulator supplier record was captured through the same public endpoints used by the pinned CLI for diagnosis only; it does not replace the supported import workflow.

Supplier catalogue/search responses may carry different stock counts or prices and do not establish live JLCPCB assembly allocation. No final cost or assembly stock claim is made.

## Additional manufacturer evidence

- [TI TPS63802 datasheet SLVSEU9D](https://www.ti.com/lit/ds/symlink/tps63802.pdf): saved `tps63802.pdf`; package drawing and land pattern pages 35–36 rendered and visually inspected. Complete application review remains pending.
- [ALPS exact EC11E15244G1 product](https://tech.alpsalpine.com/e/products/detail/EC11E15244G1/).
- [ALPS exact mounting drawing](https://tech.alpsalpine.com/cms.media/product_detail_fig_ec11_d_83_en_1f3da99620.gif): saved `alps-ec11e15244g1-mounting.gif`, visually inspected.
- [ALPS EC11E catalogue](https://tech.alpsalpine.com/cms.media/product_catalog_ec_01_ec11e_en_611f078659.pdf): saved `alps-ec11e.pdf`; page 2 drawing 2 inspected in `../evidence/datasheets/alps-ec11e-2.png`.
- [ALPS alternative EC11J1525402](https://tech.alpsalpine.com/e/products/detail/EC11J1525402/): manufacturer status Not Recommended for New Designs; unselected alternative C209762. LCSC identity: https://www.lcsc.com/product-detail/Rotary-Encoders_span-style-background-color-ff0-ALPSALPINE-span-EC11J1525402_C209762.html.
- [Waveshare 1.54 inch LCD wiki](https://www.waveshare.com/wiki/1.54inch_LCD_Module): saved HTML/text. Module 50 × 35 mm; exact sourcing/assembly decision remains unresolved.
- [Waveshare schematic](https://files.waveshare.com/wiki/1.54inch_LCD_Module/1.54inch_LCD_Module_SchDoc.pdf): saved `waveshare-1.54-schematic.pdf`; page 1 inspected. PH connector J2 order differs from J1.
- [Waveshare mechanical download](https://files.waveshare.com/wiki/1.54inch_LCD_Module/1_54inch_lcd_module_2d.zip): saved zip and extracted DXF; not visually reviewed.

Manufacturer references are preliminary qualification evidence, not completed schematic/BOM validation. Encoder LCSC PDF request returned an HTML challenge; preserved under `../evidence/downloads/` and not treated as a datasheet.

## Continued microphone/display review

- [TDK ICS-43434 DS-000069 v1.2](https://product.tdk.com/system/files/dam/doc/product/sw_piezo/mic/mems-mic/data_sheet/ds-000069-ics-43434-v1.2.pdf): official PDF text accessed, page 10 pin identities and page 17 acoustic-hole recommendation. Local download returned HTML rather than PDF; no local visual package review claimed.
- [TDK Product Center ICS-43434](https://product.tdk.com/en/search/sw_piezo/mic/mems-mic/info?part_no=ICS-43434): Production/NRND status.
- [InvenSense ICS-43434](https://www.invensense.tdk.com/en-us/products/microphone/ics-43434): EOL status. Lifecycle discrepancy remains unresolved; no active-production claim.
- [Wisevision N177-1216TCWPG01-H14 / C5123575 catalogue](https://www.lcsc.com/product-detail/C5123575.html): investigated 1.77 inch display candidate, not imported, selected or qualified. Does not establish required display procurement.

## 2026-10-03 update and accepted product direction

- Direct user instructions accept `../assets/product-concepts/ai-remote-v1-infographic-v3.png`: square, dominant screen, one top hold-to-talk button, top assembly only, speaker, rechargeable battery. Authoritative changes: `../REQUIREMENTS.md`.
- Published npm registry metadata queried directly: tscircuit 0.0.2736 / CLI 0.1.2232; exact metadata saved in `../evidence/update-check-2026-10-03/published-versions.json`. Installed and tested locally, not a version inferred from search snippets.
- TDK DS-000069 v1.2 page 17 acoustic-hole recommendation rechecked against a fresh supported C5656610 import: hole still 0.3999992 mm; B-002 persists.
- [JST battery connector C295747 catalogue identity](https://www.lcsc.com/product-detail/C295747.html): SMT right-angle S2B-PH-SM4-TB(LF)(SN), 2 mm pitch, 2 A catalogue rating. Catalogue reported 19,795 stock at lookup; this does not verify JLCPCB PCBA allocation.
- [Official JST PH connector family](https://www.jst.com/products/crimp-style-connectors-wire-to-board-type/ph-connector/) and [PH drawing PDF](https://www.jst.com/wp-content/uploads/2025/06/ePH.pdf). PDF fetch returned 403 both through web and local request. No completed manufacturer drawing/footprint review is claimed.
- [TI BQ24074 datasheet](https://www.ti.com/lit/ds/symlink/bq24074.pdf) supports the one-cell charger/power-path architecture; exact cell, current, protection, thermistor and layout remain unqualified.

## User-authorized local microphone correction

The linked supplier investigation in `/Users/anassarkiz/Documents/Codex/2026-09-30/is-x20/work/microphone-import-investigation/` was read as evidence, not as instructions. Findings and raw EasyEDA response are preserved under `../evidence/microphone-local-correction-2026-10-03/`. Independent radius conversion confirms 0.3999992 mm. The user's latest direct instruction authorizes changing only the local acoustic hole to 0.60 mm. The converter and supplier library remain unchanged. The new native-renderer ground-port blocker is documented separately as B-003.

## Controls review references — 2026-10-03

- [Panasonic side-operated Light Touch Switch catalogue](https://mediap.industry.panasonic.eu/assets/imported/industrial.panasonic.com/ac/cdn/e/control/switch/light-touch/catalog/sw_lt_eng_smalls_side.pdf): July 2025 ANCTB23E, saved panasonic-side-switch.pdf. Printed pages 1–2 rendered and inspected. EVQPUC02K contacts 1↔3, 2↔4 and 0.75 +0.10/−0 mm locating-hole requirement confirm B-006.
- [TI TPS22919 SLVSEN5B](https://www.ti.com/lit/ds/symlink/tps22919.pdf): saved tps22919.pdf; pin table page 3 rendered/inspected, actual pin 1→V3V3 wiring verified. Missing imported power classification remains visible.
- [TI TPS3839 SBVS193D](https://www.ti.com/lit/ds/symlink/tps3839.pdf): saved tps3839.pdf; electrical table rendered/inspected. Application review remains incomplete.
- [TI TLV3201 SBOS561C](https://www.ti.com/lit/ds/symlink/tlv3201.pdf): saved tlv3201.pdf; pages 3 and 6 rendered/inspected. C105188 exact identity verified from [JLCPCB](https://jlcpcb.com/partdetail/TexasInstruments-TLV3201AIDBVR/C105188). Supported import retained unchanged; missing reference text B-008 remains.
- [TI SN74LVC2G125 SCES204Q](https://www.ti.com/lit/ds/symlink/sn74lvc2g125.pdf) and [SN74LVC1G125](https://www.ti.com/lit/ds/symlink/sn74lvc1g125.pdf): saved original manufacturer PDFs. SD receiver selection rejected after logic-level review; clock-buffer application margins/power-off behavior remain unresolved.

Exact new component-source checksums and import logs are in the controls-review
evidence directory. Catalogue identities were checked, but cached availability
is not live assembly allocation. No stock guarantee, custom component or local
import-metadata correction is claimed.

## MCU/USB, display and clock-switch research — 2026-10-03

- [Espressif module datasheet v1.8](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf), saved esp32-s3-module.pdf. N8R8 reserves GPIO35/36/37; ordinary octal PSRAM limits −40…65 °C without ECC.
- [Espressif hardware checklist](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/schematic-checklist.html): supply/EN, USB 22 Ω, boot and programming requirements.
- [TI TPD2EUSB30A](https://www.ti.com/lit/ds/symlink/tpd2eusb30a.pdf), saved tpd2eusb30a.pdf; exact C94934 imported unchanged, reference-text defect remains.
- [JST SH official family drawing](https://www.jst.com/wp-content/uploads/2025/06/eSH.pdf), saved jst-sh.pdf; C160405 exact import retained unchanged.
- [HS17QS178RX manufacturer specification via supplier](https://atta.szlcsc.com/upload/public/pdf/source/20221215/3E47753EF985E64F0BD11377D6B95218.pdf), saved HS17QS178RX.pdf. Mechanical drawing inspected; manufacturer VDD 2.7–3.3 V overrides broader catalogue range. C5329581 imported unchanged.
- [TI TPS7A20](https://www.ti.com/lit/ds/symlink/tps7a20.pdf), saved tps7a20.pdf. C2869847 2.8 V regulator accuracy guaranteed at VIN≥3.1 V; not yet an implemented display circuit.
- [TI SN74LVC245A](https://www.ti.com/lit/ds/symlink/sn74lvc245a.pdf), saved sn74lvc245a.pdf; C7848 imported unchanged, display buffer candidate.
- [TI TS5A23157](https://www.ti.com/lit/ds/symlink/ts5a23157.pdf), saved ts5a23157.pdf; C11133 dual SPDT hardware microphone candidate.
- [EEMB protected-pack specification on supplier mirror](https://macrogroup.ru/upload/iblock/80a/i2bksi77p3ephpa70n95kv0izxtrs2jg/LP503450.pdf), saved eemb-LP503450-PCM-NTC-LD.pdf. 2017-11-13 specification, pack continuous limit only 1 A; unselected. Current sourcing/thermistor/visual review unresolved.
- [ALPS SKRTLAE010 exact product](https://tech.alpsalpine.com/e/products/detail/SKRTLAE010/) and [October 2025 catalogue](https://tech.alpsalpine.com/cms.media/product_catalog_ta_02_skrt_en_01ec237785.pdf). C110293 supported import and drawing comparison in progress.

Cached catalogue availability is not assembly allocation. All new candidates
remain unqualified until drawing, ratings, import geometry and application checks
are complete. No physical measurements or supplier-library repairs are claimed.
