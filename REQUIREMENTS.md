# Latest A3 BuyDisplay and first-copper checkpoint — 2026-10-04

**Engineering prototype — NOT FABRICATION READY.** This supersedes conflicting A2/A1 selections below. The external screen is now **BuyDisplay/EastRising ER-TFT022-1, bare 2.2-inch 240×320 TFT, no touch**, purchased separately from the PCB. JLCPCB supplies the board electronics and the genuine **AFC07-S50ECA-00/C262650 top-contact50-pin connector**, not the screen. Its54.36×40.3 mm landscape glass spans the full50 mm PCB width. The raised-glass/flex/height tolerance study remains open inside the unchanged50×65 mm PCB and60×75×15 mm maximum enclosure.

Electrical source wiring uses panel n→J7(51−n) for the planned right-edge single fold, SPI II mode1110,2.8 V logic/level translation and three separate TPS60231 current sinks. The old HS20HS072RX,12-pin connector and resistor-fed backlight are superseded. Battery centre2 staysPACK_NTC and the outer contacts stay open.

Actual partial copper now exists: two short MCU USB traces and two compact regulator switch traces,0vias. Original native routes/events and supported replay are preserved before moves; the regulator island/cache were moved together−8 mm X. The other nets are not routed. Current whole board:134physical components(126purchased+8testpoints),502PCB ports,75named nets. Required remaining-connection errors are retained; no fabrication outputs are approved. Full technical review: [BuyDisplay integration and fit limits](evidence/a3-routing-2026-10-04/buydisplay/review.md). [Live mechanical study](http://127.0.0.1:4949/evidence/a3-routing-2026-10-04/mechanical.html).

Native placement overlap/keepout errors are zero. Source, netlist and pin-specification checks have no errors; supplier metadata warnings and connector-access warnings remain disclosed. Four orientation suggestions were applied. The source-level schematic pin-map and imported connector orientation tests are distinct from physical panel operation. Full routing/schema/fabrication tests retain their failures; publication never means fabrication approval.

Source parent0300c2eed5d591b24dba9d2bdd59e17de0f94bf7. Intended public release0.0.2-wip-a3-buydisplay-first-copper; verify receipts before claiming it published. Background watcher remains paused. The user revoked cross-thread issue messages; no issues are sent to another chat.

# Latest A2 checkpoint — 2026-10-04

**NOT FABRICATION READY.** This section supersedes conflicting historical A0/A1 selections and status below. A2 updates the genuine C11051 twelve-pin display connector, manufacturer display wiring, centre battery NTC, two native M2 mounting trials and provisional placement. Battery outer numbering remains pending; both outer contacts are unconnected/unrouted. Display/flex/enclosure/RF fit is still open; routing remains disabled. Full report: [A2 fabrication checkpoint](evidence/routing-intake-2026-10-04/fabrication-report.md).

Display HS20HS072RX/C5329582, bottom-contact twelve-pin AFC07-S12FCC-00/C11051; protected AKY2945/LP5234501000mAh3.7/4.2V, max pack35×52.5×5.7mm, PH3, 10kNTC. Approved PCBmax50×65mm; current50×65. Red/black outer contacts **PENDING PIN-NUMBER CONFIRMATION**; centre yellow NTC. No final mechanical or current acceptance implied.

# AI Remote — accepted product direction

Updated 2026-10-03 from the user's direct follow-up instructions. These requirements
supersede conflicting controls and enclosure styling in `references/user-brief.txt`.
The original brief is preserved as historical input.

## Form and interaction

- Compact square enclosure with rounded corners and a display dominating the front.
- Primary top-edge hold-to-talk button plus a side-edge physical microphone privacy switch (latest user instruction).
- Hold → speak → release → send over Wi-Fi → show and speak the AI response.
- No exterior encoder, APPROVE/REJECT buttons or separate power button. BOOT/RESET stay inside the enclosure.
- Status indication belongs on the screen; no separate front status LED is required.
- Top-side PCB assembly only: all populated electronic parts and connector solder
  joints must be assembled from the top. Four copper layers remain intended.
- Enclosure-mounted speaker and rechargeable battery connect to the top-side PCB;
  they are separate mechanical parts, not bottom-side PCB population.
- USB-C access at the bottom edge. Speaker grille and microphone acoustics must
  follow the real parts and acoustic paths, rather than the illustration alone.

Accepted visual reference: `assets/product-concepts/ai-remote-v1-infographic-v3.png`.
This is a concept illustration, not dimensioned CAD or a validated placement.

Latest preview milestone starts at **50 × 55 mm**, within the approved **50 × 65 mm** maximum. The actual A1 preview expanded to 50 × 65 mm to resolve first-trial overlaps. Enclosure square styling and final fit remain provisional. Final enclosure dimensions,
display active area/glass, mounting, speaker depth, battery thickness and antenna
clearances remain unresolved. A 1.54–1.9 inch display from the original brief must
be checked against the desired front coverage; the concept does not prove that fit.

## Rechargeable power

- One protected **1S rechargeable LiPo/Li-ion pack**, nominal 3.7 V, with a 4.2 V
  charge termination specification. No series-cell battery architecture.
- Target **500–1000 mAh**, preferring 1000 mAh if the actual protected pack fits.
- USB-C 5 V charging and power-path operation while plugged in.
- BQ24074RGTR / C54313 remains the charger/power-path candidate.
- TPS63802DLAR / C2845237 remains the 3.3 V regulator candidate.
- JST S2B-PH-SM4-TB(LF)(SN) / C295747 is a newly imported surface-mount battery
  connector candidate. Its exact mating harness polarity must be documented and
  verified; a PH connector name does not establish battery polarity.
- Pack protection must cover overcharge, overdischarge and overcurrent/short
  protection. The charger alone does not complete pack protection.
- Retain battery temperature monitoring and ADC battery-voltage measurement.
- Set charge/input current only after pack ratings, USB current policy and the
  complete peak-load/thermal budget are established. No charge current or runtime
  has been validated.
- Keep the battery, display metal and speaker clear of the ESP32 antenna region.

The exact pack manufacturer/MPN, procurement/import path, protection circuit,
thermistor and harness are still unselected. No generic purchased-part definition
or fake battery footprint is permitted by the workspace instructions.

## Retained electronics and open interface decisions

Retain ESP32-S3 Wi-Fi/BLE/native USB, two digital microphones, I2S amplifier and
external 8 Ω speaker, and internal haptic feedback from the original brief.
Firmware implementation remains outside scope.

Hardware microphone privacy remains a requirement. The new single-control design
needs a reviewed hardware mechanism that prevents firmware enabling the microphones
when disabled, without adding a second exterior control. Button-controlled power
and signal isolation are an architecture candidate, not a verified implementation.
Do not silently replace hardware privacy with a software-only mute.

Any action confirmation, navigation and power/sleep behavior must use the screen
and the single button. Touch support is not assumed without selecting a compatible
display/interface. BOOT/RESET and test access are service features inside the
enclosure, not additional exterior controls; physical access is still to be planned.

## Validation state

Stage 1 remains in progress. B-002 is corrected locally with user authorization:
C5656610 now has a 0.60 mm hole. B-003 now passes native component generation on aligned core 0.0.2058. B-005 now blocks microphone ground-paste qualification. Stage 2
remains incomplete because the complete circuit/BOM and component qualification
are still being authored. No complete schematic, PCB placement, copper routes or fabrication files
exist. See `VALIDATION.md` for evidence and gates.

## A1 preview scope — latest user priority, 2026-10-03

The user explicitly permits a complete provisional schematic/placement before
full qualification, while still prohibiting routing. External protected battery,
speaker and motor use genuine imported PCB connectors; their exact enclosure
models can remain provisional. This supersedes earlier unresolved permission
for an externally sourced protected battery and the old absent-speaker/motor
import gates for this preview. All PCB electronic components remain genuine JLC
imports; imported definitions are not manually patched. The historical C370970
and C5656610 exceptions retain their narrow scope.

Four layers/1.6 mm/3 mm board corners are preview assumptions, not a released
manufacturing stackup. The LCD envelope is 33.7 × 42.94 mm, active 28.03 × 35.04 mm,
center (0, -3); it sits above top assembly with unqualified vertical separation.
The module antenna overhang and all-layer exclusion are explicit; RF clearance
from the final LCD, harnesses, pack, metal and enclosure still needs review.
Charging starts in hardware USB100; TMR/ITERM remain intentionally open for TI's
default safety timer/termination. TS goes to actual external pack NTC, with no
fake thermistor resistor. Pack capacity alone does not qualify current or safety.
