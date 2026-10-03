# Rechargeable power engineering review — A0

2026-10-03. Draft requirements and application circuit; **not a qualified battery
system or a fabrication approval**. The full handheld still has no placement or
copper. The isolated regulator fixture remains unrouted.

## Architecture

USB-C 5 V → input protection → BQ24074 IN. Its BAT pins connect to the protected
1S pack; OUT feeds VSYS. TPS63802 converts VSYS to 3.3 V for the module, display
and microphone/logic circuits. The amplifier and selected haptic driver use VSYS
subject to their eventual operating limits. Keep speaker outputs differential;
neither terminal is ground.

The pack must specify 4.2 V charging, protection thresholds, continuous/pulse
discharge, charge current, temperature limits, NTC characteristics, dimensions
including protection and leads, and exact mating polarity. A bare cell is not an
acceptable substitute. EEMB LP503450 research found a **bare 950 mAh cell**,
34.5 × 52 × 5.3 mm; it is unselected and does not prove protected-pack fit.
[Manufacturer](https://www.eemb.com/product-138).

C295747 has two contacts. Temperature sensing therefore needs an additional
qualified harness/connector or a different qualified multi-contact pack connector.
Do not install a fixed resistor that makes a missing battery NTC appear valid.
The charging window must remain inside the chosen pack's limits, including
threshold and thermistor tolerances.

## Charger decisions still pending

For C54313, connect both BAT pins, both OUT pins, VSS and the exposed pad. TS is
for the battery NTC. Preserve safety timers. Status outputs require pullups to
3.3 V. EN2/EN1 = 00 selects USB100, 01 USB500, 10 resistor current limit and
11 suspend. Establish startup defaults and USB state control before wiring them.
[TI SLUS810N, pp. 8–9, 13, 29–30](https://www.ti.com/lit/ds/symlink/bq24074.pdf).

The imported 3 kΩ / 1% C126358 is only a charge-setting candidate: 890/3000 =
**296.7 mA nominal**, with factor/resistor corners **263.0–328.3 mA**. Use it only
if the chosen pack permits at least 328.3 mA over the intended conditions.
At 5 V input, 3 V battery and the maximum candidate current, charging alone
would dissipate approximately **0.657 W**; power-path and quiescent losses add to
that. This estimate does not qualify junction or battery temperature.

Default USB power depends on bus state. A Type-C receptacle and Rd resistors do
not themselves establish permission for the full system/charging load. No PD or
BC1.2 negotiation is selected. Review attach, enumeration, suspend and dead-pack
startup; keep high-current functions disabled until an adequate source or battery
is available. [USB-IF overview, p. 17](https://www.usb.org/sites/default/files/D1T1-2%20-%20USB%20Type-C%20System%20Overview.pdf).

## Regulator application circuit

Source: `src/power/regulated-3v3.tsx`; isolated A4 review entry:
`evidence/controls-review-2026-10-03/regulated-3v3.circuit.tsx`.

| Ref | Exact imported component | LCSC | Nominal function |
|---|---|---|---|
| U2 | TPS63802DLAR | C2845237 | Buck-boost |
| L1 | DFE201612E-R47M=P2 | C668312 | 470 nH |
| C4 | GRM188R61A106ME69D | C90053 | 10 µF, 10 V input |
| C5 | GRM188R61A226ME15D | C84419 | 22 µF, 10 V output |
| R5 | RC0603FR-07511KL | C188257 | 511 kΩ, 1% feedback high |
| R6 | RC0603FR-0791KL | C137671 | 91 kΩ, 1% feedback low |
| R7 | RC0603FR-07100KL | C14675 | 100 kΩ PG pullup |

U2 pins: 1 EN→VSYS; 2 MODE→GND; 3 AGND→GND; 4 FB→divider;
5 PG→pullup; 6 VOUT→3.3 V; 7 L2→L1; 8 GND→GND; 9 L1→L1;
10 VIN→VSYS. MODE low selects automatic power saving. Capacitors and inductor
follow TI's application recommendations. Effective capacitance must remain
≥4 µF input and ≥7 µF output; effective inductance must meet 0.37–0.57 µH.
Manufacturer bias/current curves and actual power-loop placement remain pending.
[TI SLVSEU9D, pp. 4–7, 17–20](https://www.ti.com/lit/ds/symlink/tps63802.pdf).

The current divider follows TI's 3.3 V application choice: **511 kΩ / 91 kΩ**,
nominal **3.3077 V**. Including initial 1% resistance tolerance, provisional
100 ppm/K drift over −20…85 °C, 0.495…0.505 V PWM reference and ±100 nA FB bias
gives calculated static corners **3.1352…3.4849 V**. The lower resistor's maximum
is 92.456 kΩ, below TI's 100 kΩ recommendation. Effective capacitor/inductor
behavior, actual resistor temperature coefficients, PFM behavior, line/load,
ripple, transients and self-heating still require qualification. These corners
are not a qualified rail range. The previous 560 kΩ / 100 kΩ calculation is
historical in the power-review evidence. Current native build and five isolated
checks exit 0 with zero count-reported warnings; current PCB and A4 previews
were inspected. No PCB traces or vias exist.

Calculation: `evidence/controls-review-2026-10-03/feedback-corner-review.json`.

## Preliminary load envelope

Allocate **650 mA peak on 3.3 V** for the initial study, subject to the final
display and full-load review. Espressif lists a 355 mA Wi-Fi TX peak under its
stated conditions; that is not a guaranteed whole-device current ceiling.
[Module datasheet, p. 28](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf).

At an assumed 2.8 V VSYS and assumed 80% conversion efficiency, that rail
requires **0.958 A** upstream. Adding provisional **0.4 A amplifier**, **0.1 A
haptic** and **0.03 A other VSYS load** gives **1.488 A**. These are design
allocations, not selected-load specifications or proof of a peak-current bound.
Target at least 2 A pack/harness capability with margin; verify the C295747 rating,
wire gauge, protection trip thresholds and simultaneous audio/radio behavior.
Do not infer safety merely from a connector's nominal current rating.

The 8 Ω amplifier datasheet lists typical 0.77 W at 3.7 V and 1% THD+N under
its test conditions. Select speaker power/inductance ratings and maximum VSYS,
then calculate real current. Do not use software gain alone as a power guarantee.
[ADI MAX98357A/B, pp. 4–5, 33](https://www.analog.com/media/en/technical-documentation/data-sheets/max98357a-max98357b.pdf).

Battery runtime, charge time, low-battery cutoff, thermal performance and fault
behavior remain unvalidated. They require the exact pack/load specifications,
generated copper review and later physical prototype measurements.
