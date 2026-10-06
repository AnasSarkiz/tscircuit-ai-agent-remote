# MCU correction and fabrication continuation — 2026-10-06

**Revision `0.0.3-wip-local-bypass`; NOT READY TO ORDER.** This is an accepted
independent correction and matching publication task. It does not close every
issue from the requested six-point review.

Reviewed parent: `c0aca2b64708c04c1793e39093b3fd8bf8b41e5d`.
Current native SHA256:
`772195341bd21450085576075af162a3a45adc9c311e5fcc747488d01bb56ebe`.
Final native rendering completed in214.91seconds with1.67GB peak process-group
RSS under the cloud supervisor. Actual loaded source snapshots, native events
and circuit JSON are preserved in `final-native/`; event archives verify every
original byte. The canonical JSON is copied from this completed native render.

## Accepted electrical changes

C31, genuine GRM188R71C104KA01D/C45000,100nF, moves from(0,0) to
(-23.45,29.9),rotation180°. Its power-pin distance to U1.pin2 drops from
35.9998mm to1.99993mm. Its actual0.8mm,0.3mm-wide top branch contacts the
existing U1 supply via's annular copper. No new supply via is inserted. The
native ground contact runs beyond the pad into the top ground pour. Independent
physical groups prove C31's supply and return share U1's supply and ground.

C30 now uses the existing genuine GRM188R61A226ME15D/C84419,22µF import,
matching the nominal value in Espressif's ESP32-S3-WROOM-1 v1.8 peripheral
reference circuit. The supplier receipt describes10V/X5R/0603. C84419 quantity
is4 and C90053 quantity is10; purchased count remains125/43identities.
C30's bulk placement is still remote, and DC-bias/effective capacitance and
Wi-Fi transient/current performance are not qualified by this nominal change.

[Acceptance receipt](accepted-step.json) checks actual annular contact, source
snapshot equality, physical groups, the complete unchanged open-net partition,
zero new violations, all152 authored region widths and eight programmer target
copper groups. It deliberately keeps full-copper and fabrication verdicts false.

## Rejected placement/copper proposals

The first C30/C31/C32 trial had rounded-edge, antenna-keepout and courtyard
errors. Its early native operation was stopped; no routed output was accepted.
The revised three-capacitor trial passed placement but its full copper had12
geometry violations, signal contacts and47open nets. A direct capacitor-to-pin
path also violated the native1mm capacitor-branch length rule and prevented
replay of other phases. The source was restored before the narrower C31 trial.

Only the final C31 move and C30 nominal substitution are accepted. Original
import definitions, model bytes, dependency pins and solver route caches remain
unchanged. No generated JSON editing, invented replay cache, shortened clearance,
trace-length relaxation or nominal-width exemption was used.

## Current whole-board findings

| Gate | Current result |
| --- | --- |
| Native placement | Zero errors, including courtyards/keepouts/edge checks |
| Physical copper geometry | Zero measured shorts and clearance violations |
| Required connectivity | **26 open nets,90 native open-port errors**; GND35islands |
| Authored power-region widths | All152pass |
| Trace widths |306traces/792segments; none below0.20mm;2below explicit source width and55below net nominal still require correction/current review |
| Purchased population |125placements/43exact JLC identities;10native solder pads |
| Strict native schema | **169failing elements** |
| Stencil paste | **32missing pill-pad apertures**, U16 and U27 |
| Official Gerber export / shorts | **Fail: Unsupported shape polygon** |
| Default BOM converter |125rows,31blank descriptions,125supplier-code package labels |
| Supported resolved BOM |125rows,**0blank descriptions /0supplier-code package labels** |
| Assembly rotations |125missing supplier pin1 metadata warnings; strict export rejects U1 |
| Programmer target copper | Eight reviewed UART/power/reset/BOOT groups pass; adapter and hardware tests pending |
| Current JLC stock / external mating | **Unverified/blocked** |
| Board regressions |48pass /2retained fabrication/schema failures;60routing regressions pass |
| Formatting / TypeScript | Pass |

