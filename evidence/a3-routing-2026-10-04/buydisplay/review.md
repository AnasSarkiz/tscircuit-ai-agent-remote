# A3 BuyDisplay integration review — 2026-10-04

This supersedes the A2 external HS20HS072RX/C5329582 and twelve-pin J7 selections. The external display is sourced directly from BuyDisplay/EastRising under the user's explicit sourcing exception; PCB electronics remain genuine JLC imports. No display component or footprint was invented. No purchase was placed.

## Selection and actual fit limits

Selected engineering candidate: ER-TFT022-1, **no-touch bare 2.2-inch 240 × 320 TFT**, ILI9341 controller, four-wire SPI II. It is a TFT, not an OLED or a qualified IPS panel. Manufacturer source: https://www.buydisplay.com/serial-qvga-2-2-inch-tft-spi-240x320-lcd-touch-display-module-ili9341 . Product displayed in stock at $6.70 on the review date; final procurement availability must be checked again. Official Rev2.0 drawing, no-touch page6, is saved in `references/a3/buydisplay/ER-TFT022-1_Datasheet.pdf` with the ILI9341 datasheet and official unexecuted demo code. Touch/module adapter options are not selected.

Landscape glass: 54.36 ±0.2 mm wide ×40.3 ±0.2 mm high ×2.3 mm maximum, centre(-0.5,-5.225). Nominal body edges X[-27.68,26.68], Y[-25.375,14.925]. It spans the complete 50 mm PCB width, with enclosure overhang. Active pixels44.64 ×33.48 mm, centre(-2.31,-5.225), using the manufacturer's3.05 mm left margin; active pixels do not cover the full PCB. The antenna exclusion remains X[-22,-2],Y[31.675,39.675],all heights/layers.

The2.4-inch alternative's actual no-touch drawing is59.46 ±0.2 ×42.72 ±0.2; in landscape its worst width59.66 exceeds the58.4 mm inside width of a60 mm case with0.8 mm side walls. Portrait overlaps the tall PH connectors. The2.0-inch ER-TFT020-3 is a smaller14-pin IPS alternative,34.6 ×47.8 mm; the2.2 candidate was chosen for better PCB-width coverage. No larger enclosure was authorized or used.

Glass rear is a **nominal study position** Z4.1 mm; module model maximum under the glass is3.9099999 mm, giving only0.19 mm nominal gap. This is not a manufactured tolerance guarantee. With conditional10% swelling on the5.7 mm battery body, battery bottomZ−7.37,0.5 mm rear cover and0.6 mm front cover, total nominal external thickness is14.87 mm. This leaves0.13 mm within the15 mm hard maximum. Battery thickness tolerance, actual swelling allowance, adhesive, support, module height variation and cable bend can consume this budget. **Do not mark mechanical fit passed or force compression of the pack.** Maximum case remains60 ×75 ×15 mm; PCB50 ×65 ×1.6 mm.

Tall PH connectors were moved beyond the glass: J3 bodyY16.475..25.525, J4Y24.05..31.95, J8Y15.300..23.200. J8-to-glass nominal plan gap is0.375 mm (0.275 withglass half-height tolerance alone). J6 body lies under glass with3.71 mm maximum model height; its mated harness needs separate clearance. Connector-access warnings remain disclosed, not suppressed or fixed by editing imported footprints.

## Connector and folded pin correspondence

BuyDisplay specifies50 contacts,0.5 mm pitch,0.3 mm stiffened FPC and **top-contact ZIF**. The bottom-contact C11063 trial was rejected; its import remains historical/unselected. Active J7 is the unmodified genuine **JUSHUO AFC07-S50ECA-00 / C262650**, top contact,0.5 mm,50 positions,2 mm height abovePCB. Exact manufacturer drawing is saved as `references/a3/buydisplay/AFC07-S50ECA-00.pdf`; circuit1 is identified in that drawing. JLC page https://jlcpcb.com/partdetail/AFC07-S50ECA-00/C262650 displayed18,884 stock/18,712 available order quantity during the review. Neither number guarantees later order availability.

Native placement J7(8.2,-12.625), rotation90°. Model mouth is toward the right-hand flex fold. Native pad1 is south at(6.6638969,-24.873007); pad50 north at(6.6654209,-0.376485), nominal24.5 mm pitch span. In the manufacturer's front landscape display drawing panel1 is north. A single right-edge180° fold preserves this north/south order, hence **panel n → J7(51−n)**. This reversal is in board wiring, not an imported pin-number edit. Anchors51/52 remainGND.

