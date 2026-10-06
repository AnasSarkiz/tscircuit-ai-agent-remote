# Manual routing and Freerouting continuation — 2026-10-06

**No new board routes were accepted. Routing remains incomplete; NOT
FABRICATION READY.** The actual Freerouting SES contains zero new wires and
zero vias. Both manual contact trials returned zero proposals. The board
also received a fresh 0.05 mm manual-grid trial with the supported
0.0001 mm extra reserve (actual 0.2001 mm clearance), which returned zero paths
on all six eligible signal nets. Required native clearances remain unchanged.
The canonical native board and its inputs are unchanged from public board commit
`f9218aeda3400357075a57367aec7b89008f83af`.

Fresh independent audit of `dist/index/circuit.json`: **0 measured geometry
violations, 0 shorts, 26 physically disconnected nets**. Native output retains
**90 open-port errors**, 306 traces, 250 full-span vias and 190 pours. The full
connectivity/DRC gate fails (audit exit 1). All **152 authored region widths
pass**. Native JSON SHA256:
`81c31f77ac0871bfc4414b0940752e4f4fe0692a62089320b409908d4a8d5315`.
An unchanged board did not require another native render; the matching original
native build/source snapshot remains in the existing checkpoint. This turn ran
fresh copper/width audits and verified the preserved source bytes.

## Completed tool changes

- Installed official Freerouting **2.5.0** and Temurin **JDK 25.0.4.1+1** under
  the ignored `.tools/freerouting` directory. Official release digests were
  verified; the maintained installer repeats that verification. No TLS or
  checksum checks were disabled. Dependencies and lockfile remain unchanged.
- Added an explicit native-to-Specctra bridge retaining actual pad contours,
  old trace/via protection, complete via spans, drilled apertures, board outline,
  keepouts and every native BREP copper region including holes. Exact 5 mm
  subdivision changes region representation, not their union. Circular/pill
  geometry stays analytical. No imported component definition was edited.
- Measured the engine's actual **10 nm grid**, aligned synthetic pad centres
  to it and checked pad topology at the native auditor's 1 nm contact threshold.
  A permissive per-piece rounding check alone had concealed split concave pads;
  the strengthened check rejects that case.
- Represented existing SMT pad metal as fixed wiring areas, covered by its
  original pad geometry. Structure `plane` scopes made active nets plane nets
  before network parsing and caused the router to skip their remaining
  connections. Actual engine plane flags and net classes are now checked.
- Decoded actual SES units (one integer = 1 nm), placements, net identity,
  required widths and via stacks into **unaccepted proposals**, with no edits
  to Circuit JSON or fabrication of solver caches. The official CLI's
  extensionless base-design name is supported and tested.
- Added a proposal-to-native-source helper with an explicit 1 µm outward
  serialization reserve. It rejects reserved layers, protected nets, partial
  vias and degenerate/self-intersecting paths. The real SES produced an empty
  native-source proposal, so no board component was added.
- Fixed manual contact planning's universal 0.3 mm width: physical connections
  now use the source net's width (0.2 mm signals, 0.3 mm VMIC, 0.5 mm VBUS,
  1.0 mm PACK_BAT/VSYS). Existing 0.2 mm GND marker contacts remain limited to
  already physically connected islands. Real channel regressions prove legal
  narrow signal escapes and reject undersized power escapes.

The authored source checkpoint records this reviewed helper change and the new
maintained tools; all other prior checkpoint hashes are retained. This is a
tooling/diagnostic revision, not a new board version.

## Actual routing attempts

| Input / attempt | Actual result |
| --- | --- |
| Dense baseline, combined DRC/routing flags | `-drc` selected DRC-only mode; stopped at its 150 s budget in zone geometry. No routing success. |
| Dense baseline routing | Operator cancelled after 216.24 s in post-load connectivity; exit 143, no SES. |
| Exact partitioned baseline | Reached autorouting; 402 fixed-input clearance reports and 524 engine-global incompletes. Operator cancelled after 412.99 s in maze/drill geometry; exit 143, no SES. Peak process RSS 6.66 GB. |
| Initial pad-metal input | Plane-net semantics skipped real routing. Process tried to write a comma-separated output filename and failed (exit 1). `-do` actually accepts separate filenames. |
| Pad-metal input, output argument corrected | Saved an empty SES; still had the plane-net classification error. Process completion is not board completion. |
| Qualified fixed wiring-area input, all eligible nets | Actual active connections queued. First maze expansion was still running after 300 s; captured thread dump shows `ShapeSearchTree.completeShape` / expansion-room initialization. Operator cancelled at 347.84 s; exit 143, no SES. |
| Same qualified input, signal-only / all pours treated as obstacles | Attempted connections and logged no-connection, coordinate-range and null simplex-division errors. Saved an actual SES after 227.74 s: **0 wires / 0 vias**. No completed autorouting-pass event appears in the log. Exit 0 does not establish completion: official 2.5.0 CLI also returns 0 for timed-out jobs with saved output. |
| Manual nonzero contacts, old universal width | 0 proposals. |
| Manual nonzero contacts, actual nominal widths | 0 proposals; 30 unresolved contact groups recorded. |
| Manual 0.05 mm grid / actual 0.2001 mm copper clearance | 0 paths on AUDIO_ENABLE_SUPPLY, AMP_SD_MODE, MCU_LCD_RESET_N, MIC_SD, MIC_WS and MIC_BCLK; every missing ordinary through-via path recorded. |

