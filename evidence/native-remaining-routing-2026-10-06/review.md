# Native router continuation — 2026-10-06 (Europe/Tirane)

Engineering WIP; not fabrication ready. The user authorized remaining-trace
routing and suggested tscircuit bus lanes and fanout. All heavy work used the
Linux resource supervisor, sequentially. Pinned dependencies and supplier
imports were preserved. No incomplete solver output was added to replay caches.

## Native bus and fanout results

| Trial | Result | Elapsed | Peak RSS |
| --- | --- | --- | --- |
| Native bus-lanes phase, AMP_SD_MODE and AUDIO_ENABLE_SUPPLY | `source_net_4: two terminals required`; native output rejected | 148.69 s | 1.81 GB |
| Bus-lanes public solver, AUDIO_ENABLE_SUPPLY alone | `No collision-free local dogbone assignment` | 1.00 s | 229 MB |
| Public fanout solver, Q2, original boundary | Best assignment routed 0/1 | 1.50 s | 462 MB |
| Public fanout solver, Q2, boundary expanded by 2 mm | Best assignment routed 0/1 | 1.50 s | 460 MB |

The three-terminal AMP input truthfully records that R63/R64 were already
externally connected. That did not make the bus-lane solver accept the input.
Single-net diagnostics retained every captured obstacle, existing trace and
manufacturing constraint. `scripts/routing/solve-native-stage.mjs` provides the
public API repro for bus lanes/fanout and refuses to split differential pairs
or constrained buses. Inputs, requests and failed outcomes are retained.

## Freerouting export qualification

Freerouting was not invoked with the stock DSN export. The installed CLI
0.1.2237 bundles dsn-converter 0.0.90; its `convertCircuitJsonToDsnJson` calls
component/pad, plated-hole, net and trace processing only. It does not preserve
our native BREP pours, keepouts or standalone vias. Its default clearance is
0.15 mm and default via pad is 0.60 mm, versus this board's 0.20 mm clearance
and 0.70 mm via pad. Trace-via processing also uses a 600 micrometre diameter.
See `node_modules/@tscircuit/cli/dist/cli/main.js`, lines 353374, 353642,
353669, 353709 and 353723–353725 in the pinned installed version. A geometry-
and rule-faithful export/import adapter is required before accepting an external
route. No DSN route was claimed or substituted into native Circuit JSON.

## Manual routing trials

A 0.05 mm signal grid produced no complete routes on the original board for
nine selected upstream/amplifier/microphone nets. The fine full-span power
planner produced seven partial escapes and no complete distribution regions;
none were accepted. Conservative planner failures are not proofs that routing
is impossible.

R63/R64 placement trials were generated natively before acceptance. The first
had courtyard/pad clearance errors. A corrected courtyard position still
crossed Q1 gate copper. Moving R64 to (-10.1,-4.0), keeping R63 at
(-11.75,-2.5), retired the old AMP resistor link and removed those errors.
The manual planner then found two AMP_SD_MODE paths. Their first native build
measured zero geometry violations/shorts and preserved all 152 authored power
strip widths, but split the amplifier GND island. Moving the first signal via
0.40 mm to the right retained the same ground regression. Both are rejected.

Ground stitches, short contacts, ordinary via escapes and longer connections
to existing copper produced no complete ground repair. A final top-pour cutout
trial uses 0.21 mm rather than 0.26 mm. The manufacturing clearance requirement
and independent audit threshold remain 0.20 mm. It completed in 175.24 seconds / 1.68 GB peak RSS. Independent auditing found
six copper-to-drill clearance violations, zero shorts and the same U3 ground
regression. It is rejected; the 0.26 mm margin is restored. Required 0.25 mm
drill clearances and every original manufacturing check remain unchanged.

## Cloud setup observation

Existing retained Linux tools and the four supervisor smoke cases worked.
The supported setup script's frozen dependency install returned HTTP401 for
`api.github.com/repos/tscircuit/pcb-trace-linter/tarball/4c035f9`. This is a
clean-install blocker, not a passing clean setup. Dependencies/lockfile were
not changed to bypass it. The current workflow remains reproducible only with
the retained dependencies or restored authorized access to that archive.


