# A2 fabrication checkpoint — 2026-10-04

**NOT FABRICATION READY**

This continues the existing handheld AI remote. It uses a dominant front display, one hold-to-talk button, a side hardware privacy switch, ESP32-S3 Wi-Fi/BLE/USB, two digital microphones, an I2S speaker amplifier, external speaker and haptic connections, rechargeable 1S power and top-side assembly. Firmware and physical testing are not completed.

The human confirmed the exact AKY2945 harness as red BAT+, yellow 10 kΩ NTC, black GND. Yellow is the physical centre contact. The outer contacts are not numbered in the drawing. J3 pin 2 is now PACK_NTC; J3 pins 1 and 3 have no source connections and remain unrouted. Documentation reads **outer — NTC — outer**, with both red/black outer assignments **PENDING PIN-NUMBER CONFIRMATION**. Written supplier confirmation or a keyed physical pack/multimeter measurement must establish the outer numbering. These contacts are unresolved required connections, not final intentional NCs. Mechanical anchors remain grounded.

## Board and current build

| Item | Actual result |
|---|---|
| Outline | 50 × 65 mm, nominal 3 mm rounded corners; exported coordinate extrema X ±25, Y ±32.5 mm |
| Stack | Four layers, nominal 1.6 mm; proposed JLC04161H-7628 stack, not a completed impedance order |
| Population | 122 purchased PCB parts plus 8 native copper test points; 130 PCB component records, all top |
| Schematic | 13 native A4 sheets |
| Routed traces / vias | 0 / 0; routing disabled |
| Routed trace length | 0 mm; no routed connection validation exists |
| Native error records | 0 in the current unrouted JSON |
| Placement DRC | 0 errors, 3 preserved connector orientation warnings |
| Full native schema | 162 failing records: 130 components, 15 PCB groups, 15 schematic groups, 2 standalone mounting holes |
| Tests | 35 pass / 1 existing strict-schema failure, 319 assertions |
| Required unrouted count | Completion count not evaluated; all intended inter-component connections lack routed copper. 388 source-trace records are logical declarations, not a count of physical routes |
| Shorts | Unrouted diagnostic only; cannot establish zero shorts for a future routed board |

Current native Circuit JSON SHA-256: `fbf9e2b576a9e37f695e894d9458500c33d5508b052b10692dcf99bc474dcd3f`. Parent GitHub main: `420d8239ab03d360c0a837a89562ea4a1ffd86ef`. Dependencies unchanged: CLI 0.1.2235, core 0.0.2070, tscircuit 0.0.2742, easyeda 0.0.370, props 0.0.682, Circuit JSON 0.0.513.

## Completed independent changes

- Imported genuine AFC07-S12FCC-00 / C11051 unchanged and replaced the old ten-contact J7 with this twelve-contact bottom-contact FPC connector.
- Connected the HS20HS072RX drawing's contacts: 1/12 GND, 2 CS, 3 DC, 4 SCLK, 5 SDA, 6 RESET, 7 NC, 8/9 VLCD, 10 backlight anode, 11 backlight cathode. Anchors 13/14 are grounded. Display C5329582's supplier library contains a non-PCB placeholder, so it is preserved as evidence and not placed or remade as a fake screen footprint.
- Corrected J3 centre NTC and removed both unconfirmed outer assignments.
- Added two native 2.2 mm NPTH mounting trials and 6 mm all-layer circular copper keepouts. Moved the privacy switch, speaker connector and nearby passives to clear their actual native courtyards.
- Expanded the four-layer antenna keepout to cover the nominal antenna body plus 1 mm planar margin. This does not establish enclosure RF clearance.
- Updated the native LCD body outline to 36.2 × 51.8 mm and active area to 30.6 × 40.8 mm. They are PCB notes, not external assembly CAD.
- Built and inspected the unrouted PCB, ratsnest, current A4 sheet renders and native GLB board/connector views. Reviewed snapshots before updating them. GLB omits the external display/pack/speaker/motor and lacks some detailed component models; it cannot certify the complete enclosure.

## Mounting trial

Coordinates use the native PCB origin. Prefer plastic M2 hardware. Exact screw length, head/standoff envelope, enclosure wall and load/deflection qualification remain pending. A 6 mm keepout is a constraint on the eventual hardware, not evidence that any chosen screw fits.

| Mount | X / Y mm | NPTH | Keepout diameter | Hole edge to PCB edge | Minimum native courtyard gap to keepout | Nominal antenna-body distance from keepout |
|---|---|---|---|---|---|---|
| M1 | −21.5 / +6.7 | 2.2 mm | 6 mm, all four layers | 2.4 mm | 0.2501 mm to SW5 | 19.0657 mm |
| M2 | −21.5 / −29.5 | 2.2 mm | 6 mm, all four layers | 1.9 mm | 0.3266 mm to U4 | 55.2621 mm |

