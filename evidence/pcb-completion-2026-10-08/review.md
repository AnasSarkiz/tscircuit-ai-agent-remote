# Generator and fabrication-export WIP qualification — 2026-10-08

**0.0.11-wip-generator-qualification. NOT READY TO ORDER.**

The actual board is regenerated with three pinned canonical project packages.
These fixes remove schema and paste failures, preserve genuine supplier
geometry, correct Excellon slots, and enforce routing-disable controls. They do
not complete the still-unqualified display/backlight or battery interfaces.
No generated JSON, supplier geometry, solver results or validation threshold
has been edited to pretend that a required connection is complete.

## Measured before and after

| Metric | Before .10 | After .11 |
|---|---:|---:|
| Native traces | 381 | 381 |
| Ordinary full-span vias | 320 | 320 |
| Missing PCB-port connections | 50 | 50 |
| Physically open assigned nets | 12 | 12 |
| Unassigned J3 outer contacts | 2 | 2 |
| Measured shorts | 0 | 0 |
| Measured geometric clearance violations | 0 | 0 |
| Explicit source width violations | 2 | 0 |
| Full native schema failures | 169 | 0 |
| Missing exposed pill-pad paste records | 32 | 0 |

Every actual geometry/electrical record is compared to the audited completed
native generation. `current-copper-audit.json` is a fresh direct audit of the latest generated
native, whose exact SHA is bound by the final receipts;
`current-connection-preservation.json` independently checks every parent pair.
All 9,813 previously connected terminal pairs and all 125 purchased poses remain.
U14 uses the untouched genuine C7848 download with 20 pads and correct supplier
pin-1 rotation; other 124 supplier geometries remain identical. No additional
purchased components are introduced. No previously open net is newly closed.

## Runtime corrections and verification

`toolchain/provenance.json` binds all canonical source changes, bases, regressions
and three actual package artifacts. Core is based on 0.0.2090 and emits valid
position/optional ownership metadata and actual-world pill paste. Circuit JSON
0.0.521 accepts legitimate ownerless board silkscreen but rejects malformed
records. Gerber 0.0.112 emits both G85 slot endpoints in one Excellon block.
The schematic source also corrects both symbol label widths, capacitor grouping,
R42 rail orientation, charger set-resistor placement and local support branches.
All 15 original UI issues are eliminated in actual schematic trials. One newly
exposed diode/resistor facing advisory remains: VMOTOR is a multiway power rail
with a flyback diode and independent bleeder, not a two-terminal series node.
Both positive contacts face up and align on the same rail. Its reported failure
and exact endpoint review remain preserved; it is not suppressed or counted as
a passed UI style gate. All actual PCB/CAD placement records stay identical.

Core additionally fixes an update lifecycle path that ignored both disabled
routing controls; the preserved baseline fails both controls, and the patched
three-test regression retains a routing-enabled positive control. Ten focused
core regressions and full typed builds pass. Actual MCU diagnostic has zero
routing events and zero copper. Board tests: 51 pass / 1 fabrication failure.
Completed full regeneration uses Bun 1.4.0. The prior Bun 1.3.9 build hit its
600-second budget without completing; source/phases and the failed outcome
remain retained, with its copied stale native explicitly excluded. Frozen install
and board tests still run on Bun 1.3.9. This records observed outcomes, not a
proven cause of the runtime performance difference.

Ninety-nine routing regressions pass. Failed gates remain visible.

REG_L1 and REG_L2 have an explicit local 0.275 mm escape contract limited to
0.751 mm, on top, followed by at least 1 mm of 1 mm trunk. With finished 35 um
outer copper, resistivity at 125 C and the TI 5.75 A peak bound treated
conservatively as DC, each measured path is 3.574 milliohm, 20.55 mV and
118.16 mW. Tests reject undersized, extended, inner-layer and missing-trunk
paths. This is a calculated escape contract, not whole-board thermal approval.
All 65 remaining named-net nominal-width differences still require individual
branch-current, copper-union and electrical qualification. All 250 authored
region width checks pass. Vias remain through-hole 0.30/0.45 mm; high-current
trunks remain on outer layers; unchanged microphone bypass is 1.442790 mm
supply and 0.599976 mm ground entry, with no bypass via.

## Exports and components

