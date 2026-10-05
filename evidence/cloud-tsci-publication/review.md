# Current tscircuit publication request — 2026-10-05

## Authenticated public outcome

The user completed the native browser login flow; the authenticated account is verified as **AnasSarkiz**. The supported compressed push created the public, listed [0.0.2-wip-cloud-routing release](https://tscircuit.com/AnasSarkiz/tscircuit-ai-agent-remote?version=0.0.2-wip-cloud-routing#files). Its public web URL responds HTTP200. **Publication remains incomplete: 114/116 staged files match anonymous readback; two required files are missing and ready_to_build=false.**

The full archive receives HTTP413. Native file-by-file fallback reports113 successes and3 failures, then exits1 after211.76 seconds. Exact anonymous readback verifies that the USB-C STEP persisted despite its reported timeout. The missing files are:

- `dist/index/circuit.json`: 5,071,958 bytes, SHA256 `81c31f77ac0871bfc4414b0940752e4f4fe0692a62089320b409908d4a8d5315`; HTTP413 upload and HTTP404 anonymous readback.
- `imports/AFC07_S50ECA_00/AFC07_S50ECA_00.step`: 11,395,444 bytes, SHA256 `ddbd85a8e13ece9dbf820c09c5187c37d91c28286b1e6db82c32adef13dfb3e0`; HTTP413 upload and HTTP404 anonymous readback.

All114 other files match exact local hashes, with no extra, mismatched or unverified remote files. See `authenticated-remote-receipt.json`, `authenticated-safe-push-status.log` and explicit outcomes. The readback helper's first attempt encountered a response-variable shadowing bug; the helper was corrected and rerun against all116 files. Its original failed log/outcome is retained rather than mistaken for completed verification.

All116 staging hashes still match the reviewed manifest. No board source, imported model, native JSON or pinned dependency was modified to reduce upload size. The current official upstream `lib/shared/push-snippet.ts` was inspected and retains the same full-archive/file-by-file paths; no supported resumable/chunked CLI route was found there. No duplicate unchanged full push or readiness override was attempted. The exact native JSON is already verified on public GitHub, separately from this incomplete registry release.

The raw publisher log remains outside Git in `/tmp`; its hash/size and safe diagnostic status lines are recorded, without committing full archive request payloads or credentials. Native browser authentication now works, and actual registry requests succeeded despite unknown network-policy metadata. Applying the saved network draft is no longer a demonstrated prerequisite for these observed requests. Startup instructions were updated as a draft to reflect this outcome and avoid repeating the earlier unnecessary network/login instructions.

**The remaining publication blocker is the registry request-size limit. The board remains an engineering WIP, not fabrication ready.** Routing/paste/schema/mating/export gates remain documented in `../cloud-runs/review.md`; registry publication would not clear them.

## Initial preparation before browser authentication — historical

**Prepared engineering WIP; registry upload blocked before any upload. NOT FABRICATION READY.** The user explicitly requested "push it to tsci", superseding the earlier registry deferral.

The existing board-only packaging helper now accepts the already-used Zod schema module and includes its exact installed version, 3.25.76. Its obsolete A6 description is replaced by the current WIP description. No board source, native JSON, imported definition/model, saved routing cache, or installed dependency changed.

`bun run publish:prepare` succeeds. Staging contains 116 files, including 111 source/model files byte-identical to the checkout and the exact current `dist/index/circuit.json`, SHA256 `81c31f77ac0871bfc4414b0940752e4f4fe0692a62089320b409908d4a8d5315`, 5,071,958 bytes. The staged package TypeScript check passes. The complete package manifest is `package-manifest.json`; preparation/typecheck logs and explicit supervised outcomes are retained.

The native command from `.publish/board` was:

```sh
../../node_modules/.bin/tsci push index.circuit.tsx --include-dist --compress --version-tag wip-cloud-routing
```

It exits1 in 2.5 seconds, before creating/uploading a release: `You need to log in to save package. Run 'tsci login' to authenticate.` The read-only `tsci auth whoami` also reports login required. Current runtime configuration has no declared secrets or outbound identities, and no tscircuit credential variable is present. GitHub Git authentication does not grant tscircuit registry access.

The runtime network policy does not list the required registry/login hosts. The environment draft preserves the prior api.github.com allowance and package-manager presets, adding registry-api.tscircuit.com and tscircuit.com. Complete startup instructions record the pending native authentication/publication workflow. Both draft saves succeeded; **saving does not apply the settings or establish authentication**. No raw credentials were requested, inspected, printed or committed. No proxy bypass or runtime/CLI patch was used.

To resume, the user must apply the environment draft and complete the supported `tsci auth login` browser flow as AnasSarkiz in this cloud environment. Then verify the account and run the same supervised native upload. Intended version is `0.0.2-wip-cloud-routing`; the CLI may bump the base version if that release already exists, so inspect its actual outcome. Verify public visibility and every remote file by exact anonymous byte/hash readback before reporting success.

The required C262650 display-connector STEP is preserved (11,395,444 bytes, SHA256 `ddbd85a8e13ece9dbf820c09c5187c37d91c28286b1e6db82c32adef13dfb3e0`). Earlier registry releases rejected it with HTTP413. This new attempt never reached that stage; a future failure must be diagnosed without omitting the model, substituting a custom upload, or overriding registry readiness.

Current board still has 90 native open-port errors and 26 disconnected nets, despite zero independently measured geometry violations/shorts. Missing paste, schema/export, mating and fabrication qualification remain blocking as recorded in `../cloud-runs/review.md`. No new tscircuit release is published or verified by this attempt. The watcher remains paused; no orders, physical tests or other-chat messages are claimed.
