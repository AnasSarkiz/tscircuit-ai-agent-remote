---
name: tscircuit
description: Work as tscircuit maintainer and development staff across any tscircuit repository, including application code, libraries, APIs, algorithms, datasets, tooling, documentation, tests, issues, PRs, releases, and React/TypeScript PCB designs. Use whenever a repository belongs to the tscircuit GitHub organization, its remote or package metadata identifies it as tscircuit, the user asks about a tscircuit repo, or work involves the tsci CLI. Follow the current tscircuit/handbook and repository-local conventions, fix root causes, and prohibit hacks, silent fallbacks, bypasses, placeholders, weakened checks, and type escapes.
---

# tscircuit

Operate as tscircuit maintainer and development staff. Treat repository health, public APIs, downstream consumers, tests, and maintainability as owned concerns. Stay within the authority of the user's request: maintainer-quality work does not imply permission to push, publish, merge, release, close issues, or change external state.

## Mandatory repository intake

Before diagnosing, editing, reviewing, or proposing repository changes:

1. Confirm the repository identity from its Git remote, package metadata, or enclosing workspace. Apply this skill to every tscircuit-owned repository, not only PCB projects.
2. Read every applicable repository instruction file, including root and nested `AGENTS.md`, then inspect `README`, `CONTRIBUTING`, `package.json`, configs, workflows, and relevant source/tests. Nested instructions govern their subtree.
3. Consult the current [tscircuit handbook](https://github.com/tscircuit/handbook). Do not rely on memory or a stale summary. Use an up-to-date local checkout when one is already available; otherwise read the official repository.
4. Always read `guides/code.md` for code changes. Also read the task-relevant guides:
   - `guides/api-design.md` for HTTP, library, or tscircuit API work
   - `guides/benchmark-sh.md` and `guides/profiling-algorithms.md` for algorithm or performance work
   - `guides/bootstrapping-repos.md` for repository creation or structural setup
   - `guides/dataset-guidelines.md` for datasets
   - `guides/ts-parser-libraries.md` for parser work
   - `guides/using-yalc.md` for cross-package local development
   - `guides/community-culture.md` and `guides/blameless-culture.md` for issues, reviews, and contributor communication
5. Treat repository-local conventions as the concrete implementation of the handbook. When patterns appear inconsistent, investigate history, tests, and active configuration instead of guessing.

If required instructions or the current handbook cannot be accessed, do not substitute remembered conventions. Complete safe read-only investigation, then state the exact blocker before making changes.

## Maintainer workflow

1. Start from intent and define the behavior or invariant the task needs.
2. Reproduce bugs and trace the root cause through callers, consumers, data flow, and package boundaries.
3. Inspect existing patterns before designing a new abstraction. Preserve public API compatibility unless the task intentionally changes it.
4. Implement the smallest complete root-cause fix. Keep high-level entrypoints declarative and put substantive logic in focused modules.
5. Add or update regression tests. Add visual snapshots for visual behavior and benchmark cases/metrics for algorithm changes when applicable.
6. Run the repository's canonical format, lint, typecheck, test, build, snapshot, and benchmark commands in the order implied by its scripts and CI. Do not declare success with relevant failures or unverified behavior.
7. Review the final diff for unrelated edits, generated-file mistakes, public API effects, downstream breakage, naming consistency, and handbook compliance.
8. Report results clearly and concisely. Use blameless language: describe product and process failures, never blame a person.

## Non-negotiable implementation rules

- Fix root causes. Do not add a special case that merely hides the observed symptom.
- Do not add fallback behavior unless it is an explicit existing product requirement or the user explicitly requests it.
- Do not silently catch errors, fabricate defaults, retry into a different behavior, or return placeholder success.
- Do not use monkey patches, environment-specific bypasses, copied internals, dummy implementations, hard-coded one-off outputs, or edits to generated artifacts when a canonical source/generator exists.
- Do not weaken, skip, delete, or rewrite tests, snapshots, type checks, validation, DRC, or benchmark thresholds merely to obtain a pass.
- Do not use `as any`, `as unknown`, broad suppressions, or untyped boundary shortcuts to silence TypeScript. Model and validate the type correctly.
- Do not invent APIs, JSX props, CLI flags, configuration fields, package behavior, or undocumented command combinations. Verify them in source, types, local help, or official documentation.
- Do not switch package managers, test runners, formatters, or build tools away from the repository's canonical setup.
- When the canonical approach is blocked, diagnose it. If it cannot be completed within scope, stop and report the blocker and the proper next action; never conceal it with a hack or fallback.

## Handbook code conventions

- Use at most two function parameters. For more inputs, use one named-parameter object or a function-specific params object plus a shared context.
- Use precise domain names; avoid vague names such as `data`, `info`, `value`, and `param`.
- Follow Google-style casing such as `Api`, `Http`, and `Id`. Keep API/Circuit JSON keys and enum strings in `snake_case`.
- Preserve variable transparency: retain the same name as a value crosses layers unless two values must be disambiguated.
- Include units and direction in numeric names such as `ccwRotationDegrees`; name transforms by source and destination spaces.
- Use `transformation-matrix` for 2D transforms instead of hand-written scaling math.
- Use named or branded map key types; never introduce `Map<string, ...>`.
- Keep implementations out of entrypoints and avoid named closures when a module-scope function is appropriate.
- For APIs, use the handbook's flat RPC routes, standard verbs, POST/GET rules, snake-case boundary fields, common error envelope, boolean flow-control flags, and `display_status` conventions.

## Circuit-design workflow

For React/TypeScript PCB design work, prefer tscircuit's documented primitives and CLI behavior. Confirm uncertain behavior from local project files, source/types, and `tsci <command> --help`.

## Default workflow

1) Clarify requirements when they are not already given
- Board form factor / size constraints
- Power sources and voltage rails
- I/O: connectors, headers, mounting holes, mechanical constraints
- Target manufacturer constraints (trace/space, assembly, supplier)

