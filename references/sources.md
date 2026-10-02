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

Import provenance: JLCEDA/EasyEDA Official Library, accessed by the supported `tsci import --jlcpcb` workflow. [JLCEDA](https://lceda.cn/) / [EasyEDA](https://easyeda.com/). Component sources/assets are preserved verbatim. The raw regulator supplier record was captured through the same public endpoints used by the pinned CLI for diagnosis only; it does not replace the supported import workflow.

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
