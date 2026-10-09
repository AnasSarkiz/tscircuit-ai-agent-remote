# AI Remote PCB — Complete Routing, Zero DRC, Zero Missing Connections

Act as a senior electronics engineer, PCB layout engineer, mechanical integration engineer, and tscircuit maintainer.

**Your primary task is to FINISH THE ACTUAL PCB, not produce another research-only report.**

Repository:
https://github.com/AnasSarkiz/tscircuit-ai-agent-remote

Published board:
https://tscircuit.com/AnasSarkiz/tscircuit-ai-agent-remote/releases/d17c1129-2a2a-4834-a186-e562b77aa268/preview

Latest review:
https://github.com/AnasSarkiz/tscircuit-ai-agent-remote/blob/main/evidence/microphone-local-bypass-2026-10-08/review.md

Starting implementation: `0.0.10-wip-microphone-bypass`.

## 1. Mandatory setup and engineering rules

Read and apply:

- Root `AGENTS.md` and `CLOUD_HANDOFF.md`
- `.agents/skills/tscircuit/SKILL.md`
- `.agents/skills/board-cloud-start/SKILL.md`
- Current official `tscircuit/handbook`, especially `guides/code.md`
- `context/user-decisions.md`
- `context/build-checkpoint.json`
- `REQUIREMENTS.md`, `VALIDATION.md`, and `BOM.md`
- Current display integration, native copper, schema, width, and manufacturing evidence

Continue the existing repository and accepted checkpoint. Do not bootstrap a replacement design.

Use the existing Bun and dependency lockfile. In the Linux cloud environment, use `scripts/cloud/setup.sh` and `scripts/cloud/env.sh` as documented.

Run heavy operations one at a time using the existing `scripts/cloud/run_with_budget.py` supervisor. Preserve solver events, original phase paths, native JSON, and logs.

Cloud environment draft revision 30 was saved but not confirmed published. Verify the active environment rather than assuming the draft settings are applied.

Do not patch generated Circuit JSON, fabricate solver cache results, silently change imported manufacturer geometry, disable checks, weaken DRC thresholds, or claim unperformed validation passed.

## 2. Required result

Target the following outcomes on the SAME regenerated board revision:

- **0 PCB port connection errors**
- **0 physically open assigned nets**
- **0 unresolved or unassigned required connector contacts**
- **0 electrical shorts**
- **0 copper clearance violations**
- **0 keepout violations**
- **0 unresolved trace-width violations**
- **0 drill/via/board-edge violations**
- **0 native Circuit JSON schema failures**
- **0 unintended solder-paste omissions**
- Successful native build, manufacturing exports, and independent Gerber/drill inspection

Do not manipulate error classifications, remove functional connections, or mark genuinely required pins NC merely to make these counts zero.

Distinguish routing completeness from fabrication readiness. Do not claim either without evidence.

## 3. Preserve the successfully repaired circuitry

Current verified starting evidence:

- 381 traces
- 320 through-vias
- 273 copper pours
- 50 reported missing PCB-port connections
- 12 physically open assigned nets
- Two unresolved battery outer contacts
- 0 measured shorts and geometric clearance violations
- 9,813 preserved connected terminal pairs

Retain the successful ICS-43434 microphone bypass:

- C81 to U5
- 0.30 mm top-layer copper
- Approximately 1.443 mm supply connection
- Approximately 0.600 mm ground-pour entry
- No bypass via

Retain the existing USB, audio, power, programmer, microphone, and control routes unless a specific electrical or physical defect requires modification.

Any replacement route must preserve its previously connected terminals and pass the full copper audit.

## 4. Solve the actual 2.8-inch landscape LCD integration

This is the most important prerequisite.

The latest user requirement supersedes earlier provisional 2.3-inch and 2.6-inch display selections.

Target:

