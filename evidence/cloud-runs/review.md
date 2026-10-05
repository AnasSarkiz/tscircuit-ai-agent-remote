# Cloud routing checkpoint — 2026-10-05

**Engineering WIP. Routing is incomplete and fabrication is blocked.**

The canonical native output is `dist/index/circuit.json`, byte-identical to `evidence/cloud-runs/final-native/circuit.json` and generated from the current main/board source snapshot. SHA256 `81c31f77ac0871bfc4414b0940752e4f4fe0692a62089320b409908d4a8d5315`, 5,071,958 bytes. Native counts: **306 traces, 250 ordinary through vias, 190 pours, 90 open-port errors**. The independent physical audit finds **26 disconnected nets**. Of the 90 native errors, 46 concern J7; the two unassigned J3 outer contacts are absent from that count and still require qualification.

## Accepted changes and actual geometry

- U2 ground via moved to (-3.35, -14.15) mm. The original closest foreign bottom wire is **CHARGER_ILIM**, correcting the historical REG_PG label. Its actual copper gap increases from 0.192052957 mm to **0.298118974 mm**; requirement 0.20 mm. See `final-u2-clearance.json`.
- Native manual signal/power routing, 152 internal/bottom copper regions and 81 explicit through-via features added. There are 269 authored manual trace paths. These are labelled manual, never represented as solver caches. Board dimensions remain 50×65×1.0 mm/four layers.
- Inner1 GND and four top GND source regions avoid antenna/mounting keepouts and the deferred J7 contact strip. Native pours use actual outlines, zero additional perimeter erosion, 0.21 mm copper clearance and 0.26 mm cutout margin.
- R103 moved from (-2, -9.5) to (1, 18.9) mm after a demonstrated excessive PWM detour. Two failed placement/clearance trials were rejected. The accepted PCB placement and copper checks pass; fresh final mechanical qualification is still pending.
- AUDIO_ENABLE_SUPPLY is a roughly 5.05 mA resistor-bias feed, with an explicit 0.20 mm source width qualification. Speaker/power requirements were not relaxed. See `audio-enable-width-qualification.json`.
- Ten earlier manual paths produced 19 partial-span vias. They were removed and replaced with ordinary full-span via escapes and native internal copper regions. The geometry audit now rejects every ordinary via whose span differs from all four layers. Earlier 93-open trial results do **not** establish manufacturing-compliant vias.
- Required strip widths are verified against actual native BREP copper, excluding drilled apertures and rounded termination overhang. **152/152 widths pass**. Compact source polygons use mitered corners/flat caps; the previous 44,121 source vertices became approximately 1,000. A short HOLD_HARDWARE detour avoids native cutouts without narrowing the route.

`final-copper-audit.json` reports **zero measured geometry violations, zero shorts, no named-net merges**, but its full connectivity/fabrication gate **fails**. The audit covers actual native wires, pad contours, annuli, drills, board edges, keepouts and BREP clearance/connectivity; these results are not a completed manufacturer, thermal or signal-integrity approval. `final-region-widths.json` records every nominal-width measurement. Ordinary via drill/pad minima are 0.30/0.70 mm, annulus 0.20 mm; copper clearance 0.20 mm, ordinary drill-to-pad 0.20 mm including same net, drill separation 0.25 mm, board-edge copper 0.25 mm. Imported fine-pitch pad spacing retains its documented separate 0.10 mm rule.

## Checks on this source/build

| Check | Actual result |
|---|---|
| Direct native render | Completed, 180.20 s; peak process-group RSS 1,682,649,088 bytes; errors retained |
| TypeScript | Pass |
| Maintained-source Biome format | Pass, 60 files; no ignored board-source formatting errors |
| Routing regressions | 17 pass, including rounded grid edges, via spans, physical joining, USB clearance and true strip narrowing |
| Board tests | 42 pass / 2 fail / 581 assertions / 16 files; full fabrication and native strict-schema gates remain failing |
| Standard copper-free CLI placement build | Pass, 33.56 s; zero traces/vias/pours and native errors |
| Placement preservation fixture | Native API render passes; same renderer as the routed artifact, full real-electronics placement/electrical partition comparison passes |
| Required netlist / pin specification / source / schematic-placement / placement checks | All pass; PCB checks consumed the untouched prebuilt native JSON |
| Full routed CLI build | Initial memory stop; after lossless archiving, still incomplete after 300 s plus termination grace, peak RSS 10,154,262,528 bytes |
| Bitmap shorts CLI | Incomplete after 180 s plus termination grace; no passing result inferred |
| Gerber shorts / Gerber export | Fail `Unsupported shape polygon`; requested fabrication ZIP does not exist |
| Strict native schema | 169 failing elements: 135 PCB components, 15 schematic groups, 15 PCB groups, 2 holes, 2 silk texts |
| Snapshot command | Incomplete after 120 s plus termination grace; no snapshot accepted as a fabrication baseline |

