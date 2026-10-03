# MCU and USB application review — A0

Unrouted, untested diagnostic foundation. `src/mcu/esp32-s3-usb-review.tsx`
is not a complete handheld or final placement. Native A4 sheet and current
60 × 50 mm study previews were inspected; all 16 PCB parts are top-side.
No RF or signal-integrity approval follows from this spread-out fixture.

ESP32-S3-WROOM-1-N8R8 C2913201 physical module pins: 2 supply, 3 EN,
13 GPIO19 USB D−, 14 GPIO20 USB D+, 27 GPIO0 BOOT, 36 RXD0, 37 TXD0;
1/40/41 ground. The nine exposed ground shapes preserve native pin41 hints
and their internal group. Pins 28/29/30 (GPIO35/36/37) remain unused because
octal PSRAM occupies them. Straps GPIO3/45/46 remain unallocated. Module
supply must stay 3.0–3.6 V; ≥500 mA supply capability is a design requirement,
not proof that the completed device stays below 500 mA. N8R8 operating range
is −40…65 °C without PSRAM ECC; full product temperature remains unqualified.

USB series resistors C107701 are 22 Ω each, near the module in the final layout.
C94934 ESD pin1 D+, pin2 D−, pin3 GND matches TI. The connector's duplicate
D+ contacts 8/10 and D− contacts 7/9 join their respective nets; 15/16 VBUS,
13/14 and four shell anchors ground; pin6 CC1 and pin12 CC2 each get 5.1 kΩ
C105580 to ground. SBU5/11 remain open. Correct attach/current entitlement,
VBUS detection, input protection and charger policy remain pending. Rd does
not authorize full input current. Final USB pair requires 90 Ω ±10% impedance,
length matching, short stubs and continuous return plane. No traces exist.

C485802 TPS3839G33 reset is push-pull, 3.08 V nominal threshold, with native
120–280 ms startup delay. EN has a 100 kΩ ground pulldown and a 4.7 kΩ
C99782 series connection to the supervisor RESETn output. A service tool can
pull EN low through this resistance without shorting the push-pull output
(approximately 0.74 mA at provisional rail maximum). Actual supervisor output,
hysteresis and EN low/high corners require full rail/transient qualification.
The supervisor replaces the usual EN RC delay in this candidate architecture;
50 µs module startup/reset timing must still be verified in hardware.

C160405 service connector contacts: 1 ground; 2 V3V3 reference sense;
3 EN; 4 GPIO0 BOOT; 5 TX via 1 kΩ C22548; 6 RX; anchors7/8 ground.
VREF is a sense output, never an external programmer supply. Exact mating
harness and programming levels remain pending. Espressif recommends 499 Ω
TX resistance; candidate 1 kΩ requires edge-rate/programming verification and
is not a claimed manufacturer recommendation. GPIO0 gets a 10 kΩ pullup.
C90053 10 µF and two C45000 100 nF parts bypass module supply; effective
capacitance and final low-inductance loop placement remain pending.

Native build and five checks exit 0, but qualification is incomplete:
B-005 omits paste from four USB polygon pads; B-008 ESD symbol lacks D2;
B-010 generated JSON violates its schema. Eight pin-metadata and two J-prefix
warnings remain visible. Manufacturer wiring tests pass independently; full
schema regression remains failing. No error, warning or check was suppressed.
Current logs, JSON, SVG/PNG and unrouted diagnostic Gerbers are preserved in
`evidence/mcu-usb-review-2026-10-03`. They are not a fabrication package.
