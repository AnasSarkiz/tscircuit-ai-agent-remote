# Current board order-readiness review — 2026-10-06

**NOT READY TO ORDER.** The board does not satisfy zero DRC and complete
connectivity. Passing clearance checks alone does not establish a working board.

Reviewed source parent: `999001f04798250e75e5508fd21d38cf22461cbb`.
The fresh native render completed in 190.24 seconds and is byte-identical to
`dist/index/circuit.json`: SHA256
`81c31f77ac0871bfc4414b0940752e4f4fe0692a62089320b409908d4a8d5315`.
Board: 50 × 65 × 1.0 mm, four layers; top population. Pipeline9 remains selected.
This review adds verification tooling/evidence, not new copper or a new routing
completion claim. Imported parts, saved routes, board inputs and dependencies
remain unchanged.

## Physical copper and connections

Independent exact supported pad/drill/wire/BREP geometry measurement reports:

| Check | Actual result | Qualification |
|---|---:|---|
| Measured shorts | 0 | Pass within audited geometry |
| Measured clearance/geometry violations | 0 | Pass within audited geometry |
| Merged named nets | 0 | Pass |
| Physically disconnected nets | 26 | **Fail** |
| Native unconnected-port errors | 90, including 46 J7 errors | **Fail** |
| Ordinary vias | 250, 0.70 mm copper / 0.30 mm drill, full four-layer span | Geometry passes |
| Required overall zero-DRC, zero-shorts, connected gate | false | **Fail** |

Minimum measured ordinary via drill-to-pad clearance is 0.200001194 mm
(requirement 0.20 mm, including same-net cases). Copper pad-to-trace minimum is
0.200075098 mm (requirement 0.20 mm). These nominal geometry checks do not
qualify manufacturing tolerances or current/impedance. Every pad-to-net island is
retained in [copper-audit.json](copper-audit.json) and the current
[496-pin table](pin-assignments.csv). Error markers are not used as a substitute
for actual physical copper contact. J3's two unassigned outer battery contacts
are **additional omissions**, absent from the 26/90 counts.

Disconnected nets and physically separate copper groups:

| Net | Islands |
|---|---:|
| GND | 35 |
| MCU_LCD_RESET_N | 2 |
| USB_DN | 4 |
| USB_DP | 4 |
| VBUS | 4 |
| PACK_BAT | 2 |
| VSYS | 5 |
| VLCD | 8 |
| LCD_SDA | 3 |
| LCD_SCLK | 3 |
| LCD_DC | 3 |
| LCD_RESET_N | 2 |
| LCD_CS_N | 2 |
| LCD_BACKLIGHT_RETURN_4 | 2 |
| LCD_BACKLIGHT_RETURN_3 | 2 |
| LCD_BACKLIGHT_RETURN_2 | 2 |
| LCD_BACKLIGHT_RETURN_1 | 2 |
| LCD_BACKLIGHT_OUTPUT | 2 |
| AMP_SD_MODE | 2 |
| SPEAKER_P | 2 |
| SPEAKER_N | 2 |
| AUDIO_ENABLE_SUPPLY | 2 |
| VMIC | 5 |
| MIC_WS | 2 |
| MIC_BCLK | 3 |
| MIC_SD | 2 |

The missing USB, battery/system power, display, speaker and microphone paths
prevent approval of their real operation. A correct logical net assignment does
not connect these separate copper islands.

## Every trace width

[trace-widths.csv](trace-widths.csv) lists **all 306 native traces**.
[trace-widths.json](trace-widths.json) measures **all 792 actual wire segments**,
including segment lengths, layers, coordinates, source minima and named-net
nominal widths. Native constant-mode segment widths use the starting route
point, verified against the installed renderer; widths were not inferred solely
from board settings. Missing named-net width settings are disclosed rather than
assigned an invented requirement.

