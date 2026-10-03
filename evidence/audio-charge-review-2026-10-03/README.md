# A0 amplifier application and charging intake — 2026-10-03

Independent, unrouted diagnostic work. The complete board is still unfinished;
no copper, route cache, fabrication package or hardware tests exist.

The native 46 × 32 mm amplifier fixture has 17 top-side components, 53 rectangular
pads and 53 native paste shapes. Build and all five required connectivity / placement
checks exit 0; command results are preserved. C51 was rotated 180 degrees to
resolve a native placement advisory. Connector faces the right edge. Native A4
schematic and PCB renders were inspected. The missing Q1/Q2 schematic references
remain actionable B-008; snapshot acceptance and component qualification are
withheld. Imported components/models remain byte-for-byte native imports.

The full generated JSON fails the published schema in 19 elements (B-010),
including numeric component display offsets and null group fields. The existing
board regression remains failing; new manufacturer connection tests pass.
Board total: 14 pass, 1 fail, 107 assertions. Formatting and TypeScript pass.
No global board stage is passed by these diagnostic results.

C265101 / JST S3B-PH-SM4-TB(LF)(SN), C132554 / TI TUSB320LAIRWBR,
C2862740 / TI TPS7A2033PDBVR and C6617702 / Panasonic EVQ-P4HB3B imported
successfully as candidates. Manufacturer land, orientation, current/startup,
mechanics and actual application qualification remain unfinished. C20917 /
AO3400A and C15127 / AO3401A successfully imported but reproduce B-008.

B-012: native imports C3311258 / PUI Audio AS04008PS-4W-R, C6230316 /
Taoglas SPKM.20.8.A and C50387211 / XHXDZ 23MM-8Ω2W-JFHM fail because
no EasyEDA library records exist. The first two were independently confirmed
by the fix chat. No substitute electronic definition was authored. Speaker
selection/procurement and series inductance remain unqualified. PUI drawing
page 3 inspected: 40±0.2 × 28.3±0.2 mm body, 12±0.5 mm depth, four Ø3.1
mounting holes. It is not the earlier assumed 40 × 20 mm package.

B-004: exact MPN discovery queries for RC0603FR-07470KL and
RC0603FR-07430KL imported unrelated C16195750 (inductor) and C326810
(510 kΩ 2010 resistor). These are rejected, unwired research imports. Exact
supplier IDs must be used; query-result identity never substitutes qualification.

Git c82e7deb display review is verified on private main. Native private version
0.0.2-wip-a0-display-logic-review exited 1: 582 successes and 4 failures.
Both timed-out STEP files reached the server byte-for-byte; the HTTP413 model
and PDF return404. ready_to_build=false. Exact readback receipt and native log
are saved here. No publication success, forced-ready flag or file dropping.

All material findings were sent to the user-authorized fix chat. The protected
battery sourcing exception still awaits the human reply. No pack or thermistor
is bypassed or replaced with a fabricated definition.

Exact queries were resolved with supplier-verified C114622 / RC0603FR-07470KL
and C482869 / RC0603FR-07430KL; both imported successfully, remain unwired
charging candidates. C7666 / TI SN74LVC1G08DBVR also imported for startup
qualification logic. No wrong search result was used in the circuit.
