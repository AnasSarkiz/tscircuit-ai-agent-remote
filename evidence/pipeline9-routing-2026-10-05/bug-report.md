# Pipeline9: high memory use and iteration exhaustion on a four-layer USB routing input

## Summary

`AutoroutingPipelineSolver9_PreloadedTraceGraph` from
`@tscircuit/capacity-autorouter@0.0.958` did not complete routing two USB nets
in the attached board input. A native run exceeded its time budget; a direct
public-library run of the same input exceeded its memory budget while in
`topologyMergingSolver`. A separate native trial with less existing copper
returned an iteration-limit error.

These are observed failures for specific inputs, not a confirmed root-cause
diagnosis or proof that a valid route exists. The original board copper was
restored, and no routes from these failed trials were accepted.

Observed: 2026-10-05. All reproduction artifacts below are pinned to public
repository revision
[`8d478c7ccb2cfb0df53f14447c7d71cad78c43d2`](https://github.com/AnasSarkiz/tscircuit-ai-agent-remote/tree/8d478c7ccb2cfb0df53f14447c7d71cad78c43d2).

## Environment

| Item | Version / setting |
| --- | --- |
| Runtime | Bun 1.3.9, Linux cloud |
| Capacity autorouter | 0.0.958 |
| tscircuit core | 0.0.2090 |
| tscircuit props | 0.0.688 |
| tscircuit | 0.0.2744 |
| tscircuit CLI | 0.1.2237 |
| Explicit selection | `autorouterVersion="beta_pipeline9"` |
| Recorded native solver | `AutoroutingPipelineSolver9_PreloadedTraceGraph` |
| Routing preset / effort | `auto_local` / 1 |
| Solver cache | Disabled: `no_cache_engine` |
| Supervisor memory limit | 22,333,829,939 bytes, 65% of available instance memory |

No dependency, router runtime, iteration-limit or manufacturing-rule patches
were applied. Exact installed-source hashes and selection references are in
[`supported-pipeline9-reference.json`](https://github.com/AnasSarkiz/tscircuit-ai-agent-remote/blob/8d478c7ccb2cfb0df53f14447c7d71cad78c43d2/evidence/pipeline9-routing-2026-10-05/supported-pipeline9-reference.json).

## Routing input

The board is 50 × 65 mm with four copper layers and 135 electronic components.
The selected phase contains two nets, `source_net_68` (USB_DN) and
`source_net_69` (USB_DP), each with four terminals. These routes cross much of
the board, from the lower connector toward the MCU area; this is not a minimal
two-pin routing example.

- Net trace widths: 0.2979 mm; global minimum trace width: 0.20 mm.
- Via pad diameter: 0.70 mm; drill diameter: 0.30 mm; blind/buried vias disabled.
- Trace-to-pad-edge clearance: 0.20 mm; board-edge clearance: 0.25 mm.
- Differential pair: 0.2101 mm gap, 0.5 mm length tolerance, maximum
  uncoupled length 5 mm.
- Full-copper input: 9,279 obstacles and 7 preloaded traces.
- Reduced-copper input: 2,996 obstacles and 0 preloaded input traces. This
  temporary source trial omitted manual signal/power copper while retaining
  the components, placements, constraints and original saved-route files.

The exact full-input metadata is recorded in
[`actual-pipeline9-start-receipt.json`](https://github.com/AnasSarkiz/tscircuit-ai-agent-remote/blob/8d478c7ccb2cfb0df53f14447c7d71cad78c43d2/evidence/pipeline9-routing-2026-10-05/actual-pipeline9-start-receipt.json).
Original inputs and events are preserved losslessly, rather than recreated
from the current board source.

## Actual results

Peak memory below is the supervisor's sampled process-group RSS, in bytes.

| Attempt | Elapsed seconds | Peak RSS | Observed result |
| --- | ---: | ---: | --- |
| Full input, native rendering | 660.99 | 11,803,729,920 | Supervisor `TIME_BUDGET_REACHED`; process terminated with SIGTERM, exit −15. Last reported progress approximately 0.2323. No completed route or phase-end event. |
| Same full input, direct public-library runner | 96.84 | 22,385,528,832 | Supervisor `MEMORY_BUDGET_REACHED`; SIGTERM, exit −15. Last recorded phase `topologyMergingSolver`, progress 0.2327936323, iteration 167014. No completed output. |
| Reduced-copper input, native rendering | 448.21 | 17,378,430,976 | Router returned `aJ ran out of iterations (capacity-autorouter@0.0.958)` after progress reached 0.44. Native render process exited 0 but its output retained a routing error. |

The first two are externally stopped incomplete runs, not solver-returned
iteration failures. The direct-library run generated no intermediate preview
frames, so that attempt's memory-limit failure does not require preview
generation. The precise source of the memory growth remains unconfirmed.

The reduced-copper native error was:

```text
Async effect error in PcbTraceRender "autorouting":
AutorouterError: aJ ran out of iterations (capacity-autorouter@0.0.958)
    at runCycleAndQueueNextCycle (.../@tscircuit/core/dist/index.js:107448:24)
    at <anonymous> (.../@tscircuit/core/dist/index.js:107483:27)
```

That rejected trial output contains one `pcb_autorouting_error`, 418
`pcb_port_not_connected_error` elements and seven `pcb_trace_missing_error`
elements. The additional disconnected ports cannot all be attributed to a
router defect: manual copper was intentionally omitted in this trial.
Rendering exit 0 must not be interpreted as successful routing.

## Reproduce the observed direct-library failure

Use a fresh disposable checkout, Bun 1.3.9, Python 3 and GNU tar on Linux.
Dependency installation needs access to the package sources used by the
lockfile. Commands use the public API and unchanged captured route input:

```sh
git clone https://github.com/AnasSarkiz/tscircuit-ai-agent-remote.git
cd tscircuit-ai-agent-remote
git checkout 8d478c7ccb2cfb0df53f14447c7d71cad78c43d2
source scripts/cloud/env.sh
bun install --frozen-lockfile

tar -xOzf evidence/pipeline9-routing-2026-10-05/usb-net-phase-native/native-events.tar.gz \
  start-35.json > /tmp/pipeline9-start.json
sha256sum /tmp/pipeline9-start.json

python3 scripts/cloud/run_with_budget.py \
  --seconds 600 --log /tmp/pipeline9-repro.log -- \
  bun scripts/routing/solve-pipeline9.mjs \
  /tmp/pipeline9-start.json /tmp/pipeline9-output.srj.json
```

Expected extracted-file SHA256:
`01445de85cc77738ea9aec7ff79f7beeda0b5f1e99de323104bbc72c86d16e04`.
The supervisor chooses 65% of available RAM, so a smaller machine may stop
earlier. It writes the actual resource limit and result to
`/tmp/pipeline9-repro.log.outcome.json`; observed time and RSS are not guaranteed
to match on other machines.

The runner calls:

```js
const solver = new AutoroutingPipelineSolver9_PreloadedTraceGraph(
  capturedStart.simpleRouteJson,
  { effort: capturedStart.effort ?? 1 },
)
// Repeated solver.step() until solver.solved or solver.failed.
```

It writes `getOutputSimpleRouteJson()` only after the solver succeeds and
throws if the solver reports failure. This is a diagnostic runner, not a
replacement cache or a generated board artifact.

## Reproduce the reduced-copper native iteration error

In the same fresh disposable checkout, after the preceding operation has
ended, restore the three preserved trial source files. This overwrites those
files with the historical reduced-copper trial; do not apply it to an active
board checkout.

```sh
trial=evidence/pipeline9-routing-2026-10-05/usb-before-manual-copper/source-snapshot
cp "$trial/main.tsx.txt" main.tsx
cp "$trial/src/board/Routing.tsx.txt" src/board/Routing.tsx
cp "$trial/src/board/nets.tsx.txt" src/board/nets.tsx

python3 scripts/cloud/run_with_budget.py \
  --seconds 900 --log /tmp/pipeline9-native-repro.log -- \
  bun evidence/a7-routing-2026-10-05/capture-native.tsx \
  /tmp/pipeline9-native-repro 840000
```

Inspect both the log and emitted `circuit.json` for `pcb_autorouting_error`;
the observed native process exited 0 despite the error. The corresponding
historical native input can also be extracted as `start-35.json` from
`usb-before-manual-copper/native-events.tar.gz`. Its SHA256 is
`795cee7ba121e876bebc6228704f698de47f80a591b3b4204f7aa67ac448cc99`.
A direct-library run of this reduced input has not been tested.

## Expected behavior and investigation request

For a supported input, return valid routes if feasible, or an actionable
failure describing the stage and limiting constraint. Investigate memory
growth during topology merging and the reduced-input iteration exhaustion.
If the input is unsupported or infeasible, identify the relevant constraint
or validation rule so the caller can correct it before an expensive solve.

Only effort 1 and the versions above were tested. No claim is made about
higher effort, newer releases, repeatability across machines or a known
memory leak. The native timeout does not establish a deadlock. The input is
large in obstacle count and has strict differential-pair constraints; its
routability has not been independently proven.

## Evidence links

All links refer to the pinned revision above:

- [Full native event/input archive](https://github.com/AnasSarkiz/tscircuit-ai-agent-remote/blob/8d478c7ccb2cfb0df53f14447c7d71cad78c43d2/evidence/pipeline9-routing-2026-10-05/usb-net-phase-native/native-events.tar.gz)
  and [native timeout receipt](https://github.com/AnasSarkiz/tscircuit-ai-agent-remote/blob/8d478c7ccb2cfb0df53f14447c7d71cad78c43d2/evidence/pipeline9-routing-2026-10-05/usb-net-phase-native.log.outcome.json).
- [Direct-library progress log](https://github.com/AnasSarkiz/tscircuit-ai-agent-remote/blob/8d478c7ccb2cfb0df53f14447c7d71cad78c43d2/evidence/pipeline9-routing-2026-10-05/pipeline9-library.log)
  and [memory-limit receipt](https://github.com/AnasSarkiz/tscircuit-ai-agent-remote/blob/8d478c7ccb2cfb0df53f14447c7d71cad78c43d2/evidence/pipeline9-routing-2026-10-05/pipeline9-library.log.outcome.json).
- [Reduced-copper event/input archive](https://github.com/AnasSarkiz/tscircuit-ai-agent-remote/blob/8d478c7ccb2cfb0df53f14447c7d71cad78c43d2/evidence/pipeline9-routing-2026-10-05/usb-before-manual-copper/native-events.tar.gz),
  [native error log](https://github.com/AnasSarkiz/tscircuit-ai-agent-remote/blob/8d478c7ccb2cfb0df53f14447c7d71cad78c43d2/evidence/pipeline9-routing-2026-10-05/usb-before-manual-copper.log),
  [resource receipt](https://github.com/AnasSarkiz/tscircuit-ai-agent-remote/blob/8d478c7ccb2cfb0df53f14447c7d71cad78c43d2/evidence/pipeline9-routing-2026-10-05/usb-before-manual-copper.log.outcome.json)
  and [rejected native output](https://github.com/AnasSarkiz/tscircuit-ai-agent-remote/blob/8d478c7ccb2cfb0df53f14447c7d71cad78c43d2/evidence/pipeline9-routing-2026-10-05/usb-before-manual-copper/circuit.json).
- [Public-library reproduction helper](https://github.com/AnasSarkiz/tscircuit-ai-agent-remote/blob/8d478c7ccb2cfb0df53f14447c7d71cad78c43d2/scripts/routing/solve-pipeline9.mjs).

## Board impact

Routing remains incomplete. The restored accepted board retains 90 native
open-port errors and 26 independently identified disconnected nets. Its
physical copper audit reports zero measured geometry violations and zero
shorts, but its full connectivity/fabrication gate fails. These Pipeline9
failures do not explain every outstanding board error, and the board is not
fabrication-ready.