The nearest nominal board edges are straight segments at these points; the lower hole is near the rounded corner. The keepout-to-LCD trial envelope gaps are 0.4 / 1.2802 mm; pack trial gaps are 1.0 / 1.5894 mm. These conservative XY studies exclude real flex/cables, assembly tolerance and Z. Support against USB/TALK/switch forces is not yet proven. The diagnostic drill file explicitly declares NonPlated and contains T13C2.200000 at both coordinates. No 2.2 mm hole is in the plated drill file. Copper intrusion after routing is untested.

## Display, battery and RF prerequisites

The HS20HS072RX mechanical drawing is 36.2 × 51.8 × 2.05 ±0.05 mm, with a 12-contact 0.5 mm tail. The drawing and pin table agree on contact functions. Its text/drawing disagree on ST7789T3 versus ST7789V2 and LED topology, and one description calls it 2.4 inches. Exact supplied revision and backlight behavior need confirmation. The current 100 Ω VSYS backlight branch is unqualified for the listed 80 mA nominal backlight and low-battery brightness; no regulated-current replacement has been selected.

The connector is bottom contact; current J7 rotation 0 presents its opening in +Y and is internal. Actual screen contact-side/pin-1 orientation, 20.7 mm tail path, fold, bend radius, latch access and raised Z fit remain unqualified. The shortest planar distance to the current mouth may exceed the drawn tail extension; a real keyed assembly path is required before final J7 placement.

Exact AKY2945 maximum pack envelope is 35 × 52.5 × 5.7 mm, not just the cell size. The supplier states 1000 mAh, 1C maximum charge and 3C maximum discharge; protection thresholds, peak duration and NTC Beta remain unqualified. A conditional 10% thickness expansion gives 6.27 mm before installation clearance. The 80 mm cable exits a short edge. Availability and a final harness have not passed procurement review.

The trial LCD top at Y24.9 and pack top at Y25.25 are only 3.86 and 3.51 mm from the nominal antenna region beginning Y28.76. Espressif recommends at least 15 mm antenna clearance in all directions inside the housing and prefers the module antenna outside/cut away from the baseboard. The expanded PCB copper keepout does not resolve display/battery metal proximity, baseboard cutout or enclosure fit. Do not treat a raised display as automatic RF approval.

## Power review

All rows below **FAIL final qualification** because no actual routes exist. TBD means current allocation has not been verified, not zero current. Layer/via/width columns describe actual emitted routed copper, not desired configuration.

| Net | Expected peak current basis | Actual route width | Actual routed layer | Via count | Result |
|---|---|---|---|---:|---|
| VBUS | USB default 100 mA policy candidate; higher-current negotiation/partial-rail behavior unqualified | None | None | 0 | FAIL — current policy and route open |
| PACK_BAT | Pack capability up to 3 A; system provisional around 1.5 A, pulse/PCM limits unresolved | None | None | 0 | FAIL — outer polarity and current qualification open |
| VSYS | Approximately 1.5 A provisional combined load; actual coincident peak TBD | None | None | 0 | FAIL |
| V3V3 | ESP32/transient and peripheral allocation TBD | None | None | 0 | FAIL |
| BACKLIGHT | Datasheet nominal 80 mA; current 100 Ω branch does not establish this | None | None | 0 | FAIL |
| SPEAKER SUPPLY | 8 Ω load; output power/volume/duty and peak input current TBD | None | None | 0 | FAIL |
| HAPTIC | External motor operating/stall current and duty TBD | None | None | 0 | FAIL |

Saved TI/IPC-2221 empirical screening at a 20 °C rise yields nominal external 35 µm widths of 0.3450 mm at 1.5 A and 0.8976 mm at 3 A. Reserving −20% width tolerance gives design widths 0.4313 and 1.1220 mm, before copper-thickness/thermal qualification. For 15.2 µm inner copper the corresponding tolerance-reserved widths are 2.5836 and 6.7210 mm. This is screening, not an IPC-2152 thermal qualification or a selected final net class. Manufacturer process minima still apply. A 0.30 mm finished via with assumed 25 µm plating has 0.025525 mm² barrel area; equivalent trace area does not prove via ampacity. Plating guarantees, sharing and temperatures must be reviewed.

## Critical interfaces

