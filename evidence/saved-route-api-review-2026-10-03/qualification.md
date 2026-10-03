# Saved-route API source review — no copper captured yet

Pinned official core0.0.2058 and props0.0.677 expose a supported per-routing-phase replay API. AutoroutingEndEvent has optional pcbTracePaths (FanoutTracePath[]) and pcbTracePathsUnavailableReason. The documentation states that saved paths describe that stage only in its enclosing group's local PCB frame; physical layers stay unchanged, and replay uses the same phase options/placement. The generator applies transformation-matrix internally and preserves each unique PCB-port selector as connection plus actual wire/via route geometry.

The public <autoroutingphase pcbTracePaths={...}> property is present in pinned props/types and consumed by pinned core, including coverage validation. The actual autorouting:end event is the canonical source for the serialized paths. Do not reconstruct paths by joining separate trace routes or invent coordinates, connection names, empty caches or transforms. Do not presume the phase output covers the entire board: collect every relevant phase, preserve phase/subcircuit identity and confirm final circuit connectivity/copper after replay.

Core omits pcbTracePaths rather than exporting a partial route when junctions, non-wire/via geometry or endpoint ambiguity cannot be represented. Preserve the original complete native routing event and complete final Circuit JSON regardless; if replay paths are absent, record the actual reason and resolve supported persistence before claiming saved-route qualification. Do not silently drop unsupported geometry or label a full JSON backup as proven replayable routes.

The older pcbRouteCache type remains exposed as {pcbTraces,cacheKey}. Source inspection found Trace_doInitialPcbTraceRender reading pcbTraces and flattening their routes; that branch does not show per-source trace matching or key validation. Its applicability/behavior has not been reproduced on a routed qualification fixture, so no new confirmed defect is claimed. This inspection is insufficient to qualify arbitrary multi-net cache replay. Follow the supported stage-event replay API only after its actual round trip is checked; do not use an untested legacy cache to obtain passing copper.

Required actual-board sequence after all pre-routing gates pass:
1. Route natively with actual clearances, widths and via settings, and collect each routing-stage end event plus the final complete Circuit JSON.
2. Save those exact original artifacts with source revision, dependency lock/checksum, placement/frame/phase settings and hashes under a new versioned routes directory. Preserve the pre-change state before moving anything.
3. Where canonical pcbTracePaths are present, replay through the same native autoroutingphase options. Build and compare physical routes, source-net/port endpoints, widths, vias/layers and coverage. Run shorts and geometric/connectivity checks on the actual replayed output.
4. For an offending segment, change the persisted source route through the supported native path API; keep the saved earlier version. Rebuild and re-run all affected checks, then regenerate the entire fabrication package from the validated source revision.

Whole-board stages1/2 are unfinished/blocked; routing is disabled and no actual copper, saved route, replay proof or fabrication package exists. This is source/API investigation only. It does not authorize early routing, normalize native output, patch components or complete a validation gate.

Verified source locations in installed packages:
- core/dist/index.d.ts: AutoroutingEndEvent, lines2027–2045.
- core/dist/index.js: getAutoroutingPhasePcbTracePaths around20007; saved path consumption/coverage around111850; event emission around114764.
- props/dist/index.d.ts: AutoroutingPhaseProps.pcbTracePaths around161853 and FanoutTracePath schema around45105–45249.
- core/dist/index.js: older Trace_doInitialPcbTraceRender cache branch around7040.

No public API, JSX property or saved geometry has been invented. Actual round-trip qualification remains required.