All actual outputs are labeled NOT FOR FABRICATION. Strict PnP covers 125 rows
with zero supplier rotation errors or warnings. The official resolved BOM has
125 rows, zero empty descriptions and genuine packages for all 43 identities.
Raw unconfigured BOM output still fails its content gate and is retained.
PyGerber 2.4.3 parses all 12 actual Gerbers with Raise-on-error. PCB-tools 0.1.6
reads 320 via drills, four genuine USB plated slots and five other round plated
holes; eight nonplated holes include six genuine component holes and two
mounting holes. The complete independent parser receipts and four-layer/outline
screenshots are retained. The patched Gerber artifact is a typed library build;
the standalone upstream CLI and unavailable full visual suite are not claimed.

Official current public JLCPCB records have no unresolved HTTP results across
43 exact identities. Thirty-nine conservatively cover one board. D2/C94934 is
out of stock. U1/C2913201, U16/C54313 and R5/C364359 have positive public stock
but uncertain assembly eligibility; zero presale fields are not treated as proof
of zero assembly inventory. C97502 is a researched USB-protection lead, not an
installed or qualified replacement. No assembler allocation or order is made.

## Exact remaining interface and mechanical evidence

There is **no final qualified selected LCD or verified final J7 mapping**.
The current rejected ER-TFT026-1 / AFC07-S50ECA source remains provisional.
ER-TFT028A3-4 primary manufacturer mechanical/contact/pinout documentation is
unavailable through the current network. Alternate manufacturer ER-TFT028A2-4
PDF verifies ILI9341, 50 pins at 0.5 mm, top-contact mating, 0.30 +/- 0.03 mm
terminal thickness, 26.7 mm tail, 69.3 x 50.2 x 2.8 mm folded body and
57.6 x 43.2 mm active area in landscape. Its centered candidate overlaps the
current RF zone by 59.5 mm2. Exact mating registration and minimum folded-flex
bend radius/material or unbent geometry remain unqualified. It has common
cathode/four anodes, 70 mA typical / 80 mA maximum total; the current TPS60230
current-sink circuit is not connected unchanged to this opposite topology.
No final backlight redesign or verified current-setting BOM is claimed.

AKY2945 documentation verifies red positive, yellow NTC and black negative;
J3 centre pin 2 is NTC. It does not register either outer numbered contact to
an unambiguous mating-face/latch view. Final J3 pins 1/3 polarity is unresolved.
The PCB remains approximately 50 x 65 x 1 mm. The requested enclosure limit
is 60 x 75 x 16 mm; a complete final LCD/battery/RF/connector assembly is not
qualified. The standard direct JST SH3 programmer interface remains implemented,
with separate power, manual BOOT/RESET and enclosure access; hardware untested.

The running environment still reports restricted network, spec 1, no custom
hosts; TI/Waveshare/DFRobot CONNECT attempts and preferred display HTTP403 are
preserved. The saved onboarding draft retains all old hosts plus the necessary
manufacturer hosts; **saving does not apply or publish runtime configuration**.
Primary missing documents are listed in `network-qualification.json`.

Unresolved assigned nets: GND, VLCD, LCD_SDA, LCD_SCLK, LCD_DC, LCD_RESET_N,
LCD_CS_N, LCD_BACKLIGHT_OUTPUT and LCD_BACKLIGHT_RETURN_1 through _4. The native
50 connection errors are 46 J7 contacts plus four U27 outputs. Two unassigned
J3 contacts are additional: 52 unresolved required contacts in total. Do not
confuse zero geometric violations with zero full-board DRC errors.

**ROUTING COMPLETE = NO**  
**UNCONNECTED REQUIRED CONTACTS = 52**  
**PHYSICAL OPEN NETS = 12**  
**DRC ERRORS = 50 native connection errors; 0 measured geometric violations**  
**SCHEMA FAILURES = 0**  
**FABRICATION READY = NO**

Source/publication and latest native SHA are established by the final receipts,
not by a presumed cloud build. Public upload success does not qualify routing,
mechanics, current capacity, physical hardware or fabrication.

## Latest generated output and retained warnings

The final schematic-source build uses Bun 1.4.0; its exact completed duration
is retained in `final-schematic-native-build.log.outcome.json`.
Its exit code remains 1 for the 50 connection errors, not a passed routing gate.
The fresh full native UI analysis reports one retained style advisory, down
from 15 original issues; `ui-analysis/ui-style-analysis-receipt.json` binds it
to the exact latest native SHA. All five source checks pass.

