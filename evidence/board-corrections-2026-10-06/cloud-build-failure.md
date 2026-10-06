# Public cloud build failure — 2026-10-06

Public release: `AnasSarkiz/tscircuit-ai-agent-remote@0.0.3-wip-local-bypass`.
Release ID: `8dd2f2c2-5ce3-4826-a126-aa7cc7ea78b8`.
Build ID: `5f93c81b-9582-428b-872d-654926e8d60d`.
Exact complete package inputs: `publication-inputs.json`; all 119 files are
verified by `final-registry-receipt.json`. Native JSON SHA256:
`772195341bd21450085576075af162a3a45adc9c311e5fcc747488d01bb56ebe`.

The registry automatically scheduled the normal cloud build after the supported
archive transaction completed. Its runner wrote all files, created bundled
dependency symlinks and executed `bunx tscircuit build --ci --concurrency 4`.
Heartbeats showed one busy worker for `/workspace/index.circuit.tsx`, waiting
on `analyze-part-orientation`, including at 210,005 and 240,005 ms.
The stream then failed: `ReadableStream received over RPC disconnected prematurely.`
The registry recorded `user_code_job_infrastructure_error`, completed at
2026-10-06T13:42:50.630Z. No successful cloud CI result is claimed.

Expected: the worker completes supplier orientation analysis or returns a bounded,
explicit analysis failure, then completes the board build with its actual board
validation results. Observed: infrastructure stream disconnect during that phase.
The exact supplier part and remote dependency versions are not exposed by these
logs; the wait and disconnect do not prove which service caused the failure.

Evidence: `cloud-build-followup.json` contains the actual final registry status
and logs. Read the existing build anonymously with:

```sh
curl 'https://registry-api.tscircuit.com/package_builds/get?package_build_id=5f93c81b-9582-428b-872d-654926e8d60d&include_logs=true'
```

The current canonical core source queues the named orientation effect and awaits
`partsEngine.fetchPartCircuitJson`; this matches the phase named in logs, not
proof of remote root cause. No check was disabled, supplier orientation invented,
import/model omitted or generated output patched to work around this failure.
No duplicate cloud build was queued. The clean locally frozen package build
completes, generates identical physical copper records and fails correctly on
90 open-port errors. Both original SVG snapshots also mismatch.

The existing uploaded native JSON is independently discoverable in the public
[preview](https://tscircuit.com/AnasSarkiz/tscircuit-ai-agent-remote/releases/8dd2f2c2-5ce3-4826-a126-aa7cc7ea78b8/preview).
That does not clear cloud CI or the board's separate fabrication gates.
