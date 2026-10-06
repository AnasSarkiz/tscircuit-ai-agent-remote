# Speaker routing diagnostics

These are actual failures, not accepted routes or proof that the layout is
unroutable. The remaining negative speaker output needs an outer-layer corridor
that preserves both speaker connections, the existing copper and their widths.

`current-native.srj.json` was exported with the installed public core converter
from untouched `usb-clock-native/circuit.json` and the actual source board's
pair declarations. Its receipt records native SHA-256
`3faeacd8b974b94cbbf85306326e7247d238c27e3923b2242795ee6538bc52ef`,
verified original port identities, 108 connections and 670 obstacles. The full
input is retained separately from the selected-pair diagnostic inputs.

Both speaker members (`source_net_65`, `source_net_64`) are selected together.
Their original 0.6 mm nominal widths, 0.2 mm pair gap, 2 mm skew tolerance,
5 mm maximum uncoupled length, board outline, native obstacles, clearances and
0.30/0.45 mm through-via geometry remain in the diagnostic request. Input bounds
include outboard keepouts; the actual outline still defines the PCB boundary.

Run from the Linux checkout after `source scripts/cloud/env.sh`, under the cloud
supervisor and with no other heavy operation running:

```sh
python3 scripts/cloud/run_with_budget.py --seconds 150 --log /tmp/speaker-bus.log -- bun scripts/routing/solve-native-pair.mjs evidence/connection-repair-2026-10-06/current-native.srj.json source_net_65 source_net_64 /tmp/speaker-bus.json
python3 scripts/cloud/run_with_budget.py --seconds 100 --log /tmp/speaker-fanout.log -- bun scripts/routing/solve-native-pair.mjs evidence/connection-repair-2026-10-06/current-native.srj.json source_net_65 source_net_64 /tmp/speaker-fanout.json fanout pcb_component_51
```

Core 0.0.2090's `BusLanesPipelineSolver` failed after four iterations with
`No collision-free local dogbone assignment`. `FanoutSolver`, using the actual
PCB component ID and explicit 0.275 mm package escapes, failed after 55
iterations with `best layer assignment routed 0/2 connections`. Original inputs,
requests, logs and outcomes are retained. An earlier fanout attempt mistakenly
used the source component ID; the corrected PCB-ID attempt supersedes it.

The independent copper audit finds SPEAKER_P physically connected through native
authored strips, while the exported P connection has no
`externallyConnectedPointIds`. This is a diagnostic observation requiring
converter investigation, not a confirmed upstream bug or an accepted route.
The selected-pair inputs have not been modified to claim that result came from
the native converter. No GitHub issue or other-chat message was sent.

The manual simultaneous-pair proposals are also retained. They reserve both
package escapes but find only one complete trunk; none of those partial paired
replacements was integrated. No nominal speaker width, DRC threshold, imported
pad, generated native JSON or original Pipeline9 cache was weakened or edited
to declare the speaker routed.