Logs and `.outcome.json` files preserve the real command statuses, budgets and
memory observations. Operator cancellation receipts distinguish those trials
from successful completion. The signal-only run had a 3 minute internal timeout
and 300 s outer budget; its outer supervisor did not terminate the process.
Its terminal job state was not independently captured. Only the real empty SES
was decoded. No route was accepted from an unfinished or empty result.

All original DSNs, SESs, full export manifests and engine-rule receipts are
losslessly stored in `geometry-artifacts.tar.gz` (24 members, 52,703,028 original
bytes). `geometry-archive.json` records every member SHA256/size and verifies
every archived byte before removing duplicate loose files. Restore these inputs
with `tar -xzf evidence/freerouting-continuation-2026-10-06/geometry-artifacts.tar.gz -C evidence/freerouting-continuation-2026-10-06`.
Router-emitted whitespace is retained for exact reproduction; it is not source
formatting. The maintained-source whitespace check excludes raw evidence.

The final qualified transfer checked **1,013 pad layer/piece shapes, 523 native
pad/layer unions, 250 existing vias and 1,046 fixed areas** (559 exact native
pour subdivisions plus 487 existing SMT pad metal areas). Its qualification is
`fixed-areas-verification.json`, with actual engine receipts in
`fixed-areas-engine-rules.json`. The original input SHA256 is
`259574092f076374ee390e62d33df1463252997daccfdfad4166262cabfba74c`.
Use this original DSN, not `fixed-areas-roundtrip.dsn`: the official writer omits
cross-class clearance rules. Earlier qualifications are historical development
receipts and predate the active-net semantics requirement.

The engine reported **220 fixed-input clearance violations** with areas ignored,
and **2,299** when all areas acted as obstacles. Its 0.21/0.27 mm reserves are
stricter than the native auditor's 0.20 mm copper requirement, and its drill/
area/fragment representations and connectivity model differ. These engine
counts remain unresolved diagnostics; they are not a zero-DRC result and are not
silently discarded. Engine-global incompletes are also not the native 90 errors
or 26 physically disconnected nets. The native full-connectivity gate fails.

## Verification and continuation

- Routing/geometry regressions: **52 passed**.
- TypeScript and canonical maintained-source formatting: **passed** (92 files).
- Canonical board tests: **42 passed / 2 failed**, the retained native fabrication
  and strict Circuit JSON schema gates. Neither test was weakened or skipped.
- Fresh native copper audit: partial geometry/short checks pass; overall gate
  **fails** on connectivity. Fresh 152-region width audit passes.
- Frozen-lockfile cloud setup and all four supervisor smoke cases passed in the
  actual cloud instance. Verified installer repeat and JDK/CLI help passed.
- No board-source, imported-definition, dependency, lockfile, replay-cache or
  canonical Circuit JSON edits. No duplicate unchanged registry upload.

The maintained procedure is `scripts/routing/FREEROUTING.md`. Remaining routing
needs a qualified escape/placement solution and a successful native regeneration
that preserves previously connected ground and existing power widths. Existing
manual AMP routes from the preceding turn remain rejected because they split
U3 ground. Do not reuse them merely because they close AMP_SD_MODE.

J3 keyed outer BAT+/GND numbering and J7 physical FPC orientation remain
unqualified. J7 accounts for 46 native errors; unassigned J3 outer contacts are
not counted. The existing 169 schema failures, 32 missing pill-pad paste records,
unsupported polygon Gerber export, current/SI, BOM/CPL/stock and mechanical
qualification remain fabrication blockers. No orders or physical-test claims.

Reusable installation/start instructions are saved separately as a cloud
configuration draft after actual tool validation. A draft save does not apply
runtime settings, publish the environment or prove restoration in a new task.
