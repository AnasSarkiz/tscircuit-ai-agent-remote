# Current tscircuit publication request — 2026-10-05

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
