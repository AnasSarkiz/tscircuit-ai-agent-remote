# Microphone privacy and interface review — A0

2026-10-03. An independent application review, not a completed or hardware-tested
privacy circuit. Entry: `evidence/controls-review-2026-10-03/isolation-ics.circuit.tsx`.
The actual microphones and hold switch are absent because their qualification is
blocked. All 24 review components assemble on top. Routing remains disabled.

The hardware hold node drives TPS22919's ON input and a separate buffered status
path. No MCU output connects to ON or the contact node. VMIC powers the microphones,
clock-buffer candidate and voltage supervisor. QOD connects to VMIC; a 1 kΩ bleed
resistor adds a defined passive discharge path. TPS3839 monitors VMIC and its
reset signal, inverted by a Schmitt gate, controls clock-buffer enables. Hold
sensing and the SD receiver use the always-on 3.3 V rail; 1 kΩ series resistors
limit MCU pin contention. These are application decisions, not imported definitions.

The supervisor's threshold range is 2.857–2.974 V and its startup delay is
120–350 ms. Its typical hysteresis and the switch's typical discharge resistance
are not guaranteed timing limits. Microphone startup relative to clock enable,
button bounce, supervisor behavior below its reset-valid supply, power-up/down
slew, aggregate pin leakage and actual rail decay must still be checked.
[TI TPS3839](https://www.ti.com/lit/ds/symlink/tps3839.pdf),
[TI TPS22919](https://www.ti.com/lit/ds/symlink/tps22919.pdf).

SD output guarantees from ICS-43434 are VOH≥0.65×VMIC and VOL≤0.35×VMIC.
They do not cover both input thresholds of the previous LVC/LV1T receivers.
The current diagnostic uses C105188 / TLV3201AIDBVR with a 10 kΩ/10 kΩ divider
from VMIC, filtered by 100 nF, as its negative input. SD drives the positive input
and has a 100 kΩ pull-down. Pins 1/2/3/4/5 are OUT/GND/IN+/IN−/VCC, verified
against the rendered manufacturer drawing. Its specified switching maximum is
55 ns with 100 mV overdrive and 15 pF load at the listed supply/temperature
conditions. The reference and SD connections are one-way sensing paths; there
is no MCU output wired to microphone SD.
[TI TLV3201, pp. 3, 5–6](https://www.ti.com/lit/ds/symlink/tlv3201.pdf),
[TDK ICS-43434](https://product.tdk.com/system/files/dam/doc/product/sw_piezo/mic/mems-mic/data_sheet/ds-000069-ics-43434-v1.2.pdf).

A provisional voice target is 16 kHz, 64 clocks/frame (1.024 MHz SCK, 488.3 ns
half-period). Final receiver capacitance, comparator/clock delays, SD settling,
MCU setup/hold and microphone operating mode still require a complete timing
budget. This arithmetic alone is not a guaranteed timing pass. Clock-buffer
high/low margins, its 10 kΩ output loads and all intermediate power-off voltages
also remain unresolved; alternative hardware clock-disconnection circuits are
being evaluated. No privacy-off deadline or guaranteed rail range is claimed.

B-005 blocks microphone stencil qualification. B-006 blocks C79174 contact pairs
and locating holes. B-007 leaves the C2149796 supply metadata warning visible;
the actual supply connection was manually checked. B-008 blocks C105188's missing
schematic reference label. No import or checker was modified to conceal them.
The current native build and five connectivity/placement checks exit 0 with those
documented warnings; this does not pass any complete-board validation gate.


## Independent speaker amplifier review — 2026-10-03

`src/audio/speaker-amplifier-review.tsx` implements an unrouted native A4
application using MAX98357AETE+T / C910544, AO3400A / C20917,
AO3401A / C15127 and JST C295747. Evidence, actual command results and
manufacturer connection checks are in `evidence/audio-charge-review-2026-10-03/`.
It is not the final microphone circuit or a qualified whole-board placement.

ADI's Rev16 datasheet: VDD2.5–5.5V; digital inputs VIH1.3/VIL0.6V and
absolute input limit6V independently of VDD. Supply bypass10µF plus100nF;
gain pin2 tied to VDD selects6dB; ground pins3/11/15 and exposed pad17 grounded.
Speaker connects between pins9/10, neither output grounded. Speaker inductance
must exceed10µH and actual power/thermal/EMI qualification remains pending.
[ADI MAX98357A/B](https://www.analog.com/media/en/technical-documentation/data-sheets/max98357a-max98357b.pdf).

The shutdown pin has VDD+0.3V absolute limit and B0 minimum0.08V / B2 maximum1.5V.
The NMOS gate has100Ω series/10kΩ ground pull-down; it pulls down a PMOS gate
with1kΩ VSYS pull-up. PMOS sourceVSYS/drain through100Ω drives shutdown,
with1kΩ pull-down. At assumed VSYSmin2.8V the enabled pin exceeds2.52V.
16kHz/64Fs is the provisional I2S target; disable before stopping clocks.
Never stop LRCLK while BCLK runs. 8kHz/32Fs has additional startup sequencing
and is not this fixture's operating target. Firmware and measured timing remain pending.

AOS G/S/D pins1/2/3 were checked against primary drawings. Both tolerate±12V
VGS and specify on-resistance at2.5V gate magnitude. The 100Ω gate resistor
preserves >=2.519V from the provisional MCU VOH floor; the earlier1kΩ candidate
would not preserve the guaranteed2.5V drive condition. At TJ55°C the specified
5µA PMOS leakage gives <=5.08mV on1kΩ, below the80mV shutdown boundary.
This is a limited static calculation, not a guarantee across85°C or intermediate
rail ramps. Temperature, parasitic capacitance, hot on-resistance and shutdown
transients must still be qualified. Gate pull-up1kΩ consumes up to4.5mA when on;
external shutdown pull-down adds up to4.5mA. Approximate combined bias40mW
belongs in the system budget, not the speaker efficiency claim.
[AOS AO3400A](https://www.aosmd.com/pdfs/datasheet/AO3400A.pdf),
[AOS AO3401A](https://www.aosmd.com/pdfs/datasheet/AO3401A.pdf).

B-008 now includes both MOSFET symbols' missing references; no symbol edit
was made. B-012 blocks speaker imports C3311258/C6230316/C50387211. The
PUI C3311258 drawing is40×28.3×12mm,2W rated/4W maximum,8Ω±15%; actual
minimum impedance and inductance across frequency, enclosure/harness and
procurement remain pending. At VSYS4.5V a rail-limited ideal sine into6.8Ω is
1.49W; this is not a bound on clipped signals, PWM heating or clock-fault DC.
[PUI manufacturer drawing](https://api.puiaudio.com/filename/AS04008PS-4W-R.pdf).

Native build/required checks pass for this diagnostic. Actionable symbol warnings
and19 strict JSON schema failures remain visible; snapshots are not accepted
while reference labels are missing. No routing, copper or full-board stage pass.
