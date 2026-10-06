# Native board / Freerouting continuation

Manual native paths remain appropriate for ground, matched USB and speaker
connections. J3/J7 contact-dependent routes remain deferred until their exact
numbered contacts and mating orientation are qualified. Freerouting proposals
are usable only after native regeneration and the independent board gates pass.

The stock DSN exporter does not retain this board's copper and fabrication rules.
`freerouting_bridge.py` transfers the actual native geometry instead, without
editing imported components, generated Circuit JSON or saved solver caches.
The official Freerouting 2.5.0 and Temurin JDK 25 artifacts are pinned and
checksum-verified by `scripts/cloud/install-freerouting.py` in the ignored cache.

Run from the existing Linux checkout after `source scripts/cloud/env.sh`, with
one heavy operation at a time under `scripts/cloud/run_with_budget.py`:

Historical exact inputs/outputs and engine receipts are losslessly archived in
`evidence/freerouting-continuation-2026-10-06/geometry-artifacts.tar.gz`.
`geometry-archive.json` verifies every member's bytes and records the restore
command. Extract that archive in its evidence directory to reproduce an old
trial; export fresh input for a new board revision.

1. Export the current native board with the explicit eligible net names:
   `python3 scripts/routing/freerouting_bridge.py export dist/index/circuit.json <input.dsn> --pour-tile-mm 5 --nets <eligible nets>`.
2. Load/write it through the official public file APIs:
   `.tools/freerouting/jdk-25.0.4.1+1/bin/java -Xmx6g -Djava.awt.headless=true --class-path .tools/freerouting/freerouting-2.5.0.jar scripts/routing/FreeroutingTransfer.java <input.dsn> <roundtrip.dsn> <engine.json>`.
3. Qualify geometry, actual engine pad topology, net classes, plane flags,
   clearances and existing via spans:
   `python3 scripts/routing/freerouting_bridge.py verify <input.dsn> <roundtrip.dsn> <qualification.json> --engine-rules <engine.json>`.
4. Route the **original qualified input**, never the normalized roundtrip.
   Keep strict DRC enabled, inner1 disabled, optimizer/fanout disabled and the
   `PRESERVE` class ignored. Set `--router.plane_as_obstacle=true` to retain
   existing copper as foreign routing obstacles. `-do` accepts separate output
   filenames: `-do <proposed.ses> <proposed.dsn>`, not a comma-separated argument.
   Use a finite internal job timeout plus a larger cloud supervisor budget.
5. Decode the actual session:
   `python3 scripts/routing/freerouting_bridge.py session <proposed.ses> <input.dsn.manifest.json> <qualification.json> <proposals.json>`.
6. Prepare reviewable source proposals with
   `python3 scripts/routing/freerouting_copper_source.py <proposals.json> <copper-source.json>`.
   These are centreline-derived native region/via proposals with an explicit
   0.001 mm serialization reserve. They are not accepted routes or solver caches.

Retain actual input/output bytes, logs, thread dumps, command outcomes and source
hashes. `COMPLETED`, exit zero, a saved SES, an engine-global incomplete count or
geometry-transfer qualification does not establish native board completion.
An internal/supervisor timeout or operator cancellation is an incomplete trial.

Import candidate geometry only through supported native board features. Rebuild
with the existing native capture helper, then run `audit-copper.py` and
`audit-region-widths.py` against the regenerated output. Require zero new shorts,
clearance/drill violations, preserved existing widths and no split of any
previously connected port group. Verify original pads, routes and vias remain.
Require an actual reduction in native missing connections. Reject candidates
that improve a signal but disconnect ground. Never edit Circuit JSON directly.

The complete fabrication gate also requires all physical opens/native errors to
be resolved and the existing schema, paste, Gerber, BOM/CPL, interface, mechanical
and electrical qualification blockers to pass. This continuation does not change
those gates. Current evidence is in
`evidence/freerouting-continuation-2026-10-06/`; earlier intermediate qualifications
there predate the active-net plane-semantics check and are unsuitable for import.
