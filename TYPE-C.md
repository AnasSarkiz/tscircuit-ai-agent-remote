# AI Remote A0 — hardware USB current review

This is an unrouted, partial application review, not a fabrication-ready board. The charger, protected pack, temperature sensing, input protection and system load enable are not integrated. The published board entry point still guards against building an incomplete device.

The independent source is `src/power/type-c-current-review.tsx`; native fixture and exact output are under `evidence/type-c-current-review-2026-10-03/`. It uses 17 unmodified JLCPCB imports on the top layer and a native A4 schematic. Native build and all five connectivity/placement checks exit 0. The PCB and A4 render were inspected: no overlaps or boundary violations; R74/R75 references face 180 degrees but remain readable. Output contains 54 pads, 54 native paste shapes, zero copper traces or vias, and zero emitted errors. Full installed Circuit JSON validation still fails for 19 elements under B-010. Passing CLI checks does not clear that blocker.

## Manufacturer wiring

TUSB320LAIRWBR (C132554) uses its integrated Rd on CC1/CC2. PORT is grounded for UFP mode, ADDR is open for GPIO mode, EN_N is grounded, and unused OUT3 and ID stay open. Full-board integration must remove the old external 5.1k CC resistors before connecting this controller.

TPS7A2033PDBVR (C2862740) powers the controller from charger VSYS. It is not connected to raw USB VBUS: BQ24074's overvoltage cutoff is 10.2–10.8 V, while this LDO's absolute maximum is 6 V. BQ24074 OUT is regulated to 4.3–4.5 V with valid USB input. The controller outputs are pulled up to their own supply, preventing pull-ups from another live rail backpowering the non-failsafe pins. The 1k LDO output bleed keeps its load above 1 mA when its 3.3 V accuracy specification applies. Output regulation at low battery VSYS is not guaranteed; higher USB current is disabled while this rail is invalid.

VBUS detection uses C114622 470k plus C482869 430k in series. Total nominal resistance is 900k. The provisional ±1.6% combined initial tolerance and temperature allowance gives 885.6–914.4k, inside TI's 855–920k range. Exact resistor temperature range and voltage coefficient must still be qualified.

GPIO OUT1 is high for unattached/default current and low for a source advertising 1.5 A or 3 A. SN74LVC1G14DBVR (C7835) inverts it. SN74LVC1G08DBVR (C7666) requires both this high-current indication and TPS3839K33DBZR (C96333) RESET_N before asserting the future charger EN2 net. The controller's 50 ms maximum startup is below the supervisor's 120 ms minimum delay, subject to the controller's required VDD ramp of 25 ms or less. EN_N is tied low; no firmware override exists. Ramp timing and brownout transitions still require qualification and prototype measurement.

The future BQ24074 EN1 must stay low. EN2 low selects USB100 (100 mA maximum); EN2 high will select resistor-limited current only after the hardware conditions above. The actual charger connection and ILIM resistor are not present in this fixture. A provisional 1.2k ILIM resistor at ±1.6% would bound the 1500–1720 A-ohm KILIM range to 1.230–1.457 A, below a 1.5 A advertisement; C22765 (0603WAF1201T5E) is now imported through the supported workflow, but has not yet been wired or qualified for the intended temperature range. Default USB attachment alone does not authorize 500 mA.

The 1k EN2 pull-down bounds the TI AND gate's 10 µA maximum Ioff to 10.16 mV when unpowered, below the charger's 0.4 V low limit. Gate VOH is at least 2.4 V at a 3 V supply and a 24 mA test load; the pull-down requires less than 3.5 mA and the charger requires 1.4 V high. Supply ramp and simultaneous partial-power behavior remain unverified. The main system must remain disabled during dead-battery charging on a default-current source; the controller alone does not implement that system policy.

## Sources and remaining work

TI TUSB320LAI Rev D: https://www.ti.com/lit/ds/symlink/tusb320lai.pdf . TPS7A20: https://www.ti.com/lit/ds/symlink/tps7a20.pdf . TPS3839: https://www.ti.com/lit/ds/symlink/tps3839.pdf . SN74LVC1G08 Rev AA: https://www.ti.com/lit/ds/symlink/sn74lvc1g08.pdf . BQ24074: https://www.ti.com/lit/ds/symlink/bq24074.pdf . Retrieved manufacturer PDFs are preserved in the preceding audio/charge evidence folder; exact part provenance remains in the unmodified imports.

Remaining: charger and pack qualification, 1.2k resistor qualification and wiring, transient and inrush protection, controller rail ramp, default-current system load gating, battery cutoff/restart hysteresis, minimum effective capacitance, current and thermal budget, physical CC/USB layout and prototype attach/detach tests. The pending battery procurement exception has no answer and is not assumed approved.

The same evidence folder records the separate unqualified C6617702 hold-button candidate. The historical Panasonic cutout width differs from the imported geometry. That discrepancy was forwarded to the authorized fix chat without altering the import. The controller review does not qualify that switch.