The zero-geometry result is not zero overall DRC: the connection errors remain.
J3's two unresolved outer contacts are additional omissions outside the open-net
count. J7's physical panel mating is still unqualified and contact-dependent
fanout is deferred. USB, audio, power and microphone open nets remain visible.
No fabrication ZIP, complete connection claim or physical hardware success is
approved.

## Supported BOM correction

The official `circuit-json-to-bom-csv@0.0.19` exporter accepts a `resolvePart`
callback. The default exporter does not use native manufacturer part numbers
as chip descriptions and has no package label for these imported footprints.
[export-resolved-bom.mjs](export-resolved-bom.mjs) matches each selected native
JLC identity/MPN to its exact recorded supplier package, then invokes that API.
The CSV is generated by the official converter; it is not manually repaired.
Unknown manufacturer-company names stay empty in the resolver record and are
explicitly disclosed. No company name, stock or qualified land pattern is
invented from the MPN/package label.

[Resolved output receipt](resolved-bom-receipt.json) covers all125purchased
parts. The file remains `NOT-FOR-FABRICATION-resolved-bom.csv`: current stock,
orientation, connectivity, stencil and assembler qualification are unfinished.
Historical JLC quantities are not a reservation. Priority stock refresh remains
C107701(8previously listed,5per board) and C98220(22previously listed,20per board).

## Generator and external blockers

Authoritative npm metadata/tarballs were inspected with advertised SHA512
integrity verification. Newest published core0.0.2095 still inserts pill and
rotated-pill pads without paste. CLI0.1.2251's embedded Gerber converter still
rejects polygon solder paste. Updating versions alone does not remove these
failures. Board dependency pins were preserved. [Source inspection](upstream-blockers.json)
and specific strict-schema diagnostics identify the canonical generators; no
runtime/import/generated-output patch was substituted for a fix.

The current official BuyDisplay ER-TFT026-1 PDF returned inherited proxy
CONNECT403. JLC search was already confirmed blocked on the unchanged network.
The saved restricted draft preserves package-manager access and api.github.com,
registry-api.tscircuit.com,tscircuit.com,jlcsearch.tscircuit.com, and adds
www.buydisplay.com. Tested startup instructions were refreshed. The draft save
is confirmed; runtime application/publication is not.

