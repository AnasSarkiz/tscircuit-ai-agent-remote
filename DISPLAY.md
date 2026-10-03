# A0 display interface review — 2026-10-03

This is a partial, unrouted application study, not a qualified handheld display.
All 19 PCB parts use untouched exact JLC imports and top-side assembly.
`src/display/display-logic-review.tsx` implements the 2.8 V logic interface;
backlight, external LCD mounting/cable, power sequence and current budget remain
unfinished. The full board entry point remains guarded.

## Manufacturer limits and interface

The exact HS17QS178RX / C5329581 drawing specifies 2.7–3.3 V VDD, nominal
2.8 V; input absolute maximum is VDD + 0.3 V. Its supply-current fields are TBD.
Do not assume a 20 mA supply limit or drive it directly from the provisional
3.182–3.438 V main rail. Screen is 1.77 inch, 128×160; its 33.70×42.94 mm
body and 17.28 mm FPC tail still require actual enclosure/bend/access review.
Source: `references/HS17QS178RX.pdf`.

TPS7A2028PDBVR / C2869847 provides 2.8 V ±1.5% with VIN≥3.1 V and
1–300 mA output over its specified temperature range. A 1 kΩ, 1% output bleed
sets minimum load above 2.73 mA, covering the accuracy condition while providing
an off-state discharge path. It consumes about 2.8 mA whenever enabled.
The provisional 3.182 V rail minimum leaves 82 mV before the LDO accuracy
input condition; ripple and transients are unverified. Effective bypass
capacitance, total LCD/driver load and thermal headroom are pending.
Source: https://www.ti.com/lit/ds/symlink/tps7a20.pdf

SN74LVC245APWR / C7848 runs from VLCD with DIR high and /OE grounded.
MCU CS/reset/DC/clock/data go A1–A5; B1–B5 go to LCD contacts 5–9.
Unused A6–A8 are grounded; B6–B8 are open. Input thresholds at 2.7–3.6 V
are VIH=2.0 V / VIL=0.8 V. Its guaranteed 2.2 V output high at 12 mA
exceeds the LCD's maximum 0.7×2.842=1.9894 V threshold; 0.4 V low is
below the minimum 0.3×2.758=0.8274 V threshold. The 10 kΩ output loads
stay below 0.29 mA. This does not prove signal timing or full-temperature MCU
input-drive bounds. Source: https://www.ti.com/lit/ds/symlink/sn74lvc245a.pdf

All MCU-side inputs have 100 kΩ pulldowns. LCD-side CS has 10 kΩ to VLCD;
reset/DC/clock/data have 10 kΩ to ground. LCD_ENABLE has a 100 kΩ pulldown.
With VCC exactly zero, the buffer's ±10 µA Ioff at ≤85°C implies at most
0.1016 V into a 10 kΩ resistor with the provisional ±1.6% allowance, below
LCD's 0.3 V unpowered input ceiling. Five channels into the 1 kΩ bleed imply
about 50.8 mV, making the CS estimate about 152.4 mV after its pullup
rail offset is included. This is a limited DC estimate, not proof during partial-power
ramps or all possible back-power paths. Power sequencing needs native circuit
integration and physical checks. Firmware must initialize CS/reset/data/clock
before enabling VLCD; system-off behavior must also be verified.

## Connector and unfinished backlight

J7 is AFC07-S10FCC-00 / C11050, 10 contacts, 0.5 mm pitch, bottom contact,
0.3 mm FFC thickness. Pin 1 LEDK, 2 LEDA, 3 VDD, 4 TE (unused), 5 CS,
6 reset, 7 DC, 8 clock, 9 data, 10 ground; anchors 11/12 grounded.
Actual cable contact orientation and tail mating are unverified. The current
land drawing's one-decimal tolerance is ±0.20 mm: imported anchors 2.0×2.8
versus nominal 2.0×3.0, and contacts 0.3×1.5 versus nominal 0.3×1.3 are
at that tolerance boundary. B-011 is NOT a demonstrated footprint defect;
no imported geometry was edited. Drawing date is 2004.6.16. Revision
applicability and mating fit remain qualification questions.
Source: https://jlcpcb.com/partdetail/Jushuo-AFC07_S10FCC00/C11050

The LCD has two parallel backlight LEDs: 40 mA ±10% total, 3.0–3.4 V Vf.
TPS61160DRVR / C165143 is an imported research candidate, not yet wired.
A boost-only current driver fed by the main rail cannot cover the low-Vf corner
where Vf+0.2 V < 3.438 V; its output path also needs an off-state review.
Feeding from VLCD leaves little margin above its 2.7 V input minimum and must
include switch drop/ripple and the LCD's unknown supply current. Exact driver,
inductor/diode/capacitors/sense resistor and shutdown topology are pending.
Source: https://www.ti.com/lit/ds/symlink/tps61160.pdf

## Native evidence

Fixture: `evidence/display-review-2026-10-03/display-logic.circuit.tsx`,
45×32 mm diagnostic canvas, A4 schematic, routing disabled. Build and all five
required connection/placement commands exit 0 after connector rotation and
capacitor spacing corrections. Schematic-placement output is empty, PCB
placement reports zero errors/warnings. Native PCB and A4 outputs were inspected.
Five imported metadata warnings remain visible (J-prefix convention, J7 pin
roles, LDO power role); no definitions or pin attributes were patched.
The native JSON has 19 top-side components, zero traces/vias/errors. B-010
schema failure still blocks whole-board qualification. This fixture does not
pass a final handheld placement, DRC, fabrication or physical-test gate.