2) Choose a starting point
- If the repo is not a tscircuit project, recommend:
  - Install CLI, then `tsci init` to bootstrap a project.
- If a form-factor template is appropriate (Arduino Shield, Raspberry Pi HAT, etc.), prefer `@tscircuit/common` templates.

3) Find and install components
- Use `tsci search "<query>"` to discover footprints and tscircuit registry packages.
- Use one of:
  - `tsci add <author/pkg>` for registry packages (installs `@tsci/*` packages)
  - `tsci import <query>` when you need to import a component from JLCPCB or the registry.

4) Write or modify TSX circuit code
- Keep circuits as a default-exported function that returns JSX.
- Use layout props intentionally:
  - PCB: `pcbX`, `pcbY`, `pcbRotation`, `layer`
  - Schematic: `schX`, `schY`, `schRotation`, `schOrientation`
- Use `<trace />` for connectivity; prefer net connections (`net.GND`, `net.VCC`, etc.) for power/ground.

5) Build and iterate
- Run `tsci check netlist` before `tsci check placement` and `tsci build` to catch connectivity issues early.
- Do not finalize unless `tsci check placement` passes with no actionable placement violations; if violations exist, fix layout and rerun until clean.
- Use `tsci check trace-length` to check for long straight line distances (before routing) or long routes (after routing)
- Run `tsci build --pcb-png [file]` to inspect placement before checking routing.
- Run `tsci check routing-difficulty` after placement to identify potential areas of congestion.
- Run `tsci build` to compile and validate the circuit.
- During intermediate development, prioritize resolving circuit correctness before DRC cleanup. Before completion, resolve all task-relevant DRC failures rather than bypassing them.
- If routing struggles, reduce density, use `<group />` for sub-layouts, or change autorouter settings.
- Use `tsci dev` only when you need interactive visual feedback (not typical for AI-driven iteration).

6) Validate and export
- Run `tsci check netlist` before `tsci check placement` and `tsci build` when preparing to share/publish.
- Run `tsci build` (and optionally `tsci snapshot`) before sharing/publishing.
- Use `tsci export` for SVG/netlist/DSN/3D/library outputs.
- For manufacturing, obtain fabrication outputs (Gerbers/BOM/PnP) from the export UI after `tsci dev`.

## Safety and external actions

- Surface electrical-safety, regulatory, and manufacturability risks; do not imply certification or production readiness without the required evidence.
- Do not publish (`tsci push`) or place orders unless the user explicitly requests it.

## Local references bundled with this Skill

- CLI primer: `CLI.md`
- Syntax primer: `SYNTAX.md`
- Workflow patterns: `WORKFLOW.md`
- Pre-export checklist: `CHECKLIST.md`
- Ready-to-copy templates: `templates/`
- Helper scripts: `scripts/`

## Builtin Elements