The [onboarding skill](skill://plugin_connector_1p_ed5feb9070a08191b08c81c47947bc16/setup/SKILL.md)
states: “Saving persists configuration; it does not execute scripts, apply
runtime changes, or publish.” Apply the saved network/startup draft through
environment settings before retrying the blocked supplier operations. This is
an environment action, not another tscircuit login or a request to guess pins.

Even with access restored, the exact pack keyed/numbered BAT+/GND contacts and
current panel contact face/pin1/fold/mating must be established from actual
supplier evidence. The historical drawings do not supply that qualification.
No unrelated connector drawing or conventional wire colour is treated as proof.

## Publication package installation/build correction

The old packaging helper copied the root lockfile but changed its direct
package declarations. The helper now preserves the exact original dependency
list/overrides, and includes the current README, validation and BOM notes.
A genuine frozen installation of the complete publication package succeeds:
303packages installed in10.52seconds, unchanged original lockfile bytes.
No dependency version, checksum, install script or verification was bypassed.

The required native CLI build completed from the complete source/model/runtime
package in222.33seconds,2.52GB peak RSS. It produced actual PCB PNG/SVG,
schematic SVG and Circuit JSON. It correctly exits1 because of90open-port
errors; this is a completed failed board build, not a source-discovery failure.
All pad/hole/port/trace/via/pour/keepout/board records in its output are exactly
equal to the independently validated native output. Nonphysical metadata differs,
so the whole JSON is not called byte-identical. Actual outputs and comparison
receipt are retained; published canonical JSON remains the validated native bytes.

The earlier full CLI timeout is superseded for this exact package workflow.
The WIP label and failed electrical/fabrication gates remain. Logical netlist,
pin-specification, source and schematic-placement commands exit0; existing
schematic suggestions and React warnings remain disclosed, not final approval.

Native MCU close-up and four-layer diagnostic views were inspected. The local
C31 contact and antenna/rounded-edge geometry are visible. Long pre-existing
warning annotations obscure parts of the composite; these are diagnostics,
not final stencil/assembly drawings or physical-board photographs.

## Validation and publication

Each actual command/result/budget is retained in this directory. Independent
copper and width commands exit1 because full connectivity/source-width gates
still fail; those exits are not relabelled passes. Required logical CLI checks,
full CLI rendering, snapshots and public package readback have individual
receipts. Publication confirms the accepted WIP revision only. Upload, preview
discovery and cloud-CI completion are separate outcomes.

The required snapshot command was also run from a fresh303-package frozen
installation of the corrected publication manifest. It completes in246.93seconds,
3.27GB peak RSS, and exits1: both original PCB and schematic snapshots mismatch.
References are byte-unchanged; no snapshot was updated or accepted to pass.
All generated physical records again exactly match the accepted native board.
[Snapshot receipt](snapshot-receipt.json) records the original references and
physical comparison. These outcomes supersede the earlier loader timeout, not
the remaining board errors.

## Completed public WIP publication

The accepted implementation is public on GitHub at
[7c8c78e](https://github.com/AnasSarkiz/tscircuit-ai-agent-remote/commit/7c8c78efcd8ffb6072ce824aa95de75672c36188).
Anonymous HTTP200 readback verifies the canonical native JSON, changed electrical
source, publisher helper and all three packaged review documents byte-for-byte.

The public listed tscircuit release is
[0.0.3-wip-local-bypass](https://tscircuit.com/AnasSarkiz/tscircuit-ai-agent-remote/releases/8dd2f2c2-5ce3-4826-a126-aa7cc7ea78b8/preview).
All119/119 files match exact anonymous hashes; no missing, extra or mismatched
files remain, and ready_to_build=true. The native preview endpoint discovers
index.circuit.tsx and returns the exact full validated native array. HTTP200
on the preview page is recorded; browser thumbnails have not been verified.

Native CLI push encountered HTTP413 for the full archive and two large files.
The supported official multipart gzip resume returned HTTP502 initially, but
its transaction subsequently persisted both files. A fresh all-file readback
first saw117 files; the retry helper then detected the changed remote file set
and refused any duplicate upload. A subsequent fresh readback proves119 files.
Do not mistake the failed transport response for absent content or overwrite
that original outcome with a false successful request. Raw full-archive error
output is retained outside Git, with its size/hash and safe status lines recorded.

The registry scheduled build5f93c81b-9582-428b-872d-654926e8d60d automatically.
Its status is recorded separately in cloud-build-observation.json; no duplicate
build was requested. Exact upload and existing native preview discovery are
verified; a running cloud job does not establish successful CI or fabrication.

The first80-second cloud observation ended while the build was still running,
with no completion timestamp or error. Registry logs show successful file
creation, bundled dependency symlinks and execution of
`bunx tscircuit build --ci --concurrency 4`. Cloud bundled versions are not
assumed to match the locally validated frozen installation. The observation
deadline did not cancel or fail the remote job. The latest follow-up observation
is preserved separately; pending must not be reported as successful cloud CI.

### Final remote cloud result

The follow-up observation completed with **failed infrastructure**, not pending
or successful CI. Registry completion:2026-10-06T13:42:50.630Z; error code
`user_code_job_infrastructure_error`. Logs show a worker waiting on
`analyze-part-orientation`, then `ReadableStream received over RPC disconnected
prematurely.` The exact part/service root cause is unproven.
[Cloud failure report](cloud-build-failure.md) preserves reproducible package
inputs, public IDs, expected/observed behavior and the actual final logs.
Publication and existing native preview remain verified. No orientation check
was disabled and no duplicate job was queued.