- No segment is below the general 0.20 mm board minimum.
- **Two regulator switching traces fall below their explicit 1.0 mm source
  minimum.** `saved_phase_null_0_0` (U2.pin7→L1.pin2) and
  `saved_phase_null_0_1` (U2.pin9→L1.pin1) each have approximately 0.75 mm of
  0.275 mm width, then 0.4/0.7 mm sections before widening to 1.0 mm.
  Existing pad escapes cannot be accepted as rated switching-current paths
  merely because the 1.0 mm section exists. They require proper current,
  switching-loop and layout qualification or a qualified redesign.
- **55 other traces fall below their named net's nominal width.** They meet
  their explicitly authored branch minimum where present. Many are authored
  short pad escapes, but the nominal/actual differences remain review items;
  this audit does not convert them into approved thermal exceptions.
- All **152 authored copper regions** preserve their required strip widths in
  actual native BREP copper, excluding drilled apertures. This is independently
  measured in [region-widths.json](region-widths.json).

| Named net | Nominal width (mm) | Smallest actual trace width (mm) | Traces below net nominal |
|---|---:|---:|---:|
| VSYS | 1.0 | 0.275 | 15 |
| V3V3 | 0.8 | 0.275 | 24 |
| PACK_BAT | 1.0 | 0.3 | 4 |
| VBUS | 0.5 | 0.3 | 2 |
| HAPTIC_N | 0.4 | 0.3 | 4 |
| GND | 0.3 | 0.2 | 6 |

**Trace-width suitability for the real load is not approved.** The load/peak
current budget, guaranteed copper/barrel thickness, enclosure temperature,
voltage-drop/temperature-rise and narrow-section limits remain unqualified.
The historical IPC-2221 screening study uses an earlier provisional stackup and
cannot qualify the current 1.0 mm board. USB's existing 0.2979 mm sections are
not evidence of a complete differential pair; USB_DN/DP remain disconnected.
Speaker paths, return geometry and final stackup/impedance need qualification.

## Components and real pin assignments

Fresh [component inventory](component-inventory.json): **125 purchased PCB
parts /43 exact JLCPCB identities plus10 native pads**, all on top. Exact MPNs,
supplier codes, placement, pad shapes and paste omissions are recorded.
New current-whole-board manufacturer regression checks pass for MCU
power/USB/reset/boot and reserved PSRAM pins, BQ24074 charger, TPS3808 supervisor,
TPS63802 power/feedback/switch pin identities, MAX98357A supply/speaker polarity,
and dual ICS-43434 microphone supply/data/clock/channel selection. The existing
current-board display/backlight logical tests remain part of the canonical suite.
These reapply the stored manufacturer requirements; they do not stand in for a
fresh vendor stock check, complete datasheet review, physical assembly or runtime
hardware testing.

**Unqualified external connections:**

- J3/C157929 and AKY2945/LP523450 pack: centre pin2 is PACK_NTC, consistent with
  the supplier's yellow centre10kNTC wire. The exact pack drawing does not number
  the keyed BAT+/GND outer contacts, so J3.pin1/3 remain unassigned/unrouted.
  Generic JST numbering does not establish this particular pack's polarity.
  [Stored supplier drawing review](../a6-bom-routing-2026-10-04/mechanical-search.md).
- J7/C262650 and ER-TFT026-1: current logical panel-pin mapping is provisional.
  Exact current-revision contact face, pin1 direction, fold and mating orientation
  remain unqualified. The historical drawing cannot qualify the current flex.
  Thus logical pin-map tests do not approve the physical display connection.
- Speaker/motor harness strain relief, PH connector pin tails, acoustic/RF
  clearance and actual enclosure fit remain pending. The latest accepted
  enclosure maximum is60 ×75 ×16 mm, superseding older15 mm references.

## Fabrication and assembly