| Interface | Final result | Remaining review |
|---|---|---|
| USB D+/D− | FAIL — unrouted | Pair/reference/ESD/stubs and real impedance geometry |
| Display SPI | FAIL — unrouted | Logical pin mapping corrected; FPC fit, controller revision, timing/power sequence open |
| Microphone I2S | FAIL — unrouted | Clock/SD timing, privacy ramp/off behavior, quiet returns and paste |
| Speaker I2S | FAIL — unrouted | Clock/data timing and actual amplifier supply/output return geometry |
| ESP32 antenna | FAIL — mechanical fit unqualified | Battery/display metal, 15 mm housing clearance/baseboard cutout, every copper layer |
| Charger | FAIL | BAT pin order, thermal copper, input/OUT/BAT paths, all charger paste absent |
| Buck-boost | FAIL — unrouted | Switch loops, caps, feedback/ground and actual current paths |
| Battery ADC/NTC | FAIL | Centre NTC corrected; outer polarity, NTC curve, fault/threshold behavior open |

USB D+/D− routed lengths: unavailable; mismatch unavailable; vias zero because routing is disabled. The earlier selected-stack study targets 90 Ω with L1 width 0.2906 mm/gap 0.1999 mm over L2, 0.2104 mm 7628 dielectric, εr4.4 and outer 35 µm copper. This is a conditional calculation, not measured/validated USB copper. Intended layers remain L1 components/critical signals, L2 continuous GND, L3 power/slower signals, L4 additional signals. No planes or route replay cache have been generated.

## Fabrication outputs and blockers

Native diagnostic ZIP contains four copper layers, mask/paste/silk, outline, separate PTH/NPTH drills, BOM and CPL (16 files). It is explicitly **NOT-FOR-FABRICATION**. The outline and mounting drills were checked in exported coordinates; routed copper, planes, final thermal/clearance and assembler review remain absent.

| Output | Result |
|---|---|
| Gerbers | FAIL final release — unrouted diagnostic only |
| Mounting drills | PASS limited exported 2.2 mm NPTH identity/coordinates; whole assembly/clearance not passed |
| BOM | FAIL — 122 native rows, 32 blank Comment fields; B-015 unresolved; whole BOM/lifecycle/availability/physical lands unqualified |
| CPL | FAIL — 122 top-side rows; U14 C7848 rotation 0 unverified (`incompatible_pin1_locations`) |
| Paste | FAIL — U4/U5 C5656610 each have 9 SMT pads but only 5 paste records; J1 C165948 has 12/8; U16 C54313 has 17/0, including 16 pill pads and its polygon exposed pad |
| Schema | FAIL — B-010, including standalone mounting-hole null component relation |

Official core PR4344 polygon paste support was merged and then reverted by PR4349. Manual latest core0.0.2080 verification does not establish a released B-005 fix; no unrelated dependency upgrade was installed. The charger pill-pad coverage observation was sent to the authorized correction chat as additional B-005 evidence, without assuming a common root cause. B-003 ground identity remains resolved in the current runtime.

Mechanical prerequisites and unresolved battery polarity block final placement/routing. Paste, schema and assembly metadata separately block fabrication. Existing lifecycle/catalogue/land qualification, source metadata/reference warnings, startup/privacy/timing and full current budget also remain open; they are not invented copper shorts. No actual routed short or clearance failure is asserted when no routed copper exists.

## Checks, evidence and next actions

Native build and all five required pre-routing checks pass (netlist, pin_specification, source, schematic-placement, placement). Format and TypeScript pass; reviewed native snapshots were updated and the final comparison passes. The unrouted shorts diagnostic exits0 (zero reported shorts), which does not validate routed copper. Tests retain the strict-schema failure; full current schema audit retains all 162 failed records without rewriting output. Native connector warnings remain visible. A4 sheets and board CAD renders were inspected for this preview; some supplied symbols/models and edge text still need final schematic/assembly readability qualification.

Evidence is in this directory: manufacturer PDFs under `references/routing-a2/`; rendered datasheet pages; current PCB/ratsnest/A4/3D images; native command logs; `native-analysis.json`, `schema-failures-summary.json`, `diagnostic-export-review.json`, `power-width-study.json`; failed earlier placement builds preserved separately. The native root `dist/index/circuit.json` is included in the runtime-only publication. Documents, scripts, evidence and unused imports are excluded from the tscircuit runtime package; GitHub retains the engineering evidence.

Next: confirm battery outer numbering, close real display/FPC/enclosure/RF fit and final backlight/current decisions, resolve footprint/paste and assembly export blockers, then enable native routing. Save genuine router events/full JSON/per-phase replay data before any route-moving work and verify actual copper connectivity/shorts/clearances/widths/returns. Regenerate and inspect final fabrication files only from the routed validated revision. The background watcher stays paused. No order or physical-test result exists.