- Approximately 2.8-inch landscape LCD
- Prefer exact ER-TFT028A3-4 or a fully qualified close alternative
- PCB approximately 50 × 65 × 1.0 mm
- Maximum enclosure approximately 60 × 75 × 16 mm
- Display body centered on the PCB/front assembly
- Landscape FPC exits left or right in the finished device
- No overlap with the ESP32 RF exclusion region

ER-TFT028A2-4 has already been researched as a candidate, not accepted as the final part.

Do the following:

1. Obtain authoritative manufacturer documents for the exact panel selected.
2. Verify body dimensions, active area, FPC geometry, pitch, contact thickness, pin numbering, and contact face.
3. Verify the exact mating ZIF connector, pin-one location, insertion direction, and accessible latch.
4. Determine a physically valid FPC routing path and minimum bend radius from evidence, not assumptions.
5. Resolve the existing approximately 59.5 mm² panel/antenna keepout overlap.
6. Reposition J7 and interfering components where necessary.
7. Verify enclosure walls, antenna clearance, battery clearance, component heights, screws, and FPC access in 3D.
8. Update the real circuit's placement, schematics, and component references.
9. Regenerate and inspect the complete native board.

Do not reuse the old provisional `51 - panel_pin` numbering formula without proving it matches the final physical connection.

If the preferred panel cannot be qualified, actively investigate a documented 2.8-inch alternative with a compatible connector and mechanical envelope. Prefer a design that avoids an unsupported folded-FPC assumption.

Do not declare the layout correct from a 2D image alone.

## 5. Correct the backlight electrical design

Inspect:

- `src/board/DisplaySheet.tsx`
- `src/board/BacklightSheet.tsx`
- U27 / TPS60230
- All LCD power, enable, and control circuitry

The A2 candidate uses a common-cathode backlight with separate anodes, whereas the current board uses a common-anode-style connection.

These topologies must not be connected together unchanged.

Choose the correct manufacturer-qualified driver topology for the final LCD.

Verify:

- LED anode/cathode polarity
- Constant-current regulation
- Maximum and nominal LED current
- LED forward-voltage range
- Required supply voltage and headroom
- PWM brightness control
- Startup and fault conditions
- Driver thermal dissipation
- Actual pin-to-pin connectivity

Replace or reconfigure the driver if the present topology cannot safely drive the selected backlight.

Update the PCB source and routing accordingly. Retire obsolete U27 connections properly rather than leaving dead or falsely satisfied nets.

## 6. Complete every remaining connection

The existing native errors include:

**J7: 46 missing PCB-port connections**

**U27: 4 missing output connections**

The existing physically open assigned nets are:

- GND
- VLCD
- LCD_SDA
- LCD_SCLK
- LCD_DC
- LCD_RESET_N
- LCD_CS_N
- LCD_BACKLIGHT_OUTPUT
- LCD_BACKLIGHT_RETURN_1
- LCD_BACKLIGHT_RETURN_2
- LCD_BACKLIGHT_RETURN_3
- LCD_BACKLIGHT_RETURN_4

Recompute this list after final display/backlight redesign; do not force obsolete nets to survive if the correct circuit changes.

The current independent audit shows 28 separate GND islands and 8 VLCD islands. Eliminate every unintended physical island.

Route each verified connection all the way to its actual pad, not merely near the component.

For J7:

- Use the approved physical mating pin map.
- Connect every required ground contact.
- Connect all required display power contacts.
- Complete the SPI/control routing.
- Complete the corrected backlight routing.
- Account for connector mounting and shell contacts correctly.

For U27 or its qualified replacement:

- Route every required LED driver output.
- Preserve suitable local decoupling.
- Keep power and switching loops short.
- Avoid sensitive microphone, RF, and audio paths.

Run the native connectivity audit after each major routing group.

### Battery J3

J3's center contact is already identified as PACK_NTC.

The outer contacts still require authoritative BAT+ and GND numbering.

Find the exact manufacturer mating-view documentation, terminal drawing, or verified physical evidence.

Only assign and route those contacts once polarity is established.

Never guess battery polarity. A falsely connected lithium battery interface is not an acceptable zero-error result.

