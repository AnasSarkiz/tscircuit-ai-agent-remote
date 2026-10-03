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