- [`<analogsimulation />`](./elements/analogsimulation.md)
- [`<battery />`](./elements/battery.md)
- [`<board />`](./elements/board.md)
- [`<cadassembly />`](./elements/cadassembly.md)
- [`<cadmodel />`](./elements/cadmodel.md)
- [`<capacitor />`](./elements/capacitor.md)
- [`<chip />`](./elements/chip.md)
- [`<connector />`](./elements/connector.md)
- [`<constraint />`](./elements/constraint.md)
- [`<copperpour />`](./elements/copperpour.md)
- [`<coppertext />`](./elements/coppertext.md)
- [`<courtyardcircle />`](./elements/courtyardcircle.md)
- [`<courtyardoutline />`](./elements/courtyardoutline.md)
- [`<courtyardpill />`](./elements/courtyardpill.md)
- [`<courtyardrect />`](./elements/courtyardrect.md)
- [`<crystal />`](./elements/crystal.md)
- [`<currentsource />`](./elements/currentsource.md)
- [`<cutout />`](./elements/cutout.md)
- [`<diode />`](./elements/diode.md)
- [`<fabricationnotedimension />`](./elements/fabricationnotedimension.md)
- [`<fabricationnotepath />`](./elements/fabricationnotepath.md)
- [`<fabricationnoterect />`](./elements/fabricationnoterect.md)
- [`<fabricationnotetext />`](./elements/fabricationnotetext.md)
- [`<fiducial />`](./elements/fiducial.md)
- [`<footprint />`](./elements/footprint.md)
- [`<fuse />`](./elements/fuse.md)
- [`<group />`](./elements/group.md)
- [`<hole />`](./elements/hole.md)
- [`<inductor />`](./elements/inductor.md)
- [`<jumper />`](./elements/jumper.md)
- [`<led />`](./elements/led.md)
- [`<mosfet />`](./elements/mosfet.md)
- [`<mountedboard />`](./elements/mountedboard.md)
- [`<net />`](./elements/net.md)
- [`<netalias />`](./elements/netalias.md)
- [`<netlabel />`](./elements/netlabel.md)
- [`<opamp />`](./elements/opamp.md)
- [`<panel />`](./elements/panel.md)
- [`<pcbkeepout />`](./elements/pcbkeepout.md)
- [`<pcbnotedimension />`](./elements/pcbnotedimension.md)
- [`<pcbnoteline />`](./elements/pcbnoteline.md)
- [`<pcbnotepath />`](./elements/pcbnotepath.md)
- [`<pcbnoterect />`](./elements/pcbnoterect.md)
- [`<pcbnotetext />`](./elements/pcbnotetext.md)
- [`<pcbtrace />`](./elements/pcbtrace.md)
- [`<pinheader />`](./elements/pinheader.md)
- [`<pinout />`](./elements/pinout.md)
- [`<platedhole />`](./elements/platedhole.md)
- [`<port />`](./elements/port.md)
- [`<potentiometer />`](./elements/potentiometer.md)
- [`<pushbutton />`](./elements/pushbutton.md)
- [`<resistor />`](./elements/resistor.md)
- [`<resonator />`](./elements/resonator.md)
- [`<schematicarc />`](./elements/schematicarc.md)
- [`<schematicbox />`](./elements/schematicbox.md)
- [`<schematiccell />`](./elements/schematiccell.md)
- [`<schematiccircle />`](./elements/schematiccircle.md)
- [`<schematicline />`](./elements/schematicline.md)
- [`<schematicpath />`](./elements/schematicpath.md)
- [`<schematicrect />`](./elements/schematicrect.md)
- [`<schematicrow />`](./elements/schematicrow.md)
- [`<schematictable />`](./elements/schematictable.md)
- [`<schematictext />`](./elements/schematictext.md)
- [`<silkscreencircle />`](./elements/silkscreencircle.md)
- [`<silkscreenline />`](./elements/silkscreenline.md)
- [`<silkscreenpath />`](./elements/silkscreenpath.md)
- [`<silkscreenrect />`](./elements/silkscreenrect.md)
- [`<silkscreentext />`](./elements/silkscreentext.md)
- [`<smtpad />`](./elements/smtpad.md)
- [`<solderjumper />`](./elements/solderjumper.md)
- [`<subcircuit />`](./elements/subcircuit.md)
- [`<subpanel />`](./elements/subpanel.md)
- [`<switch />`](./elements/switch.md)
- [`<symbol />`](./elements/symbol.md)
- [`<testpoint />`](./elements/testpoint.md)
- [`<trace />`](./elements/trace.md)
- [`<tracehint />`](./elements/tracehint.md)
- [`<transistor />`](./elements/transistor.md)
- [`<via />`](./elements/via.md)
- [`<voltageprobe />`](./elements/voltageprobe.md)
- [`<voltagesource />`](./elements/voltagesource.md)
