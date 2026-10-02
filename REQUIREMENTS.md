# AI Remote — accepted product direction

Updated 2026-10-03 from the user's direct follow-up instructions. These requirements
supersede conflicting controls and enclosure styling in `references/user-brief.txt`.
The original brief is preserved as historical input.

## Form and interaction

- Compact square enclosure with rounded corners and a display dominating the front.
- Exactly one exterior physical control: a top-edge hold-to-talk button.
- Hold → speak → release → send over Wi-Fi → show and speak the AI response.
- No exterior encoder, APPROVE/REJECT buttons, privacy slider or separate power button.
- Status indication belongs on the screen; no separate front status LED is required.
- Top-side PCB assembly only: all populated electronic parts and connector solder
  joints must be assembled from the top. Four copper layers remain intended.
- Enclosure-mounted speaker and rechargeable battery connect to the top-side PCB;
  they are separate mechanical parts, not bottom-side PCB population.
- USB-C access at the bottom edge. Speaker grille and microphone acoustics must
  follow the real parts and acoustic paths, rather than the illustration alone.

Accepted visual reference: `assets/product-concepts/ai-remote-v1-infographic-v3.png`.
This is a concept illustration, not dimensioned CAD or a validated placement.

Start the mechanical study with a **50 × 50 mm square PCB target**, within the
previously approved maximum 50 × 65 mm envelope. The 50 × 50 mm target is an
engineering assumption, not a completed fit review. Final enclosure dimensions,
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

Stage 1 remains in progress. Stage 2 remains blocked by B-002: C5656610's fresh
import still contains a 0.3999992 mm acoustic hole, below TDK's recommended 0.50 mm
minimum. No complete schematic, PCB placement, copper routes or fabrication files
exist. See `VALIDATION.md` for evidence and gates.
