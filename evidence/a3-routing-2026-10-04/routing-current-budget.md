# A3 copper design allocations — 2026-10-04

Untested prototype engineering allocations, not measured consumption. Four-layer JLC04161H-7628 assumed, 1.6 mm FR4, outer 35 um copper / inner 17.5 um. The prior manufacturer stackup study supplies outer-to-L2 dielectric 0.0994 mm and calculated USB 90-ohm nominal geometry: 0.2906 mm width / 0.1999 mm edge gap. Actual manufacturing stackup and impedance require assembler confirmation. Ordinary vias: 0.30 mm drill / 0.70 mm land; clearance 0.20 mm, copper-edge 0.25 mm, NPTH clearance 0.25 mm. Fine component lands constrain local fanout; no generic width is proof of safe copper.

| Net / load | Continuous allocation A | Peak allocation A | Intended main copper width mm |
|---|---:|---:|---:|
| VBUS | 0.15 | 0.15 plus unmeasured attachment inrush | 0.50 |
| PACK_BAT internal known nets | 1.50 | 2.00 | 1.00 |
| VSYS | 1.50 | 2.00 | 1.00 |
| V3V3 | 0.50 | 0.75 | 0.80 |
| VLCD logic | 0.08 | 0.10 | 0.30 |
| LCD backlight output / return | 0.052 | 0.060 | 0.30 |
| AUDIO_ENABLE_SUPPLY | 0.35 | 0.75 | 0.60 |
| SPEAKER_P / SPEAKER_N | 0.35 RMS | 0.75 | 0.60 |
| VMOTOR / HAPTIC_N | 0.11 | 0.15 | 0.40 |
| VMIC / MIC_INPUT | 0.01 | 0.02 | 0.30 |

VBUS BQ24074 EN1/EN2 both GND selects nominal USB100 mode; allocation includes limit tolerance, and is not entitlement to high-current USB charging. C1 changed from 10 uF +/-20% to genuine C19666 4.7 uF +/-10%: nominal attachment-capacitance maximum 5.17 uF before other parasitics. Charge allocation and actual inrush remain unmeasured.

V3V3 peak allocation: ESP32 0.5 A, LCD logic 0.1 A, microphones/control 0.05 A, backlight input 0.1 A. At 3.438 V, 3.023 V VSYS and assumed 80% conversion efficiency, regulator input allocation is 1.066 A. Together with 0.75 A amplifier peak, 0.15 A motor and 0.02 A other loads: 1.986 A. This is a conservative routing target, conditional on load limits/efficiency; no guaranteed simultaneous operating envelope is claimed. PH connector's 2 A rating assumes AWG24; exact supplied battery harness wire gauge remains a fabrication qualification item. Two J3 outer contacts stay OPEN until manufacturer-numbered polarity is established.

External speaker interface is 8 ohms. Intended playback <=0.7 W (software setting unimplemented), nominal RMS 0.296 A / peak 0.418 A. At a 15%-low 6.8-ohm load and 4.4 V rail an unclipped full-scale ideal peak can reach 0.647 A; copper uses 0.75 A. Slim PUI AS01508AO-WP-R envelope is a candidate, not procurement acceptance. A rated/available external speaker and real amplifier clipping/temperature tests remain required.

LEADER LCM0720A3176F manufacturer specification: rated 3.0 V, operating 2.7–3.3 V, rated <=85 mA, start <=120 mA. 0.11 A continuous and 0.15 A peak allocation include margin; selected 3.0 V TPS7A20 supply and AO3400 low-side switch retain transient diode. Locked rotor / high-temperature / harness behavior not physically tested.

Outer-layer IPC-2221 estimate (k=.048; A in mil^2), 35 um, 10 C rise gives approximately 1.00 A at 0.30 mm, 1.45 A at 0.50 mm, 2.03 A at 0.80 mm and 2.39 A at 1.00 mm. 2 A through 1.00 mm estimates ~6.7 C rise. These are screening estimates, not measured thermal qualification; local component-pad fanouts, actual vias and plane heat spreading must be audited from generated copper.

## Backlight

Genuine C544659 TPS60231RGTR replaces the earlier provisional transistor architecture. Three current sinks tied to LCD common cathode; VOUT to common anode. EN1/EN2 tied together with genuine 10k external pulldown and 100-ohm MCU series resistor. VIN is V3V3 so the enable input cannot be driven by a higher independent 3V3 rail during ordinary VSYS sag. TPS60231 input operating range 2.7–6.5 V; current-sink recommendation 25 mA each for VIN>=3.2 V; main rail calculated 3.182–3.438 V leaves low-corner brightness regulation to prototype qualification.

RSET C114639 9.1k +/-1% gives 3 * .6 / 9100 * 260 = 51.43 mA nominal total. Datasheet voltage/coefficient corners .58/.62,230/280 and resistor tolerance produce illustrative 43.54–57.81 mA; ratio limits have specified test conditions and are not a guarantee over every supply/temperature. Manufacturer LCD drawing lists three parallel LEDs while its text lists four; combined nominal 80 mA / LED forward voltage about 3.2 V. Shared current regulation is unaffected by the count ambiguity; maximum brightness is deliberately not claimed. LCD backlight should remain OFF at boot. Firmware PWM <=50 kHz and ON pulse >=2.5 us; proposed 1 kHz with duty below .25% treated as OFF. Actual firmware, partial-rail and startup tests pending.

C82/C83 genuine C15849 CL10A105KB8NNNC 1 uF flying capacitors, C84/C85 10 uF input/output. Effective capacitance/DC bias and startup/ripple require qualification, and driver thermal-pad paste remains affected by B-005. No imported geometry or fabrication outputs manually repaired.
