# Connection repairs — 0.0.6-wip-connection-repairs

**Engineering WIP; not ready to order.** The actual source-generated board has
53 native open-port errors, down from 89, and 13 physically open nets, down
from 25. No zero-error or working-hardware claim is made.

## Accepted source and native copper

`nominal-envelope-native/circuit.json` is the unmodified output of CLI 0.1.2237,
core 0.0.2090 and the frozen Bun 1.3.9 installation. The CLI ran inside the
complete publication runtime, completed in 256.86 seconds, and exited 1 on the
53 genuine native errors. The native SHA-256 is
`fb2f9c96ff000de1e18d6bf4d35bd41fea2323fc0b10730df4a0262b0bbdb73d`.
It contains 380 traces, 322 vias and 269 pours. The canonical
`dist/index/circuit.json` is byte-identical. Source snapshots and runtime input
hashes are retained; supported package metadata differs from repository scripts
and descriptions, while board source, dependency versions and models match.

Manual native paths repair charger supply/control and centre battery NTC,
USB data/control, display controller clock/reset and control escapes,
amplifier inputs/mode/positive output, microphone supply/clock branches and
U5's explicit ground connection. The J3 outer contacts and contact-dependent
J7 fanout remain untouched. No purchased component moves or import/model edits
were made. TP1 retains the preceding accepted placement.

Four complete replay phases (3, 5, 19 and 21) are replaced by labelled authored
native copper; 13 genuine retained phases replay without changing their original
cache files. Retired source routes and replacement receipts are explicit.
No new Pipeline9 or FreeRouting trial is represented as an accepted solve.

## Measured checks

- Zero physical shorts, zero clearance violations and zero merged named nets.
  The continuity audit still exits 1 because 13 nets are disconnected.
- All 8,152 terminal pairs connected in the v5 baseline remain connected;
  1,690 additional numbered-terminal pairs are connected. The rounded-pad audit
  honours the actual native corner radius and rotation. Earlier 8,146-pair
  receipts used the older contour method and remain historical evidence.
- All 245 authored regions preserve their nominal widths: 97 new connection
  regions, 124 retained power/control regions and 24 inner signal regions.
- All 322 vias have 0.30 mm drilled holes, 0.45 mm pads and a physical span over
  all four layers. No blind/buried via is accepted.
- All 80 retained authored high-current trunks and 67 checked high-current
  native traces use outer layers. The new inner VSYS segment is the separately
  identified U3 GAIN_SLOT input branch; its input-current qualification remains
  open, rather than being approved as a supply trunk.
- All 380 traces / 654 wire segments meet the 0.20 mm board minimum. **Two
  regulator source routes still violate their explicit 1.0 mm minimum with
  0.275 mm sections; 63 traces fall below named-net nominal widths.** Current,
  package necks, USB impedance and speaker pair quality are not qualified.
- All 125 purchased identities, footprints, poses and CAD models are unchanged.
  Source netlist, pin specification, source, schematic-placement and placement
  checks pass. Final native CLI schematic-placement reports zero issues.
- TypeScript and formatting pass; 80 routing regressions pass. Full board tests
  report 48 pass / 2 fail: fabrication completeness and strict native schema.
- Full installed schema still rejects 169 native elements. Official shorts/
  Gerber conversion still fails with `Unsupported shape polygon`. These are
  blocked official checks, even though the independent geometry audit finds no
  shorts. No generated record, import or check was weakened to bypass them.
- All 135 component explanations cover the 26 native A4 sheets and pass the
  annotation schema. Twenty-five rendered sheet SVGs exactly match the reviewed
  v5 pages; the changed speaker page and representative other pages were viewed.
  Four copper layers, mask/paste and USB/charger, both microphone, speaker and
  display details were viewed. Visual review is not fabrication approval.

## Outline generator defect and verified repair

The VBUS width failures were in the authored strip outline, not solely a via
termination. Flat-cap offset buffers at a short bend are not monotonic: increasing
drawn width can remove a wedge required by the nominal width. The generated
outline now unions the width-reserve contour with the complete nominal contour.
The real failing bend is covered by a regression test. Native verification then
passes the original full 0.5 mm trunks. Rejected 0.35 mm via-neck experiments
were removed; all prior native candidates and failed width receipts are retained.

## Remaining connections and fabrication gates

`remaining-native-errors.json` binds every remaining error to this native SHA:
46 J7 contacts, four U27 backlight contacts, U3/J4's two SPEAKER_N contacts and
U4's ground report. Both microphone ground pads physically contact the main
ground island; U4's native connection report remains an unresolved gate. The
disconnected GND islands are J7 pads. The physical open-net list consists of
GND, VLCD, five display logic nets, five backlight nets and SPEAKER_N.

J3's confirmed centre NTC is routed. Its outer numbered BAT+/GND polarity is
unassigned and excluded from the open-net count. J7 FPC contact face, pin-1 and
fold/mating orientation remain unqualified. Do not guess these interfaces.

The dated October 6 stock receipts still match all 125 exact identities; they
report J6/C160405 out of stock and do not qualify U1/D2/U16 assembly allocation
or reservations. Missing pill-pad paste, assembler rotations, bypass placement,
current/stackup, signal integrity, mechanics and final Gerbers remain blockers.
The standard JST programmer requires the documented three-to-six adapter,
separate target power and manual BOOT/RESET; no hardware test is claimed.

## Reproduction and publication

Use `scripts/cloud/setup.sh`, source `scripts/cloud/env.sh`, and run one heavy
operation at a time through `scripts/cloud/run_with_budget.py`. Do not resume
the old whole-net coordinator or run heavy routing on the Mac. The source/native
audit commands, per-command logs and explicit failures are retained here.
Snapshot and setup outcomes are recorded separately; references are not changed
merely to pass a comparison. Exact original native events and schema failure
trees are losslessly archived only after verifying every original byte.

`final-native.srj.json` is the latest actual converter input, with its own native
SHA receipt. The earlier speaker bus-lane and fanout failures and full inputs are
documented in [autorouter-diagnostics.md](autorouter-diagnostics.md); no external
issue or other-chat message was sent. Partial paired routes were not integrated.

GitHub and public tscircuit publication are completed only when their separate
anonymous verification receipts show exact source/native bytes. Native preview
availability does not establish passing cloud CI. No duplicate build, order,
watcher resume or physical-test claim is authorized by this WIP publication.

Final component inventory binds 496 numbered pin assignments to this native output and confirms 32 missing paste records on U16/U27. All eight documented programmer target paths remain logically and physically connected; both microphone grounds contact main GND. The original snapshot references are byte-identical after the completed 58.59-second failing comparison. Cloud setup verifies 397 checkpoint files, installs locked dependencies and passes all four supervisor smoke cases; its saved configuration draft still requires Environment settings publication.