Continue unrelated safe routing and manufacturing fixes while obtaining any missing supplier evidence.

## 7. Repair routing using real tscircuit source

Inspect and modify the canonical source as needed:

- `src/board/Routing.tsx`
- `src/board/placement.ts`
- `src/board/ManualConnectionCopper.tsx`
- `src/board/ManualPowerCopper.tsx`
- `src/board/ManualInnerSignalCopper.tsx`
- Associated route JSON and source-generated copper

Use supported native tscircuit routing phases, validated saved replays, and genuinely authored manual routes.

Try localized routing, alternate legal layers, route-order changes, and small justified placement changes before considering larger reorganization.

Keep the four-layer stack electrically intentional:

- Top: components, short critical signals, and power escapes
- Inner1: continuous GND reference
- Inner2: appropriately planned signals and power distribution
- Bottom: permitted signals and current-carrying paths

Preserve the complete ESP32 antenna keepout across all copper layers.

Maintain the verified through-via design of 0.30 mm drill and 0.45 mm land where applicable. Respect the existing routing clearance constraints.

Do not substitute visually adjacent copper for a proven physical electrical connection.

## 8. Fix the two regulator width failures

Inspect the actual native routes:

- `U2.pin7 → L1.pin2`
- `U2.pin9 → L1.pin1`

Each has an explicit 1.0 mm source requirement, but the current pad escape reaches 0.275 mm.

Review the TPS63802 manufacturer-recommended layout and real pad geometry.

Minimize switching-loop area and ensure an appropriately wide copper path as soon as the pad geometry permits.

Where a narrow entrance is physically unavoidable, demonstrate its permitted current, thermal behavior, and manufacturer-layout compatibility. Model any legitimate local neckdown explicitly and keep its engineering justification separate from the intended wide trunk.

Do not merely lower a board-wide minimum to make a violation disappear.

Also investigate all 65 other nominal-width discrepancies, especially VBUS, VSYS, V3V3, PACK_BAT, speaker and haptic paths.

Measure the final widths from the generated copper, not just the JSX settings.

## 9. Resolve the manufacturing/toolchain errors

Do not leave known fabrication output defects unaddressed.

### Circuit JSON schema

Current evidence contains 169 validation failures, including:

- 135 PCB components
- 15 PCB groups
- 15 schematic groups
- 2 PCB holes
- 2 silkscreen text records

Use the complete retained schema failure tree to identify actual causes.

Fix the canonical generator, schema compatibility, or source representation as appropriate.

Do not repair the generated JSON afterward.

Do not assume that simply upgrading package versions will solve the problem; use verified compatibility tests and regression fixtures.

### Solder paste

32 genuine U16/U27 pill-shaped pads are missing native paste records.

Investigate the previously tested canonical pill-pad paste repair and whether an approved, compatible runtime fix is available.

Apply a proper generator fix, regenerate the board, and verify the actual exported stencil apertures against the manufacturer footprints.

Do not synthesize paste polygons directly into the final JSON.

### Official short checker

The current official checker fails on an unsupported polygon shape.

Reproduce that failure and fix the relevant canonical tooling or use a verified corrected implementation.

Run independent geometric checks too, but do not claim the official check passed while it still fails.

### Pick-and-place

Resolve U14's `incompatible_pin1_locations` rotation problem using genuine pad, manufacturer, and assembly orientation information.

Generate and inspect actual BOM and PnP files, including physical orientation and polarity.

### Gerbers

Export real fabrication copper, solder mask, solder paste, silkscreen, outline, and drill data from the regenerated design.

Perform a separate inspection of the Gerber/drill output, including layer alignment, mask openings, paste, holes, and manufacturing clearances.

Do not create a fabrication ZIP from an invalid source or failed export.

## 10. Validation loop — repeat until resolved

Use the repository's actual supported commands and scripts, verifying CLI compatibility from the installed version.

Run:

