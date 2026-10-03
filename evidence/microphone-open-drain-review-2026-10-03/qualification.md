# Regulated microphone clock candidate — A0 WIP

This independent application review does not complete the board schematic,
placement, privacy qualification or fabrication gates. Parent revision:
`a1e76d5f2879d74b68d882c3ea5576359b0ccc42`. Exact candidate source and native
Circuit JSON hashes are in `source-manifest.json`. Routing remains disabled.
No purchased component definitions were modified.

## Finding and candidate

TDK ICS-43434 C5656610 supply operation allows up to 3.63 V, but its I²S
Table 5 specifies timing and input thresholds for **1.8 < VDD < 3.3 V**.
The previous VMIC supply follows the provisional main rail, whose calculated
static range is 3.18204–3.43818 V. The upper end is outside Table 5's stated
conditions. This is a hardware qualification gap, reported to the authorized
fix chat; it is not evidence of a converter defect.

The new candidate uses genuine TI TPS7A2028PDBVR C2869847 as a dedicated
microphone regulator. Its physical SOT-23 pin 1 is IN, 2 GND, 3 EN, 4 NC and
5 OUT. EN is connected to HOLD_HARDWARE, with an external 100 kΩ ground
pulldown. No MCU net drives EN. NC remains open. The 1 kΩ output bleed draws
at least 2.71 mA under the stated resistor assumptions, exceeding TI's 1 mA
minimum load for the ±1.5% output-accuracy specification. Conditional output
range: **2.758–2.842 V**. TI requires VIN ≥ 3.1 V for this accuracy; the
provisional main-rail static minimum provides only 82.04 mV of margin.
Dynamic main-rail droop, startup and capacitor effective values remain to be
qualified before integration. Output-discharge resistance is **150 Ω typical**,
not a guaranteed maximum or a proven release-to-off deadline.

Genuine Nexperia 74LVC2G07GW,125 C24478 is powered from VMIC. Physical pin
1 is 1A, 2 GND, 3 2A, 4 2Y, 5 VCC and 6 1Y. MCU BCLK and WS enter through
100 Ω resistors with 10 kΩ input ground pulldowns. Each output has a genuine
YAGEO RC0603FR-07330RL C105881 330 Ω pullup **to VMIC** and a 10 kΩ ground
pulldown. Open-drain outputs cannot actively drive a clock high from an
always-on rail. The buffer preserves clock polarity. This application has
no microphone SD path; the existing comparator application still needs
integration review against the changed VMIC rail.

TI SN74LVC2G07DCKR C7849 was also genuinely imported for comparison. It is
not used in this candidate. Its and Nexperia's imports remain unmodified.
Current supplier stock, assembler qualification and final BOM selection
remain to be checked; successful import is not proof of continued availability.

## Conditional voltage and timing calculations

`voltage-and-clock-calculations.json` records assumptions and formulas' basis.
For -40 to +85 °C, ±1% initial resistor tolerance plus ±100 ppm/°C gives a
conservative ±1.75% resistance envelope relative to 25 °C. This is a component
calculation range, not a new product operating-temperature specification.

- Maximum pullup sink current is 8.77 mA; Nexperia specifies VOL ≤ 0.4 V at
  12 mA and VCC = 2.7 V through +85 °C (0.6 V through +125 °C). Even using
  0.6 V gives 0.2274 V margin to the microphone's minimum 0.3 × VDD limit.
- The minimum resistor-only clock-high ratio is 0.96695 × VMIC. A conditional
  2 µA leakage estimate leaves approximately 0.736 V high-level margin.
  **Nexperia tests IOZ at VCC = 5.5 V**; the 2.8 V calculation does not invent
  an additional manufacturer guarantee.
- The microphone requires SCK rise/fall ≤ 25 ns, high/low ≥ 50 ns and
  40–60% duty cycle. At the target 16 kHz/64 SCK frame, BCLK is 1.024 MHz.
  Conservatively evaluating 10–90% of VMIC, with the final high below VMIC
  due to the pulldown and conditional leakage, requires total clock load
  **≤ approximately 30 pF**. Using ln(9) alone would omit this final-level
  correction and overestimate allowable capacitance.
- TDK does not give a maximum SCK/WS input capacitance. Both microphones,
  buffer output, traces and any connector load must be included. Its 85 pF
  SD output load rating does **not** specify clock input capacitance.