| Panel pin/function | J7 pin | Board connection |
|---|---:|---|
|1 LED anode|50|LCD_BACKLIGHT_OUTPUT|
|2/3/4 LED cathodes1/2/3|49/48/47|LCD_BACKLIGHT_RETURN_1/_2/_3|
|5 NC|46|open|
|6 IM0|45|GND|
|7/8/9 IM1/IM2/IM3|44/43/42|VLCD; IM[3:0]=1110 SPI II|
|10 RESET|41|LCD_RESET_N|
|11..32 RGB/parallel bus inputs|40..19|GND, per controller unused-input guidance|
|33 SDO|18|open, output|
|34 SDI|17|LCD_SDA|
|35 RD|16|VLCD, unused active-low input|
|36 WRX/DC|15|LCD_DC|
|37 D/CX/SCL|14|LCD_SCLK|
|38 CSX|13|LCD_CS_N|
|39 TE|12|open, output|
|40/41/42 VCI/IOVCC/IOVCC|11/10/9|VLCD|
|43 GND|8|GND|
|44..47 unselected touch contacts|7..4|open|
|48..50 GND|3..1|GND|

2.8 V TPS7A20 rail conditional2.758..2.842 V is within panel VCI2.5..3.3 and VDDI1.65..3.0 V. Existing SN74LVC245A level translation remains because the main3.3 V rail maximum3.43818 exceeds the panel I/O rail. Final sequencing, SPI rate and startup timing require review; actual powered display operation has not been tested. Driver unused inputs areGND and unused outputs open.

## Backlight

TI TPS60231RGTR/C544659 replaces the previous resistor/PMOS LED control. D1(pin6),D2(pin5),D3(pin4) are **separate** cathode current sinks, not tied together. Pin8 VOUT drives the common anode. Genuine1uF C15849 flying caps C82/C83 connect physical C1+/C1− andC2+/C2−; VIN and enable source useV3V3, both enables controlled viaBACKLIGHT_GATE/100Ω series and10k pulldown. R1029.1k sets about17.14 mA/channel,51.43 mA combined. Prior static corner allocation gives43.54..57.81 mA combined, below the panel60 mA maximum and20 mA/channel; this is conditional on the documented TI factor/resistor bounds, not a measured guarantee. Output compliance, startup, ripple, effective cap values, rail load and thermal behavior remain to be qualified. The panel's typicalVF3.2/max3.4 V makes a plain3.3 V resistor feed unsuitable at corners.

## Flex qualification remains open

The manufacturer's tail projection is27.15 ±0.5 mm, tongue width25.5 ±0.1 mm, exposed contacts3.5 ±0.2 mm and stiffened end5.5 ±0.2 mm. Drawing includes a COF/broader flex region; neither it nor the stiffener may be casually bent. No guaranteed static bend radius, exact assembled fold geometry or additional twist has been provided. The tongue offset is inferred from the drawing, not a dimensioned tolerance. The current connector pose and repeated-contact mapping are a trial and need a supplier-confirmed/physical fold check before release. Do not fabricate an extension, sharpen the bend, treat a planning box as an actual cable path, or claim the display is physically fitted. The live viewer shows an orange **planning volume**, not the old incompatible L-tail or an asserted completed fold.

## Actual copper and validation scope

Four physical top copper traces currently exist: two short MCU USB paths and two compact regulator switching paths. REG native originals/full events were saved before modification in `routes/a3/regulator-native-original.json` and earlier A3 evidence. Supported replay reproduces geometry after removal of adjacent duplicate zero-length points only. The compact edited routes have0vias; widths taper from0.275 mm short pin fanout to1 mm trunk. New REG placement moved every saved point−8 mm X with the entire regulator island; originals remain unchanged. This does not complete power-current or USB impedance validation.

The complete current board has134 physical components(126 purchased+8 native copper testpoints),502 PCB ports and75 named nets. Routing is deliberately scoped to the saved regulator phase and manual MCU paths; all remaining connection errors are retained. Battery outer contacts1/3 remain open, centre2PACK_NTC. No complete Gerber/BOM/CPL approval is possible yet. Tool/schema/paste/BOM and full routing gates remain open; watcher stays paused and issues are not sent to another chat.
