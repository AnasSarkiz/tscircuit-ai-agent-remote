# Manual routing repair and unresolved zero-DRC goal

Version `0.0.7-wip-manual-routing-repairs` is an untested engineering WIP.
**The board is not at zero DRC and is not ready to order.** The accepted repair
is U4 ground plus the clock/data escapes needed to clear its actual pad corridor.
The accepted native is `final-native/circuit.json`, copied byte-for-byte to
`dist/index/circuit.json`; SHA-256
`f9b4cd7b7974f24c830b212e4d175cc865d19a163ec30b43c139fc3b5894d184`.

## Accepted source and copper

The U4 ground route connects the real rounded pad edge near
(-16.296584, -28.505577) mm to the through via at
(-16.667038, -28.722740) mm with 0.36 mm top copper. Existing U5's 0.40 mm
edge escape remains intact. The conflicting U4 data path/region and original
clock escape are retired explicitly in authored source, then replaced on their
same electrical nets with real 0.20 mm paths. No fictitious pads, native JSON
edits or fabricated solver caches were used. `microphone-integration-receipt.json`
and the complete final CLI source snapshot identify this integration.

`final-cli-build.log.outcome.json` records the exact frozen-runtime supported
CLI build: completed in 251.86 seconds, peak process-group RSS 4,116,844,544
bytes, exit 1 on 52 native open contacts. Output has 381 traces, 325 through vias,
271 pours and 7,568 native elements. Repository/runtime board sources were
verified byte-identical before capturing the final output. Dependency versions
remain CLI 0.1.2237, core 0.0.2090, tscircuit 0.0.2744, checks 0.0.237 and
Circuit JSON 0.0.517. Curated publication changes only supported package
metadata/scripts; version, dependencies, board source and generated native
remain bound to the checked build.

`final-qualification/` contains the actual full-copper geometry audit, native
wire-width audit, three nominal region-width audits and connection preservation.
Measured shorts and geometric violations are both zero. All 9,842 previously
connected numbered-terminal pairs are preserved, with no missing ports. All
247 authored regions pass: 99 connection, 124 power and 24 inner-signal regions.
All 325 vias physically span all four layers at 0.30 mm hole / 0.45 mm pad.
All 80 authored high-current trunks and 67 native high-current traces use outer
layers. All 125 purchased component footprints, poses, models and supplier
identities remain unchanged. `protected-baseline-comparison.json` verifies 242
original imported/model/lock/solver files unchanged against the v6 manifest.

The geometric audit still exits 1: 52 real native connection errors and 13
physically open nets remain. The wire-width audit still exits 1: two regulator
traces contain 0.275 mm sections below explicit 1.0 mm source requirements,
and 63 traces are below named-net nominal widths. No trace is below the general
0.20 mm board minimum. Nominal regions passing does not qualify those narrow
wire sections, load/current or USB/speaker signal integrity.

Native edge-GND warnings associate 0.30 mm `pcb_trace_0` with the named direct
edge escapes; actual named U5/U4 output is 0.40/0.36 mm respectively. The native
warnings are retained, and the measured-width receipts identify the real copper.
This association problem was not used to delete or approve any actual error.

## Rejected speaker routing

The 0.60 mm SPEAKER_N attempt needed a real 1.0 mm VSYS reflow. A diagnosed
planner defect tested layer exits before reserving a proposed through-via drill;
that reachability is now checked after reserving the actual drill on all layers.
Keeping the original right-side VSYS bridge fixed allowed a proposal reconnecting
all 23 original VSYS anchors. Its explicit paths/regions and preserved source
indices are recorded; no supply copper was silently discarded.

`speaker-named-pair-native/circuit.json` is the completed actual candidate.
It measures zero shorts/clearance violations and connects SPEAKER_N, but the
native pour reflow splits U25.2/C76.2 ground and loses 266 prior terminal pairs.
It also emits `pcb_bus_length_skew_error`. Therefore it is rejected and is not
in the canonical/published native or current board sources. Original source
power copper, port-based speaker-pair selectors, maximum skew 2 mm, trace gap
0.20 mm and maximum uncoupled length 5 mm are restored unchanged.

`speaker-skew-reproduction.json` reproduces the actual error with installed
`checkPcbBusLengthSkew` on the untouched candidate. It compares separate
source traces: one P escape (2.400 mm), the N escape (2.254 mm) and the N trunk
(75.154 mm), even though N's two pieces share a net. P's existing BREP trunk has
no `pcb_trace` length contribution. The 72.900 mm native finding remains real;
this representation issue does not establish acceptable physical full-net skew
or coupling. The separate P replacement proposal would still leave approximately
9.35 mm total skew, exceeding the original 2 mm requirement. Neither it nor the
proposed ground repair is native-qualified or accepted. See
`speaker-candidate-disposition.json` for explicit rejection.

The installed supported manual phase `pcbTracePaths`/fanout API permits widths
on individual wire points. A future paired manual implementation must preserve
real endpoints and source-trace associations, all supply anchors and previous
terminal connections, then qualify actual full-net skew/coupling. It must be
identified as authored manual phase paths, never forged autorouter output.

## Checks, visual review and blockers

All five supported source checks pass on the exact final runtime: netlist,
pin specification, source, schematic placement and PCB placement. Their complete
receipts are in `final-source-checks/`. The earlier 180-second attempt was stopped
partway through source analysis; its retained log is not counted as passing.
The complete rerun took 407.65 seconds.

