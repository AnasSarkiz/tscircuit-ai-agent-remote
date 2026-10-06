# Six-point board review — 2026-10-06

**NOT READY TO ORDER. Placement and complete electrical connectivity are not
approved.** The review identifies new decoupling-placement problems and the
exact adapter needed for the requested Standard JST programmer. No board parts,
placements, saved copper, imports, dependencies or native output were changed.

Reviewed Git parent: `02035bbec54e20763c8f6e401b25fffeca1b7898`.
Native SHA256: `81c31f77ac0871bfc4414b0940752e4f4fe0692a62089320b409908d4a8d5315`.
The [previous same-day full audit](../order-readiness-2026-10-06/review.md)
remains applicable to this exact unchanged native board. Its completed native
render and physical copper measurements are not described as new executions.

| Requested check | Verdict | Evidence |
| --- | --- | --- |
| 1. Correct placement | **Fail electrical qualification** | Overlap/native placement checks pass, but MCU/microphone bypass layout needs correction; final mechanics remain unqualified. |
| 2. Correct components | **Partially verified; blocked overall** | Exact125 purchased parts/43JLC identities; critical pin tests pass. Load, thermal, effective capacitance, interface mating and assembly qualification remain incomplete. |
| 3. Available at JLCPCB | **Current stock unverified** | Current lookup is blocked by proxy403; all43 part statuses explicitly retain dated historical stock. |
| 4. Correct nets / board will work | **Fail physical connectivity** | 26 physically open nets,90 native port errors and two additional unassigned battery contacts. Logical pin tests do not complete copper. |
| 5. Standard JST programmer | **Conditional UART compatibility** | Public v0.8.0 has J5UART, but its3-pin socket cannot directly mate with board6-pinJ6. Adapter, separate power, matching firmware and manual BOOT/RESET required. |
| 6. No board/connection issues | **Fail** | Placement, copper, power-width, external-interface, schema, paste and fabrication gates remain open. |

## Placement findings beyond overlap checks

[Native supply-to-capacitor measurements](decoupling-placement.json) cover19 IC
supply pins. Distances are Euclidean native port-centre distances, a lower bound
on interconnect length; they are not measured loop inductance or an invented
maximum-distance rule. Nearest candidates must have the same named supply and a
GND-return terminal. Copper-island equality is recorded separately.

| Supply pin | Assigned bypass capacitor | Pad-centre distance | Finding |
| --- | --- | ---: | --- |
| U1.2 ESP32 3V3 | C30 10µF | 26.160mm | Nearest external same-rail bypass is already26.160mm away. |
| U1.2 | C31 100nF | 36.000mm | Does not provide a short external local bypass connection. |
| U1.2 | C32 100nF | 41.556mm | Does not provide a short external local bypass connection. |
| U4.5 left microphone | C80 100nF | 4.414mm | Current via-based bypass layout needs correction against the manufacturer's short single-layer recommendation. |
| U5.5 right microphone | C81 100nF | 18.191mm | Different supply copper island; nearest same-rail bypass of any reference is C75 at15.601mm. |
| U23.1 microphone LDO input | C73 10µF | 13.364mm | Input bypass loop also needs review/relocation. |

TDK ICS-43434 DS-000069, **Power Supply Decoupling**, explicitly recommends
0.1µF X7R or better, capacitor close to the pins, shortest connections on one
layer **without vias**, and ground-plane connection on the far side of the
capacitor. Current C80/C81 and microphone supply escapes use separate vias;
their saved paths do not implement that local arrangement. The capacitor type
is suitable; its correct value alone does not qualify the layout.

Espressif ESP32-S3-WROOM-1 peripheral schematic shows22µF plus0.1µF externally.
The currently assigned MCU bulk capacitor is10µF and its100nF parts are remote.
Review local bulk/effective capacitance and supply/return geometry against the
manufacturer application before accepting Wi-Fi transient performance. The
module's internal capacitors do not qualify the baseboard supply path.