The final dump-enabled generation retains 16 HTTP503 supplier-refresh warnings
and four pin-attribute lookup warnings. Every genuine local imported footprint,
model, purchased pose, source component and electrical port record remains
unchanged. Nineteen replayed traces omit optional endpoint tags; four equivalent
vias receive new record IDs. These are reviewed metadata differences, not
byte-identical raw records. The complete rejected byte comparison and exact
review are retained in `final-dump-generation-comparison-rejected.json` and
`final-retained-metadata-review.json`. No output warning or record is removed.
Fresh direct copper, connected-pair, schema, strict supplier rotation and UI
checks are required on the latest raw native. The final CLI completed output
and all 13 real SRJs are retained; original session supervisor telemetry became
unavailable, so no unverified final duration or memory claim is made.

The full routed schematic also exposed R63/U3 net-label overlap missed by the
placement-only trial. The suggested simultaneous schematic moves (R63 X -1
to -1.13; U3 X 2 to 2.13) are applied to the source, and the final regeneration
and actual UI recheck determine the accepted result. Previous native, visible
UI failure, exact highlighted SVGs and snapshots remain archived in
`before-final-label-clearance/`. These are schematic changes only.

Cloud continuation draft revision 32 is independently read back. Its current
priority supersedes the historical .10 package instructions, preserving all
repositories, network and credential requirements. Saving does not apply the
runtime policy. Setup now prepares the checksum-verified official Bun 1.4.0
binary separately from Bun 1.3.9 frozen install/tests.

## Publication recovery qualification

GitHub implementation commit: `3d2393b8ac5670e1ea3a76000a4e6a0e17905c46`.
The clean 134-file runtime package exactly matches the completed source/native
archive. The released CLI archive push receives HTTP413; file-by-file fallback
partially uploads before its 180-second budget. Anonymous readback, not the
CLI success lines, establishes the exact missing set. The native is stored
through the supported archive endpoint without changing its bytes.

The existing supported archive-resume helper now preserves binary runtime
artifacts using the released CLI's `content_base64` field. JSON remains text
for the native preview. Actual gzip round trips and hashes are checked, and
staged-byte changes are rejected. The preserved before fixture fails on binary
bytes; the corrected fixture passes. Two new guards pass without network or
credentials. Supported JSON and multipart transports are recorded explicitly.
A gateway HTTP502 completed a supplier STEP write later; the strict fresh-list
guard correctly refuses the stale receipt. No upload failure or readiness is
counted as a complete publication. Final anonymous receipts determine delivery.

## Verified public delivery and latest checks