`artifact-checks.json` records every remaining actual command and outcome.
Board tests execute 50 tests: 48 pass, two fail on native errors and strict native
schema. Strict schema finds 169 invalid emitted records. Official shorts exits 1
with `Unsupported shape polygon`; independent geometry does not replace that
required export/check gate. Purchased-part inventory finds 32 missing pill-pad
paste records on U16/U27. Resolved BOM has 125 rows, 43 exact supplier identities,
zero blank descriptions and zero supplier codes used as package names.
No diagnostic BOM/PnP output is approved for fabrication. Guide coverage passes
for all 135 references and 26 A4 pages. The actual current SRJ and converter
receipt are `final-native.srj.json` and its receipt.

`final-visual-review.json` records only images actually inspected in this run:
U4 zoom, the four-layer mosaic and microphone schematic. Fresh renders of every
layer and all 26 schematic pages are retained. Diagnostic warning overlays remain
visible. The unchanged component guides and electrical schematic are not a new
claim of production silkscreen, mechanical or assembly approval. The supported
source snapshot comparison and unchanged references are recorded separately;
snapshot failures are not accepted solely to obtain a green result.

Current routing opens are 46 J7 display contacts, four U27 backlight contacts and
two speaker contacts. J3 centre NTC is connected, but its unassigned outer contacts
are excluded from the count. Battery keyed contact numbering and the exact
ER-TFT026-1 no-touch panel contact face, pin-1 and fold/mating orientation remain
unqualified. Primary exact product/drawing retrieval failed with HTTP 403;
`suppliers/retrieval-receipts.json` preserves URLs and actual denials. Public
code references point to the same blocked PDF and are not supplier confirmation.

Required outside action: add `www.buydisplay.com` and `www.elektronik.ropla.eu`
to the existing Environment settings allowlist, then save and publish it. The
editable allowlist was unavailable and was not replaced. The onboarding setup
skill explicitly says to report required domain additions “rather than replacing
an unknown list.” See
[setup skill](skill://plugin_connector_1p_ed5feb9070a08191b08c81c47947bc16/setup/SKILL.md).
No unsupported battery polarity or display mating was guessed.

Dated JLCPCB stock review still has J6/C160405 unavailable; quantities/allocation,
rotations, bypass placement, stackup/current, signal integrity and mechanical
fit remain unqualified. The public standard JST programmer needs the documented
three-to-six UART adapter, separate target power and manual BOOT/RESET. No
physical prototype, programmer test, order or cloud-CI success is claimed.

## Cloud process cleanup

The short source-check budget exposed a real supervisor defect: a Bun descendant
ignored SIGTERM after its parent exited, allowing the wrapper to clear the lock
while the child was still live. The task-owned orphan was stopped. The supervisor
now checks live process-group members, waits for the group and kills stubborn
descendants before releasing its exclusive lock. Zombies are excluded from live
resource checks. All five smoke cases pass, including the new actual descendant
case; `supervisor-smoke/receipt.json` preserves full outcomes. Routing runs remain
serial and budget-limited. Saved installation/startup instructions remain in the
existing environment draft; fresh-task publication was not observed here.

Acceptance gates remain explicit: requirements/interfaces **blocked**;
schematic/BOM **blocked**; final physical placement **in progress**;
routing and automated/fabrication qualification **blocked**; ordering and
physical testing **not started**. Publication receipts, final code-check counts,
snapshot outcome and checkpoint verification are recorded separately and never
turn this partial repair into zero DRC.

Final code validation passes: all 87 routing regressions, TypeScript and
formatting are recorded in `final-source-checks-complete.log`. The supported
source snapshot completes in 61.10 seconds and exits 1 with PCB and schematic
mismatches. Existing snapshot references were preserved. All underlying failed
commands completed normally; a completed command is not inferred to have passed.

## Verified public publication

Source commit [`b47059aa028a9e3bba37be1e64d101fd57e24097`](https://github.com/AnasSarkiz/tscircuit-ai-agent-remote/commit/b47059aa028a9e3bba37be1e64d101fd57e24097)
is public. Anonymous GitHub readback verifies all 125 packaged paths against
the repository source/native bytes and observes the HTML Public badge. Only
supported `package.json` publication metadata differs between repository and
curated runtime; the board source and native JSON match exactly.

Public tsci version `0.0.7-wip-manual-routing-repairs` is release
`52ef3bae-1c65-4056-81db-2e9841c86fb6`.
[Exact native preview](https://tscircuit.com/AnasSarkiz/tscircuit-ai-agent-remote/releases/52ef3bae-1c65-4056-81db-2e9841c86fb6/preview).
All 125 files hash-match anonymous readback; no missing/extra/mismatched files
remain. The public/listed release is ready to build. Its native preview exactly
matches all 7,568 validated local elements and 26 A4 pages, with HTTP 200.

The initial official compressed push completed with exit 1 after HTTP 413/502
upload failures. Anonymous inspection after completion established exactly 122
matching stored files and three missing files. Only those missing native/STEP
files were resumed through the official archive API, with a 2,645,759-byte
round-trip-verified archive and HTTP 200. The first read made while the upload
was still running had inconsistent transient file/list counts and was not used
for a retry. All authenticated raw logs remain outside the repository in `/tmp`.
`official-tsci-push-outcome.json`, `stable-partial-registry-receipt.json`,
`resume-registry-upload-receipt.json` and `final-registry-receipt.json` preserve
the distinct failed/partial/resumed/verified outcomes.

One existing automatic cloud job is observed:
`84d57c5a-b0b1-474a-abfb-f164c10dcb8b`. Its user-code job started at
2026-10-06T23:56:42.772Z; circuit JSON building had not started at the recorded
read. No duplicate job was queued and no passing cloud CI is claimed.
Publication and preview verification do not alter the 52 open connections or
any other fabrication blocker. This metadata update changes no packaged board,
source, model, dependency or native bytes.