Primary PDFs: [Espressif](../../references/esp32-s3-module.pdf),
[TDK](../microphone-open-drain-review-2026-10-03/ICS-43434.pdf).
Their extracted text is preserved here; input PDF hashes are in
`review-input-receipt.json`. The actual current top PCB was inspected using the
unchanged [native view](../order-readiness-2026-10-06/visual-review/top.png).

The prior conditional placement freeze therefore cannot be treated as final
electrical acceptance. A corrective pass must move the bypass parts, connect
them locally, update affected authored copper, regenerate native output and
prove no new shorts, clearance, width or disconnected-ground failures. Existing
saved C31/C32/C80/C81 power/GND escapes are affected; moving coordinates alone
is not a completed fix. No speculative moved placement has been accepted.

Board50×65×1.0mm/four layers/top population fits the accepted nominal envelope;
the A7 height allocation15.092mm is below the16mm enclosure limit. This is an
allocation, not a physical fit test. Antenna overhang/all-layer exclusion exist;
actual metal/display/harness RF clearance, FPC fold, connector insertion access,
screw/pin-tail clearance and acoustic paths remain unqualified.

## Components, nets and power

Fresh current manufacturer regressions: **5pass /0fail,70 assertions** for
ESP32 supply/USB/BOOT/reserved PSRAM pins, charger/battery supervisor,
buck-boost pin identities, amplifier differential output and dual-microphone
pins/channel select. [Execution](manufacturer-pins.log).
This checks logical pin assignments, not all electrical operating conditions.
Current formatting and TypeScript checks pass; all336 checkpoint file hashes
remain unchanged. The two audit helpers executed successfully. These results
do not replace the unchanged whole-board47pass/2failed fabrication/schema gates.

The functional architecture remains compatible in principle: protected1S pack,
BQ24074 power path, TPS63802 nominal3.3V, ESP32-S3,2.8V display/microphone
domains, differential MAX98357A speaker output and regulated haptic supply.
Peak-load/transient/thermal and effective capacitor/inductor limits are not yet
qualified. USB100 policy limits input current; simultaneous active loads depend
on a correctly connected, suitably rated protected battery. Do not treat the
regulator's headline current rating or a capacitor's printed value as approval.

Existing physical audit: **0measured shorts /0measured clearance violations**,
but **26 open nets /90 port errors**, including USB/power/display/audio/mics.
GND has35 separate islands. J3.1/3 are unassigned additional omissions; centre
J3.2 is PACK_NTC. Exact pack numbered outer polarity and current display FPC
contact-face/pin1/mating evidence are still missing. These cannot be resolved
by reading an unrelated connector pinout or reversing the cable by assumption.

All306 traces/792 native segments were checked in the same-day audit. Two
regulator switching routes include0.275mm sections despite1.0mm source minima;
55 other branches are below their named net's nominal width and need current/
escape qualification. No segment is below the general0.20mm rule. This is not
a rated-current approval. See the complete per-trace CSV in the prior audit.

## Exact Standard JST programmer connection