All logs and explicit outcomes are retained. The CLI placement output adds empty supplier metadata to ten native pads; `cli-placement-native.json` retains that exact output. The current native placement fixture was freshly generated with `capture-placement.tsx`, rather than weakening comparison assertions or editing output. The original four switching/USB paths are preserved geometrically, except the previously qualified USB width change for the 1.0 mm stackup.

## Visual evidence

Inspected `visual-review/four-layer-review.png`, top mask/paste and USB/charger, amplifier/regulator, microphones and display/backlight details. The top GND contact exclusion, antenna/board perimeter, internal signal/power strips and ordinary vias are visible. J7 contacts and upstream missing wiring remain visibly incomplete. U16/U27 pill-pad paste remains missing. Native diagnostic overlays and all error records are retained. The current full schematic, final silk/CAD/FPC/harness/current/SI/fabrication review is not approved by these PCB views.

## Remaining engineering and external blockers

The 26 actual disconnected nets and their exact real-port islands are listed in `final-copper-audit.json`. Safe upstream work still includes USB_DN/DP, VBUS/internal PACK_BAT/VSYS, several GND islands, MCU_LCD_RESET_N/LCD_SDA/SCLK/DC, AMP_SD_MODE/AUDIO_ENABLE_SUPPLY, MIC rails/data/clocks and the matched speaker pair. Fine-grid and existing-copper passes failed many congested escapes; that is not proof that routing is impossible. Candidate partial-span, clearance, capacitor-length and speaker-skew trials were rejected, not published as accepted copper.

J3 centre remains PACK_NTC. The AKY2945 supplier drawing specifies red BAT+, yellow centre NTC, black GND, but does not verify the numbered keyed outer contacts. J7's AFC07 upper contacts and the panel's contact/stiffener drawing still do not qualify the actual portrait fold/mating pose and pin-1 direction. Both interfaces stay deferred; no guessed supplier confirmation was created.

There are **32 missing native paste records**, 16 each on U16/U27. The official core 0.0.2091 investigation still lacks pill paste; pinned runtime and imported definitions remain unchanged. The supported Gerber converter rejects polygon paste. Source/schema consistency, assembly metadata/stock, current/SI, and final mechanical/stencil/BOM/CPL checks remain blocking. No fabrication package or order is approved, and no physical test is claimed.

## Reproducibility and preservation

Native captures include actual events, final JSON and exact source snapshots. The CLI virtual filesystem reads diagnostic text/JSON across the project, causing memory pressure from raw events. Every removed raw event/start file has been losslessly archived and its exact original bytes verified before removal. Each capture's `native-event-archive.json` gives hashes and restoration instructions. Archiving fixed the CLI placement memory failure; no library/runtime patch or resource/check relaxation was used.

All 265 protected import/route/dependency/asset files still match the migration hashes. `context/checkpoint-sha256.json` is refreshed for the accepted current board and new helpers; the original migration manifest is preserved separately. A clean frozen dependency install is still blocked by the unapplied api.github.com allowance; current installed dependencies support the verified operations. The onboarding start instructions were saved as a draft, not applied or published.

GitHub publication is an authorized public WIP checkpoint with matching native JSON; exact remote/anonymous verification is recorded separately after push. Registry retries remain deferred and the watcher remains paused.

Staged whitespace diagnostics are limited to the exact captured `check-format.log`, `format-routing-source.log` and `check-netlist.log`. Their generator whitespace is preserved as original evidence; maintained board source formatting passes.