- The 330 Ω resistor's worst static dissipation is approximately 24.9 mW,
  below its 100 mW rating at 70 °C; temperature derating still applies.

Clock capacitance/rise/fall/duty, startup, partial-power AC feedthrough,
off-state rail injection and release-to-off timing remain **unqualified**.
II/Ioff DC test limits do not prove system-level privacy under arbitrary
GPIO toggling or supply ramps. No physical measurements have been performed.

## Native checks and visual review

Pinned versions remain tscircuit 0.0.2742, core 0.0.2058, CLI 0.1.2235 and
Circuit JSON 0.0.510. Native build and all five diagnostic checks exit 0:
netlist, pin_specification, source, schematic-placement and placement.
The initial placement check exited 1 for C74's connection orientation;
rotating that application instance by 180° cleared it. The initial log is
preserved. No footprint was patched. The fixture contains 15 top components,
37 pads and 37 paste entries, **zero PCB traces, zero vias and zero native
Circuit JSON error elements**. It is intentionally not an assembled board.

The sandboxed initial build could not reach supplier footprint endpoints;
the network-enabled native rebuild resolved those fetch warnings. Both logs
are retained. PCB PNG and native schematic PDF were inspected. The PDF is
one landscape A4 page (841.89 × 595.28 points); connections and reference
labels are readable. Native schematic and PCB SVGs are preserved.

Formatting and TypeScript checks exit 0. Two new native-JSON hardware boundary tests pass: regulator enable belongs
only to HOLD_HARDWARE and ground bias; both open-drain clock pullups belong
only to VMIC. These checks do not simulate power-off behavior. The canonical
board test suite reports
21 pass, 1 fail, 204 assertions; the existing strict MCU schema test fails
B-010. Independently applying the unchanged strict schema to every candidate
JSON element finds **17 invalid elements**. The original JSON is retained;
`native-schema-summary.json` lists every failing element index and type with
top-level schema issue summaries. Union suberrors are not duplicated in this
summary; reproduce from the original JSON and unchanged pinned schema. No
schema, source output, tests or checker were weakened.

The microphone C5656610 paste issue B-005, physical hold-switch qualification
B-006 and missing comparator references B-008 remain. The candidate does not
integrate those blocked imports, replace them with placeholders, enable full
board routing or mark a fabrication gate passed.

## Manufacturer sources reviewed 2026-10-03

- [TDK ICS-43434 Rev 1.2](https://product.tdk.com/system/files/dam/doc/product/sw_piezo/mic/mems-mic/data_sheet/ds-000069-ics-43434-v1.2.pdf),
  Table 5 p6. Manufacturer-host download returned 403; the matching
  TDK-authored Rev 1.2 supplier mirror is preserved as `ICS-43434.pdf`.
- [TI TPS7A20 Rev H](https://www.ti.com/lit/ds/symlink/tps7a20.pdf), pp4,6–7;
  board `references/tps7a20.pdf` remains unchanged.
- [Nexperia 74LVC2G07 Rev 13](https://assets.nexperia.com/documents/data-sheet/74LVC2G07.pdf),
  pin diagram, DC conditions and timing tables. Matching Rev 13 supplier
  mirror saved as `74LVC2G07-nexperia.pdf` after manufacturer-host 403.
- [YAGEO RC0603FR-07330RL](https://yageogroup.com/component-documentation/download/specsheet/RC0603FR-07330RL),
  exact 330 Ω part specification; web-rendered sheet generated 2026-10-02,
  preserved manufacturer download generated 2026-10-03.
- [TI SN74LVC2G07](https://www.ti.com/lit/ds/symlink/sn74lvc2g07.pdf),
  comparison only; PDF preserved as `sn74lvc2g07.pdf`.

Official releases were rechecked: core 0.0.2063 is unchanged; latest CLI
0.1.2237's current gitHead differs from the previous check by a version bump
in package.json only. Neither check verifies publication of the required
fixes. No dependency update was applied.

Git whitespace inspection reports unchanged native SVG blank-line spaces, a
native netlist trailing blank line and carriage-return lines inside the original
manufacturer PDF (Git classified that PDF as text). These diagnostic outputs
were not rewritten; source formatting passes. This is not acceptance of a
board DRC violation, schema failure or fabrication warning.