Reviewed public [tscircuit/standard-jst-programmer](https://tscircuit.com/tscircuit/standard-jst-programmer#3d)
**v0.8.0**, release `3d6952c4-e6ee-4711-a7c7-dded0cdef4eb`.
Source and native JSON were downloaded anonymously with hashes recorded in
`programmer-source-receipt.json`. The native JSON is stored as lossless gzip;
`programmer-native-archive.json` verifies exact decompressed bytes and records
restoration instructions. The audit reads it directly. Borrowed TSX sources have
`.txt` snapshot suffixes and exact-byte hashes so they are not compiled as part
of this target board. Its **UART J5**, not its ARM SWD sockets, is
the appropriate interface for this ESP32-S3 UART ROM bootloader.

| Programmer J5,3-pin JST SH | Target J6,6-pin JST SH |
| --- | --- |
| 1: TX output,GPIO8 through100Ω | 6: MCU_UART_RX → U1.36 RXD0 |
| 2: GND | 1: GND |
| 3: RX input,GPIO9 through100Ω | 5: SERVICE_UART_TX ← R38 1kΩ ← U1.37 TXD0 |

This is a **custom3-to6 adapter**, not a direct straight-through3-pin cable.
J6.2(3V3),.3(EN),.4(BOOT) are left unconnected to J5. Numbered contacts must
be checked against actual connector drawings and adapter continuity; do not
identify pins from wire colours or an unverified viewing direction.

[Programmer compatibility audit](programmer-compatibility.json):5 host logical
edges and8 target logical/actual copper groups pass. The target checks include
UART, local shared GND,3V3,BOOT pullup and RESET control. They reuse hash-matched
physical measurements; they do not approve the35-island whole-board GND.
Host copper, real adapter continuity and actual programming were not tested.

U12 is **TPS3839G33DBZR, push-pull**, not an open-drain TPS3808. R35=4.7kΩ
connects its active-low reset to EN; R37=100kΩ pulls EN down, and R36=10kΩ
pulls BOOT high. Its push-pull output supplies EN's high state; the pulldown
is not by itself proof of a missing pullup. Startup/brownout timing, manual reset
loading and supply transients still need qualification. SW1 pulls BOOT to local
GND, SW2 pulls EN to local GND; these actual paths are connected.

After board qualification, the intended flashing procedure is:

1. Use programmer firmware built fromv0.8.0 source. The documented oldv0.5.0UF2
   does not bridge J5. No programmer firmware was built/flashed in this review.
2. Power the target separately through its qualified power input; UART J5 has
   no power pin. Logic is fixed3.3V irrespective of the programmer power selector.
   Do not apply5V to J6.2 or drive an unpowered target via UART.
3. Select USB CDC0 **CDC-ACM UART Interface**, not CDC1 power telemetry. Use
   DTR enabled and initial1152008N1. Pinned upstream UART source/config confirms
   UART1GPIO8/9 and the CDC bridge; firmware patches separate CDC0/CDC1.
4. Enter ROM download mode manually: hold SW1BOOT, press/release SW2RESET,
   then release BOOT. Use a flashing host configuration that keeps the UART
   bridge's required DTR state and does not rely on nonexistent automatic
   BOOT/RESET wiring. Press RESET after flashing. Verify communication on hardware.

There is no directly exposed RTS/CTS or automatic ESP32 reset circuit on J5.
Adapter wiring is a reviewed design, not a manufactured/tested harness.

## JLCPCB availability and assembly

[Stock manifest](stock-audit.csv) lists all43 exact identities/125 placements,
per-board quantities, historical stock dates and explicit **current UNVERIFIED**
status. No blocked lookup is interpreted as zero stock. Historical active parts
had enough listed units for one board before assembly loss, but two risks stand
out: C107701 had8units vs5/board; C98220 had22units vs20/board. Refresh these
before selecting a replacement or an assembly quantity; old counts are not stock
reservations. The external battery/display/speaker/motor are separate purchases.

The supported fresh `tsci search C43698 --jlcpcb --json` failed to parse JSON;
the same endpoint through the inherited proxy confirms **CONNECT403Forbidden**.
The precise one-domain addition `jlcsearch.tscircuit.com` was saved to the
environment draft, preserving existing domains/preset/scripts/secrets. It was
not applied/published; no unchanged denied lookup was repeatedly retried.

The [setup skill](skill://plugin_connector_1p_ed5feb9070a08191b08c81c47947bc16/setup/SKILL.md)
requires the environment-settings flow: **“Saving persists configuration; it
does not execute scripts, apply runtime changes, or publish.”** Review/save and
publish that network setting, then retry current stock and verify actual JLC
assembly availability/allowance for the intended quantity. No secret is needed.

Remaining fabrication gates on this same native board:169 strict-schema
failures,32 missing U16/U27 pill-pad paste records, unsupported polygon paste
Gerber export,31 blank BOM descriptions and125 unqualified supplier rotation
metadata warnings. Required complete build/shorts/snapshot/fabrication gates
have not passed. Imported definitions and generated JSON were not edited to
hide these failures. This review is not an order or working-hardware approval.

The original programmer-audit attempt encountered valid unnumbered native ports;
the lookup was corrected to support both named and numbered ports. Both logs
are retained, and the corrected audit passes. No board gate was weakened.
This is a verification/documentation revision; the existing public Pipeline9
WIP board remains unchanged and needs no duplicate unchanged registry upload.