| Check | Actual result |
|---|---|
| Full installed Circuit JSON schema | **169 failing elements**:135 pcb_component,15 pcb_group,15 schematic_group,2 pcb_silkscreen_text,2 pcb_hole |
| Native paste on purchased pads | **32 missing**:16 pill pads each on U16/BQ24074/C54313 and U27/TPS60230/C1848364 |
| Official BOM converter | 125 rows; **31 blank Comment fields**,125 supplier-code footprint fields |
| Official JLC supplier placement conversion | 125 top-side rows; **125 missing supplier pin1 metadata warnings**; strict rotation conversion rejects U1 |
| Current whole-BOM stock | Not refreshed; earlier dated stock receipts are historical |
| Stackup, mask/stencil, enclosure/harness and assembler approval | Not qualified |

Exact official converter outputs are named **NOT-FOR-FABRICATION** and are not
an approved assembly package. All supplier rotation warnings and the strict
failure are retained in [assembly-export-audit.json](assembly-export-audit.json).
A missing supplier orientation field is a qualification failure; it does not by
itself prove that125 actual footprints are rotated incorrectly.
Imported definitions were not patched to manufacture paste/schema/orientation
success. Component/import-generator failures remain blocking instead.

## Executed validation and evidence preservation

Fresh netlist source check passes. The initial attempt to pass prebuilt JSON to
`check netlist` was unsupported by this CLI and failed; it is preserved separately
and was corrected with the supported `index.circuit.tsx` command.
TypeScript passes. **60 routing regressions pass** (8 new width-audit cases).
Canonical board tests: **47 pass /2 fail**, retaining the real complete-copper
and strict-schema gates. Five new tests cover current-board manufacturer pin
assignments. No tests or limits were weakened.

Fresh netlist, pin-specification, source, schematic-placement and actual native
PCB placement checks all pass. Gerber export and the required Gerber-based shorts
check both fail **Unsupported shape polygon** in paste conversion. No completed
Gerber ZIP exists. Individual commands/exits/budgets are retained in
`validation-job-results.json` and `.outcome.json` receipts.
The earlier required full routed CLI build, PCB bitmap shorts and snapshot reached
their budgets. Those unchanged jobs are not re-run here and remain unapproved;
the fresh completed RootCircuit render does not erase those required gates.

Original native source snapshots, start/end events and strict-schema failures
are retained losslessly, with per-file hashes verified before any loose-file
archival removal. Diagnostic evidence is linked to the exact same native JSON.
No physical test, fabrication approval or order is claimed. Public WIP registry
version0.0.2-wip-pipeline9 remains the same board revision; a verification-only
commit does not require another unchanged package upload.

To approve ordering, all physical connections and unqualified interfaces must
be resolved, actual narrow power sections/USB/speaker geometry qualified, and
native schema/paste/Gerber/BOM/CPL/stock/mechanical/assembler gates must pass from
one matching revision. **This board currently fails those requirements.**

## Final visual and generator review

Inspected the fresh four-layer composite, top mask/paste, USB/charger,
amplifier/regulator, display/backlight and microphone detail images. Copper
regions and ordinary vias are visible, with the deferred J7 strip, J3 outer
contacts and remaining incomplete circuitry. Diagnostic warning text overlays
remain in the native images. These are PCB diagnostic views, not an approved
schematic/stencil/assembly visualization or proof of physical fit.

[Specific installed schema diagnostics](schema-details.json) confirm the same
169 failures: numeric `display_offset_x/y` where strings are required,
null `anchor_alignment`/`subcircuit_id`, and null `pcb_component_id` on native
mounting holes/two silk labels. These identify generator/schema inconsistencies;
they are not a reason to edit imported definitions or hand-rewrite native JSON.
The full original union error tree is [losslessly compressed](schema-audit.json.gz)
and hash-verified in [schema-archive.json](schema-archive.json).
Native start/end events are losslessly archived inside `native-build/`, with
per-member hashes and exact-byte restore instructions in its archive receipt.