## Accepted final state

**No new copper or placement was accepted.** Exact baseline source bytes and
canonical native JSON are restored and verified in `restored-checkpoint.json`.
The rejected candidates remain diagnostic evidence with their exact native
source snapshots, outputs and audits. Lossless native event archives retain
every original byte and include verified restoration receipts.

The accepted board still has **90 native open-port errors, 26 physically open
nets, zero measured geometry violations and zero shorts**. All 152 authored
power-region widths passed the baseline audit. The global connectivity/DRC
gate still fails. These trials do not resolve J3 numbered outer polarity, J7
contact orientation, 32 missing paste records, strict schema failures or
unsupported polygon Gerber export. No fabrication-ready claim is made.

The amplifier ground break demonstrates why a locally solved signal route
is insufficient. Further layout work must provide a qualified ground return
as well as signal escapes. An intentional thermal via inside the exposed pad
would require manufacturer layout guidance, an explicit assembly process and
separate documented validation; ordinary via rules must not be silently
relaxed to allow it. A qualified native or external routing adapter may also
need more escape candidates and preservation of pour connectivity.

Only diagnostic tooling/evidence is changed in this revision. The previously
verified public tscircuit release `0.0.2-wip-pipeline9` still matches the
accepted board; there is no new board version to upload. Upstream Pipeline9
report and exact original SRJs are already public in
https://github.com/tscircuit/tscircuit-autorouter/issues/2878.


## Verification and publication hygiene

TypeScript passes, all 17 routing regression tests pass, and maintained-source
formatting passes. Board tests retain 42 passes / 2 failures (fabrication
connectivity and strict native schema); these failures are not suppressed.
The refreshed checkpoint verifies all 325 recorded files. Native board source,
imports, caches and canonical board JSON are unchanged.

Root formatting initially scanned ignored `.tools` reference/configuration
files. A formatter log included the native CLI session credential; its saved
occurrences were redacted before staging. No credential value is included in
published evidence. Biome's documented force-ignore syntax now excludes both
`.tools` and `.geometry-runtime`, without excluding maintained sources.
The historical publication receipt was formatted with parsed JSON equality
verified, preserving every recorded value. The original receipt bytes are
retained as evidence. `publication-hygiene.json` records the saved-evidence
credential-pattern check. The credential appeared in tool output in the chat;
redacting saved logs cannot remove that earlier transcript output.

The maintained bus helper was rerun and reproduced the dogbone failure on
an input deep-equal to the prior single-net capture. To reproduce, restore
`start-35.json` from `amplifier-bus-lanes/native-events.tar.gz`, source
`scripts/cloud/env.sh`, then run under the supervisor:

```sh
python3 scripts/cloud/run_with_budget.py --seconds 60 --log /tmp/native-bus.log -- \
  bun scripts/routing/solve-native-stage.mjs bus_lanes \
  /tmp/remaining-native-bus-start.json source_net_5 /tmp/native-bus-result.json
```

For fanout, replace `bus_lanes` with `fanout` and append `pcb_component_53`;
an optional final `2` selects the tested expanded boundary. Outputs are trial
inputs/outcomes, not approved board routes.

All 359 initially staged files were checked for session credential patterns; no matches remained. The authored diff whitespace check passes; the full diff retains whitespace in captured native/source/log evidence as recorded in `whitespace-review.json`. No native evidence bytes were reformatted to hide these diagnostics.

The diagnostics source commit `2e789746bb1297f2b98a59715a393cfd4eea5259` is pushed to public main. Anonymous GitHub report and native JSON readbacks match local bytes. The unchanged native hash matches the previously complete public tscircuit receipt. A fresh registry download redirect was blocked by the cloud proxy (HTTP403); no new registry readback is claimed. `publication-receipt.json` records UTC timing; this evidence folder uses the local Europe/Tirane date.