```sh
bun run format:check
bun run typecheck
bun test ./tests

tsci check netlist index.circuit.tsx
tsci check pin_specification index.circuit.tsx
tsci check source index.circuit.tsx
tsci check schematic-placement index.circuit.tsx
tsci check placement index.circuit.tsx

tsci build index.circuit.tsx --pcb-png --pcb-svgs --schematic-svgs
tsci check shorts dist/index/circuit.json
tsci snapshot index.circuit.tsx
```

Run all heavyweight commands through the repository's documented cloud budget supervisor.

Also run the project's complete native schema, copper-connectivity, copper-geometry, current/width, solder-paste, rotation, and export audits.

Do not accept successful exit codes from a limited-scope helper as evidence of whole-board success.

If any check fails:

1. Identify its actual failure records.
2. Find the root cause.
3. Change the canonical source or correct upstream implementation.
4. Rebuild.
5. Re-run the affected checks.
6. Repeat until the real failure is eliminated.

Do not stop after one failed autorouter attempt.

## 11. Visual and electrical engineering review

Generate and inspect:

- Full routed PCB
- All four individual copper layers
- Top and bottom PCB views
- 3D assembly with the final LCD/FPC/battery
- Ratsnest and disconnected-net view
- Regulator switching-current loop
- USB-C and D+/D− routing
- Audio and speaker current paths
- Microphone supply/clock paths
- Display connector fanout
- Battery polarity and connector access

Verify USB differential routing and its electrical assumptions, grounding, power-path current handling, amplifier/speaker routing, and RF clearance.

Do not claim measured USB impedance or thermal performance without a justified calculation or appropriate verification.

## 12. Publish real progress

The existing repository authorizes publishing validated WIP implementation steps to its GitHub repository and matching public tscircuit package.

Make actual implementation changes, commits, and verifiable WIP publications according to `AGENTS.md`.

Keep the full reports and failed-trial evidence.

Do not publish unqualified Gerbers as fabrication-ready. Do not order PCBs.

## 13. Required final response

Report the BEFORE and AFTER measurements:

| Metric | Before | After |
|---|---:|---:|
| Traces | 381 | measured |
| Vias | 320 | measured |
| Missing PCB-port connections | 50 | measured |
| Physically open assigned nets | 12 | measured |
| Unassigned battery contacts | 2 | measured |
| Shorts | 0 measured | measured |
| Clearance violations | 0 measured | measured |
| Explicit width violations | 2 | measured |
| Schema failures | 169 | measured |
| Missing paste records | 32 | measured |

Also provide:

- Exact final selected LCD and verified pin mapping
- Final backlight design and current calculation
- J3 battery polarity evidence
- Final PCB and enclosure geometry
- All repaired nets
- Independent copper/DRC results
- Actual Gerber, BOM, and PnP status
- New commit SHA
- Updated tscircuit preview
- Evidence paths and screenshots
- Remaining risks, if any

**Final acceptance labels:**

`ROUTING COMPLETE = YES/NO`

`UNCONNECTED REQUIRED CONTACTS = N`

`PHYSICAL OPEN NETS = N`

`DRC ERRORS = N`

`SCHEMA FAILURES = N`

`FABRICATION READY = YES/NO`

Use YES and zero only when verified by the regenerated design and relevant checks.

## Execution priority

Do not finish this task with another diagnosis-only report.

Make substantive PCB source changes and complete every connection that has sufficient verified electrical and physical information.

Actively work to resolve the LCD selection, backlight redesign, antenna clearance, and battery mapping instead of repeatedly restating them as blockers.

Keep iterating on all safe, actionable work. If truly indispensable manufacturer evidence is unavailable, identify the exact missing document or measurement, preserve all completed work, and report the affected connection as unresolved.

Never invent pin numbers, bypass a DRC failure, alter generated JSON to fake success, or claim the hardware is ready when critical electrical or mechanical evidence is missing.

**The target is a genuinely complete, electrically correct, physically manufacturable AI Remote PCB with zero real DRC errors and zero missing required connections.**