# Explicit Pipeline9 selection and actual routing trials

The human requested Pipeline9. `main.tsx` now explicitly selects the supported
`autorouterVersion="beta_pipeline9"`. Installed capacity-autorouter 0.0.958
already exports Pipeline9 as its default; this change makes the selection
explicit. Core's recorded native solver is
`AutoroutingPipelineSolver9_PreloadedTraceGraph`. Dependencies, imported parts
and existing genuine route caches remain unchanged.

**No newly solved copper was accepted. The board remains a WIP with incomplete
routing and no fabrication approval.** Default builds continue to replay the
previously accepted copper; this selection does not reroute saved paths or
silently enable routing to the unqualified J3/J7 contacts.

## Actual attempts

- `usb-native`: completed replay-only trial. Net selectors did not select new
  connections. No routing progress claimed; all existing copper was identical.
- `usb-paired-native`: completed replay-only port-selector trial. Native merged
  net connections were not selected. No Pipeline9 solve or progress claimed.
- `usb-net-phase-native`: assigning USB_DP/USB_DN to phase23 started the actual
  native Pipeline9 solver. Input had two four-terminal nets, 0.2979 mm widths,
  four layers, 0.30/0.70 mm full-stack vias, 0.20 mm pad clearance and the
  0.5 mm skew/0.2101 mm gap/5 mm uncoupled-length pair constraints. The input
  contained 9,279 obstacles. The supervisor stopped the unfinished operation
  at 660.99 seconds; peak process-group RSS 11,803,729,920 bytes. No end event
  or completed route exists.
- `pipeline9-library`: the documented public Pipeline9 library API consumed
  the exact same captured input without intermediate visualization frames.
  Topology merging exhausted the 65% RAM budget after 96.84 seconds, with
  measured peak RSS 22,385,528,832 bytes. No completed output exists.
- `usb-before-manual-copper`: a preserved, temporary source trial deferred
  the manual signal and power copper while keeping all purchased components,
  placement, constraints and genuine saved-route files. Input fell to 2,996
  obstacles. Native rendering settled after 448.21 seconds, but the router
  returned `aJ ran out of iterations (capacity-autorouter@0.0.958)`.
  Peak RSS 17,378,430,976 bytes. The output retains one autorouting error,
  418 open-port errors and seven missing-trace errors. A render exit 0 does
  not mean the routing succeeded. This source/output was rejected.

The trial USB phase, net assignments, added pair and temporary copper omissions
were removed from the default board after these failures. The only accepted
board-source change is the explicit Pipeline9 version selection. No iteration
limits, manufacturing rules, assertions or error records were relaxed.

`baseline-receipt.json`, `supported-pipeline9-reference.json`, the actual native
start receipt, source snapshots and supervisor outcomes identify the inputs
and failures. `scripts/routing/solve-pipeline9.mjs` is a diagnostic public-library
runner; it does not alter native output or create a replay cache. Archived
events can be restored using each capture's exact-byte archive receipt.

## Final validation and publication

The restored default board is rebuilt and checked separately below. No failed
trial replaces `dist/index/circuit.json`. Publication of the explicit setting
is an engineering WIP checkpoint, not a claim of completed routing.

Final native rendering completed in 180.74 seconds with peak RSS
1,688,854,528 bytes. The generated JSON is byte-identical to the prior accepted
build: SHA256 `81c31f77ac0871bfc4414b0940752e4f4fe0692a62089320b409908d4a8d5315`.
It retains 306 traces, 250 full-span vias, 190 pours and 90 native open-port
errors. Fresh physical auditing reports zero measured geometry violations and
zero shorts, with 26 disconnected nets; the full gate correctly fails.
TypeScript and formatting pass. All 265 protected files match their prior
hashes. Existing strict-schema, paste, supplier-mating and fabrication failures
remain applicable because the native geometry and components are unchanged.

The board source and evidence were pushed to public main at
`a9600d81e40761d3fc7c2471c57cb05d77c548a4`.
Public tscircuit release `0.0.2-wip-pipeline9`, release ID
`60b0df33-f229-4c85-8515-e9f5d2250674`, now has all 116 files byte-verified
by anonymous readback: no missing, extra or mismatched files. The supported
release-create API's default readiness was preserved, and normal build
scheduling was enabled by the official archive upload endpoint.

The first 5,823,924-byte full multipart archive was rejected HTTP413. Explicit
3,000,000-byte archive budgeting in the resume helper produced three exact-byte
archives: 2,756,770 bytes/16 files, 2,991,947 bytes/68 files and 78,366 bytes/32
files. All three returned HTTP200. The helper preserves local-hash/stale-remote
guards, validates every archive round trip and every server-returned file set,
and records each accepted chunk. No original file was truncated or omitted,
and no library/runtime or readiness override was used. The client timeout is
300 seconds per request to accommodate complete model uploads. A partial chunk
failure remains an error and requires fresh readback before resuming.

`final-registry-receipt.json` is the authoritative 116/116 receipt. The earlier
empty-release and rejected full-upload receipts are retained historical evidence.
Publication is not evidence of completed cloud CI, new browser visual review,
zero native errors or fabrication readiness.

The preview API finds `index.circuit.tsx` and returns all 6,848 native elements
equal to the local JSON. Its preview page and the exact public GitHub source
respond HTTP200. See `public-preview-receipt.json`. The onboarding startup
instructions were saved as a draft with the Pipeline9 diagnostics and explicit
archive budgeting; that save does not apply or publish the environment.