The implementation is [commit 3d2393b8ac5670e1ea3a76000a4e6a0e17905c46](https://github.com/AnasSarkiz/tscircuit-ai-agent-remote/commit/3d2393b8ac5670e1ea3a76000a4e6a0e17905c46).
Public [WIP .11 preview](https://tscircuit.com/AnasSarkiz/tscircuit-ai-agent-remote/releases/8fe561a8-c751-44f1-a168-fe0dba085bf8/preview).
All **134/134** GitHub and registry files match the exact clean source/native
package anonymously, including the three genuine binary runtime archives.
The native preview equals every actual local record. The release is public,
unlisted=false, ready-to-build=true. Publication and native access are complete;
cloud CI and fabrication success are not inferred. `final-cloud-build-observation.json`
retains the actual jobs; no duplicate request or watcher is started.

Actual source snapshot runs complete with unchanged golden references and fail;
references were not overwritten to manufacture acceptance. A full rerun exposed
an optional replay-annotation assumption in the contact-preservation test.
The raw failed results remain. The corrected comparison now requires a unique
actual port at each endpoint's position/layer AND declared connectivity, then
compares the same real numbered terminals and all original copper coordinates,
widths and layers. Negative cases reject moved copper and a wrong declared
contact. No source copper or emitted native record is changed by this correction.
Final full suite: **54 pass / one genuine fabrication-gate failure**, with
717 assertions; typecheck and formatting pass. The 51 original positive board
checks, one new physical-contact guard and two binary publication guards pass.
The failure is still the 50 real native connection errors. See
`delivery-code-checks-qualified.log` and `replayed-contact-and-binary-regressions.log`.

Saved cloud draft **33** is independently read back, preserving install script,
main repository membership, network policy and credential requirements. It
contains the actual verified source/native/release and current continuation
controls. `final-network-observation.json` proves the running policy still has
no custom hosts; a draft save is not runtime application. To activate those
manufacturer-domain settings, review/save them in Environment settings and
publish the environment. No settings activation is claimed here.

Latest screenshots: `ui-analysis/ui-style-analysis.png`,
`ui-analysis/style-issue-0.svg`, and all four copper/outline PNGs in
`NOT-FOR-FABRICATION-qualified-gerbers/`. Actual Gerber, resolved BOM and strict
PnP outputs remain explicitly NOT FOR FABRICATION. No newly open net was closed
in this step; all 9,813 existing connected pairs are preserved.

The final cloud observation has three terminal jobs: the latest-created job
`30adaa51-46ef-4f39-8c75-d3f6542eb77a` completes with null reported user-code
error; two earlier jobs report code build errors. No jobs remain in progress,
no duplicate rebuild is requested, and full-board DRC/fabrication is not inferred.
The public native is rechecked after these jobs finish; its exact current
object remains the accepted generated board. See `post-cloud-preview-confirmation.json`.

## Cloud-generated final native adoption

After the platform jobs completed, the preview selected the genuine cloud
source output rather than the earlier uploaded local output. The previous
preview-equality receipts are historical. The accepted final native is the original cloud-produced file, SHA-256
`2d9986066c0b4198ac56fba7308fbbbc841c2fd5999bbf560b89d16fd3f94e67`. Its parsed object exactly equals the separately qualified
`c4142f7c7cd77f85db22c48e49781b18bddb30a48f5927786376a478ed13b7bf`
serialization. Original file bytes were acquired from the registry file endpoint. Its raw HTTP envelope and both
whole generated native files are retained in `cloud-generated-native/`.
No output record is removed, repaired, overridden or merged. Only the complete
object's file representation is serialized. This is an actual cloud source
regeneration, not a hand repair of Circuit JSON.

The source filesystem metadata is exactly equal. All schematic/electrical
source records, purchased geometry and all actual copper match. The cloud
restores 19 optional endpoint annotations and four equivalent original via IDs,
and naturally has none of the 16 supplier/four pin-attribute lookup warnings.
The older warning-bearing local output is retained intact. Fresh raw-native
schema/paste, official shorts, strict rotation, BOM, actual SRJ, regulator/region
width, direct copper/pair/independent Gerber and UI checks qualify the accepted
cloud output separately. The local actual 13-phase SRJs and source archive remain
valid source/geometry evidence; no cloud solver input is fabricated.

The GitHub and registry native files are synchronized to this complete genuine
output, then all 134 public file bytes and the current public preview are checked
again. Final delivery receipts supersede earlier local-output receipts.

Original cloud file schema/paste and independent copper were checked again directly; direct comparison preserves all 9,813 pairs with zero newly connected pairs. Historical receipts retain their original input hashes; `cloud-generated-native/raw-cloud-artifact-adoption.json` binds exact parsed-object equality without rewriting those execution receipts.

## Final authoritative delivery

Source commit `8ef0fc6992b41d5cc57030c6c64c2519e260e4e9` is publicly verified: all 134 prepared source/runtime/native files match anonymous GitHub and registry bytes; the current preview equals the actual cloud native exactly. Registry additionally retains 37 platform-generated compiled, asset and preview files. Consequently the original strict exact-file-list helper correctly fails on extra paths despite 134/134 uploaded-byte matches; this gate has not been weakened and no cloud output is deleted. `final-registry-receipt.json` lists every extra path.

Saved cloud draft **34** independently preserves installation/repositories/network/credential metadata and corrects current native/source provenance. It still requires review/save/publish in Environment settings for runtime application. Earlier draft/public-native claims are historical.

ROUTING COMPLETE = NO; UNCONNECTED REQUIRED CONTACTS = 52; PHYSICAL OPEN NETS = 12; DRC ERRORS = 50 native connection errors (0 measured copper shorts/clearance violations); SCHEMA FAILURES = 0; FABRICATION READY = NO.
